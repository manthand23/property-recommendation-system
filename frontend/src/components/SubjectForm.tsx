import React from "react";
import { SubjectProperty } from "../types";

interface Props {
  subject: SubjectProperty;
  setSubject: (value: SubjectProperty) => void;
}

const SubjectForm: React.FC<Props> = ({ subject, setSubject }) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setSubject({
      ...subject,
      [name]:
        name.includes("num_") ||
        name.includes("year") ||
        name === "gla" ||
        name === "lot_size_sf" ||
        name === "latitude" ||
        name === "longitude"
          ? parseFloat(value)
          : value,
    });
  };

  return (
    <form className="form-grid">
      <input
        type="text"
        name="address"
        placeholder="Address"
        onChange={handleChange}
        required
        title="Must match an address from the dataset"
      />
      <input
        type="number"
        name="gla"
        placeholder="GLA"
        onChange={handleChange}
        min={0}
        required
      />
      <input
        type="number"
        name="lot_size_sf"
        placeholder="Lot Size (sq ft)"
        onChange={handleChange}
        min={0}
      />
      <input
        type="number"
        name="num_beds"
        placeholder="Bedrooms"
        onChange={handleChange}
        min={0}
      />
      <input
        type="number"
        name="num_baths"
        placeholder="Bathrooms"
        onChange={handleChange}
        min={0}
      />
      <input
        type="number"
        name="year_built"
        placeholder="Year Built"
        onChange={handleChange}
        min={1800}
        max={new Date().getFullYear()}
      />
      <input
        type="date"
        name="effective_date"
        onChange={handleChange}
        required
      />
      <input
        type="number"
        name="latitude"
        placeholder="Latitude"
        onChange={handleChange}
        step="any"
      />
      <input
        type="number"
        name="longitude"
        placeholder="Longitude"
        onChange={handleChange}
        step="any"
      />
      <input
        type="text"
        name="structure_type"
        placeholder="Structure Type"
        onChange={handleChange}
      />
      <input
        type="text"
        name="style"
        placeholder="Style"
        onChange={handleChange}
      />
      <input
        type="text"
        name="condition"
        placeholder="Condition"
        onChange={handleChange}
      />
      <input
        type="text"
        name="basement"
        placeholder="Basement Description"
        onChange={handleChange}
      />
    </form>
  );
};

export default SubjectForm;
