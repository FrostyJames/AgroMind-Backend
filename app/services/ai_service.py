import json
import re
import os
import logging
from typing import Optional
import openai
from ..config.settings import settings

logger = logging.getLogger(__name__)
openai.api_key = settings.OPENAI_API_KEY

def extract_json(text: str) -> Optional[dict]:
    """Extracts the first JSON object from a string."""
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            logger.warning("Failed to parse extracted JSON block.")
    return None

def load_crop_profile(crop: str) -> dict:
    """Loads a crop profile from app/data/crops/{crop}.json"""
    path = f"app/data/crops/{crop.lower()}.json"
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Error loading crop profile for {crop}: {e}")
    return {}

def classify_crop_query(query: str) -> str:
    """Classifies the query into a known crop-related category."""
    query = query.lower()
    if "health" in query or "condition" in query:
        return "health_analysis"
    elif "fertilizer" in query or "input" in query or "nutrient" in query:
        return "input_recommendation"
    elif "water" in query or "irrigation" in query:
        return "irrigation_advice"
    elif "pest" in query or "disease" in query or "holes" in query or "spots" in query:
        return "pest_diagnosis"
    else:
        return "general_crop_question"

PROMPT_TEMPLATES = {
    "health_analysis": lambda crop: f"""
        You are an agricultural expert. Assess the health of {crop} and give a score (0–100) with advice.
        Respond in JSON:
        {{
            "health_score": <number>,
            "advice": "<short recommendation>"
        }}
    """,
    "input_recommendation": lambda crop: f"""
        Recommend ideal inputs (fertilizer, nutrients) for growing {crop}.
        Respond in JSON:
        {{
            "recommendations": ["input1", "input2"],
            "notes": "<brief explanation>"
        }}
    """,
    "irrigation_advice": lambda crop: f"""
        Provide irrigation advice for {crop} based on typical growth needs.
        Respond in JSON:
        {{
            "schedule": "<watering frequency>",
            "notes": "<brief explanation>"
        }}
    """,
    "pest_diagnosis": lambda crop: f"""
        Diagnose common pests or diseases affecting {crop} and give advice.
        Respond in JSON:
        {{
            "possible_issue": "<diagnosis>",
            "treatment": "<brief recommendation>"
        }}
    """,
    "general_crop_question": lambda crop: f"""
        Answer the user's crop-related question about {crop}.
        Respond in JSON:
        {{
            "response": "<brief answer>"
        }}
    """
}

def route_crop_query(query: str, crop: str, kiswahili: bool = False) -> dict:
    """Routes the query to the correct prompt template and calls the AI model."""
    query_type = classify_crop_query(query)
    prompt = PROMPT_TEMPLATES[query_type](crop)

    # Inject crop profile
    profile = load_crop_profile(crop)
    if profile:
        prompt += f"\nCrop profile:\n{json.dumps(profile)}"

    # Optional Kiswahili toggle
    if kiswahili:
        prompt += "\nRespond in Kiswahili."

    logger.info(f"Prompt sent to OpenAI:\n{prompt}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a precision agriculture AI assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
        )

        content = response.choices[0].message["content"].strip()
        logger.info(f"Raw response:\n{content}")
        data = extract_json(content)

        return data or {"response": "AI returned invalid format."}

    except Exception as e:
        logger.error(f"AI Service Error: {e}")
        return {"response": "AI service unavailable. Please try again later."}