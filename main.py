from googleapiclient.discovery import build
from google.oauth2 import service_account

class GPTAnswerer:
    def __init__(self, model_name: str, project_id: str, location: str):
        self.model_name = model_name
        self.project_id = project_id
        self.location = location
        self.service = build(
            'generativeai', 'v1beta',
            credentials=service_account.Credentials.from_service_account_file(
                'path/to/your/service_account_key.json'
            )
        )

    def answer(self, question: str) -> str:
        response = self.service.models().predict(
            name=f'projects/{self.project_id}/locations/{self.location}/models/{self.model_name}',
            body={
                'prompt': question,
                'temperature': 0.7,  # Adjust for creativity
                'maxOutputTokens': 100  # Adjust for response length
            }
        ).execute()
        return response['predictions'][0]['content']
