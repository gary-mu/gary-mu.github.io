// Cut the subject out of an image with macOS's built-in subject lifting (Vision).
// swift _build/lift_subject.swift <in.jpg> <out.png>
import Foundation
import Vision
import CoreImage
import AppKit

let args = CommandLine.arguments
guard args.count == 3, let src = CIImage(contentsOf: URL(fileURLWithPath: args[1])) else { print("usage: lift_subject <in> <out.png>"); exit(2) }
let handler = VNImageRequestHandler(ciImage: src, options: [:])
let request = VNGenerateForegroundInstanceMaskRequest()
do {
    try handler.perform([request])
    guard let obs = request.results?.first else { print("no subject found"); exit(1) }
    let buffer = try obs.generateMaskedImage(ofInstances: obs.allInstances, from: handler, croppedToInstancesExtent: false)
    let out = CIImage(cvPixelBuffer: buffer)
    let ctx = CIContext()
    guard let cs = CGColorSpace(name: CGColorSpace.sRGB) else { exit(1) }
    try ctx.writePNGRepresentation(of: out, to: URL(fileURLWithPath: args[2]), format: .RGBA8, colorSpace: cs)
    print("ok \(obs.allInstances.count) instance(s) -> \(args[2])")
} catch { print("error: \(error)"); exit(1) }
