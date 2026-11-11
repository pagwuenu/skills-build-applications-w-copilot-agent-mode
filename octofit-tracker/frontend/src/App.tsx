import { Link, Navigate, NavLink, Route, Routes } from 'react-router-dom';
import Activities from './components/Activities.js';
import Teams from './components/Teams.js';
import Leaderboard from './components/Leaderboard.js';
import Workouts from './components/Workouts.js';
import Users from './components/Users.js';

export default function App() {
  return (
    <div className="container app-shell py-4">
      <header className="app-header mb-4">
        <Link className="app-brand d-inline-block mb-3" to="/">
          <h1 className="display-6 fw-bold mb-1">OctoFit Tracker</h1>
          <span className="app-tagline">Move together. Make every minute count.</span>
        </Link>
        <nav aria-label="OctoFit sections" className="nav nav-pills flex-wrap gap-2">
          <NavLink className="nav-link" to="/activities">Activities</NavLink>
          <NavLink className="nav-link" to="/teams">Teams</NavLink>
          <NavLink className="nav-link" to="/leaderboard">Leaderboard</NavLink>
          <NavLink className="nav-link" to="/users">Users</NavLink>
          <NavLink className="nav-link" to="/workouts">Workouts</NavLink>
        </nav>
      </header>
      <main className="page-content">
        <Routes>
          <Route path="/" element={<Navigate to="/activities" replace />} />
          <Route path="/activities" element={<Activities />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/users" element={<Users />} />
          <Route path="/workouts" element={<Workouts />} />
        </Routes>
      </main>
    </div>
  );
}
