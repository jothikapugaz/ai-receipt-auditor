import os
import json
import google.generativeai as genai

def analyze_receipt(uploaded_file):
    """
    Sends receipt image bytes to Google Gemini 1.5 Flash 
    using the stable legacy library engine framework.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return {
            "store_name": "Local Vendor (Simulation Mode)",
            "amount": 250.00,
            "category": "Food & Groceries",
            "date": "2026-08-20"
        }

    try:
        # Initialize the stable configuration path
        genai.configure(api_key=api_key)
        
        # Load the multimodal model matrix
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # CORRECTLY format file byte streams for Gemini vision engine
        image_data = uploaded_file.read()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": image_data
            }
        ]
        
        prompt = (
            "Analyze this receipt image. Extract details into a clean JSON structure with these exact keys: "
            "'store_name', 'amount', 'category', 'date'. Output raw JSON text only, no markdown wrappers.\n"
            "Fallback Rules:\n"
            "1. For handwritten chits or informal scribbles, extract the calculated text total into 'amount'.\n"
            "2. If store branding is absent, make store_name 'Local Vendor'.\n"
            "3. If the date layout is invisible, default the date string to '2026-08-20'."
        )
        
        # Generate model calculations
        response = model.generate_content([prompt, image_parts[0]])
        
        # Clean up any accidental markdown backticks returned by the engine string
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        
        return json.loads(clean_text)
        
    except Exception as e:
        print(f"Systemic parsing exception captured: {e}")
        return {
            "store_name": "Error Processing",
            "amount": 0.0,
            "category": "Uncategorized",
            "date": "2026-08-20"
        }
