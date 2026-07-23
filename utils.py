import re
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Read Gemini API key from .env
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)


def analyze_code(code, language, mode):
    """
    Analyze {language} code using Gemini AI.
    """

    prompt = f"""
You are an expert programming mentor.
Your task is: {mode}
If the selected mode is:

- Code Review:
  Review the overall code quality, readability, and maintainability.

- Find Bugs:
  Only identify bugs, logical errors, syntax issues, and possible runtime errors.

- Optimize Code:
  Suggest performance improvements and more efficient coding practices.

- Explain Code:
  Explain the code line by line in simple beginner-friendly language.

Analyze the following {language} code.

Provide your answer in Markdown format.

Use these headings:

# ⭐ Code Quality Score

# 🐞 Bugs or Mistakes

# 💡 Suggestions for Improvement

# ✅ Best Practices

# 🔧 Improved Code

Keep the explanation beginner-friendly.

{language} Code:
{code}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text

score = "--"

match = re.search(r'(\d+(\.\d+)?)\s*/\s*10', text)

if match:
    score = match.group(1) + "/10"

    return {
    "analysis": text,
    "score": score
}