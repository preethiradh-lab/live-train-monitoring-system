import { useEffect, useState } from 'react'
import { useParams,useNavigate } from 'react-router-dom'

function getDelayStatus(delay) {
  if (delay === 0) {
    return 'on-time'
  }

  if (delay <= 5) {
    return 'delayed'
  }

  return 'highly-delayed'
}
function TrainDetails() {
  const { trainNumber } = useParams()
  const navigate = useNavigate()
  const [train, setTrain] = useState(null)
 useEffect(() => {
  const fetchTrain = () => {
   fetch(`http://127.0.0.1:8000/api/trains/${trainNumber}/live/`)
  .then(response => {
    if (!response.ok) {
      throw new Error('Unable to fetch train details')
    }

    return response.json()
  })
      .then(data => {
        setTrain(data)
      })
  }

  fetchTrain()

  const interval = setInterval(fetchTrain, 10000)

  return () => {
    clearInterval(interval)
  }
}, [trainNumber])

  return (
    <div>
      <h1>Train Details</h1>
      {!train && <p>Loading train information...</p>}
{train && (
  <div className="train-details-card">
    <h2>
      {train.train_number} - {train.train_name}
    </h2>

    <p>
  Status:
  <span className={`status-badge ${train.status.toLowerCase()}`}>
    {train.status}
  </span>
</p>

    <p>
      Speed: {train.live_position.speed} km/h
    </p>

    <p>
  Delay:
  <span
    className={`delay-status ${getDelayStatus(
      train.live_position.delay_minutes
    )}`}
  >
    {train.live_position.delay_minutes} minutes
  </span>
</p>

    <p>
      Current: {train.live_position.current_station}
    </p>

    <p>
      Next: {train.live_position.next_station}
    </p>
    <p>
  Last Updated:{' '}
  {new Date(train.live_position.recorded_at).toLocaleString()}
</p>
  </div>
)}
<button
  className="back-button"
  onClick={() => navigate('/')}
>
  Back to Dashboard
</button>
    </div>
  )
}

export default TrainDetails