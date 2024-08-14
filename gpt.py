    def _initialize_gemini(self):
        # Initialize the Gemini API client
        aiplatform.init(project="my-gcp-project", location="us-central1")

        # Specify the Gemini model endpoint
        endpoint = aiplatform.Endpoint.fetch("my-gemini-endpoint")

        # Create a prediction client
        client = endpoint.predict()

        # Define a function to query Gemini
        def query_gemini(prompt: str):
            response = client.predict(instances=[{"content": prompt}])
            return response.predictions[0]["content"]

        return query_gemini
