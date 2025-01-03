import React, { useState } from 'react';

function UploadForm({ updatePlayerStats, fetchFiles }) {
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
        </div>
    );
}

export default UploadForm;
