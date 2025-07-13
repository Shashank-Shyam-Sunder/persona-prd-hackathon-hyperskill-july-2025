import React from "react";

function PRDGeneratorPanel({ selectedPainPoint, onGeneratePRD }) {
  const handleGenerate = () => {
    if (selectedPainPoint) {
      // Simulate PRD generation using the selectedPainPoint data
      const simulatedPRD = {
        title: `PRD Draft for: "${selectedPainPoint.summary}"`,
        problemSummary: `Users are experiencing significant issues related to "${selectedPainPoint.summary.toLowerCase()}", as evidenced by feedback from approximately ${
          selectedPainPoint.postCount
        } discussions. This indicates a widespread bottleneck.`,
        whyItMatters: `For **${selectedPainPoint.persona}s**, this problem is critical because it directly impacts their core workflows by leading to increased manual effort, missed insights, or frustrating technical hurdles. Addressing this will significantly improve their efficiency and satisfaction with our tools/platform.`,
        potentialSolutions: [
          "Develop a dedicated feature or module to automate or simplify the process causing the pain.",
          "Enhance existing functionalities with capabilities to mitigate the specific pain point.",
          "Provide comprehensive documentation, tutorials, or tooling to guide users through complex aspects.",
          "Explore integration with third-party services that offer solutions to this problem.",
        ],
        mvpFeatures: [
          "Basic automation/simplification of the most critical part of the pain point.",
          "A clear user interface element to interact with the new functionality.",
          "Logging or telemetry to understand initial user adoption and identify further bottlenecks.",
          "A simple feedback mechanism within the tool for users to report on the effectiveness of the solution.",
        ],
        fallbackPlan:
          "If the primary solution development proves too complex or time-consuming for MVP, a fallback could involve providing a curated list of best practices or a manual workaround guide, coupled with a highly responsive support channel. For Stage 2, consider deeper integrations, advanced analytics, or broader automation.",
      };
      onGeneratePRD(simulatedPRD);
    } else {
      alert("Please select a pain point first from the list above!");
    }
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
      <h2 style={{ color: "#333", marginTop: "0" }}>Generate PRD Draft</h2>
      {selectedPainPoint ? (
        <div>
          <p style={{ color: "#555", marginBottom: "15px" }}>
            You have selected the pain point:
            <strong style={{ color: "#007bff" }}>
              {" "}
              "{selectedPainPoint.summary}"
            </strong>
          </p>
          <button
            onClick={handleGenerate}
            style={{
              padding: "12px 25px",
              backgroundColor: "#28a745" /* Green button for Generate */,
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
              fontSize: "1em",
              fontWeight: "bold",
              boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
            }}
          >
            Generate PRD Draft
          </button>
        </div>
      ) : (
        <p style={{ color: "#777" }}>
          Select a pain point from the list above to generate a PRD draft.
        </p>
      )}
    </div>
  );
}

export default PRDGeneratorPanel;
