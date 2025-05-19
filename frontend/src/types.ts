export interface Property {
  id: number;
  address: string;
  gla?: number;
  lot_size_sf?: number;
  bedrooms?: number;
  full_baths?: number;
  half_baths?: number;
  year_built?: number;
  close_date?: string;
  latitude?: number;
  longitude?: number;
  structure_type?: string;
  style?: string;
  condition?: string;
  basement_finish?: string;
}

export interface SubjectProperty {
  gla?: number;
  lot_size_sf?: number;
  num_beds?: number;
  num_baths?: number;
  year_built?: number;
  effective_date: string;
  latitude?: number;
  longitude?: number;
  structure_type?: string;
  style?: string;
  condition?: string;
  basement?: string;
  subject_age?: number;
  effective_age?: number;
  address: string;
}

export interface CompResult {
  id: number;
  address: string;
  score: number;
  explanation?: Record<string, number>;
}
