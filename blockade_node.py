import time
import requests

class BlockadeLabsNode:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://backend.blockadelabs.com/api/v1"
        self.headers = {
            "x-api-key": self.api_key,
            "Accept": "application/json"
        }

    def generate_skybox(self, prompt: str, style_id: int = 2) -> str:
        """
        Sends a prompt to generate a 360-degree skybox and polls until complete.
        Returns the URL of the finished equirectangular image.
        """
        # Step 1: Start the generation job
        generate_url = f"{self.base_url}/skybox"
        payload = {
            "prompt": prompt,
            "skybox_style_id": style_id
        }
        
        response = requests.post(generate_url, headers=self.headers, data=payload)
        response.raise_for_status()
        
        job_id = response.json().get("id")
        if not job_id:
            raise Exception("Failed to retrieve Job ID from Blockade Labs.")

        # Step 2: Poll for completion
        poll_url = f"{self.base_url}/imagerequests/{job_id}"
        
        while True:
            time.sleep(3) # Wait 3 seconds between checks
            poll_response = requests.get(poll_url, headers=self.headers)
            poll_response.raise_for_status()
            
            data = poll_response.json()
            status = data.get("status")
            
            if status == "complete":
                return data.get("file_url")
            elif status == "error":
                raise Exception("Skybox generation failed on the server.")
            elif status == "abort":
                raise Exception("Skybox generation was aborted.")
            
            # If status is "pending" or "processing", the loop continues