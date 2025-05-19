import React, { useState } from "react";
import { SubjectProperty, CompResult } from "./types";
import SubjectForm from "./components/SubjectForm.tsx";
import Results from "./components/Results.tsx";
import axios from "axios";

const App: React.FC = () => {
  const [subject, setSubject] = useState<SubjectProperty>({
    gla: 0,
    lot_size_sf: 0,
    num_beds: 0,
    num_baths: 0,
    year_built: 0,
    effective_date: "",
    latitude: 0,
    longitude: 0,
    structure_type: "",
    style: "",
    condition: "",
    basement: "",
    address: "",
  });

  const [results, setResults] = useState<CompResult[]>([]);
  const [loading, setLoading] = useState(false);

  const handleRecommend = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/recommend-from-dataset", {
        address: subject.address,
      });
      setResults(response.data);
    } catch (err: any) {
      console.error("Recommendation failed", err);
      const detail = err?.response?.data?.detail || "Could not fetch recommendations. Try using an address from the dataset.";
      alert(detail);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "900px", margin: "auto", fontFamily: "Arial, sans-serif" }}>
      <h1>🏡 Property Comp Recommender</h1>
      <p>Enter a subject property (must match address from dataset) and we’ll find 3 comparable sales.</p>
      <SubjectForm subject={subject} setSubject={setSubject} />
      <button onClick={handleRecommend} disabled={loading} style={{ marginTop: "1rem", padding: "0.5rem 1rem" }}>
        {loading ? "Evaluating..." : "Get Top 3 Comps"}
      </button>
      <Results subject={subject} results={results} />
    </div>
  );
};

export default App;
