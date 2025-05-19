import React, { FC } from "react";
import { Property } from "../types";

interface Props {
  setCandidates: (value: Property[]) => void;
}

const CandidateInput: FC<Props> = ({ setCandidates }) => {
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    try {
      const parsed = JSON.parse(e.target.value);
      if (Array.isArray(parsed)) {
        setCandidates(parsed);
      } else {
        console.error("Input is not a valid array of properties.");
      }
    } catch {
      console.error("Invalid JSON format.");
    }
  };

  return (
    <div>
      <h3>Candidate Properties</h3>
      <textarea
        placeholder="Paste JSON array of candidate properties..."
        rows={10}
        cols={80}
        onChange={handleChange}
      />
    </div>
  );
};

export default CandidateInput;
