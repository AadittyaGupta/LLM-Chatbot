import requests
import json

def get_available_models():
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = []
            for model in data.get("models", []):
                model_name = model.get("name", "").split(":")[0]
                if model_name and model_name not in models:
                    models.append(model_name)
            return sorted(models)
        else:
            return []
    except:
        return []

def get_bot_response(user_message, model_name):
    try:
        if model_name == 'qwen3':
            model_name = 'qwen3:0.6b'

        payload = {
            "model": model_name,
            "prompt": user_message,
            "stream": False
        }

        response = requests.post(
            "http://localhost:11434/api/generate",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            return result.get("response", "Sorry, I couldn't generate a response.").strip()
        else:
            return f"Error: Ollama API returned status code {response.status_code}"

    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to Ollama. Make sure it's running at localhost:11434"
    
    except requests.exceptions.Timeout:
        return "Error: Request timed out."
    
    except Exception as e:
        return f"Error: {str(e)}"
