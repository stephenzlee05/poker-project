import React, { useState, useEffect } from 'react';
import UploadForm from './components/UploadForm';

function App() {
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const [selectedFile, setSelectedFile] = useState('');
    const [playerStats, setPlayerStats] = useState({});
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    // Fetch the list of uploaded files from the backend
    const fetchFiles = async () => {
        try {
            const response = await fetch('http://localhost:5000/files');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setUploadedFiles(data);
        } catch (error) {
            console.error('Error fetching files:', error);
            setError('Failed to fetch files. Please try again later.');
        }
    };

    // Fetch player stats for the selected file
    const fetchPlayerStats = async (fileName) => {
        if (!fileName) return;

        setIsLoading(true);
        setError('');

        try {
            const response = await fetch(`http://localhost:5000/stats?file=${fileName}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setPlayerStats(data);
        } catch (error) {
            console.error('Error fetching stats:', error);
            setError('Failed to fetch player stats. Please try again later.');
        } finally {
            setIsLoading(false);
        }
    };

    // Handle file selection
    const handleFileSelect = (event) => {
        const fileName = event.target.value;
        setSelectedFile(fileName);
        fetchPlayerStats(fileName);
    };

    // Fetch files on component mount
    useEffect(() => {
        fetchFiles();
    }, []);

    return (
        <div style={{ padding: '1px', /*fontFamily: 'Arial, sans-serif'*/ }}>
            <h1 style={{ textAlign: 'center', marginBottom: '20px' }}>Poker Tracker</h1>

            {/* Upload Form */}
            <UploadForm
                updatePlayerStats={setPlayerStats}
                fetchFiles={fetchFiles}
            />

            {/* File Selector */}
            <div style={{ marginBottom: '20px' }}>
                <label htmlFor="file-selector">Select File: </label>
                <select
                    id="file-selector"
                    value={selectedFile}
                    onChange={handleFileSelect}
                    disabled={isLoading}
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

            {/* Loading and Error Messages */}
            {isLoading && <p style={{ textAlign: 'center' }}>Loading player stats...</p>}
            {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}

            {/* Player Stats Display */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', marginTop: '20px', }}>
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
                            <li>P&L: {" "}
                                <span style={{color: stats.profit > 0 ? 'limegreen' : stats.profit < 0 ? 'red' : 'black', fontWeight: 'bold',}}>
                                {stats.profit}
                                </span> 
                            </li>
                        </ul>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default App;