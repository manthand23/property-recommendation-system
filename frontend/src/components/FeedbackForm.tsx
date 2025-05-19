import React, { useState } from "react";
import axios from "axios";
import { CompResult, SubjectProperty } from "../types";

interface Props {
  subject: SubjectProperty;
  comp: CompResult;
}

const FeedbackForm: React.FC<Props> = ({ subject, comp }) => {
  const [score, setScore] = useState(5);
  const [submitted, setSubmitted] = useState(false);

  const submitFeedback = async () => {
    try {
      await axios.post("http://localhost:8000/feedback", {
        subject,
        comp_id: comp.id,
        feedback_score: score,
      });
      setSubmitted(true);
    } catch (err) {
      alert("Failed to submit feedback.");
      console.error(err);
    }
  };

  return (
    <div style={{ marginTop: "0.5rem" }}>
      <label>
        Rate this comp:{" "}
        <select
          value={score}
          disabled={submitted}
          onChange={(e) => setScore(Number(e.target.value))}
        >
          <option value={1}>1 - Poor</option>
          <option value={2}>2 - Fair</option>
          <option value={3}>3 - Okay</option>
          <option value={4}>4 - Good</option>
          <option value={5}>5 - Great</option>
        </select>
      </label>
      <button
        onClick={submitFeedback}
        disabled={submitted}
        style={{
          marginLeft: "0.5rem",
          backgroundColor: "#28a745",
          color: "white",
          border: "none",
          padding: "0.3rem 0.6rem",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        {submitted ? "Submitted" : "Submit Feedback"}
      </button>
    </div>
  );
};

export default FeedbackForm;
