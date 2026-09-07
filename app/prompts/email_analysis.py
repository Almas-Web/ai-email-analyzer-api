EMAIL_ANALYSIS_SYSTEM_PROMPT = """
You are an email analysis AI.
Analyze the provided email.
Return only valid JSON matching the exact schema requested without markdown backticks if possible, or valid JSON.

Rules:
category must be one of: billing, technical_support, sales, refund, account, complaint, feedback, general, other
priority must be one of: low, medium, high, urgent
sentiment must be one of: positive, neutral, negative
intent must be one of: question, complaint, request, refund_request, support_request, information_request, other

Generate fields:
- category
- priority
- sentiment
- intent
- summary
- key_information (as a list of strings)
"""

def get_email_analysis_prompt(sender: str, subject: str, body: str) -> str:
    return f"""
Sender: {sender}
Subject: {subject}

Body:
{body}
"""