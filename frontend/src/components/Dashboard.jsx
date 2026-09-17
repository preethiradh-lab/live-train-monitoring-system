import { useEffect, useState } from 'react'
import TrainCard from './TrainCard'
import LiveMap from './LiveMap'
import { Link } from 'react-router-dom'

function Dashboard() {
  const [trains, setTrains] = useState([])

  useEffect(() => {
    const fetchTrains = () => {
      console.log("Fetching train data...")

      fetch('http://127.0.0.1:8000/api/trains/live/')
        .then(response => response.json())
        .then(data => {
          setTrains(data)
        })
    }

    fetchTrains()

    const interval = setInterval(fetchTrains, 10000)

    return () => {
      clearInterval(interval)
    }
  }, [])

  const activeTrainCount = trains.length

  const runningTrainCount = trains.filter(
    train => train.status === 'RUNNING'
  ).length

  const delayedTrainCount = trains.filter(
    train => train.status === 'DELAYED'
  ).length

  return (
    <div>
     <header className="top-header">
  <div className="header-title">
    🚆 Live Train Monitoring System
  </div>

  <div className="header-status">
    ● SYSTEM ONLINE
  </div>
</header>
<div className="dashboard-layout">

  <aside className="sidebar">
    <h3>Navigation</h3>

    <nav>
      <Link to="/" className="sidebar-item">
  ▣ Dashboard
</Link>
      <div className="sidebar-item">🚆 Live Trains</div>
      <div className="sidebar-item">🚉 Stations</div>
      <div className="sidebar-item">⚠ Alerts</div>
      <div className="sidebar-item">📊 Reports</div>
    </nav>
  </aside>

  <main className="dashboard-content">
    <div className="dashboard-stats">
        <div className="stat-card active">
          <h3>Active Trains</h3>
          <p>{activeTrainCount}</p>
        </div>

        <div className="stat-card running">
          <h3>Running</h3>
          <p>{runningTrainCount}</p>
        </div>

        <div className="stat-card delayed">
          <h3>Delayed</h3>
          <p>{delayedTrainCount}</p>
        </div>
      </div>
       <div className="map-header">
  <h2>Live Train Map</h2>
  <span>● LIVE</span>
</div>

      {trains.length > 0 && (
        <LiveMap trains={trains} />
      )}

      <h2>Active Trains</h2>

      <div className="train-grid">
        {trains.map(train => (
          <TrainCard
            key={train.train_number}
            train={train}
          />
        ))}
      </div>
    </main></div>
      

      
    </div>
  )
}

export default Dashboard