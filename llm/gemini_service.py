from google import genai
from google.genai import types
from dotenv import load_dotenv
from base import LLMBaseModel
from bedrock_agentcore import BedrockAgentCoreApp


class Gemini(LLMBaseModel):

    def __init__(self):
        self.client = genai.Client()
        load_dotenv()

    def invoke(
        self,
        model,
        contents
    ):
        response = self.client.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction="You are a helpful assistant",
                thinking_config=types.ThinkingConfig(thinking_budget=0),  # Disables thinking
                temperature=0.1
            )
        )

        token_info = self.get_token_info(response.usage_metadata)

        return {
            "text": response.text,
            "usage": token_info
        }

    def invoke_stream(
        self,
        model,
        contents
    ):
        response = self.client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction="You are a helpful assistant",
                thinking_config=types.ThinkingConfig(thinking_budget=0),  # Disables thinking
                temperature=0.1
            )
        )
        for chunk in response:
            print(chunk.text, end="")

    def get_token_info(self, usage):
        token_info = {
            "prompt_tokens": usage.prompt_token_count,
            "completion_tokens": usage.candidates_token_count,
            "total_tokens": usage.total_token_count
        }
        return token_info


app = BedrockAgentCoreApp()
gemini = Gemini()


@app.entrypoint
def call(payload):
    model = payload.get("model", "gemini-2.5-flash-lite")
    messages = payload.get("messages", [])

    # Convert Streamlit message format to Gemini types.Content format
    contents = []
    for msg in messages:
        # Convert "assistant" role to "model" for Gemini
        role = "model" if msg["role"] == "assistant" else msg["role"]
        contents.append(types.Content(
            role=role,
            parts=[types.Part(text=msg["content"])]
        ))

    result = gemini.invoke(model, contents)

    return {
        "response": result["text"],
        "usage": result["usage"]
    }


if __name__ == "__main__":
    app.run()
