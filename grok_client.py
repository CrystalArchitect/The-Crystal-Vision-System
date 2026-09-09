import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class GrokClient:
    def __init__(self):
        self.api_key = os.getenv("XAI_API_KEY")
        self.base_url = "https://api.x.ai/v1"
        self.model = os.getenv("GROK_MODEL", "grok-2")
        
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
            )
        else:
            self.client = None

    def get_response(self, message_history):
        """
        Fetches a response from Grok based on the message history.
        Tries fallback models if the primary one fails.
        """
        if not self.client:
            return "Error: xAI API Key not found. Please add it to your .env file."

        # List of models to try in order
        models_to_try = [self.model, "grok-2", "grok-beta", "grok-latest"]
        # Remove duplicates while preserving order
        models_to_try = list(dict.fromkeys(models_to_try))

        last_error = None
        for model in models_to_try:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=message_history,
                    stream=False
                )
                # If successful, update the primary model for future calls
                self.model = model
                return response.choices[0].message.content
            except Exception as e:
                last_error = str(e)
                if "Model not found" in last_error or "invalid-argument" in last_error:
                    continue # Try the next model
                else:
                    break # Stop if it's a different kind of error (like API key)

        return f"Error communicating with Grok: {last_error}"
