import axios from "axios";
import { SubjectProperty, Property, CompResult } from "../types";

const API_URL = "http://localhost:8000";

export async function getRecommendations(
  subject: SubjectProperty,
  candidates: Property[]
): Promise<CompResult[]> {
  const response = await axios.post(`${API_URL}/recommend`, {
    subject,
    candidates,
  });
  return response.data;
}
