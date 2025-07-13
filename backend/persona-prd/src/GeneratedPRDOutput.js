import React from "react";

function GeneratedPRDOutput({ prdData }) {
  if (!prdData) {
    return (
      <div
        style={{
          border: "1px solid #ccc",
          padding: "20px",
          borderRadius: "8px",
          marginTop: "20px",
          backgroundColor: "#f9f9f9",
        }}
      >
        <h2 style={{ color: "#333", marginTop: "0" }}>Generated PRD Output</h2>
        <p style={{ color: "#777" }}>No PRD draft generated yet.</p>
      </div>
    );
  }

  return (
    <div
      style={{
        border: "1px solid #ccc",
        padding: "25px",
        borderRadius: "8px",
        marginTop: "20px",
        backgroundColor: "#eaf7ff",
        borderLeft: "5px solid #007bff",
      }}
    >
      <h2 style={{ color: "#007bff", marginTop: "0", marginBottom: "15px" }}>
        Generated PRD Output
      </h2>
      <h3 style={{ color: "#333", marginBottom: "10px" }}>{prdData.title}</h3>

      <div style={{ marginBottom: "20px" }}>
        <h4 style={{ color: "#444", marginBottom: "5px" }}>Problem Summary:</h4>
        <p style={{ color: "#555" }}>{prdData.problemSummary}</p>
      </div>

      <div style={{ marginBottom: "20px" }}>
        <h4 style={{ color: "#444", marginBottom: "5px" }}>
          Why this problem matters for the chosen persona:
        </h4>
        <p style={{ color: "#555" }}>{prdData.whyItMatters}</p>
      </div>

      <div style={{ marginBottom: "20px" }}>
        <h4 style={{ color: "#444", marginBottom: "5px" }}>
          Potential Solutions:
        </h4>
        <ul style={{ listStyleType: "disc", paddingLeft: "25px", margin: "0" }}>
          {prdData.potentialSolutions.map((solution, index) => (
            <li key={index} style={{ color: "#555", marginBottom: "5px" }}>
              {solution}
            </li>
          ))}
        </ul>
      </div>

      <div style={{ marginBottom: "20px" }}>
        <h4 style={{ color: "#444", marginBottom: "5px" }}>
          Suggested MVP Features:
        </h4>
        <ul style={{ listStyleType: "disc", paddingLeft: "25px", margin: "0" }}>
          {prdData.mvpFeatures.map((feature, index) => (
            <li key={index} style={{ color: "#555", marginBottom: "5px" }}>
              {feature}
            </li>
          ))}
        </ul>
      </div>

      <div style={{ marginBottom: "0" }}>
        <h4 style={{ color: "#444", marginBottom: "5px" }}>
          Fallback Plan / Stage 2 Considerations:
        </h4>
        <p style={{ color: "#555", fontStyle: "italic" }}>
          {prdData.fallbackPlan}
        </p>
      </div>
    </div>
  );
}

export default GeneratedPRDOutput;
