import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class ClaudeClient:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
        
        if self.api_key:
            self.client = Anthropic(api_key=self.api_key)
        else:
            self.client = None

    def get_response(self, message_history):
        """
        Fetches a response from Claude based on the message history.
        message_history is expected to be a list of dicts with 'role' and 'content'.
        """
        if not self.client:
            return "Error: Anthropic API Key not found. Please add it to your .env file."

        try:
            # Extract system prompt if present
            system_prompt = "You are a helpful and friendly Discord agent."
            filtered_messages = []
            
            for msg in message_history:
                if msg["role"] == "system":
                    system_prompt = msg["content"]
                else:
                    # Claude API expects 'user' or 'assistant' roles
                    filtered_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=filtered_messages
            )
            return response.content[0].text
        except Exception as e:
            return f"Error communicating with Claude: {str(e)}"
