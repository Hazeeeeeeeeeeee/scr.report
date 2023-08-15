import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles.css';

function Home() {
  const navigate = useNavigate();
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [gamesData, setGamesData] = useState([]);
  
  const SUPPORTED_GAMES = ["Destiny 2", "Destiny 2 Story", "Destiny 2 Lost Sectors", "Destiny 2 Content Vault"];

  const redirectToLeaderboard = (gameName, type, name) => {
    navigate(`/${gameName}/all_leaderboard/${name}`);
  };



  useEffect(() => {
    const savedMode = localStorage.getItem('dark-mode');
    setIsDarkMode(savedMode === 'true');
    
    // Create an array of fetch promises
    const fetchPromises = SUPPORTED_GAMES.map(game => {
        return fetch(`http://localhost:5000/v2/${game}/all`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            });
    });

    // Use Promise.all to wait for all fetch requests to complete
    Promise.all(fetchPromises)
        .then(dataArray => {
            setGamesData(dataArray);
        })
        .catch(error => {
            console.log('Fetch error: ', error);
        });
}, []);


  function toggleDarkMode() {
    const body = document.body;
    body.classList.toggle('dark-mode');

    // Save user preference in localStorage
    const isDarkMode = body.classList.contains('dark-mode');
    localStorage.setItem('dark-mode', isDarkMode);

    setIsDarkMode(isDarkMode);
  }

  return (
    <div>
        <button onClick={toggleDarkMode}>
            {isDarkMode ? 'Light Mode' : 'Dark Mode'}
        </button>
        
        <div className="container">
          {gamesData.map((game, index) => (
              <div key={index} className="card">  {/* Add the card class here */}
                  <h2>{SUPPORTED_GAMES[index]}</h2>
                  <h3>Levels:</h3>
                  {game.Levels.map(level => (
                      <p key={level["Level ID"]} onClick={() => redirectToLeaderboard(SUPPORTED_GAMES[index], 'level', level["Level Name"])}>{level["Level Name"]}</p>
                  ))}
                  <h3>Categories:</h3>
                  {game.Categories.map(category => (
                      <p key={category["Category ID"]} onClick={() => redirectToLeaderboard(SUPPORTED_GAMES[index], 'category', category["Category Name"])}>{category["Category Name"]}</p>
                  ))}
              </div>
          ))}
      </div>
    </div>
  );

}

export default Home;
