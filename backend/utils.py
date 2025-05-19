from pathlib import Path
import json
from datetime import datetime
import re
import numpy as np
from sklearn.metrics.pairwise import haversine_distances
from math import radians

# Regexes for parsing
BATH_REGEX = re.compile(r"(\d+)(?:\s*[:FfHh]\s*(\d+))?")
SQFT_REGEX = re.compile(r"(\d{3,5})")

def parse_bath_count(value):
    """Parses bath formats like '2:1', '2 F 1 H' -> 2.5"""
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        return np.nan
    match = BATH_REGEX.search(value)
    if match:
        full, half = match.groups()
        full = int(full)
        half = int(half) if half else 0
        return full + 0.5 * half
    return np.nan

def parse_sqft(value):
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        return np.nan
    match = SQFT_REGEX.search(value.replace(",", ""))
    if match:
        return float(match.group(1))
    return np.nan

def geo_distance_km(lat1, lon1, lat2, lon2):
    try:
        lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
        return 6371 * haversine_distances([[lat1, lon1], [lat2, lon2]])[0][1]
    except:
        return np.nan

def standardize_string(s):
    return str(s).strip().lower()

def extract_features(subject, candidate):
    gla_diff = parse_sqft(subject.get("gla")) - parse_sqft(candidate.get("gla"))
    lot_diff = parse_sqft(subject.get("lot_size_sf")) - parse_sqft(candidate.get("lot_size_sf"))
    gla_diff_norm = gla_diff / parse_sqft(subject.get("gla")) if parse_sqft(subject.get("gla")) else np.nan
    lot_diff_norm = lot_diff / parse_sqft(subject.get("lot_size_sf")) if parse_sqft(subject.get("lot_size_sf")) else np.nan

    try:
        bedroom_diff = float(subject.get("num_beds") or 0) - float(candidate.get("num_beds") or 0)
    except:
        bedroom_diff = np.nan

    try:
        bath_diff = parse_bath_count(subject.get("num_baths")) - parse_bath_count(candidate.get("num_baths"))
    except:
        bath_diff = np.nan

    try:
        age_diff = float(subject.get("year_built") or 0) - float(candidate.get("year_built") or 0)
        age_diff_norm = age_diff / (datetime.now().year - float(subject.get("year_built"))) if subject.get("year_built") else np.nan
    except:
        age_diff_norm = np.nan

    date_sbj = subject.get("effective_date")
    date_cmp = candidate.get("sale_date") or candidate.get("effective_date")
    if date_sbj and date_cmp:
        try:
            d1 = datetime.strptime(date_sbj, "%Y-%m-%d")
            d2 = datetime.strptime(date_cmp, "%Y-%m-%d")
            sale_date_diff_years = abs((d1 - d2).days) / 365
        except:
            sale_date_diff_years = np.nan
    else:
        sale_date_diff_years = np.nan

    lat1, lon1 = subject.get("latitude"), subject.get("longitude")
    lat2, lon2 = candidate.get("latitude"), candidate.get("longitude")
    geo_km = geo_distance_km(lat1, lon1, lat2, lon2) if all([lat1, lon1, lat2, lon2]) else np.nan

    return {
        "gla_diff_norm": np.abs(gla_diff_norm),
        "lot_size_diff_norm": np.abs(lot_diff_norm),
        "bedroom_diff": abs(bedroom_diff) if bedroom_diff is not None else np.nan,
        "bath_diff": abs(bath_diff) if bath_diff is not None else np.nan,
        "age_diff_norm": abs(age_diff_norm) if age_diff_norm is not None else np.nan,
        "sale_date_diff_years": sale_date_diff_years,
        "geo_distance_km": geo_km,
        "same_structure_type": int(standardize_string(subject.get("structure_type")) == standardize_string(candidate.get("structure_type"))),
        "same_style": int(standardize_string(subject.get("style")) == standardize_string(candidate.get("style"))),
        "same_condition": int(standardize_string(subject.get("condition")) == standardize_string(candidate.get("condition"))),
        "same_basement_finish": int(standardize_string(subject.get("basement")) == standardize_string(candidate.get("basement")))
    }
