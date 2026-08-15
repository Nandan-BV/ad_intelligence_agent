import json
import requests
from PIL import Image
import io
import base64

def analyze_ad_creative(image: Image.Image, api_endpoint="http://localhost:11434/api/generate", model="llava"):
    prompt = (
        "You are an elite Chief Marketing Officer, Growth Hacker, and Direct-Response Copywriting Expert. "
        "Perform a deep forensic audit of this competitor advertisement. Return ONLY valid JSON matching this exact structure: "
        "{"
        "\"hook_type\": \"Pattern Interrupt / Curiosity Gap / Fear of Missing Out / Problem-Agitate-Solve / Direct Offer\", "
        "\"core_hook_summary\": \"Detailed breakdown of the exact mechanism capturing attention in the first 3 seconds.\", "
        "\"value_proposition\": \"The underlying promise and core offer made to the consumer.\", "
        "\"target_audience_persona\": \"Deep psychological and demographic profile of the targeted buyer.\", "
        "\"call_to_action\": \"Exact CTA text or implied action.\", "
        "\"emotional_triggers\": [\"Trigger 1\", \"Trigger 2\", \"Trigger 3\"], "
        "\"competitor_weakness\": \"Identify 1 hidden vulnerability or gap in this competitor's marketing angle.\", "
        "\"counter_strategy_hook\": \"An aggressive, high-converting hook a competing brand can use to steal their audience.\", "
        "\"profit_optimization_tip\": \"Actionable tactical advice on how to outspend or outperform this ad profitably.\", "
        "\"estimated_effectiveness_score\": 8"
        "} "
        "Return strictly valid JSON with no markdown formatting backticks or extra text."
    )
    
    # Optimize image dimensions for local vision inference speed and stability
    image.thumbnail((1024, 1024))
    
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    payload = {
        "model": model,
        "prompt": prompt,
        "images": [img_str],
        "stream": False,
        "format": "json"
    }
    
    try:
        response = requests.post(api_endpoint, json=payload, timeout=120)
        result = response.json()
        
        if "response" not in result:
            return {"error": "Invalid model response structure", "hook_type": "Unknown", "core_hook_summary": "Parsing failed", "value_proposition": "N/A", "competitor_weakness": "N/A", "counter_strategy_hook": "N/A", "profit_optimization_tip": "N/A", "estimated_effectiveness_score": 0}
            
        parsed_data = json.loads(result.get("response", "{}"))
        return parsed_data
    except Exception as e:
        return {
            "error": str(e),
            "hook_type": "Connection Error",
            "core_hook_summary": "Failed to connect to local AI server.",
            "value_proposition": "N/A",
            "competitor_weakness": "N/A",
            "counter_strategy_hook": "N/A",
            "profit_optimization_tip": "N/A",
            "estimated_effectiveness_score": 0
        }
