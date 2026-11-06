const vehicleData = [
  {
    id: 'sable',
    name: 'Aurelle Sable',
    category: 'Compact luxury SUV',
    price: 74500,
    description: 'A confident urban expression with elevated comfort, calm power delivery and a quietly commanding presence.',
    image: 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&q=80&w=1200',
    gallery: [
      'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=900',
      'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?auto=format&fit=crop&q=80&w=900',
      'https://images.unsplash.com/photo-1494905998402-395d579af36f?auto=format&fit=crop&q=80&w=900'
    ],
    highlights: ['All-wheel drive', 'Panoramic glass roof', 'Driver-assist intelligence'],
    performance: {
      range: '510 km (estimated)',
      acceleration: '5.1 s 0-100 km/h',
      speed: '210 km/h',
      battery: '98 kWh',
      charging: '10-80% in 28 minutes',
      seating: '5 seats',
      drivetrain: 'Dual-motor AWD',
      dimensions: '4,620 mm x 1,990 mm x 1,700 mm'
    },
    features: [
      'Quiet, composed ride with adaptive damping',
      'Digital cabin with ambient personalization',
      'Spatially rich sound architecture',
      'Thoughtful storage with flexible rear seating'
    ],
    specs: [
      ['Estimated driving range', '510 km'],
      ['Acceleration', '5.1 s'],
      ['Maximum speed', '210 km/h'],
      ['Battery capacity', '98 kWh'],
      ['Charging time', '28 min (10-80%)'],
      ['Seating capacity', '5'],
      ['Drivetrain', 'Dual-motor AWD'],
      ['Dimensions', '4620 x 1990 x 1700 mm']
    ]
  },
  {
    id: 'beaumont',
    name: 'Aurelle Beaumont',
    category: 'Executive luxury sedan',
    price: 89000,
    description: 'A serene grand tourer with a tailored cabin, effortless range and commanding executive presence.',
    image: 'https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=1200',
    gallery: [
      'https://images.unsplash.com/photo-1553440569-bcc63803a83d?auto=format&fit=crop&q=80&w=900',
      'https://images.unsplash.com/photo-1503736334956-4c8f8e92946d?auto=format&fit=crop&q=80&w=900',
      'https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&q=80&w=900'
    ],
    highlights: ['Executive lounge seating', 'Long-range efficiency', 'Adaptive road sensing'],
    performance: {
      range: '620 km (estimated)',
      acceleration: '4.6 s 0-100 km/h',
      speed: '230 km/h',
      battery: '112 kWh',
      charging: '10-80% in 29 minutes',
      seating: '5 seats',
      drivetrain: 'Dual-motor AWD',
      dimensions: '5,160 mm x 1,940 mm x 1,470 mm'
    },
    features: [
      'Immersive acoustics with active cabin insulation',
      'Personalized seating and climate intelligence',
      'Sculpted performance without visual aggression',
      'Cinematic lighting and layered material finishes'
    ],
    specs: [
      ['Estimated driving range', '620 km'],
      ['Acceleration', '4.6 s'],
      ['Maximum speed', '230 km/h'],
      ['Battery capacity', '112 kWh'],
      ['Charging time', '29 min (10-80%)'],
      ['Seating capacity', '5'],
      ['Drivetrain', 'Dual-motor AWD'],
      ['Dimensions', '5160 x 1940 x 1470 mm']
    ]
  },
  {
    id: 'marlowe',
    name: 'Aurelle Marlowe',
    category: 'Luxury family SUV',
    price: 98000,
    description: 'A thoughtfully balanced family SUV that brings serene capability, generous space and premium refinement.',
    image: 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&q=80&w=1200',
    gallery: [
      'https://images.unsplash.com/photo-1553440569-bcc63803a83d?auto=format&fit=crop&q=80&w=900',
      'https://images.unsplash.com/photo-1489824904134-891ab64532f1?auto=format&fit=crop&q=80&w=900',
      'https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&q=80&w=900'
    ],
    highlights: ['7-seat option', 'Family-focused comfort', 'Smart charge routing'],
    performance: {
      range: '590 km (estimated)',
      acceleration: '5.4 s 0-100 km/h',
      speed: '215 km/h',
      battery: '106 kWh',
      charging: '10-80% in 31 minutes',
      seating: '7 seats',
      drivetrain: 'Dual-motor AWD',
      dimensions: '4,960 mm x 2,020 mm x 1,760 mm'
    },
    features: [
      'Flexible seating for family life, long-distance travel and everyday convenience',
      'Cabin atmosphere tuned for warm, calming luxury',
      'Adaptive route planning informed by charging and weather conditions',
      'Silent power delivery with a stable, luxurious ride'
    ],
    specs: [
      ['Estimated driving range', '590 km'],
      ['Acceleration', '5.4 s'],
      ['Maximum speed', '215 km/h'],
      ['Battery capacity', '106 kWh'],
      ['Charging time', '31 min (10-80%)'],
      ['Seating capacity', '7'],
      ['Drivetrain', 'Dual-motor AWD'],
      ['Dimensions', '4960 x 2020 x 1760 mm']
    ]
  },
  {
    id: 'regent',
    name: 'Aurelle Regent',
    category: 'Flagship luxury SUV',
    price: 124000,
    description: 'A flagship statement of power, serenity and craftsmanship for those who expect extraordinary presence.',
    image: 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&q=80&w=1200',
    gallery: [
      'https://images.unsplash.com/photo-1493238792000-8113da705763?auto=format&fit=crop&q=80&w=900',
      'https://images.unsplash.com/photo-1525609004556-c46c7d6cf023?auto=format&fit=crop&q=80&w=900',
      'https://images.unsplash.com/photo-1541443131876-44b03de101c5?auto=format&fit=crop&q=80&w=900'
    ],
    highlights: ['Grand touring dynamics', 'Signature lounge cabin', 'Luxury chauffeur configuration'],
    performance: {
      range: '660 km (estimated)',
      acceleration: '4.3 s 0-100 km/h',
      speed: '240 km/h',
      battery: '128 kWh',
      charging: '10-80% in 30 minutes',
      seating: '5 or 7 seats',
      drivetrain: 'Tri-motor AWD',
      dimensions: '5,190 mm x 2,060 mm x 1,820 mm'
    },
    features: [
      'A signature cabin with executive rear seating and elevated craftsmanship',
      'Dynamic air suspension with active road recognition',
      'Soundscapes and climate intelligence shaped for complete comfort',
      'Flagship design language balanced with subtle elegance'
    ],
    specs: [
      ['Estimated driving range', '660 km'],
      ['Acceleration', '4.3 s'],
      ['Maximum speed', '240 km/h'],
      ['Battery capacity', '128 kWh'],
      ['Charging time', '30 min (10-80%)'],
      ['Seating capacity', '5 / 7'],
      ['Drivetrain', 'Tri-motor AWD'],
      ['Dimensions', '5190 x 2060 x 1820 mm']
    ]
  }
];

