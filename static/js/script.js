document.addEventListener('DOMContentLoaded', () => {

    // ==========================================
    // 1. CHAT AUTO-SCROLL
    // ==========================================
    const chatContainer = document.getElementById('message-container') || document.getElementById('chatContainer');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // ==========================================
    // 2. INITIALIZE ANIMATIONS
    // ==========================================
    initHeroAnimation();
    initGlobalAnimation();
});


// ==========================================
// 3. AI CHAT LOGIC
// ==========================================
window.sendAIMessage = function () {
    const inputField = document.getElementById("aiInput");
    const replyBox = document.getElementById("aiReply");
    if (!inputField || !replyBox) return;

    const msg = inputField.value.trim();
    if (!msg) return;

    replyBox.innerHTML = `
        <div class="flex items-center gap-2 text-slate-500 animate-pulse">
            <i class="fa-solid fa-circle-notch fa-spin"></i> Heritage Hub AI is thinking...
        </div>`;

    fetch(`/advisor/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: `message=${encodeURIComponent(msg)}`
    })
        .then(res => res.json())
        .then(data => {
            replyBox.innerHTML = `
            <div class="animate-fade-in p-4 bg-slate-800/50 rounded-2xl border-l-4 border-brand-600">
                <p class="text-sm text-slate-200">${data.response || data.reply}</p>
            </div>
        `;
            inputField.value = "";
        })
        .catch(err => {
            console.error(err);
            replyBox.innerHTML = '<span class="text-red-500 text-sm">Connection error.</span>';
        });
}


// =========================================================
// 4. HERO ANIMATION: "SPIDER WEB" (For Dark Mode)
// =========================================================
function initHeroAnimation() {
    const canvas = document.getElementById('hero-canvas');
    const section = document.getElementById('hero-section');

    if (!canvas || !section) return;

    const ctx = canvas.getContext('2d');
    let width, height;
    let particles = [];

    let mouse = { x: -5000, y: -5000 };

    // Deep Orange / Gold for Dark Mode stars
    const config = {
        particleCount: 120,
        dotSize: 1.5,
        color: '230, 126, 34',
        connectionRadius: 160,
        mouseRadius: 250,
        baseSpeed: 0.4,
    };

    function resize() {
        width = canvas.width = section.offsetWidth;
        height = canvas.height = section.offsetHeight;
        config.particleCount = width < 768 ? 60 : 120;
        initParticles();
    }

    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.vx = (Math.random() - 0.5) * config.baseSpeed;
            this.vy = (Math.random() - 0.5) * config.baseSpeed;
            this.size = Math.random() * config.dotSize + 0.5;
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;

            if (this.x < 0 || this.x > width) this.vx *= -1;
            if (this.y < 0 || this.y > height) this.vy *= -1;

            const dx = mouse.x - this.x;
            const dy = mouse.y - this.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < config.mouseRadius) {
                const forceDirectionX = dx / distance;
                const forceDirectionY = dy / distance;
                const force = (config.mouseRadius - distance) / config.mouseRadius;
                const attractionStrength = 0.03;
                this.vx += forceDirectionX * force * attractionStrength;
                this.vy += forceDirectionY * force * attractionStrength;
            }
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${config.color}, 0.8)`;
            ctx.fill();
        }
    }

    function initParticles() {
        particles = [];
        for (let i = 0; i < config.particleCount; i++) {
            particles.push(new Particle());
        }
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);
        for (let i = 0; i < particles.length; i++) {
            particles[i].update();
            particles[i].draw();
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < config.connectionRadius) {
                    let opacity = 1 - (distance / config.connectionRadius);
                    opacity = opacity * 0.2; // Suble lines

                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(${config.color}, ${opacity})`;
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(animate);
    }

    section.addEventListener('mousemove', (e) => {
        const rect = section.getBoundingClientRect();
        mouse.x = e.clientX - rect.left;
        mouse.y = e.clientY - rect.top;
    });

    window.addEventListener('resize', resize);
    resize();
    animate();
}


// =========================================================
// 5. GLOBAL ANIMATION: "GLOWING BOKEH"
// =========================================================
function initGlobalAnimation() {
    const canvas = document.getElementById('global-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width, height;
    let particles = [];

    const config = {
        count: 50,
        minSize: 1,
        maxSize: 4,
        speed: 0.15,
        color: '148, 163, 184', // Slate-400
    };

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
        initParticles();
    }

    class Orb {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.vx = (Math.random() - 0.5) * config.speed;
            this.vy = (Math.random() - 0.5) * config.speed;
            this.radius = Math.random() * (config.maxSize - config.minSize) + config.minSize;
            this.alpha = Math.random() * 0.3 + 0.1;
            this.dAlpha = (Math.random() * 0.002) + 0.001;
            this.alphaDirection = 1;
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;

            if (this.x < -50) this.x = width + 50;
            if (this.x > width + 50) this.x = -50;
            if (this.y < -50) this.y = height + 50;
            if (this.y > height + 50) this.y = -50;

            this.alpha += this.dAlpha * this.alphaDirection;
            if (this.alpha >= 0.4) this.alphaDirection = -1;
            else if (this.alpha <= 0.1) this.alphaDirection = 1;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${config.color}, ${this.alpha})`;
            ctx.fill();
        }
    }

    function initParticles() {
        particles = [];
        for (let i = 0; i < config.count; i++) {
            particles.push(new Orb());
        }
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);
        particles.forEach(p => {
            p.update();
            p.draw();
        });
        requestAnimationFrame(animate);
    }

    window.addEventListener('resize', resize);
    resize();
    animate();
}
