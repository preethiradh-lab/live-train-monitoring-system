import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup
} from 'react-leaflet'

import 'leaflet/dist/leaflet.css'

function getMarkerColor(delay) {
  if (delay === 0) {
    return 'green'
  }

  if (delay <= 5) {
    return 'orange'
  }

  return 'red'
}

function LiveMap({ trains }) {
  return (
   <div className="map-container">
    <MapContainer
      center={[11.0168, 76.9558]}
      zoom={12}
      style={{ height: '50vh', width: '100%' }}
    >
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {trains.map(train => (
        <CircleMarker
          key={train.train_number}
          center={[
            train.latitude,
            train.longitude
          ]}
          radius={10}
           pathOptions={{
          color: getMarkerColor(train.delay_minutes),
          fillColor: getMarkerColor(train.delay_minutes),
          fillOpacity: 0.8,
          }}
        >
          <Popup>
            <strong>
              {train.train_number} - {train.train_name}
            </strong>

            <br />

            Status: {train.status}

            <br />

            Speed: {train.speed} km/h

            <br />

            Delay: {train.delay_minutes} minutes
            <br />

Current: {train.current_station}

<br />

Next: {train.next_station}
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
    <div className="map-legend">
      <h4>Map Status</h4>

      <p>🟢 On Time</p>
      <p>🟠 Delayed (1–5 min)</p>
      <p>🔴 Highly Delayed (&gt;5 min)</p>
    </div>
   </div>
    
  )
}

export default LiveMap