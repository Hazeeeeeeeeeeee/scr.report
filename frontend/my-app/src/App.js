import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Home from './home/Home';
import Leaderboard from './leaderboard/Leaderboard';
import LeaderboardsAll from './all_leaderboard/all_leaderboard';
import Game from './game/game';  
import Header from './header/header';

function App() {
    return (
        <Router>
            <Header />
            <Routes>
                <Route path="/" element={<Navigate to="/home" replace />} />
                <Route path="/home" element={<Home />} />
                <Route path="/:gameName/all_leaderboard/:groupName" element={<LeaderboardsAll />} />
                <Route path="/:gameName/leaderboard/:groupName/ref/:refName" element={<Leaderboard />} />
                <Route path="/:gameName/all_runs" element={<Game />} />

                {/* Add other routes as needed */}
            </Routes>
        </Router>
    );
}

export default App;