const chargingStations = [
  {
    name: 'Aurelle Marina District',
    city: 'Accra',
    status: 'Operational',
    type: 'CCS / Type 2',
    speed: '180 kW',
    points: 8,
    area: 'Marina District'
  },
  {
    name: 'Aurelle Tema Motorway',
    city: 'Tema',
    status: 'Operational',
    type: 'CCS / CHAdeMO',
    speed: '200 kW',
    points: 6,
    area: 'Tema Motorway'
  },
  {
    name: 'Aurelle Kumasi Exchange',
    city: 'Kumasi',
    status: 'Busy',
    type: 'Type 2 / CCS',
    speed: '120 kW',
    points: 5,
    area: 'Kejetia Junction'
  },
  {
    name: 'Aurelle Cape Coast Riviera',
    city: 'Cape Coast',
    status: 'Operational',
    type: 'Type 2 / CCS',
    speed: '150 kW',
    points: 4,
    area: 'Riviera District'
  }
];

const faqData = [
  {
    question: 'Do Aurelle vehicles operate on a public charging network?',
    answer: 'Yes. Aurelle is building an open charging network designed to accommodate Aurelle vehicles and compatible EVs from other manufacturers. This is a conceptual service model for a premium, accessible infrastructure ecosystem.'
  },
  {
    question: 'Are these performance and range figures final production numbers?',
    answer: 'No. The specifications shown throughout the site are illustrative concept specifications created for the prototype experience and should not be treated as verified production figures.'
  },
  {
    question: 'Can I choose my preferred trim and package?',
    answer: 'Yes. The interactive configurator allows selection across vehicle, exterior finish, wheels, interior trim and additional options. The final summary updates in real time with the estimated total.'
  },
  {
    question: 'What is included in the ownership experience?',
    answer: 'The ownership concept includes servicing, charging support, software updates and customer care. These details are presented as proposed offerings rather than confirmed real-world guarantees.'
  }
];

