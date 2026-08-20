import os
import json
import base64
from openai import OpenAI

def analyze_receipt(uploaded_file):
    """
    Accepts file bytes from Streamlit uploader, encodes to base64,
    and sends to OpenAI Vision API with strict fallback rules.
    """
    # Check for API key; if missing, return smart mock data for testing
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key or api_key == "mock_key":
        return {
            "store_name": "Local Vendor (Mock)",
            "amount": 250.00,
            "category": "Food & Groceries",
            "date": "2026-08-20"
        }

    client = OpenAI(api_key=api_key)
    
    # Encode uploaded image bytes to base64 string
    base64_image = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

    prompt = (
        "Analyze this receipt image. Extract information into a strict JSON format with these exact keys: "
        "'store_name', 'amount', 'category', 'date'. Do not include markdown formatting or extra text.\n"
        "Follow these strict localized fallback rules:\n"
        "1. If it is a handwritten chit or informal receipt, look for mathematical totals and extract that number into 'amount'.\n"
        "2. If the store name or letterhead is missing entirely, set 'store_name' to 'Local Vendor'.\n"
        "3. If the date is missing or illegible, set 'date' to '2026-08-20' (current date)."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            temperature=0.0
        )
        # Parse the JSON string from the response
        result_json = json.loads(response.choices[0].message.content)
        return result_json
    except Exception as e:
        print(f"Error processing AI request: {e}")
        return {
            "store_name": "Error Processing",
            "amount": 0.0,
            "category": "Uncategorized",
            "date": "2026-08-20"
        }
