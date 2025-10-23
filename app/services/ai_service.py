from openai import OpenAI
from ..config import settings
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def analyze_crop_health(crop_name: str, growth_stage: str) -> dict:
    """
    Uses OpenAI to provide AI-generated analysis of crop condition and recommendations.
    Returns a dict: {"health_score": float, "advice": str}
    """
    prompt = f"""
    You are an agricultural expert. Analyze the crop health and give a health score (0–100)
    and brief advice based on this information:

    Crop: {crop_name}
    Growth stage: {growth_stage}

    Respond strictly in JSON format:
    {{
        "health_score": <number>,
        "advice": "<short recommendation>"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precision agriculture AI assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
        )

        content = response.choices[0].message.content.strip()
        return json.loads(content)

    except json.JSONDecodeError:
        return {"health_score": 75.0, "advice": "AI returned invalid format."}

    except Exception as e:
        print(f"AI Service Error: {e}")
        return {"health_score": 50.0, "advice": "AI service unavailable."}
