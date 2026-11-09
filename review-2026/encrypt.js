#!/usr/bin/env node
/*
 Multi-passphrase gate for a single-file static page.

 The page is AES-256-GCM encrypted once with a random content key. That key is then
 wrapped (AES-GCM again) under a PBKDF2 key derived from each accepted passphrase, all
 sharing one salt, so the browser derives once and tries each wrapped copy. Any passphrase
 that unwraps the key opens the page. Nothing about the passphrases is stored; a wrong
 passphrase simply fails GCM authentication on every slot.

 Usage: node encrypt.js <plain.html> <out.html> <passphrases file> [--title T] [--button B] [--instructions I] [--key-id ID]
 The passphrases file has one passphrase per line. --key-id namespaces "remember me" in localStorage;
 pages built with the same content key file (.contentkey, created next to the passphrases) share it.
*/
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const args = process.argv.slice(2);
const [plainPath, outPath, pwPath] = args;
const opt = (name, dflt) => { const i = args.indexOf(name); return i > -1 ? args[i + 1] : dflt; };
const title = opt("--title", "2026 Unwrapped");
const button = opt("--button", "Unwrap");
const instructions = opt("--instructions", "Enter the passphrase Gary shared with you.");
const keyId = opt("--key-id", "unwrapped-2026");

const passphrases = fs.readFileSync(pwPath, "utf8").split(/\r?\n/).map((s) => s.trim()).filter(Boolean);
if (!passphrases.length) { console.error("no passphrases"); process.exit(1); }

// Content key: reuse if present so sibling pages share "remember me".
const keyFile = path.join(path.dirname(pwPath), ".contentkey");
let contentKey;
if (fs.existsSync(keyFile)) contentKey = Buffer.from(fs.readFileSync(keyFile, "utf8").trim(), "base64");
else { contentKey = crypto.randomBytes(32); fs.writeFileSync(keyFile, contentKey.toString("base64") + "\n"); }

