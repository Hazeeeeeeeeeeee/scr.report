import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './home_styles.module.css';

function Home() {
  const navigate = useNavigate();
  const SUPPORTED_GAMES = ["Destiny 2", "Destiny 2 Story", "Destiny 2 Lost Sectors"];
  const GAMES_IDS = 
    {
      "Destiny 2": '4d7y5zd7',
      "Destiny 2 Story": 'yd4or2x1',
      "Destiny 2 Lost Sectors": 'nd2853vd'
    }
  
  const [isRunsCardFlipped, setRunsCardFlipped] = useState(false);
  const [isAssetsCardFlipped, setAssetsCardFlipped] = useState(false);

  const redirectToAllRuns = (gameName) => {
    navigate(`/${GAMES_IDS[gameName]}/all_runs`);
  };

  const handleRunsCardClick = () => {
    setRunsCardFlipped(!isRunsCardFlipped);
    if (isAssetsCardFlipped) {
      setAssetsCardFlipped(false);
    }
  };

  const handleAssetsCardClick = () => {
    setAssetsCardFlipped(!isAssetsCardFlipped);
    if (isRunsCardFlipped) {
      setRunsCardFlipped(false);
    }
  };

  return (
    <div>
        <div className={styles.container}>
            {/* Destiny 2 Runs Card */}
            <div className={styles.card} onClick={handleRunsCardClick}>
                <div className={`${styles.cardInner} ${isRunsCardFlipped ? styles.flipped : ''}`}>
                    <div className={styles.cardFront}>
                        <h2>Destiny 2 Runs</h2>
                    </div>
                    <div className={styles.cardBack}>
                        {SUPPORTED_GAMES.map((game, index) => (
                            <div key={index} className={styles.gameContainer} onClick={(e) => { e.stopPropagation(); redirectToAllRuns(game); }}>
                                <img 
                                    src={`/asset/Home/${game}.png`} 
                                    onError={(e) => { e.target.onerror = null; e.target.src="/asset/Home/default.webp"; }} 
                                    alt={game} 
                                    className={styles.gameImage}
                                />
                                <span className={styles.gameName}>{game}</span>
                            </div>
                        ))}
                    </div>

                </div>
            </div>

            {/* Destiny 2 Assets Card */}
            <div className={styles.card} onClick={handleAssetsCardClick}>
                <div className={`${styles.cardInner} ${isAssetsCardFlipped ? styles.flipped : ''}`}>
                    <div className={styles.cardFront}>
                        <h2>How to start speedrun</h2>
                    </div>
                    <div className={styles.cardBack}>
                        {/* Placeholder content for the back of the Assets card */}
                        <p>resources</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
  );
}

export default Home;
