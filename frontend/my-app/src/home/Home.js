import React from 'react';
import { useNavigate } from 'react-router-dom';
import './styles.css';

function Home() {
  const navigate = useNavigate();

  const redirectToLeaderboard = (category, name) => {
    navigate(`/${category}/leaderboard/${name}`);
  };

  return (
    <div>
        <h1>Home</h1>

        <h2>Leviathan</h2>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Leviathan_Normal')}>
            Leviathan Normal
        </div>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Leviathan_Prestige')}>
            Leviathan Prestige
        </div>

        <h2>Last Wish</h2>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Last_Wish_All_Encounters')}>
            Last Wish All Encounters
        </div>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Last_Wish_Any%')}>
            Last Wish Any%
        </div>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Last_Wish_Trio_All_Encounters')}>
            Last Wish Trio All Encounters
        </div>

        <h2>Scourge of the Past</h2>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Scourge_of_the_Past_No_Major_Glitches')}>
            Scourge of the Past No Major Glitches
        </div>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Scourge_of_the_Past_Any%')}>
            Scourge of the Past Any%
        </div>

        <h2>Crown of Sorrow</h2>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Crown_of_Sorrow')}>
            Crown of Sorrow
        </div>

        <h2>Garden of Salvation</h2>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Garden_of_Salvation_Any%')}>
            Garden of Salvation Any%
        </div>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Garden_of_Salvation_Trio')}>
            Garden of Salvation Trio
        </div>

        <h2>Deep Stone Crypt</h2>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Deep_Stone_Crypt_Any%')}>
            Deep Stone Crypt Any%
        </div>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Deep_Stone_Crypt_Trio')}>
            Deep Stone Crypt Trio
        </div>

        <h2>Vault of Glass</h2>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Vault_of_Glass_Any%')}>
            Vault of Glass Any%
        </div>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Vault_of_Glass_Trio')}>
            Vault of Glass Trio
        </div>

        <h2>Vow of the Disciple</h2>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Vow_of_the_Disciple_Any%')}>
            Vow of the Disciple Any%
        </div>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Vow_of_the_Disciple_Trio')}>
            Vow of the Disciple Trio
        </div>

        <h2>King's Fall</h2>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Kings_Fall')}>
            King's Fall
        </div>

        <h2>Root of Nightmares</h2>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Root_of_Nightmares_Any%')}>
            Root of Nightmares Any%
        </div>
        <div className="button" onClick={() => redirectToLeaderboard('raid', 'Root_of_Nightmares_Trio')}>
            Root of Nightmares Trio
        </div>
    </div>
  );
}

export default Home;
