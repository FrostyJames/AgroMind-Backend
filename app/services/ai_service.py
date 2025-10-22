from openai import OpenAI
from ..config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def analyze_crop_health(crop_name: str, growth_stage: str) -> dict:
    """
    Uses OpenAI to provide AI-generated analysis of crop condition and recommendations.
    """
    prompt = f"""
    You are an agricultural expert. Analyze the crop health and give a health score (0–100)
    and brief advice based on this information:

    Crop: {crop_name}
    Growth stage: {growth_stage}

    Respond in JSON format:
    {{
        "health_score": number,
        "advice": "string"
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    content = response.choices[0].message.content
    try:
        import json
        return json.loads(content)
    except Exception:
        return {"health_score": 75.0, "advice": "AI response unavailable."}
