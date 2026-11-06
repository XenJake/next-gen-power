const configDefaults = {
  selectedVehicle: 'sable',
  color: 'Obsidian Black',
  wheel: '20" Aero',
  interior: 'Obsidian leather',
  packages: ['Premium sound system'],
  charging: 'Vehicle only'
};

const colorOptions = [
  { name: 'Obsidian Black', hex: '#111211' },
  { name: 'Pearl White', hex: '#f3efe8' },
  { name: 'Champagne Silver', hex: '#b9b0a3' },
  { name: 'Midnight Blue', hex: '#1d2a38' },
  { name: 'British Racing Green', hex: '#163423' },
  { name: 'Burgundy', hex: '#4f1a1a' },
  { name: 'Graphite Grey', hex: '#4d5155' }
];

const wheelOptions = [
  { name: '20" Aero', price: 1800 },
  { name: '21" Monarch', price: 2600 },
  { name: '22" Performance', price: 3400 },
  { name: '23" Grand Tour', price: 4600 }
];

const interiorOptions = [
  { name: 'Obsidian leather', price: 2200 },
  { name: 'Ivory leather', price: 2600 },
  { name: 'Saddle brown leather', price: 2900 },
  { name: 'Charcoal interior', price: 2100 }
];

const packageOptions = [
  { name: 'Premium sound system', price: 2600 },
  { name: 'Panoramic glass roof', price: 3200 },
  { name: 'Advanced driver assistance', price: 4800 },
  { name: 'Rear passenger comfort package', price: 4300 },
  { name: 'Extended luxury package', price: 6200 }
];

const chargingOptions = [
  { name: 'Vehicle only', price: 0 },
  { name: 'Home charging installation package', price: 1900 },
  { name: 'Home charging equipment only', price: 900 }
];

let configState = { ...configDefaults };

function readLocalStorage(key, fallback) {
  try {
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : fallback;
  } catch (error) {
    return fallback;
  }
}

