import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import './styles.css';

function Leaderboard() {
    const [leaderboardData, setLeaderboardData] = useState({});
    const { gameName, groupName, refName } = useParams();
  console.log("gameName:", gameName);
  console.log("groupName:", groupName);
  console.log("refName:", refName);

  function convertISO8601ToTime(duration) {
    const match = duration.match(/PT(\d+H)?(\d+M)?(\d+S)?/);
    
    const hours = (parseInt(match[1]) || 0);
    const minutes = (parseInt(match[2]) || 0);
    const seconds = (parseInt(match[3]) || 0);
    
    return `${hours ? hours + 'h ' : ''}${minutes ? minutes + 'm ' : ''}${seconds ? seconds + 's' : ''}`.trim();
}


  useEffect(() => {
    const fetchURL = `http://localhost:5000/v2/${encodeURIComponent(gameName)}/leaderboard/${encodeURIComponent(groupName)}/ref/${encodeURIComponent(refName)}`;
    console.log("Fetching URL:", fetchURL);
    fetch(fetchURL)



        
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log("Received data:", data);
        setLeaderboardData(data);
        })
    
      .catch(error => {
        console.error('Error fetching leaderboard data:', error);
      });
  }, [gameName, groupName, refName]);

  return (
    <div className="container">
      <h2>Leaderboard for {refName.replace(/_/g, ' ')}</h2>
      
      {/* Podium */}
      <div className="podium">
        {leaderboardData.runs && leaderboardData.runs.slice(0, 3).map((entry, index) => (
          <div key={index} className={`card ${index === 0 ? 'first-place' : index === 1 ? 'second-place' : 'third-place'}`}>
            <p><strong>Place:</strong> {index + 1}</p>
            <p><strong>Time:</strong> {convertISO8601ToTime(entry.run.times.primary)}</p>
            <p><strong>Player:</strong> <a href={entry.run.players[0].uri} target="_blank" rel="noopener noreferrer">{entry.run.players[0].id}</a></p>
            <p><strong>Video:</strong> <a href={entry.run.videos.links[0].uri} target="_blank" rel="noopener noreferrer">Link</a></p>
          </div>
        ))}
      </div>
      
      {/* Remaining Runs */}
      <div className="list-runs">
        {leaderboardData.runs && leaderboardData.runs.slice(3).map((entry, index) => (
          <div key={index + 3} className="leaderboard-entry">
            <p><strong>Place:</strong> {index + 4}</p>
            <p><strong>Time:</strong> {convertISO8601ToTime(entry.run.times.primary)}</p>
            <p><strong>Player:</strong> <a href={entry.run.players[0].uri} target="_blank" rel="noopener noreferrer">{entry.run.players[0].id}</a></p>
            <p><strong>Video:</strong> <a href={entry.run.videos.links[0].uri} target="_blank" rel="noopener noreferrer">Link</a></p>
          </div>
        ))}
      </div>
    </div>
  );
  
  

}

export default Leaderboard;
