const app = {
    init() {
        this.feedContainer = document.getElementById('feed-container');
        this.loader = document.getElementById('loader');
        this.assets = {
            legs: ['assets/images/leg_1.png', 'assets/images/leg_2.png'],
            ads: ['assets/images/ad_1.png']
        };
        this.itemCount = 0;
        this.isLoading = false;

        // Intersection Observer for Infinite Scroll
        this.observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting && !this.isLoading) {
                this.loadMoreItems();
            }
        }, { rootMargin: '200px' });

        this.observer.observe(this.loader);
        
        // Initial load
        this.loadMoreItems();
    },

    loadMoreItems() {
        this.isLoading = true;
        this.loader.classList.remove('hidden');

        // Simulate network delay
        setTimeout(() => {
            const batchSize = 6;
            for (let i = 0; i < batchSize; i++) {
                this.itemCount++;
                if (this.itemCount % 5 === 0) {
                    this.renderAd();
                } else {
                    this.renderLegItem();
                }
            }
            this.isLoading = false;
            this.loader.classList.add('hidden');
        }, 800);
    },

    getRandomAsset(type) {
        const list = this.assets[type];
        return list[Math.floor(Math.random() * list.length)];
    },

    renderLegItem() {
        const card = document.createElement('div');
        card.className = 'card';
        
        const imgSrc = this.getRandomAsset('legs');
        const likes = Math.floor(Math.random() * 2000) + 100;
        const aesthetic = ['Cyberpunk', 'Cozy', 'Streetwear', 'Vintage', 'Neon'][Math.floor(Math.random() * 5)];

        card.innerHTML = `
            <div class="card-image-wrap">
                <img src="${imgSrc}" alt="AI Generated Legs" loading="lazy">
                <div class="card-overlay">
                    <div class="card-info">
                        <h3>Legs #${this.itemCount}</h3>
                        <div class="card-meta">${aesthetic} Aesthetic</div>
                    </div>
                    <button class="like-btn" onclick="this.classList.toggle('liked')">♥</button>
                </div>
            </div>
        `;
        this.feedContainer.appendChild(card);
    },

    renderAd() {
        const card = document.createElement('div');
        card.className = 'card ad-card';
        const imgSrc = this.getRandomAsset('ads');

        card.innerHTML = `
            <div class="ad-badge">Sponsored</div>
            <div class="card-image-wrap">
                <img src="${imgSrc}" alt="Socks Advertisement" loading="lazy">
                <div class="card-overlay">
                    <div class="card-info">
                        <h3>Premium Comfort</h3>
                        <div class="card-meta">50% Off Today</div>
                    </div>
                </div>
            </div>
            <a href="#" class="cta-btn">Shop Now</a>
        `;
        this.feedContainer.appendChild(card);
    }
};

document.addEventListener('DOMContentLoaded', () => {
    app.init();
});
