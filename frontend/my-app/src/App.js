import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Home from './home/Home';
import Leaderboard from './leaderboard/Leaderboard';
import LeaderboardsAll from './all_leaderboard/all_leaderboard';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Navigate to="/home" replace />} />
                <Route path="/home" element={<Home />} />
                <Route path="/:gameName/all_leaderboard/:groupName" element={<LeaderboardsAll />} />
                <Route path="/:gameName/Leaderboard/:groupName/ref/:refName" element={<Leaderboard />} />

                {/* Add other routes as needed */}
            </Routes>
        </Router>
    );
}

export default App;
