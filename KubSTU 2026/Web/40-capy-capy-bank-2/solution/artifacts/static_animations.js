// Intersection Observer for scroll animations
document.addEventListener('DOMContentLoaded', function() {
    // Animate elements on scroll
    const animateElements = document.querySelectorAll('[data-animate]');
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const delay = entry.target.getAttribute('data-delay') || 0;
                setTimeout(() => {
                    entry.target.classList.add('animated');
                }, delay);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    animateElements.forEach(element => {
        observer.observe(element);
    });
    
    // Smooth scroll to services
    const heroScroll = document.querySelector('.hero-scroll');
    if (heroScroll) {
        heroScroll.addEventListener('click', function(e) {
            e.preventDefault();
            const servicesSection = document.querySelector('#services');
            if (servicesSection) {
                servicesSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    }
    
    // Parallax effect for hero background
    const heroBackground = document.querySelector('.hero-background');
    if (heroBackground) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * 0.3;
            if (scrolled < window.innerHeight) {
                heroBackground.style.transform = `translateY(${rate}px)`;
            }
        });
    }
    
    // Add floating animation to product cards
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach((card, index) => {
        const delay = index * 0.1;
        card.style.animationDelay = `${delay}s`;
    });
    
    // Counter animation for stats
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(stat => {
        const target = stat.textContent;
        const isNumber = /[\d,]+/.test(target);
        
        if (isNumber) {
            const observer = new IntersectionObserver(function(entries) {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        animateCounter(stat, target);
                        observer.unobserve(stat);
                    }
                });
            }, { threshold: 0.5 });
            
            observer.observe(stat);
        }
    });
    
    function animateCounter(element, target) {
        const text = target;
        const match = text.match(/[\d,]+/);
        if (!match) return;
        
        const finalNumber = parseInt(match[0].replace(/,/g, ''));
        const duration = 2000;
        const increment = finalNumber / (duration / 16);
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= finalNumber) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                const formatted = Math.floor(current).toLocaleString('ru-RU');
                element.textContent = text.replace(/[\d,]+/, formatted);
            }
        }, 16);
    }
});

