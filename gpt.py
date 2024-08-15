import os
import re
from typing import Dict

from google.api_core import retry
from google.cloud import aiplatform
from langchain_community.chat_models import ChatGooglePalm  # Import from langchain-community
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)


class LLMLogger:

    def __init__(self, llm):
        self.llm = llm

    def __call__(self, prompts, stop=None, **kwargs):
        parsed_reply = self.log_request(prompts, self.llm(prompts, stop, **kwargs))
        return parsed_reply

    @staticmethod
    def log_request(prompts, parsed_reply: Dict[str, Dict]):
        print("-" * 40)
        print(f"PROMPT: {prompts}")
        print(f"REPLY: {parsed_reply}")
        print("-" * 40)
        return parsed_reply


class GPTAnswerer:
    def __init__(self, openai_api_key: str, google_api_key: str):
        self.google_api_key = google_api_key
        self.openai_api_key = openai_api_key
        if self.google_api_key is not None:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.google_api_key
            if self.openai_api_key is not None:
                self.llm_cheap = LLMLogger(
                    ChatGooglePalm(temperature=0.1, model="models/chat-bison-001", google_api_key=self.google_api_key)
                )
            else:
                # Initialize the Gemini API client
                aiplatform.init(project='YOUR_PROJECT_ID')

                # Specify the Gemini model endpoint
                self.endpoint = aiplatform.Endpoint.fetch(endpoint_name='projects/YOUR_PROJECT_ID/locations/YOUR_REGION/endpoints/ENDPOINT_NAME')
                self.llm_cheap = self._query_gemini
        else:
            raise RuntimeError("Either an OpenAI API key or a Google API key must be provided.")

    def _query_gemini(self, prompts):
        response = self.endpoint.predict(instances=[{"content": prompts[0].content}])
        return {'output': {'output': response.predictions[0]["content"]}}

    @staticmethod
    def find_best_match(text: str, options: list[str]) -> str:
        similarity_scores = [
            len(set(text.lower().split()) & set(option.lower().split()))
            for option in options
        ]
        best_match_index = similarity_scores.index(max(similarity_scores))
        return options[best_match_index]

    def set_resume(self, resume):
        self.resume = resume

    def summarize_job_description(self, text: str) -> str:
        prompt = f"""
        Ignore irrelevant information like benefits, perks, company culture, and only very concisely summarize the job description, focusing on the required skills and experience.
        Text: {text}
        """
        return self.llm_cheap([HumanMessage(content=prompt)])['output']['output']

    def extract_number_from_string(self, output_str: str):
        match = re.search(r'\d+', output_str)
        if match:
            return int(match.group())
        return None