function writeLocalStorage(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function getVehicleById(vehicleId) {
  return (window.aurelleVehicles || []).find((vehicle) => vehicle.id === vehicleId) || (window.aurelleVehicles || [])[0];
}

function priceForVehicle(vehicleId) {
  const vehicle = getVehicleById(vehicleId);
  return vehicle ? vehicle.price : 0;
}

function getSelectedOption(options, propertyName) {
  return options.find((option) => option.name === configState[propertyName]) || options[0];
}

function getOptionPrice(name, category) {
  const options = category === 'color' ? [] : category === 'wheel' ? wheelOptions : category === 'interior' ? interiorOptions : category === 'package' ? packageOptions : chargingOptions;
  const match = options.find((option) => option.name === name);
  return match ? match.price : 0;
}

function computeTotal() {
  const vehicle = getVehicleById(configState.selectedVehicle);
  const wheel = getSelectedOption(wheelOptions, 'wheel');
  const interior = getSelectedOption(interiorOptions, 'interior');
  const charging = getSelectedOption(chargingOptions, 'charging');
  const selectedPackages = configState.packages || [];
  const packageTotal = packageOptions
    .filter((option) => selectedPackages.includes(option.name))
    .reduce((sum, option) => sum + option.price, 0);

  return (vehicle ? vehicle.price : 0) + wheel.price + interior.price + charging.price + packageTotal;
}

function renderStep(sectionType, title, options, dataKey, isMultiSelect = false) {
  const isSelectOne = !isMultiSelect;
  const html = `
    <section class="step-section">
      <div class="step-heading">
        <h3>${title}</h3>
        <span class="category-label">${sectionType}</span>
      </div>
      <div class="option-grid">
        ${options.map((option) => {
          const selected = isMultiSelect
            ? (configState[dataKey] || []).includes(option.name)
            : configState[dataKey] === option.name;

          const label = option.name;
          const extra = option.price ? `From ${currency(option.price)}` : '';
          const swatch = option.hex ? `<span class="color-swatch" style="background:${option.hex};"></span>` : '';

          return `
            <button
              type="button"
              class="option-card ${selected ? 'selected' : ''}"
              data-config-key="${dataKey}"
              data-config-value="${option.name}"
              data-multi="${isMultiSelect ? 'true' : 'false'}"
              aria-pressed="${selected}"
            >
              <div style="display:flex; align-items:center; justify-content:space-between;">
                <strong>${label}</strong>
                ${swatch}
              </div>
              <span class="option-meta">${extra || 'Included'}</span>
            </button>
          `;
        }).join('')}
      </div>
    </section>
  `;

  return html;
}

function renderConfiguratorSteps() {
  const container = document.getElementById('configurator-steps');
  if (!container) return;

  const vehicleOptions = (window.aurelleVehicles || []).map((vehicle) => ({
    name: vehicle.name,
    price: vehicle.price,
    image: vehicle.image,
    id: vehicle.id
  }));

  const vehicleStep = `
    <section class="step-section">
      <div class="step-heading">
        <h3>Step 1: Choose your vehicle</h3>
        <span class="category-label">Vehicle</span>
      </div>
      <div class="option-grid">
        ${vehicleOptions.map((vehicle) => `
          <button
            type="button"
            class="option-card ${configState.selectedVehicle === vehicle.id ? 'selected' : ''}"
            data-config-key="selectedVehicle"
            data-config-value="${vehicle.id}"
            data-multi="false"
            aria-pressed="${configState.selectedVehicle === vehicle.id}"
          >
            <div style="display:flex; justify-content:space-between; gap:0.5rem; align-items:center;">
              <strong>${vehicle.name}</strong>
              <span class="category-label">${currency(vehicle.price)}</span>
            </div>
            <span class="option-meta">${vehicle.name}</span>
          </button>
        `).join('')}
      </div>
    </section>
  `;

  const steps = [
    vehicleStep,
    renderStep('Colour', 'Step 2: Choose exterior colour', colorOptions, 'color'),
    renderStep('Wheels', 'Step 3: Choose wheels', wheelOptions, 'wheel'),
    renderStep('Interior', 'Step 4: Choose interior', interiorOptions, 'interior'),
    renderStep('Packages', 'Step 5: Choose optional packages', packageOptions, 'packages', true),
    renderStep('Charging', 'Step 6: Choose charging option', chargingOptions, 'charging')
  ];

  container.innerHTML = steps.join('');

  container.querySelectorAll('[data-config-key]').forEach((button) => {
    button.addEventListener('click', () => {
      const type = button.dataset.configKey;
      const value = button.dataset.configValue;
      const isMulti = button.dataset.multi === 'true';

      if (isMulti) {
        const current = configState[type] || [];
        const next = current.includes(value)
          ? current.filter((item) => item !== value)
          : [...current, value];
        configState[type] = next;
      } else {
        configState[type] = value;
      }

      renderConfiguratorSteps();
      renderConfiguratorSummary();
    });
  });
}

function renderConfiguratorSummary() {
  const container = document.getElementById('configurator-summary');
  if (!container) return;

  const selectedVehicle = getVehicleById(configState.selectedVehicle);
  const wheel = getSelectedOption(wheelOptions, 'wheel');
  const interior = getSelectedOption(interiorOptions, 'interior');
  const charging = getSelectedOption(chargingOptions, 'charging');
  const packages = packageOptions.filter((option) => (configState.packages || []).includes(option.name));

  container.innerHTML = `
    <div class="summary-total">${currency(computeTotal())}</div>
    <ul class="summary-list">
      <li><span>Vehicle</span><span>${selectedVehicle ? selectedVehicle.name : 'Select a vehicle'}</span></li>
      <li><span>Exterior colour</span><span>${configState.color}</span></li>
      <li><span>Wheels</span><span>${wheel.name}</span></li>
      <li><span>Interior</span><span>${interior.name}</span></li>
      <li><span>Charging</span><span>${charging.name}</span></li>
    </ul>
    <div>
      <p class="eyebrow subdued">Optional packages</p>
      <ul class="summary-list">
        ${packages.length ? packages.map((option) => `<li><span>${option.name}</span><span>${currency(option.price)}</span></li>`).join('') : '<li><span>None selected</span><span>$0</span></li>'}
      </ul>
    </div>
  `;
}

function saveConfiguration() {
  const selectedVehicle = getVehicleById(configState.selectedVehicle);
  const saved = readLocalStorage('aurelleSavedConfigs', []);
  const payload = {
    id: Date.now(),
    vehicleId: configState.selectedVehicle,
    vehicleName: selectedVehicle ? selectedVehicle.name : 'Aurelle',
    total: computeTotal(),
    summary: { ...configState }
  };

  saved.unshift(payload);
  writeLocalStorage('aurelleSavedConfigs', saved.slice(0, 5));
  updateAccountSummary();
}

function setupConfiguratorControls() {
  const saveButton = document.getElementById('save-config');
  const consultButton = document.getElementById('consult-config');
  const editButton = document.getElementById('edit-config');

  saveButton?.addEventListener('click', () => {
    saveConfiguration();
    const status = document.createElement('p');
    status.textContent = 'Configuration saved successfully.';
    status.className = 'form-status success';
    saveButton.insertAdjacentElement('afterend', status);
    setTimeout(() => status.remove(), 1600);
  });

  consultButton?.addEventListener('click', () => {
    const enquiry = {
      inquiry: 'Configurator assistance',
      email: JSON.parse(localStorage.getItem('aurelleAccount') || '{}').email || 'client@aurelle.com',
      message: `Configuration request for ${getVehicleById(configState.selectedVehicle)?.name || 'Aurelle'} at ${currency(computeTotal())}.`
    };

    const saved = readLocalStorage('aurelleEnquiries', []);
    saved.unshift(enquiry);
    writeLocalStorage('aurelleEnquiries', saved.slice(0, 5));
    updateAccountSummary();

    const status = document.createElement('p');
    status.textContent = 'Consultation request recorded.';
    status.className = 'form-status success';
    consultButton.insertAdjacentElement('afterend', status);
    setTimeout(() => status.remove(), 1800);
  });

  editButton?.addEventListener('click', () => {
    document.getElementById('configurator')?.scrollIntoView({ behavior: 'smooth' });
  });

  document.addEventListener('click', (event) => {
    const button = event.target.closest('[data-config-vehicle]');
    if (!button) return;
    const targetId = button.getAttribute('data-config-vehicle');
    if (targetId) {
      configState.selectedVehicle = targetId;
      renderConfiguratorSteps();
      renderConfiguratorSummary();
    }
  });
}

function configureVehicle(vehicleId) {
  configState.selectedVehicle = vehicleId;
  renderConfiguratorSteps();
  renderConfiguratorSummary();
}

function initializeConfigurator() {
  renderConfiguratorSteps();
  renderConfiguratorSummary();
  setupConfiguratorControls();
}

window.configureVehicle = configureVehicle;
document.addEventListener('DOMContentLoaded', initializeConfigurator);
