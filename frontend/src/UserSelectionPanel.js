import React, { useState, useEffect } from "react";

function UserSelectionPanel({ onSelectionChange }) {
  const [personas, setPersonas] = useState([]);
  const [selectedPersona, setSelectedPersona] = useState("");
  const [selectedSubreddit, setSelectedSubreddit] = useState("");
  const [subreddits, setSubreddits] = useState([]);

  // Load personas on first render
  useEffect(() => {
    fetch("http://localhost:8000/personas")
      .then((res) => res.json())
      .then((data) => setPersonas(data))
      .catch((err) => console.error("Failed to fetch personas:", err));
  }, []);

  const handlePersonaChange = (event) => {
    const persona = event.target.value;
    setSelectedPersona(persona);
    setSelectedSubreddit("");
    onSelectionChange({ persona, subreddit: "" });

    // Fetch subreddits for selected persona
    fetch(`http://localhost:8000/subreddits/${persona}`)
      .then((res) => res.json())
      .then((data) => setSubreddits(data))
      .catch((err) => console.error("Failed to fetch subreddits:", err));
  };

  const handleSubredditChange = (event) => {
    const subreddit = event.target.value;
    setSelectedSubreddit(subreddit);
    onSelectionChange({ persona: selectedPersona, subreddit });
  };

  return (
    <div style={{ border: "1px solid #ccc", padding: "20px", borderRadius: "8px", backgroundColor: "#fff" }}>
      <h2>Select User Persona</h2>

      <label>Select Persona:</label>
      <select value={selectedPersona} onChange={handlePersonaChange}>
        <option value="">--Choose a Persona--</option>
        {personas.map((persona) => (
          <option key={persona} value={persona}>
            {persona}
          </option>
        ))}
      </select>

      {selectedPersona && (
        <>
          <label style={{ marginTop: "10px" }}>Select Subreddit:</label>
          <select value={selectedSubreddit} onChange={handleSubredditChange}>
            <option value="">--Choose a Subreddit--</option>
            {subreddits.map((sub) => (
              <option key={sub} value={sub}>
                {sub}
              </option>
            ))}
          </select>
        </>
      )}
    </div>
  );
}

export default UserSelectionPanel;
