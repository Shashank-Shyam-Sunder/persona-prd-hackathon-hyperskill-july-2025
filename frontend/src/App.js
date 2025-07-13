import React, { useState, useEffect } from "react";
import UserSelectionPanel from "./UserSelectionPanel";
import PainPointsDisplay from "./PainPointsDisplay";
import PRDGeneratorPanel from "./PRDGeneratorPanel";
import GeneratedPRDOutput from "./GeneratedPRDOutput";

function App() {
  const [selectedPersonaAndSubreddit, setSelectedPersonaAndSubreddit] = useState({ persona: "", subreddit: "" });
  const [painPoints, setPainPoints] = useState([]);
  const [selectedPainPoint, setSelectedPainPoint] = useState(null);
  const [generatedPRD, setGeneratedPRD] = useState(null);

  useEffect(() => {
    const { persona, subreddit } = selectedPersonaAndSubreddit;

    if (persona && subreddit) {
      fetch(`http://localhost:8000/painpoints/${encodeURIComponent(persona)}/${encodeURIComponent(subreddit)}`)
        .then((res) => {
          if (!res.ok) {
            throw new Error(`Failed to fetch pain points: ${res.status}`);
          }
          return res.json();
        })
        .then((data) => {
          setPainPoints(Array.isArray(data) ? data : []);
          setSelectedPainPoint(null);
          setGeneratedPRD(null);
        })
        .catch((err) => {
          console.error("Backend fetch error:", err);
          setPainPoints([]);
        });
    } else {
      setPainPoints([]);
      setSelectedPainPoint(null);
      setGeneratedPRD(null);
    }
  }, [selectedPersonaAndSubreddit]);

  const handleSelectionChange = (selection) => {
    setSelectedPersonaAndSubreddit(selection);
  };

  const handlePainPointSelect = (painPoint) => {
    setSelectedPainPoint(painPoint);
  };

  const handleGeneratePRD = (prdData) => {
    setGeneratedPRD(prdData);
  };

  return (
    <div style={{ fontFamily: "Arial, sans-serif", maxWidth: "1200px", margin: "20px auto", padding: "0 20px", backgroundColor: "#f0f2f5", minHeight: "100vh", borderRadius: "8px" }}>
      <h1 style={{ textAlign: "center", color: "#333", paddingTop: "20px", marginBottom: "10px" }}>
        PersonaPRD: AI-Powered Product Drafts
      </h1>
      <p style={{ textAlign: "center", fontSize: "1em", color: "#666", marginBottom: "30px" }}>
        Streamline product development by transforming raw community feedback into structured PRD drafts.
      </p>
      <hr style={{ margin: "30px 0", border: "none", borderTop: "1px solid #ddd" }} />
      <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: "25px" }}>
        <UserSelectionPanel onSelectionChange={handleSelectionChange} />
        {selectedPersonaAndSubreddit.persona && selectedPersonaAndSubreddit.subreddit && (
          <>
            <PainPointsDisplay painPoints={painPoints} onPainPointSelect={handlePainPointSelect} />
            <PRDGeneratorPanel selectedPainPoint={selectedPainPoint} onGeneratePRD={handleGeneratePRD} />
          </>
        )}
        {generatedPRD && <GeneratedPRDOutput prdData={generatedPRD} />}
      </div>
      <div style={{ textAlign: "center", padding: "30px 0", color: "#999", fontSize: "0.8em" }}>
        <p>&copy; 2025 Clouded Sky. All rights reserved.</p>
      </div>
    </div>
  );
}

export default App;
