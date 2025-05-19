from pydantic import BaseModel
from typing import Optional, List

class Property(BaseModel):
    id: Optional[str]
    address: Optional[str]
    gla: Optional[float]
    lot_size_sf: Optional[float]
    num_beds: Optional[int]
    num_baths: Optional[str]
    year_built: Optional[int]
    structure_type: Optional[str]
    style: Optional[str]
    condition: Optional[str]
    basement: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    effective_date: Optional[str]
    sale_date: Optional[str]

class SubjectProperty(Property):
    pass

class RecommendationRequest(BaseModel):
    subject: SubjectProperty
    candidates: List[Property]

class CompExplanation(BaseModel):
    id: str
    address: str
    score: float
    explanation: dict

class FeedbackEntry(BaseModel):
    subject: SubjectProperty
    comp_id: str
    feedback_score: float
