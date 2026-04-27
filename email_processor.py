# ========================================================
# INTELLIGENT EMAIL ASSISTANT
# ========================================================
# Student: Yash Vashisth
# Roll Number: 2301730149
# ========================================================

import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', message='.*torchvision.*')

from transformers import pipeline
from datetime import datetime

# Load the text generation model with fewer constraints
try:
    generator = pipeline("text-generation", model="distilgpt2", device=-1)  # Use CPU by default
except:
    generator = pipeline("text-generation", model="gpt2", device=-1)


def generate_reply(email_text):
    """
    Generate a professional reply to an email using AI.

    Args:
        email_text: The email content to reply to

    Returns:
        Generated reply text
    """
    # Simple direct prompt without complex examples
    # This works better with GPT-2 as it avoids hallucinations
    prompt = f"Reply to this email: {email_text[:100]} Response:"

    try:
        response = generator(
            prompt, 
            max_new_tokens=150,  # Increased for longer replies
            num_return_sequences=1, 
            temperature=0.5, 
            top_p=0.9,
            do_sample=True,
            truncation=True
        )
        reply = response[0]['generated_text']
        
        # Extract only the part after "Response:"
        if "Response:" in reply:
            reply = reply.split("Response:")[1].strip()
        
        # Clean up unwanted text
        lines = reply.split("\n")
        reply = "\n".join(lines[:3])  # Take up to 3 lines for fuller response
        reply = reply.split("Email:")[0]  # Stop if it tries to generate another email
        
        # Ensure we have a response
        if not reply or len(reply) < 5:
            reply = "Thank you for your email. I'll get back to you soon."
        
        return reply.strip()
    except Exception as e:
        return f"Thank you for reaching out. I'll respond shortly."


def categorize_email(email_text):
    """
    Categorize email based on keywords.

    Args:
        email_text: The email content to categorize

    Returns:
        Category name
    """
    email_lower = email_text.lower()

    # Define keywords for each category
    categories = {
        "Meeting": ["meeting", "schedule", "appointment", "call", "discuss", "tuesday", "time"],
        "Finance": ["invoice", "payment", "bill", "receipt", "expense", "money", "amount", "$"],
        "Project": ["project", "task", "deadline", "deliverable", "sprint", "submission", "eod"],
        "Resume/Job": ["resume", "cv", "job", "position", "hiring", "vacancy", "interview", "applicant"],
        "Important": ["urgent", "asap", "important", "critical", "immediate", "must"],
        "Support": ["help", "issue", "problem", "error", "bug", "support", "troubleshoot", "fix"],
        "General": []
    }

    # Check for multiple keywords to increase confidence
    category_scores = {}
    for category, keywords in categories.items():
        if category != "General":
            score = sum(1 for keyword in keywords if keyword in email_lower)
            if score > 0:
                category_scores[category] = score

    # Return the category with highest score, or General
    if category_scores:
        return max(category_scores, key=category_scores.get)
    
    return "General"


def get_timestamp():
    """Get current timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def analyze_email(email_text):
    """
    Complete email analysis with reply generation and categorization.

    Args:
        email_text: The email content

    Returns:
        Dictionary with reply, category, and timestamp
    """
    result = {
        "original_email": email_text,
        "generated_reply": generate_reply(email_text),
        "category": categorize_email(email_text),
        "timestamp": get_timestamp()
    }
    return result


def categorize_email(email_text):
    """
    Categorize email based on keywords.

    Args:
        email_text: The email content to categorize

    Returns:
        Category name
    """
    email_lower = email_text.lower()

    # Define keywords for each category
    categories = {
        "Meeting": ["meeting", "schedule", "appointment", "conference call"],
        "Finance": ["invoice", "payment", "bill", "receipt", "expense", "money"],
        "Project": ["project", "task", "deadline", "deliverable", "sprint"],
        "Resume/Job": ["resume", "cv", "job", "position", "hiring", "vacancy"],
        "Important": ["urgent", "asap", "important", "critical", "immediate"],
        "Support": ["help", "issue", "problem", "error", "bug", "support"],
        "General": []
    }

    # Check for category keywords
    for category, keywords in categories.items():
        if category != "General":
            for keyword in keywords:
                if keyword in email_lower:
                    return category

    return "General"


def get_timestamp():
    """Get current timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def analyze_email(email_text):
    """
    Complete email analysis with reply generation and categorization.

    Args:
        email_text: The email content

    Returns:
        Dictionary with reply, category, and timestamp
    """
    result = {
        "original_email": email_text,
        "generated_reply": generate_reply(email_text),
        "category": categorize_email(email_text),
        "timestamp": get_timestamp()
    }
    return result
