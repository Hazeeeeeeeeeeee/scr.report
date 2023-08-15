import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './styles.css';

function AllLeaderboard() {
  const [leaderboardData, setLeaderboardData] = useState({});
  const { gameName, groupName } = useParams(); // Capture the dynamic parts of the URL
  const navigate = useNavigate(); // Hook to programmatically navigate

  useEffect(() => {
    fetch(`http://localhost:5000/v2/${gameName}/all_leaderboards/${groupName}`)
      .then(response => response.json())
      .then(data => setLeaderboardData(data))
      .catch(error => console.error('Error fetching leaderboard data:', error));
  }, [gameName, groupName]); // Add gameName and groupName as dependencies

  const handleCardClick = (refName) => {
    navigate(`/${gameName}/Leaderboard/${groupName}/ref/${refName}`);
  };

  return (
    <div className="container">
      {Object.keys(leaderboardData).map((key, index) => (
        <div key={index} className="card" onClick={() => handleCardClick(key)}>
          <h3>{key}</h3>
        </div>
      ))}
    </div>
  );
}

export default AllLeaderboard;
