const app = {
    init() {
        this.feedContainer = document.getElementById('feed-container');
        this.loader = document.getElementById('loader');

        // Asset Database with Metadata
        this.assets = {
            legs: [
                { src: 'assets/images/leg_1.png', tags: { color: 'fantasy', size: 'athletic', legwear: 'none' }, aesthetic: 'Cyberpunk' },
                { src: 'assets/images/leg_2.png', tags: { color: 'fair', size: 'slim', legwear: 'socks' }, aesthetic: 'Cozy Morning' },
                { src: 'assets/images/leg_dark_athletic.png', tags: { color: 'dark', size: 'athletic', legwear: 'socks' }, aesthetic: 'Sporty' },
                { src: 'assets/images/leg_tan_fishnets.png', tags: { color: 'tan', size: 'curvy', legwear: 'stockings' }, aesthetic: 'Glamour' },
                { src: 'assets/images/leg_fair_kneehighs.png', tags: { color: 'fair', size: 'slim', legwear: 'stockings' }, aesthetic: 'Pastel' },
                { src: 'assets/images/leg_fantasy.png', tags: { color: 'fantasy', size: 'athletic', legwear: 'none' }, aesthetic: 'Sci-Fi' }
            ],
            ads: ['assets/images/ad_1.png']
        };

        this.currentFilters = {
            color: 'all',
            size: 'all',
            legwear: 'all'
        };

        this.itemCount = 0;
        this.isLoading = false;

        this.bindEvents();

        // Intersection Observer
        this.observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting && !this.isLoading) {
                this.loadMoreItems();
            }
        }, { rootMargin: '200px' });

        this.observer.observe(this.loader);

        // Initial load
        this.loadMoreItems();
    },

    bindEvents() {
        document.getElementById('filter-color').addEventListener('change', (e) => this.updateFilter('color', e.target.value));
        document.getElementById('filter-size').addEventListener('change', (e) => this.updateFilter('size', e.target.value));
        document.getElementById('filter-legwear').addEventListener('change', (e) => this.updateFilter('legwear', e.target.value));
    },

    updateFilter(type, value) {
        this.currentFilters[type] = value;
        this.resetFeed();
    },

    resetFeed() {
        this.feedContainer.innerHTML = '';
        this.itemCount = 0;
        this.loadMoreItems();
    },

    getFilteredAssets() {
        return this.assets.legs.filter(asset => {
            const matchColor = this.currentFilters.color === 'all' || asset.tags.color === this.currentFilters.color;
            const matchSize = this.currentFilters.size === 'all' || asset.tags.size === this.currentFilters.size;
            const matchLegwear = this.currentFilters.legwear === 'all' || asset.tags.legwear === this.currentFilters.legwear;
            return matchColor && matchSize && matchLegwear;
        });
    },

    loadMoreItems() {
        this.isLoading = true;
        this.loader.classList.remove('hidden');

        // Simulate network delay
        setTimeout(() => {
            const filteredLegs = this.getFilteredAssets();

            if (filteredLegs.length === 0) {
                this.loader.textContent = "No matches found.";
                this.isLoading = false;
                return; // Stop loading
            } else {
                this.loader.textContent = "Targeting Aesthetics...";
            }

            const batchSize = 6;
            for (let i = 0; i < batchSize; i++) {
                this.itemCount++;
                // Show ad every 5th post, but only if we have filtered content to show
                if (this.itemCount % 5 === 0) {
                    this.renderAd();
                } else {
                    this.renderLegItem(filteredLegs);
                }
            }
            this.isLoading = false;
            this.loader.classList.add('hidden');
        }, 600);
    },

    getRandomAsset(list) {
        return list[Math.floor(Math.random() * list.length)];
    },

    renderLegItem(sourceList) {
        const item = this.getRandomAsset(sourceList);
        const card = document.createElement('div');
        card.className = 'card';

        const likes = Math.floor(Math.random() * 2000) + 100;

        card.innerHTML = `
            <div class="card-image-wrap">
                <img src="${item.src}" alt="AI Generated Legs" loading="lazy">
                <div class="card-overlay">
                    <div class="card-info">
                        <h3>Legs #${this.itemCount}</h3>
                        <div class="card-meta">${item.aesthetic} • ${item.tags.color} • ${item.tags.size}</div>
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
        const imgSrc = this.getRandomAsset(this.assets.ads);

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