window.aurelleVehicles = vehicleData;

function currency(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0
  }).format(value);
}

function renderFeaturedVehicles() {
  const grid = document.getElementById('featured-vehicles-grid');
  if (!grid) return;

  grid.innerHTML = vehicleData.slice(0, 3).map((vehicle) => `
    <article class="feature-card reveal">
      <img src="${vehicle.image}" alt="${vehicle.name}" />
      <div class="card-body">
        <div class="card-header">
          <div>
            <h3>${vehicle.name}</h3>
            <span class="category-label">${vehicle.category}</span>
          </div>
          <span class="inline-link">From ${currency(vehicle.price)}</span>
        </div>
        <p>${vehicle.description}</p>
        <div class="card-actions">
          <button class="btn btn-secondary" type="button" data-vehicle-id="${vehicle.id}">Explore vehicle</button>
          <button class="btn btn-tertiary" type="button" data-config-vehicle="${vehicle.id}">Configure</button>
        </div>
      </div>
    </article>
  `).join('');
}

function renderVehicleCards() {
  const grid = document.getElementById('vehicle-cards');
  if (!grid) return;

  grid.innerHTML = vehicleData.map((vehicle) => `
    <article class="vehicle-card reveal">
      <img src="${vehicle.image}" alt="${vehicle.name}" />
      <div class="card-body">
        <div class="card-header">
          <div>
            <h3>${vehicle.name}</h3>
            <span class="category-label">${vehicle.category}</span>
          </div>
          <span class="inline-link">From ${currency(vehicle.price)}</span>
        </div>
        <p>${vehicle.description}</p>
        <div class="card-actions">
          <button class="btn btn-secondary" type="button" data-vehicle-id="${vehicle.id}">Explore</button>
          <button class="btn btn-primary" type="button" data-config-vehicle="${vehicle.id}">Configure</button>
        </div>
      </div>
    </article>
  `).join('');
}

function renderVehicleDetail(vehicleId) {
  const container = document.getElementById('vehicle-detail-content');
  if (!container) return;

  const vehicle = vehicleData.find((item) => item.id === vehicleId) || vehicleData[0];

  container.innerHTML = `
    <div class="detail-hero">
      <img src="${vehicle.image}" alt="${vehicle.name}" />
      <div class="detail-summary">
        <p class="eyebrow subdued">${vehicle.category}</p>
        <h2>${vehicle.name}</h2>
        <p>${vehicle.description}</p>
        <div class="price">From ${currency(vehicle.price)}</div>
        <div class="card-actions" style="margin-top: 1.3rem;">
          <button class="btn btn-primary" type="button" data-config-vehicle="${vehicle.id}">Configure this vehicle</button>
          <a class="btn btn-secondary" href="#configurator">Build Your Aurelle</a>
        </div>
      </div>
    </div>

    <div class="detail-grid">
      <div class="detail-panel">
        <h3>Exterior gallery</h3>
        <div class="gallery-grid">
          ${vehicle.gallery.map((image) => `<img src="${image}" alt="${vehicle.name} gallery" />`).join('')}
        </div>
      </div>

      <div class="detail-panel">
        <h3>Key design features</h3>
        <ul class="checklist">
          ${vehicle.highlights.map((item) => `<li><span>${item}</span><span>•</span></li>`).join('')}
        </ul>
      </div>

      <div class="detail-panel">
        <h3>Performance</h3>
        <ul class="spec-list">
          <li><span>Estimated driving range</span><span>${vehicle.performance.range}</span></li>
          <li><span>Acceleration</span><span>${vehicle.performance.acceleration}</span></li>
          <li><span>Maximum speed</span><span>${vehicle.performance.speed}</span></li>
          <li><span>Battery capacity</span><span>${vehicle.performance.battery}</span></li>
        </ul>
      </div>

      <div class="detail-panel">
        <h3>Charging</h3>
        <ul class="spec-list">
          <li><span>Charging time</span><span>${vehicle.performance.charging}</span></li>
          <li><span>Seating capacity</span><span>${vehicle.performance.seating}</span></li>
          <li><span>Drivetrain</span><span>${vehicle.performance.drivetrain}</span></li>
          <li><span>Dimensions</span><span>${vehicle.performance.dimensions}</span></li>
        </ul>
      </div>

      <div class="detail-panel" style="grid-column: 1 / -1;">
        <h3>Interior and technology</h3>
        <ul class="checklist">
          ${vehicle.features.map((feature) => `<li><span>${feature}</span><span>✓</span></li>`).join('')}
        </ul>
      </div>

      <div class="detail-panel" style="grid-column: 1 / -1;">
        <h3>Technical specifications</h3>
        <ul class="spec-list">
          ${vehicle.specs.map(([label, value]) => `<li><span>${label}</span><span>${value}</span></li>`).join('')}
        </ul>
      </div>
    </div>
  `;
}

