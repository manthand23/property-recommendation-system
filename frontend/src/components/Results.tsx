import React, { FC } from "react";
import { CompResult, SubjectProperty } from "../types";
import FeedbackForm from "./FeedbackForm.tsx";

interface Props {
  subject: SubjectProperty;
  results: CompResult[];
}

const Results: FC<Props> = ({ subject, results }) => {
  return (
    <section className="results-section">
      <h2 className="results-header">Top 3 Comparable Properties</h2>

      {results.length === 0 ? (
        <p className="results-placeholder">No results yet. Submit a valid address to see comps.</p>
      ) : (
        <div className="comp-list">
          {results.map((comp) => (
            <div className="comp-card" key={comp.id}>
              <div className="comp-header">
                <strong>{comp.address}</strong>
                <span className="comp-score">Score: {typeof comp.score === "number" ? comp.score.toFixed(2) : "N/A"}</span>
              </div>

              {comp.explanation && (
                <ul className="explanation-list">
                  {Object.entries(comp.explanation).map(([key, val]) => (
                    <li key={key}>
                      <em>{key}</em>: {typeof val === "number" ? val.toFixed(3) : "N/A"}
                    </li>
                  ))}
                </ul>
              )}

              <FeedbackForm subject={subject} comp={comp} />
            </div>
          ))}
        </div>
      )}
    </section>
  );
};

export default Results;
