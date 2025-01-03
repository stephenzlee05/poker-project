import React, { useState, useEffect } from 'react';
import UploadForm from './components/UploadForm';

function App() {

    const [uploadedFiles, setUploadedFiles] = useState([]);
    const [selectedFile, setSelectedFile] = useState('');
    const [playerStats, setPlayerStats] = useState([]);

    useEffect(() => {
        fetch('http://localhost:5000/files')
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((text) => {
                setUploadedFiles(text);
            })
            .catch((error) => {
                console.error('Error fetching files:', error);
            });
    }, []);

    const handleFileSelect = (event) => {
        const fileName = event.target.value;
        setSelectedFile(fileName);

        // Fetch stats for the selected file
        fetch(`http://localhost:5000/stats?file=${fileName}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();  // Parse the response into JSON
            })
            .then((data) => {
                setPlayerStats(data);  // Set player stats from the server response
            })
            .catch((error) => {
                console.error('Error fetching stats:', error);
            });
    };


    // Function to fetch the list of uploaded files from the backend
    const fetchFiles = () => {
        fetch('http://localhost:5000/files')
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((data) => {
                setUploadedFiles(data);  // Update the uploaded files list
            })
            .catch((error) => {
                console.error('Error fetching files:', error);
            });
    };

    useEffect(() => {
        // Initially fetch the list of files
        fetchFiles();
    }, []);

    // Callback function to update player stats after file upload
    const updatePlayerStats = (stats) => {
        setPlayerStats(stats);
    };


    return (
        <div>
            <h1>Poker Tracker</h1>
            {/* Pass the updatePlayerStats and fetchFiles functions as props */}
            <UploadForm updatePlayerStats={updatePlayerStats} fetchFiles={fetchFiles} />

            <div>
                <label htmlFor="file-selector">Select File: </label>
                <select
                    id="file-selector"
                    value={selectedFile}
                    onChange={handleFileSelect}
                >
                    <option value="" disabled>
                        -- Select a file --
                    </option>
                    {uploadedFiles.map((file, index) => (
                        <option key={index} value={file}>
                            {file}
                        </option>
                    ))}
                </select>
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', marginTop: '20px' }}>
                {Object.entries(playerStats).map(([playerId, stats]) => (
                    <div
                        key={playerId}
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
            </div>

        </div>
    );
}

export default App;
