import React, { useState } from "react";

function UserSelectionPanel({ onSelectionChange }) {
  const [selectedPersona, setSelectedPersona] = useState("");
  const [selectedSubreddit, setSelectedSubreddit] = useState("");

  const personas = [
    "Vibe Coders",
    "Self-Hosting Enthusiasts",
    "Data Professionals",
  ];

  // This would ideally be dynamically loaded or mapped based on persona
  const subreddits = {
    "Vibe Coders": [
      "r/coding",
      "r/learnprogramming",
      "r/webdev",
      "r/programming",
    ],
    "Self-Hosting Enthusiasts": [
      "r/selfhosted",
      "r/homelab",
      "r/privacy",
      "r/Docker",
    ],
    "Data Professionals": [
      "r/datascience",
      "r/businessintelligence",
      "r/dataengineering",
      "r/MachineLearning",
    ],
  };

  const handlePersonaChange = (event) => {
    const persona = event.target.value;
    setSelectedPersona(persona);
    setSelectedSubreddit(""); // Reset subreddit when persona changes
    onSelectionChange({ persona, subreddit: "" }); // Notify parent immediately
  };

  const handleSubredditChange = (event) => {
    const subreddit = event.target.value;
    setSelectedSubreddit(subreddit);
    onSelectionChange({ persona: selectedPersona, subreddit }); // Notify parent
  };

  return (
    <div
      style={{
        border: "1px solid #ccc",
        padding: "20px",
        borderRadius: "8px",
        backgroundColor: "#fff",
      }}
    >
      <h2 style={{ color: "#333", marginTop: "0" }}>User Focus Panel</h2>
      <div style={{ marginBottom: "15px" }}>
        <label
          htmlFor="persona-select"
          style={{
            display: "block",
            marginBottom: "5px",
            fontWeight: "bold",
            color: "#555",
          }}
        >
          Select Persona:
        </label>
        <select
          id="persona-select"
          value={selectedPersona}
          onChange={handlePersonaChange}
          style={{
            width: "100%",
            padding: "10px",
            borderRadius: "4px",
            border: "1px solid #ddd",
            fontSize: "1em",
          }}
        >
          <option value="">--Please choose a persona--</option>
          {personas.map((persona) => (
            <option key={persona} value={persona}>
              {persona}
            </option>
          ))}
        </select>
      </div>
      {selectedPersona && (
        <div style={{ marginTop: "15px" }}>
          <label
            htmlFor="subreddit-select"
            style={{
              display: "block",
              marginBottom: "5px",
              fontWeight: "bold",
              color: "#555",
            }}
          >
            Select Subreddit:
          </label>
          <select
            id="subreddit-select"
            value={selectedSubreddit}
            onChange={handleSubredditChange}
            disabled={!selectedPersona}
            style={{
              width: "100%",
              padding: "10px",
              borderRadius: "4px",
              border: "1px solid #ddd",
              fontSize: "1em",
            }}
          >
            <option value="">--Please choose a subreddit--</option>
            {subreddits[selectedPersona] &&
              subreddits[selectedPersona].map((subreddit) => (
                <option key={subreddit} value={subreddit}>
                  {subreddit}
                </option>
              ))}
          </select>
        </div>
      )}
      {selectedPersona && selectedSubreddit && (
        <p
          style={{
            marginTop: "20px",
            fontStyle: "italic",
            color: "#777",
            backgroundColor: "#e9f7ef",
            padding: "10px",
            borderRadius: "5px",
          }}
        >
          Selected **{selectedPersona}** and **{selectedSubreddit}**. Data would
          be loaded from backend.
        </p>
      )}
    </div>
  );
}

export default UserSelectionPanel;
