import React, { useState } from 'react';

function UploadForm({ updatePlayerStats, fetchFiles }) {
    const [playerStats, setPlayerStats] = useState([]);
    const [error, setError] = useState(null);

    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://127.0.0.1:5000/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Server Error: ${response.statusText}`);
            }

            const data = await response.json();
            if (data.error) {
                throw new Error(data.error);
            }

            // setPlayerStats(Object.values(data));
            // Pass the player stats to the parent component (App.js)
            updatePlayerStats(Object.values(data));
            // Call fetchFiles to update the file list after a new file is uploaded
            fetchFiles();
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div>
            <input type="file" accept="application/json" onChange={handleFileUpload} />
            {error && <div style={{ color: 'red' }}>{error}</div>}
            {/* <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', marginTop: '20px' }}>
                {playerStats.map((stats, index) => (
                    <div
                        key={index}
                        style={{
                            border: '1px solid #ccc',
                            borderRadius: '8px',
                            padding: '10px',
                            background: 'white',
                            width: '300px',
                            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                        }}
                    >
                        <h3 style={{ textAlign: 'center' }}>{stats.name}</h3>
                        <ul style={{ listStyle: 'none', padding: '0' }}>
                            <li>Hands Played: {stats.hands_played}</li>
                            <li>VPIP: {stats.vpip_percentage.toFixed(2)}%</li>
                            <li>Limp Percentage: {stats.limp_percentage.toFixed(2)}%</li>
                            <li>PFR Percentage: {stats.pfr_precentage.toFixed(2)}%</li>
                            <li>3bet Percentage: {stats.three_bet_percentage.toFixed(2)}%</li>
                            <li>Aggression Factor: {stats.aggression_factor.toFixed(2)}</li>
                            <li>Pots Won: {stats.pots_won}</li>
                        </ul>
                    </div>
                ))}
            </div> */}
        </div>
    );
}

export default UploadForm;
