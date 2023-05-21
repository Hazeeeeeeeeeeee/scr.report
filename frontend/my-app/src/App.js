import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Home from './home/Home';
import Leaderboard from './leaderboard/Leaderboard';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Navigate to="/home" replace />} />
                <Route path="/home" element={<Home />} />
                <Route path="/:category/leaderboard/:name" element={<Leaderboard />} />
            </Routes>
        </Router>
    );
}

export default App;
