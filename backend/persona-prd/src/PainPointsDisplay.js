import React, { useState } from "react";

function PainPointsDisplay({ painPoints, onPainPointSelect }) {
  const [selectedPainPointId, setSelectedPainPointId] = useState(null);

  const handleSelect = (painPoint) => {
    setSelectedPainPointId(painPoint.id);
    onPainPointSelect(painPoint); // Pass the entire pain point object to the parent
  };

  return (
    <div
      style={{
        border: "1px solid #ccc",
        padding: "20px",
        borderRadius: "8px",
        marginTop: "20px",
        backgroundColor: "#fff",
      }}
    >
      <h2 style={{ color: "#333", marginTop: "0" }}>Identified Pain Points</h2>
      {painPoints.length === 0 ? (
        <p style={{ color: "#777" }}>
          No pain points to display yet. Please select a persona and subreddit
          above.
        </p>
      ) : (
        <div>
          {painPoints.map((painPoint) => (
            <div
              key={painPoint.id}
              onClick={() => handleSelect(painPoint)}
              style={{
                border: `1px solid ${
                  selectedPainPointId === painPoint.id ? "#007bff" : "#eee"
                }`,
                padding: "15px",
                marginBottom: "15px",
                borderRadius: "8px",
                cursor: "pointer",
                backgroundColor:
                  selectedPainPointId === painPoint.id ? "#e6f7ff" : "white",
                boxShadow:
                  selectedPainPointId === painPoint.id
                    ? "0 0 8px rgba(0, 123, 255, 0.2)"
                    : "none",
                transition: "all 0.2s ease-in-out",
              }}
            >
              <h3
                style={{
                  color: "#007bff",
                  marginTop: "0",
                  marginBottom: "8px",
                }}
              >
                {painPoint.summary}
              </h3>
              <p
                style={{
                  fontSize: "0.9em",
                  color: "#555",
                  marginBottom: "10px",
                }}
              >
                <strong>Posts contributing:</strong> {painPoint.postCount}
              </p>
              <p
                style={{
                  fontWeight: "bold",
                  color: "#444",
                  marginBottom: "5px",
                }}
              >
                Example Comments:
              </p>
              <ul
                style={{
                  listStyleType: "disc",
                  paddingLeft: "20px",
                  margin: "0",
                }}
              >
                {painPoint.exampleComments.map((comment, index) => (
                  <li
                    key={index}
                    style={{
                      fontSize: "0.85em",
                      color: "#666",
                      marginBottom: "5px",
                    }}
                  >
                    "{comment}"
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default PainPointsDisplay;
