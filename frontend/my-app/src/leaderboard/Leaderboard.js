//http://localhost:3000/leaderboard?raid=

import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import './styles.css';

const Leaderboard = () => {
    const [leaderboardData, setLeaderboardData] = useState([]);
    const [loading, setLoading] = useState(true);

    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const raidName = queryParams.get('raid');

    useEffect(() => {
        console.log(raidName);  // Add this line
        fetch(`http://localhost:5000/raid/${raidName}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                setLeaderboardData(data);
                setLoading(false);
            })
            .catch(error => {
                console.log('Fetch error: ', error);
            });
    }, [raidName]);
    
    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        
        <html>
            <div>
                <h1>Leaderboard</h1>
                {leaderboardData.map((run, index) => (
                    <thead>
                        <tr key={index}>
                            <th>Category: {run.category}</th>
                            <th>Rank: {run.rank}</th>
                            <th>Players: {run.players.join(', ')}</th>
                            <th>Time: {run.time}</th>
                        </tr>
                    </thead>
                ))}
            </div>
        </html>
    );
};

export default Leaderboard;