function renderStations(searchTerm = '') {
  const stationGrid = document.getElementById('station-grid');
  if (!stationGrid) return;

  const filtered = chargingStations.filter((station) => {
    const query = searchTerm.trim().toLowerCase();
    if (!query) return true;
    return [station.name, station.city, station.area].some((value) => value.toLowerCase().includes(query));
  });

  stationGrid.innerHTML = filtered.map((station) => `
    <article class="station-card">
      <p class="eyebrow subdued">${station.city}</p>
      <h4>${station.name}</h4>
      <p>${station.area}</p>
      <div class="station-meta">
        <span class="status-pill">${station.status}</span>
        <span>${station.speed}</span>
      </div>
      <div class="station-meta">
        <span>${station.type}</span>
        <span>${station.points} points</span>
      </div>
    </article>
  `).join('');

  if (!filtered.length) {
    stationGrid.innerHTML = '<p>No charging stations match your search. Try Accra, Tema, Kumasi or Cape Coast.</p>';
  }
}

function renderFaqs() {
  const faqList = document.getElementById('faq-list');
  if (!faqList) return;

  faqList.innerHTML = faqData.map((item, index) => `
    <div class="faq-item ${index === 0 ? 'active' : ''}">
      <button class="faq-question" type="button">
        <span>${item.question}</span>
        <span>+</span>
      </button>
      <div class="faq-answer">
        <p>${item.answer}</p>
      </div>
    </div>
  `).join('');

  faqList.querySelectorAll('.faq-question').forEach((button) => {
    button.addEventListener('click', () => {
      const item = button.parentElement;
      const isActive = item.classList.contains('active');
      item.classList.toggle('active', !isActive);
    });
  });
}

function setHeaderState() {
  const header = document.querySelector('.site-header');
  if (!header) return;
  header.classList.toggle('scrolled', window.scrollY > 30);
}

function initRevealAnimations() {
  const elements = document.querySelectorAll('.reveal');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.15 });

  elements.forEach((element) => observer.observe(element));
}

function setupNavigation() {
  const header = document.querySelector('.site-header');
  const menuToggle = document.querySelector('.menu-toggle');
  const mobileMenu = document.querySelector('.mobile-menu');

  if (menuToggle && mobileMenu) {
    menuToggle.addEventListener('click', () => {
      const isOpen = mobileMenu.classList.toggle('open');
      menuToggle.setAttribute('aria-expanded', String(isOpen));
    });

    mobileMenu.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
        menuToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  document.querySelector('[data-account-trigger]')?.addEventListener('click', () => {
    document.getElementById('account')?.scrollIntoView({ behavior: 'smooth' });
  });

  document.addEventListener('click', (event) => {
    const vehicleId = event.target.closest('[data-vehicle-id]');
    if (vehicleId) {
      const selected = vehicleId.getAttribute('data-vehicle-id');
      renderVehicleDetail(selected);
      document.getElementById('detail-view')?.scrollIntoView({ behavior: 'smooth' });
    }

    const configVehicle = event.target.closest('[data-config-vehicle]');
    if (configVehicle) {
      const vehicle = configVehicle.getAttribute('data-config-vehicle');
      if (window.configureVehicle) {
        window.configureVehicle(vehicle);
      }
      document.getElementById('configurator')?.scrollIntoView({ behavior: 'smooth' });
    }
  });
}

function setupChargerSearch() {
  const form = document.getElementById('charger-search-form');
  const input = document.getElementById('charger-search');

  if (!form || !input) return;

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    renderStations(input.value);
  });
}

