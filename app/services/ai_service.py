import json
import re
import os
import logging
import requests
from typing import Optional
from ..config.settings import settings

logger = logging.getLogger(__name__)

def extract_json(text: str) -> Optional[dict]:
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            logger.warning("Failed to parse extracted JSON block.")
    return None

def load_crop_profile(crop: str) -> dict:
    path = f"app/data/crops/{crop.lower()}.json"
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Error loading crop profile for {crop}: {e}")
    return {}

def classify_crop_query(query: str) -> str:
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
    query_type = classify_crop_query(query)
    prompt = PROMPT_TEMPLATES[query_type](crop)

    profile = load_crop_profile(crop)
    if profile:
        prompt += f"\nCrop profile:\n{json.dumps(profile)}"
    else:
        logger.warning(f"No crop profile found for '{crop}'")
        prompt += f"\nNote: No crop profile was found for {crop}. Respond based on general knowledge."

    if kiswahili:
        prompt += "\nRespond in Kiswahili."

    logger.info(f"Prompt sent to OpenRouter:\n{prompt}")

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mixtral-8x7b-instruct",
                "messages": [
                    {"role": "system", "content": "You are a precision agriculture AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.4
            }
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"].strip()
        logger.info(f"Raw response:\n{content}")
        data = extract_json(content)
        return data or {"response": content}

    except Exception as e:
        logger.error(f"AI Service Error: {e}")
        return {"response": f"AI service unavailable: {str(e)}"}