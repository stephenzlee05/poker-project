// Inside UploadForm.jsx
import React, { useState } from 'react';
import axios from 'axios';

const UploadForm = () => {
  const [file, setFile] = useState(null);
  const [hands, setHands] = useState([]);
  
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log("Response from backend:", response.data);
      setHands(response.data.hands); // Save the parsed hands to state
      alert("Upload successful! Check console for details.");
    } catch (err) {
      console.error("Error uploading file:", err);
      alert("Error uploading file. Check console for details.");
    }
  };

  return (
    <div>
      <h2>Upload Poker Log</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>

      {hands.length > 0 && (
        <div>
          <h3>Hands Details</h3>
          <table>
            <thead>
              <tr>
                <th>Hand ID</th>
                <th>Players</th>
                <th>Actions</th>
                <th>Winner</th>
                <th>Pot</th>
              </tr>
            </thead>
            <tbody>
              {hands.map((hand, index) => (
                <tr key={index}>
                  <td>{hand.hand_id}</td>
                  <td>
                    {hand.players.map((player) => (
                      <div key={player.name}>
                        {player.name} (Chips: {player.chips})
                      </div>
                    ))}
                  </td>
                  <td>
                    {hand.actions.map((action, idx) => (
                      <div key={idx}>
                        {action.player}: {action.action} {action.amount ? `Amount: ${action.amount}` : ""}
                      </div>
                    ))}
                  </td>
                  <td>{hand.winner}</td>
                  <td>{hand.pot}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default UploadForm;