function setupForms() {
  const contactForm = document.getElementById('contact-form');
  const status = document.getElementById('form-status');

  if (contactForm && status) {
    contactForm.addEventListener('submit', (event) => {
      event.preventDefault();
      const formData = new FormData(contactForm);
      const values = Object.fromEntries(formData.entries());
      const valid = Object.values(values).every((value) => String(value).trim() !== '');

      if (!valid) {
        status.textContent = 'Please complete every field before submitting.';
        status.className = 'form-status error';
        return;
      }

      const saved = JSON.parse(localStorage.getItem('aurelleEnquiries') || '[]');
      saved.push({
        ...values,
        date: new Date().toISOString()
      });
      localStorage.setItem('aurelleEnquiries', JSON.stringify(saved));

      status.textContent = 'Your enquiry has been recorded in this demonstration experience.';
      status.className = 'form-status success';
      contactForm.reset();
    });
  }

  const signInForm = document.getElementById('signin-form');
  const regForm = document.getElementById('register-form');
  const authButtons = document.querySelectorAll('.tab-button');

  authButtons.forEach((button) => {
    button.addEventListener('click', () => {
      authButtons.forEach((item) => item.classList.toggle('active', item === button));
      const mode = button.dataset.auth;
      document.getElementById('signin-form').classList.toggle('hidden', mode !== 'signin');
      document.getElementById('register-form').classList.toggle('hidden', mode !== 'register');
    });
  });

  signInForm?.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(signInForm);
    const email = formData.get('email');
    const stored = JSON.parse(localStorage.getItem('aurelleAccount') || '{}');
    stored.email = email;
    stored.name = stored.name || 'Aurelle Member';
    localStorage.setItem('aurelleAccount', JSON.stringify(stored));
    updateAccountSummary();
  });

  regForm?.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(regForm);
    const payload = {
      name: formData.get('fullName'),
      email: formData.get('email'),
      password: formData.get('password')
    };
    localStorage.setItem('aurelleAccount', JSON.stringify(payload));
    updateAccountSummary();
  });
}

function updateAccountSummary() {
  const account = JSON.parse(localStorage.getItem('aurelleAccount') || '{}');
  const accountName = document.getElementById('account-name');
  const accountEmail = document.getElementById('account-email');
  const savedConfigs = document.getElementById('saved-configurations-list');
  const savedEnquiries = document.getElementById('saved-enquiries-list');

  if (accountName) {
    accountName.textContent = account.name || 'Aurelle Member';
  }

  if (accountEmail) {
    accountEmail.textContent = account.email || 'member@aurelle.com';
  }

  const configurations = JSON.parse(localStorage.getItem('aurelleSavedConfigs') || '[]');
  const enquiries = JSON.parse(localStorage.getItem('aurelleEnquiries') || '[]');

  if (savedConfigs) {
    savedConfigs.innerHTML = configurations.length
      ? configurations.map((item) => `<li>${item.vehicleName} — ${currency(item.total)}</li>`).join('')
      : '<li>No saved configurations yet.</li>';
  }

  if (savedEnquiries) {
    savedEnquiries.innerHTML = enquiries.length
      ? enquiries.slice(0, 3).map((item) => `<li>${item.inquiry || 'General enquiry'} — ${item.email}</li>`).join('')
      : '<li>No vehicle enquiries yet.</li>';
  }
}

function initializePage() {
  setHeaderState();
  renderFeaturedVehicles();
  renderVehicleCards();
  renderVehicleDetail('sable');
  renderStations();
  renderFaqs();
  setupNavigation();
  setupChargerSearch();
  setupForms();
  initRevealAnimations();
  updateAccountSummary();

  window.addEventListener('scroll', setHeaderState);
}

document.addEventListener('DOMContentLoaded', initializePage);
window.renderVehicleDetail = renderVehicleDetail;
