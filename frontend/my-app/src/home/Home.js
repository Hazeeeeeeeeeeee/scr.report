import React from 'react';
import { useNavigate } from 'react-router-dom';
import './styles.css';

function Home() {
  const navigate = useNavigate();

  const redirectToLeaderboard = (raid) => {
    navigate(`/leaderboard?raid=${raid}`);
  };

  return (
    <div>
      <h1>Home</h1>
      <div className="button" onClick={() => redirectToLeaderboard('Leviathan')}>
        Click to redirect to Leviathan
      </div>
      <div className="button" onClick={() => redirectToLeaderboard('Eater_of_Worlds')}>
        Click to redirect to Eater of Worlds
      </div>
      <div className="button" onClick={() => redirectToLeaderboard('Spire_of_Stars')}>
        Click to redirect to Spire of Stars
      </div>
      <div className="button" onClick={() => redirectToLeaderboard('Last_Wish')}>
        Click to redirect to Last Wish
      </div>
      <div className="button" onClick={() => redirectToLeaderboard('Scourge_of_the_Past')}>
        Click to redirect to Scourge of the Past
      </div>
      <div className="button" onClick={() => redirectToLeaderboard('Crown_of_Sorrow')}>
        Click to redirect to Crown of Sorrow
      </div>
      <div className="button" onClick={() => redirectToLeaderboard('Garden_of_Salvation')}>
        Click to redirect to Garden of Salvation
      </div>
      <div className="button" onClick={() => redirectToLeaderboard('Deep_Stone_Crypt')}>
        Click to redirect to Deep Stone Crypt
      </div>
      <div className="button" onClick={() => redirectToLeaderboard('Vault_of_Glass')}>
        Click to redirect to Vault of Glass
      </div>
      <div className="button" onClick={() => redirectToLeaderboard('Vow_of_the_Disciple')}>
        Click to redirect to Vow of the Disciple
      </div>
      <div className="button" onClick={() => redirectToLeaderboard('Kings_Fall')}>
        Click to redirect to King's Fall
      </div>
      <div className="button" onClick={() => redirectToLeaderboard('Root_of_Nightmares')}>
        Click to redirect to Root of Nightmares
      </div>
    </div>
  );
}


export default Home;
