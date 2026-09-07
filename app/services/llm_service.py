from google import genai
from fastapi import HTTPException, status
from app.core.config import settings
from app.prompts.email_analysis import EMAIL_ANALYSIS_SYSTEM_PROMPT, get_email_analysis_prompt
from app.schemas.analysis import EmailAnalysis

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def analyze_email_content(sender: str, subject: str, body: str) -> EmailAnalysis:
    user_prompt = get_email_analysis_prompt(sender, subject, body)
    full_prompt = f"{EMAIL_ANALYSIS_SYSTEM_PROMPT}\n\n{user_prompt}"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
        )
        
        # Pydantic validation of LLM JSON response
        analysis_result = EmailAnalysis.model_validate_json(response.text)
        return analysis_result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service temporarily unavailable or invalid response: {str(e)}"
        )