const ITER = 310000;
const salt = crypto.randomBytes(16);
function gcm(key, plaintext) {
  const iv = crypto.randomBytes(12);
  const c = crypto.createCipheriv("aes-256-gcm", key, iv);
  const ct = Buffer.concat([c.update(plaintext), c.final()]);
  return Buffer.concat([iv, ct, c.getAuthTag()]).toString("base64");
}
const html = fs.readFileSync(plainPath);
const payload = gcm(contentKey, html);
const slots = passphrases.map((p) => gcm(crypto.pbkdf2Sync(p.normalize("NFKC"), salt, ITER, 32, "sha256"), contentKey));
// shuffle slots so order reveals nothing
for (let i = slots.length - 1; i > 0; i--) { const j = crypto.randomInt(i + 1); [slots[i], slots[j]] = [slots[j], slots[i]]; }

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");
const page = `<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>${esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500&family=Inter:wght@400;600&family=JetBrains+Mono&display=swap" rel="stylesheet">
<style>
:root{--bg:#0b0a12;--ink:#f4f1ff;--ink-2:#b7b1cf;--ink-3:#7f789b;--mint:#4ee6b8;--violet:#a78bfa;--coral:#ff6b6b}
*{box-sizing:border-box;margin:0;padding:0}
body{min-height:100vh;display:grid;place-items:center;padding:24px;background:radial-gradient(800px 500px at 15% 10%,rgba(167,139,250,.22),transparent 60%),radial-gradient(700px 500px at 85% 90%,rgba(78,230,184,.16),transparent 60%),var(--bg);color:var(--ink);font-family:Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.gate{width:min(440px,100%);background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.1);border-radius:24px;padding:32px 28px;box-shadow:0 30px 80px rgba(0,0,0,.5)}
.k{font-family:"JetBrains Mono",monospace;font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--ink-3)}
h1{font-family:Fraunces,Georgia,serif;font-weight:500;letter-spacing:-.02em;font-size:2rem;margin:10px 0 6px}
h1 span{background:linear-gradient(90deg,var(--coral),#ffd166,var(--mint),#6cc5ff,var(--violet));-webkit-background-clip:text;background-clip:text;color:transparent}
p.hint{color:var(--ink-2);font-size:.95rem;margin:10px 0 22px;line-height:1.5}
.row{display:flex;gap:8px}
input[type=password],input[type=text]{flex:1;min-width:0;padding:13px 14px;border-radius:14px;border:1px solid rgba(255,255,255,.14);background:rgba(0,0,0,.3);color:var(--ink);font:inherit;font-size:1rem;outline:none}
input:focus{border-color:var(--violet)}
button{padding:13px 18px;border-radius:14px;border:0;background:var(--ink);color:#0b0a12;font:inherit;font-weight:600;cursor:pointer}
button:hover{background:#fff}
button[disabled]{opacity:.6;cursor:wait}
label.rm{display:flex;align-items:center;gap:8px;margin-top:14px;font-size:.85rem;color:var(--ink-2)}
.err{margin-top:12px;color:var(--coral);font-size:.9rem;min-height:1.2em}
.foot{margin-top:22px;font-size:.75rem;color:var(--ink-3)}
</style></head>
<body>
<form class="gate" id="gate">
  <div class="k">Private · Gary Mu</div>
  <h1><span>${esc(title)}</span></h1>
  <p class="hint">${esc(instructions)}</p>
  <div class="row"><input id="pw" type="password" placeholder="Passphrase" autocomplete="off" autocapitalize="none" autofocus aria-label="Passphrase"><button id="go" type="submit">${esc(button)}</button></div>
  <label class="rm"><input type="checkbox" id="rm" checked> Remember me on this device for 30 days</label>
  <div class="err" id="err" role="alert"></div>
  <div class="foot">Encrypted in your browser. Nothing is sent anywhere.</div>
</form>
<script>
(function(){
  var SALT="${salt.toString("base64")}", ITER=${ITER}, SLOTS=${JSON.stringify(slots)}, PAYLOAD="${payload}", KEY_ID=${JSON.stringify(keyId)};
  var b64=function(s){var b=atob(s),u=new Uint8Array(b.length);for(var i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u;};
  var sub=crypto.subtle, enc=new TextEncoder();
  function gcmOpen(key,blob){var u=b64(blob);return sub.decrypt({name:"AES-GCM",iv:u.slice(0,12)},key,u.slice(12));}
  function importRaw(raw,usages){return sub.importKey("raw",raw,{name:"AES-GCM"},false,usages);}
  function reveal(contentKeyRaw){return importRaw(contentKeyRaw,["decrypt"]).then(function(k){return gcmOpen(k,PAYLOAD);}).then(function(buf){var html=new TextDecoder().decode(buf);document.open();document.write(html);document.close();});}
  function tryPass(p){
    return sub.importKey("raw",enc.encode(p.normalize("NFKC")),{name:"PBKDF2"},false,["deriveKey"])
      .then(function(base){return sub.deriveKey({name:"PBKDF2",salt:b64(SALT),iterations:ITER,hash:"SHA-256"},base,{name:"AES-GCM",length:256},false,["decrypt"]);})
      .then(function(wrapKey){
        var i=0;function next(){if(i>=SLOTS.length)return Promise.reject(new Error("no"));return gcmOpen(wrapKey,SLOTS[i++]).catch(next);}
        return next();
      });
  }
  // remembered?
  // Remembered on this device? Wait for the parser to finish, otherwise document.open() is a no-op and the page would append instead of replace.
  function tryRemembered(){try{var saved=JSON.parse(localStorage.getItem(KEY_ID)||"null");if(saved&&saved.exp>Date.now()){reveal(b64(saved.k)).catch(function(){localStorage.removeItem(KEY_ID);});}}catch(e){}}
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",function(){setTimeout(tryRemembered,0);});else setTimeout(tryRemembered,0);
  var form=document.getElementById("gate"),pw=document.getElementById("pw"),go=document.getElementById("go"),err=document.getElementById("err"),rm=document.getElementById("rm");
  form.addEventListener("submit",function(ev){
    ev.preventDefault();err.textContent="";go.disabled=true;
    var p=pw.value.trim().toLowerCase();
    tryPass(p).then(function(raw){
      if(rm.checked){try{var k=btoa(String.fromCharCode.apply(null,new Uint8Array(raw)));localStorage.setItem(KEY_ID,JSON.stringify({k:k,exp:Date.now()+30*864e5}));}catch(e){}}
      return reveal(new Uint8Array(raw));
    }).catch(function(){err.textContent="That passphrase did not open it. Check the spelling and try again.";go.disabled=false;pw.select();});
  });
})();
</script>
</body></html>
`;
fs.writeFileSync(outPath, page);
console.log(`gate -> ${outPath} (${Math.round(fs.statSync(outPath).size / 1024)} KB, ${passphrases.length} passphrases)`);
