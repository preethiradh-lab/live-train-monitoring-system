function TrainCard({ train }) {
  return (
    <div className="train-card">
      <h3>
        {train.train_number} - {train.train_name}
      </h3>

      <p>
  Status:
  <span className={`status-badge ${train.status.toLowerCase()}`}>
    {train.status}
  </span>
</p>

      <p>Speed: {train.speed} km/h</p>

      <p>Delay: {train.delay_minutes} minutes</p>

      <p>
        {train.current_station} → {train.next_station}
      </p>
    </div>
  )
}

export default TrainCard