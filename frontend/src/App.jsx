import { useEffect, useState } from 'react'
import './App.css'
import TrainCard from './components/TrainCard'
import LiveMap from './components/LiveMap'

function App() {
  const [trains, setTrains] = useState([])

  useEffect(() => {
    console.log("useEffect is running")
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
      <h1>Live Train Monitoring System</h1>
      <div className="dashboard-stats">
       
  <div className="stat-card">
    
    <h3>Active Trains</h3>
    <p>{activeTrainCount}</p>
  </div>

  <div className="stat-card">
    <h3>Running</h3>
    <p>{runningTrainCount}</p>
  </div>

  <div className="stat-card">
    <h3>Delayed</h3>
    <p>{delayedTrainCount}</p>
  </div>
</div>  

 <h2>Live Map</h2>
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
    </div>
  )
}

export default App