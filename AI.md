#  AI Documentation – AgroMind Project

##  Overview
The **AI Service** in AgroMind enhances the system’s ability to provide intelligent, context-aware crop management advice.  
It uses **OpenRouter’s AI API** with the `mistralai/mixtral-8x7b-instruct` model to analyze crop queries and generate actionable insights.

The AI module handles:
- Crop health assessment  
- Input (fertilizer/nutrient) recommendations  
- Irrigation scheduling advice  
- Pest and disease diagnosis  
- General crop-related Q&A  

---

##  Module Path
app/services/ai_service.py

This module integrates external AI responses into the backend API routes.  
It is invoked by the backend endpoints (such as `/ai/analyze`, `/ai/ask`, `/crops`, or `/recommendations`).

---

## Core Functionality

### `route_crop_query(query: str, crop: str, kiswahili: bool = False) -> dict`

**Description:**  
Routes the user’s text query to an appropriate AI prompt template, sends it to the AI API, and parses the structured JSON response.

**Parameters:**

| Parameter | Type | Required | Description |
|------------|------|-----------|-------------|
| `query` | `str` | ✅ | User’s crop-related question or request |
| `crop` | `str` | ✅ | Name of the crop (e.g., "maize") |
| `kiswahili` | `bool` | ❌ | If `True`, response is generated in Kiswahili |

**Returns:**  
A `dict` containing structured AI output such as health score, recommendations, or advice.

---

##  Query Classification
User input is classified into one of five categories:

| Category | Keywords | Purpose |
|-----------|-----------|----------|
| `health_analysis` | "health", "condition" | Assess crop health and give a score |
| `input_recommendation` | "fertilizer", "nutrient", "input" | Recommend inputs or nutrients |
| `irrigation_advice` | "water", "irrigation" | Suggest watering schedule |
| `pest_diagnosis` | "pest", "disease", "spots", "holes" | Diagnose common crop issues |
| `general_crop_question` | any other query | Provide general farming advice |

---

## Prompt Templates
Each query type generates a structured prompt for the AI model.  

Example for health analysis:
```json
{
  "health_score": 91,
  "advice": "Your maize appears healthy. Maintain watering frequency and monitor leaves for spots."
}
```
Other templates may include:

Input recommendations: list of inputs and notes

Irrigation advice: schedule and short explanation

Pest diagnosis: issue and treatment recommendation

## Multilingual Support

If kiswahili=True, an instruction “Respond in Kiswahili.” is appended to the prompt, enabling localized responses.

Example:
```json
{
  "health_score": 84,
  "advice": "Mimea yako ya mahindi ipo vizuri. Hakikisha kumwagilia mara mbili kwa wiki."
}
```
## Example API Flow
```text
Frontend → Backend /ai/analyze → route_crop_query() → OpenRouter API
```

Request Example
```json
{
  "crop": "maize",
  "query": "Check crop health"
}
```

Response Example
```json
{
  "health_score": 92,
  "advice": "Your maize is healthy. Continue regular irrigation."
}
```
## AI Model Information
| Field            | Description                                     |
| ---------------- | ----------------------------------------------- |
| Provider         | OpenRouter                                      |
| Model            | `mistralai/mixtral-8x7b-instruct`               |
| API Endpoint     | `https://openrouter.ai/api/v1/chat/completions` |
| Temperature      | `0.4` (for consistent factual responses)        |
| Input Type       | JSON prompt with user message                   |
| Output Type      | JSON-formatted advice or structured data        |
| Integration File | `app/services/ai_service.py`                    |
## Environment Variables

The AI service requires the following variable in your .env file:
```ini
OPENROUTER_API_KEY=<your_api_key_here>
```
## Error Handling

If an error occurs (e.g., network issues or invalid response), the service returns:
```json
{
  "response": "AI service unavailable: <error_message>"
}
```

Additionally, all prompts and responses are logged for debugging:
```json
logger.info(f"Prompt sent to OpenRouter: {prompt}")
logger.info(f"Raw response: {content}")
```
## System Flow Summary

```text
User Query
   │
   ▼
classify_crop_query()
   │
   ▼
generate prompt from PROMPT_TEMPLATES
   │
   ▼
send request to OpenRouter API
   │
   ▼
parse response with extract_json()
   │
   ▼
return structured output to backend routes
```

## Example Outputs by Query Type
| Query Type                | Example JSON Response                                                                                |
| ------------------------- | ---------------------------------------------------------------------------------------------------- |
| **health_analysis**       | `json<br>{"health_score": 87, "advice": "Maintain nitrogen levels for better growth."}`              |
| **input_recommendation**  | `json<br>{"recommendations": ["DAP fertilizer", "urea"], "notes": "Best applied before flowering."}` |
| **irrigation_advice**     | `json<br>{"schedule": "3 times per week", "notes": "Ensure soil moisture remains moderate."}`        |
| **pest_diagnosis**        | `json<br>{"possible_issue": "stem borer", "treatment": "Apply neem oil or biological control."}`     |
| **general_crop_question** | `json<br>{"response": "Rotate maize with legumes to improve soil nitrogen."}`                        |
