import json
import requests
from PIL import Image
import io
import base64

def analyze_ad_creative(image: Image.Image, api_endpoint="http://localhost:11434/api/generate", model="llava"):
    prompt = "You are an expert Chief Marketing Officer and Competitive Intelligence Analyst. Analyze this competitor advertisement image and break it down into the following strict JSON format: {\"hook_type\": \"Visual / Emotional / Statistical / Problem-Agitate-Solve\", \"core_hook_summary\": \"One sentence describing the primary hook capturing attention.\", \"value_proposition\": \"The main benefit or promise made to the consumer.\", \"target_audience_persona\": \"Inferred ideal customer profile based on imagery and tone.\", \"call_to_action\": \"The explicit or implicit CTA used.\", \"emotional_triggers\": [\"List\", \"of\", \"emotions\", \"targeted\"], \"estimated_effectiveness_score\": 1 to 10, \"strategic_takeaway\": \"Actionable advice on how a competitor could counter or improve upon this ad.\} Return ONLY valid JSON. No markdown backticks, no extra text.\"
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    payload = {"model": model, "prompt": prompt, "images": [img_str], "stream": False, "format": "json"}
    try:
        response = requests.post(api_endpoint, json=payload, timeout=60)
        result = response.json()
        return json.loads(result.get("response", {}))
    except Exception as e:
        return {"error": str(e), "hook_type": "Unknown", "core_hook_summary": "Analysis failed to parse correctly.\", "value_proposition": "N/A", "estimated_effectiveness_score": 0}
