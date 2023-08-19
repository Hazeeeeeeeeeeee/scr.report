import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import styles from './header_styles.module.css';


function Header() {
    const navigate = useNavigate();
    const location = useLocation();

    const SUPPORTED_GAMES = ["Destiny 2", "Destiny 2 Story", "Destiny 2 Lost Sectors"];
    const GAMES_IDS = 
    {
      "Destiny 2": '4d7y5zd7',
      "Destiny 2 Story": 'yd4or2x1',
      "Destiny 2 Lost Sectors": 'nd2853vd'
    }

    const handleLeftClick = () => {
        navigate('/home');
    };

    const handleGameClick = (game) => {
        navigate(`/${GAMES_IDS[game]}/all_runs`);
    };

    return (
        <div className={styles.header}>
            <div className={styles.left} onClick={handleLeftClick}>
                <span className={styles.title}>Report</span> 
                <img src="/asset/Destiny 2/icon_header.png" alt="Logo" className={styles.logo} /> 
                <span className={styles.title}>Speedrun</span>
            </div>

            {location.pathname !== '/home' && (
                <div className={styles.center}>
                    {SUPPORTED_GAMES.map((game, index) => (
                    <React.Fragment key={index}>
                        <span onClick={() => handleGameClick(game)}>
                            {game}
                        </span>
                        {index !== SUPPORTED_GAMES.length - 1 && <span className={styles.dot}>&middot;</span>}
                    </React.Fragment>
                ))}

                </div>
            )}

            <div className={styles.right}>
                <input type="text" placeholder="Search..." className={styles.searchBar} />
            </div>
        </div>
    );
}



export default Header;
