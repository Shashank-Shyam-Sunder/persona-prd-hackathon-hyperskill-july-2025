import React, { useState, useEffect } from "react";
import UserSelectionPanel from "./UserSelectionPanel";
import PainPointsDisplay from "./PainPointsDisplay";
import PRDGeneratorPanel from "./PRDGeneratorPanel";
import GeneratedPRDOutput from "./GeneratedPRDOutput";

function App() {
  const [selectedPersonaAndSubreddit, setSelectedPersonaAndSubreddit] =
    useState({ persona: "", subreddit: "" });
  const [painPoints, setPainPoints] = useState([]);
  const [selectedPainPoint, setSelectedPainPoint] = useState(null);
  const [generatedPRD, setGeneratedPRD] = useState(null);

  // --- Dummy Data Simulation ---
  // In a real app, this would be fetched from your backend
  useEffect(() => {
    // Correctly reference properties from selectedPersonaAndSubreddit
    if (
      selectedPersonaAndSubreddit.persona &&
      selectedPersonaAndSubreddit.subreddit
    ) {
      // Simulate data fetching delay
      console.log(
        `Simulating data load for persona: ${selectedPersonaAndSubreddit.persona}, subreddit: ${selectedPersonaAndSubreddit.subreddit}`
      );
      setTimeout(() => {
        // Dummy data for different personas/subreddits
        let dummyPainPoints = [];
        if (selectedPersonaAndSubreddit.persona === "Vibe Coders") {
          dummyPainPoints = [
            {
              id: "pp1_vc",
              summary: "IDE performance issues with large codebases",
              postCount: 55,
              persona: selectedPersonaAndSubreddit.persona,
              exampleComments: [
                "My VS Code lags terribly on big projects, drives me nuts.",
                "IntelliJ consumes too much RAM when indexing, makes my fan scream.",
                "Debugging often freezes my entire editor, very frustrating.",
              ],
            },
            {
              id: "pp2_vc",
              summary: "Difficulty integrating new AI coding assistants",
              postCount: 40,
              persona: selectedPersonaAndSubreddit.persona,
              exampleComments: [
                "Copilot suggestions are often irrelevant to my specific context.",
                "Struggling to make Tabnine work with my custom frameworks.",
                "AI code generation is great but integration steps are complex.",
              ],
            },
            {
              id: "pp2_vc", // Corrected ID to be unique
              summary: "Difficulty integrating new AI coding assistants",
              postCount: 40,
              persona: selectedPersonaAndSubreddit.persona,
              exampleComments: [
                "Copilot suggestions are often irrelevant to my specific context.",
                "Struggling to make Tabnine work with my custom frameworks.",
                "AI code generation is great but integration steps are complex.",
              ],
            },
            {
              id: "pp3_vc",
              summary: "Lack of consistent styling/linting configurations",
              postCount: 30,
              persona: selectedPersonaAndSubreddit.persona,
              exampleComments: [
                "ESLint rules are a nightmare to configure for new projects.",
                "Prettier keeps reformatting things I don't want, hard to customize.",
                "Wish there was a simple way to enforce consistent code style across teams.",
              ],
            },
          ];
        } else if (
          selectedPersonaAndSubreddit.persona === "Self-Hosting Enthusiasts"
        ) {
          dummyPainPoints = [
            {
              id: "pp1_sh",
              summary: "Complex setup for reverse proxies and SSL certificates",
              postCount: 70,
              persona: selectedPersonaAndSubreddit.persona,
              exampleComments: [
                "Setting up Nginx Proxy Manager with Let's Encrypt is always a headache.",
                "Struggling with wildcard certificates for my subdomains.",
                "Docker-compose for Caddy is confusing for a beginner.",
              ],
            },
            {
              id: "pp2_sh",
              summary: "Keeping self-hosted services updated and secure",
              postCount: 60,
              persona: selectedPersonaAndSubreddit.persona,
              exampleComments: [
                "Fear breaking everything every time I update my Nextcloud instance.",
                "CVEs for self-hosted apps pop up too often, hard to keep track.",
                "Automated update solutions often fail or cause conflicts.",
              ],
            },
            {
              id: "pp3_sh",
              summary: "Resource management and optimization on home servers",
              postCount: 45,
              persona: selectedPersonaAndSubreddit.persona,
              exampleComments: [
                "My Plex server is constantly buffering, need better hardware utilization.",
                "Docker containers are eating up all my RAM, how to optimize?",
                "Struggling to balance CPU usage between VMs and containers.",
              ],
            },
          ];
        } else if (
          selectedPersonaAndSubreddit.persona === "Data Professionals"
        ) {
          dummyPainPoints = [
            {
              id: "pp1_dp",
              summary: "Data cleaning and preprocessing is too time-consuming",
              postCount: 80,
              persona: selectedPersonaAndSubreddit.persona,
              exampleComments: [
                "Spending 80% of my time cleaning dirty data, it's exhausting.",
                "Merging disparate datasets with inconsistent formats is a nightmare.",
                "Wish there were more automated tools for handling missing values.",
              ],
            },
            {
              id: "pp2_dp",
              summary: "Difficulties with deploying ML models to production",
              postCount: 65,
              persona: selectedPersonaAndSubreddit.persona,
              exampleComments: [
                "Translating Jupyter notebooks to production-ready code is hard.",
                "Containerizing models for deployment introduces too much complexity.",
                "Monitoring model performance in real-time is a significant challenge.",
              ],
            },
            {
              id: "pp3_dp",
              summary:
                "Lack of standardized practices for data governance and quality",
              postCount: 50,
              persona: selectedPersonaAndSubreddit.persona, // Changed selectedSubreddit.persona to selectedPersonaAndSubreddit.persona
              exampleComments: [
                "Our data definitions are inconsistent across different teams.",
                "No clear ownership for data quality issues, leading to errors.",
                "Struggling to implement robust data validation rules.",
              ],
            },
          ];
        }
        setPainPoints(dummyPainPoints);
        setSelectedPainPoint(null); // Reset selection when new data loads
        setGeneratedPRD(null); // Clear previous PRD
      }, 700); // Small delay to simulate network latency
    } else {
      setPainPoints([]);
      setSelectedPainPoint(null);
      setGeneratedPRD(null);
    }
  }, [selectedPersonaAndSubreddit]); // Keep the dependency array as selectedPersonaAndSubreddit

  // ... rest of the App.js component remains the same ...

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
    <div
      style={{
        fontFamily: "Arial, sans-serif",
        maxWidth: "1200px",
        margin: "20px auto",
        padding: "0 20px",
        backgroundColor: "#f0f2f5",
        minHeight: "100vh",
        borderRadius: "8px",
      }}
    >
      <h1
        style={{
          textAlign: "center",
          color: "#333",
          paddingTop: "20px",
          marginBottom: "10px",
        }}
      >
        PersonaPRD: AI-Powered Product Drafts
      </h1>
      <p
        style={{
          textAlign: "center",
          fontSize: "1em",
          color: "#666",
          marginBottom: "30px",
        }}
      >
        Streamline product development by transforming raw community feedback
        into structured PRD drafts.
      </p>

      <hr
        style={{
          margin: "30px 0",
          border: "none",
          borderTop: "1px solid #ddd",
        }}
      />

      <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: "25px" }}>
        <UserSelectionPanel onSelectionChange={handleSelectionChange} />

        {selectedPersonaAndSubreddit.persona &&
          selectedPersonaAndSubreddit.subreddit && (
            <>
              <PainPointsDisplay
                painPoints={painPoints}
                onPainPointSelect={handlePainPointSelect}
              />
              <PRDGeneratorPanel
                selectedPainPoint={selectedPainPoint}
                onGeneratePRD={handleGeneratePRD}
              />
            </>
          )}
        {generatedPRD && <GeneratedPRDOutput prdData={generatedPRD} />}
      </div>
      <div
        style={{
          textAlign: "center",
          padding: "30px 0",
          color: "#999",
          fontSize: "0.8em",
        }}
      >
        <p>&copy; 2025 Clouded Sky. All rights reserved.</p>
      </div>
    </div>
  );
}

export default App;
