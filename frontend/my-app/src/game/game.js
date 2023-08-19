import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

import styles from './game_styles.module.css';

function Game() {

    function ComponentName() {
        return <div className={styles.someClass}></div>;
    }

    const { gameName } = useParams();
    const [gameData, setGameData] = useState(null);
    const [flippedCard, setFlippedCard] = useState(null);

    const navigate = useNavigate();
    const redirectToLeaderboard = (gameName, groupName) => {
        navigate(`/${gameName}/all_leaderboard/${groupName}`);
    };

    useEffect(() => {
        const fetchURL = `http://localhost:5000/v2/${encodeURIComponent(gameName)}/all`;
        console.log("Fetching URL:", fetchURL);

        fetch(fetchURL)
            .then(response => response.json())
            .then(data => {
                setGameData(data);
            })
            .catch(error => {
                console.error("Error fetching game data:", error);
            });
    }, [gameName]);

    const [leaderboardData, setLeaderboardData] = useState({});

    const fetchLeaderboardData = (gameId, groupId, CorL) => {
        const fetchURL = `http://localhost:5000/v2/${encodeURIComponent(gameId)}/all_leaderboards/${CorL}/${encodeURIComponent(groupId)}`
        console.log("Fetching from fetchLeaderboardData:", fetchURL);

        fetch(fetchURL)
            .then(response => response.json())
            .then(data => {
                setLeaderboardData(data);
            })
            .catch(error => {
                console.error("Error fetching leaderboard data:", error);
            });
    };

    const handleCardFlip = (gameId, groupId, CorL) => {
        console.log("Card clicked:", gameId, groupId);
        setFlippedCard(groupId);
        fetchLeaderboardData(gameId, groupId, CorL);
    };

    return (
        <div>
            <ComponentName/>
            <h1>{gameName}</h1>
    
            {gameData && (
                <div>
                    <h2>Categories:</h2>
                    <div className={styles.cardContainer}>
                        {gameData.Categories.map(category => (
                            <div key={category["Category ID"]} className={`${styles.card} ${flippedCard === category["Category Name"] ? styles.flipped : ''}`} onClick={() => handleCardFlip(gameName, category["Category ID"], "C")}>
                                <div className={styles.cardFront}>
                                    {category["Category Name"]}
                                </div>
                                <div className={styles.cardBack}>
                                    {/* Display the image for the category */}
                                    <img 
                                        src={`/asset/${encodeURIComponent(gameName)}/${encodeURIComponent(category["Category Name"])}.jpg`} 
                                        alt={category["Category Name"]} 
                                        className={styles.leaderboardImage}
                                        onError={(e) => {
                                            e.target.onerror = null;
                                            e.target.src = '/asset/default.jpg';
                                        }}
                                    />
                                    {Object.entries(leaderboardData).map(([key, value], index, array) => (
                                        <React.Fragment key={key}>
                                            <div>
                                                {category["Category Name"]} {key}
                                            </div>
                                            {index !== array.length - 1 && <hr />} {/* This will add a horizontal line between items */}
                                        </React.Fragment>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>

                    
                    <h2>Levels:</h2>
                    <div className={styles.cardContainer}>
                        {gameData.Levels.map(level => (
                            <div key={level["Level ID"]} className={`${styles.card} ${flippedCard === level["Level Name"] ? styles.flipped : ''}`} onClick={() => handleCardFlip(gameName, level["Level ID"], "L")}>
                                <div className={styles.cardFront}>
                                    {level["Level Name"]}
                                </div>
                                <div className={styles.cardBack}>
                                    {/* Display the image for the level */}
                                    <img 
                                        src={`/asset/${encodeURIComponent(gameName)}/${encodeURIComponent(level["Level Name"])}.jpg`} 
                                        alt={level["Level Name"]} 
                                        className={styles.leaderboardImage}
                                        onError={(e) => {
                                            e.target.onerror = null;
                                            e.target.src = '/asset/default.jpg';
                                        }}
                                    />
                                    {Object.entries(leaderboardData).map(([key, value], index, array) => (
                                        <React.Fragment key={key}>
                                            <div>
                                                {level["Level Name"]} {key}
                                            </div>
                                            {index !== array.length - 1 && <hr />} {/* This will add a horizontal line between items */}
                                        </React.Fragment>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>

                </div>
            )}
        </div>
    );
    
      
}

export default Game;
