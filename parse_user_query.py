import spacy
import re
from datetime import datetime

nlp = spacy.load("en_core_web_sm")

def parse_user_query(query: str) -> dict:
    doc = nlp(query)

    # Extract states
    states = [ent.text for ent in doc.ents if ent.label_ == "GPE"]

    # Extract crop type
    crop_type = None
    crop_keywords = ["cereal", "rice", "wheat", "maize", "pulses", "cotton", "sugarcane"]
    for word in crop_keywords:
        if word in query.lower():
            crop_type = word.capitalize()

    # Extract number of years
    match = re.search(r"last (\d+) years", query.lower())
    if match:
        n_years = int(match.group(1))
        current_year = datetime.now().year
        years = list(range(current_year - n_years + 1, current_year + 1))
    else:
        years = []

    # Detect task type
    task = None
    if "compare" in query.lower() and "rainfall" in query.lower():
        task = "compare_rainfall_and_crop_production"
    elif "trend" in query.lower() and "production" in query.lower():
        task = "analyze_crop_trend"
    elif "correlate" in query.lower() or "impact" in query.lower():
        task = "correlate_crop_and_climate"
    elif "policy" in query.lower() or "scheme" in query.lower():
        task = "support_policy_with_data"

    return {
        "task": task,
        "states": states,
        "years": years,
        "crop_type": crop_type,
        "metrics": ["rainfall", "production"]
    }