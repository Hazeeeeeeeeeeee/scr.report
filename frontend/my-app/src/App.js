import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Home from './home/Home';
import Leaderboard from './leaderboard/Leaderboard';
import LeaderboardsAll from './all_leaderboard/all_leaderboard';
import All_runs from './all_runs/all_runs';  
import Header from './header/header';
import CategoryLeaderboard from './categoy_leaderboard/categoy_leaderboard'

function App() {
    return (
        <Router>
            <Header />
            <Routes>
                <Route path="/" element={<Navigate to="/home" replace />} />
                <Route path="/home" element={<Home />} />
                <Route path="/:gameName/all_leaderboard/:groupName" element={<LeaderboardsAll />} />
                <Route path="/:group_type/leaderboard/category/:ref_name" element={<CategoryLeaderboard />} />
                <Route path="/:gameName/leaderboard/:groupName/ref/:refName" element={<Leaderboard />} />
                <Route path="/:gameName/all_runs" element={<All_runs />} />

                {/* Add other routes as needed */}
            </Routes>
        </Router>
    );
}

export default App;
