import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import './styles.css';

const Leaderboard = () => {
    const [leaderboardData, setLeaderboardData] = useState([]);
    const [loading, setLoading] = useState(true);

    const params = useParams();
    const { category, name } = params;

    useEffect(() => {

        fetch(`http://localhost:5000/${category}/${name}`)
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
    }, [category, name]);
    
    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1> {name} Leaderboard</h1>
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Players</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody>
                    {leaderboardData.map((run, index) => (
                        <tr key={index}>
                            <td>{run.rank}</td>
                            <td>{run.players.join(', ')}</td>
                            <td>{run.time}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Leaderboard;
