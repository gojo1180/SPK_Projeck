// Hero Carousel
document.addEventListener('DOMContentLoaded', () => {
  const carouselImages = [
    'https://foodrevolution.org/wp-content/uploads/2019/03/iStock-925240050-1-1.jpg',
    'https://www.eatthis.com/wp-content/uploads/sites/4/2021/01/banana-chia-pudding.jpg?quality=82&strip=1',
    'https://images.squarespace-cdn.com/content/v1/5ea3b22556f3d073f3d9cae4/1739232967306-FYB9WV8AC48QOEVNX67H/IMG_1180.jpg'
  ];

  const hero = document.getElementById('hero-carousel');
  let currentIndex = 0;

  carouselImages.forEach((src, i) => {
    const img = document.createElement('img');
    img.src = src;
    img.className = 'hero-image';
    if (i === 0) img.classList.add('active');
    hero.appendChild(img);
  });

  const images = hero.querySelectorAll('.hero-image');

  function nextSlide() {
    images[currentIndex].classList.remove('active');
    currentIndex = (currentIndex + 1) % images.length;
    images[currentIndex].classList.add('active');
  }

  setInterval(nextSlide, 4000);
});

// Tab Filter
function showTab(tabName) {
  document.querySelectorAll('.tab-button').forEach(btn => {
    btn.classList.remove('bg-green-600', 'text-white');
    btn.classList.add('bg-gray-200', 'text-gray-700');
  });

  const activeBtn = [...document.querySelectorAll('.tab-button')]
    .find(btn => btn.textContent.toLowerCase().includes(tabName));

  if (activeBtn) {
    activeBtn.classList.remove('bg-gray-200', 'text-gray-700');
    activeBtn.classList.add('bg-green-600', 'text-white');
  }

  document.querySelectorAll('.card').forEach(card => {
    if (card.dataset.tab === tabName) {
      card.classList.remove('hidden');
    } else {
      card.classList.add('hidden');
    }
  });
}

showTab('bulking');

// Statistik Count-up dan Tilt
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const number = entry.target.querySelector('.stat-number');
      const target = parseInt(entry.target.getAttribute('data-target'));
      const suffix = entry.target.getAttribute('data-suffix') || "";
      let count = 0;
      const increment = target / 60;

      const update = () => {
        count += increment;
        if (count < target) {
          number.textContent = Math.floor(count) + suffix;
          requestAnimationFrame(update);
        } else {
          number.textContent = target + suffix;
        }
      };
      update();
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.6 });

document.querySelectorAll('.stat-card').forEach(card => observer.observe(card));

// Tilt effect
document.querySelectorAll('.stat-card').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const rotateX = (y / rect.height - 0.5) * -10;
    const rotateY = (x / rect.width - 0.5) * 10;
    card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.05)`;
  });

  card.addEventListener('mouseleave', () => {
    card.style.transform = `rotateX(0deg) rotateY(0deg) scale(1)`;
  });
});

// AOS Init
AOS.init();

document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('nav-toggle');
    const menu = document.getElementById('nav-menu');

    toggle.addEventListener('click', () => {
      menu.classList.toggle('hidden');
      menu.classList.toggle('flex');
      menu.classList.add('flex-col', 'bg-white', 'py-4', 'px-4', 'shadow-md', 'rounded', 'mt-2', 'md:flex-row', 'md:shadow-none', 'md:bg-transparent', 'md:mt-0');
    });
  });