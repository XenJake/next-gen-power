(() => {
  const mapElement = document.getElementById('charging-map');
  const fallback = document.getElementById('map-fallback');
  const dataElement = document.getElementById('station-map-data');
  if (!mapElement || !dataElement) return;

  try {
    if (!window.L) throw new Error('Map library is unavailable');
    const stations = JSON.parse(dataElement.textContent);
    const map = L.map(mapElement, { scrollWheelZoom: false }).setView([7.9465, -1.0232], 6);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    const bounds = [];
    stations.forEach((station) => {
      const position = [station.latitude, station.longitude];
      bounds.push(position);
      const color = station.available > 0 ? '#15846f' : station.statuses.includes('Occupied') ? '#b77b1c' : '#687a82';
      const marker = L.circleMarker(position, {
        radius: 9,
        color: '#ffffff',
        weight: 3,
        fillColor: color,
        fillOpacity: 1
      }).addTo(map);

      const popup = document.createElement('div');
      const title = document.createElement('strong');
      title.textContent = station.name;
      const type = document.createElement('p');
      type.textContent = station.site_type;
      const address = document.createElement('p');
      address.textContent = station.address;
      const state = document.createElement('p');
      state.textContent = `${station.available} available of ${station.charger_count} chargers`;
      const equipment = document.createElement('p');
      equipment.textContent = Array.from(new Set(station.equipment)).join(', ');
      const link = document.createElement('a');
      link.href = station.url;
      link.textContent = 'Station details';
      popup.append(title, type, address, state, equipment, link);
      if (station.is_demo) {
        const demo = document.createElement('small');
        demo.textContent = 'Demonstration location';
        popup.append(demo);
      }
      marker.bindPopup(popup);
    });

    if (bounds.length > 1) map.fitBounds(bounds, { padding: [36, 36], maxZoom: 9 });
    if (fallback) fallback.hidden = true;
    window.setTimeout(() => map.invalidateSize(), 100);
  } catch (error) {
    mapElement.classList.add('map-unavailable');
    if (fallback) {
      fallback.textContent = 'The map is temporarily unavailable. Use the station list below to view details and directions.';
      fallback.hidden = false;
    }
  }
})();
