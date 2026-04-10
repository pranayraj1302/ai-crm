from groq import Groq
from django.conf import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def generate_followup_email(contact, interactions):
    interaction_text = "\n".join(
        [f"{i.interaction_type}: {i.notes}" for i in interactions]
    )

    prompt = f"""
You are a professional sales assistant.

Write a short follow-up email.

Contact Name: {contact.name}
Company: {contact.company}

Previous Interactions:
{interaction_text}

Keep it friendly and professional.

Return format:
Subject: <subject line>
Body: <email body>
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content