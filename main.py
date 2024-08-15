from google.cloud import aiplatform

class GPTAnswerer:
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.api_key = api_key
        self.aiplatform = aiplatform.gapic.PredictionServiceClient()

    def answer(self, question: str) -> str:
        endpoint = aiplatform.Endpoint(name=self.model_name)
        instance = {
            "text": question
        }
        response = self.aiplatform.predict(endpoint=endpoint, instances=[instance])
        return response.predictions[0]['text']
