// import the css
import 'leaflet/dist/leaflet.css';
// Optional if you want to fix icons
import L from 'leaflet';
import iconUrl from 'leaflet/dist/images/marker-icon.png';
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png';
import shadowUrl from 'leaflet/dist/images/marker-shadow.png';
import mapImage from "../../images/locations/jkuatentrance.jpeg";


window.L = L;
window.L.Icon.Default.mergeOptions({
    iconUrl,
    iconRetinaUrl,
    shadowUrl,
});

// Get current time and day
const now = new Date();
const day = now.getDay(); // Sunday = 0, Monday = 1, ..., Saturday = 6
const hour = now.getHours(); // 0 - 23

// Check if current time is Monday to Saturday and 8AM - 5PM
const isOfficeOpen = (day >= 1 && day <= 6) && (hour >= 8 && hour < 17);
const officeStatus = isOfficeOpen
    ? '<a role="button" style="color: green;">Office Open</a>'
    : '<a role="button" style="color: red;">Office Closed</a>';
const jkuatCoords = [-1.0905, 37.011];

const map = L.map('map').setView(jkuatCoords, 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

L.marker(jkuatCoords)
    .addTo(map)
    .bindPopup(`
          <div style="text-align:center; max-width: 250px;">
            <h3 style="margin: 0;">Pkenya JKUAT</h3>
            <p style="margin: 4px 0;">Jomo Kenyatta University of Agriculture and Technology</p>
            <img src="${mapImage}" 
                alt="JKUAT Gate" 
                style="width:100%; border-radius: 8px; margin: 6px 0;" />
            <p style="margin: 0;">Located in Juja, along Thika Superhighway.</p>
            ${officeStatus}
          </div>
        `)
    .openPopup();
