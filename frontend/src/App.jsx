import { Routes, Route } from 'react-router-dom'
import Dashboard from './components/Dashboard'
import TrainDetails from './components/TrainDetails'
import './App.css'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route
        path="/train/:trainNumber"
        element={<TrainDetails />}
      />
    </Routes>
  )
}

export default App