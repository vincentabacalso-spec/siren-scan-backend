import requests
import os
from dotenv import load_dotenv
import time
load_dotenv()

VIRUS_TOTAL_API_KEY = os.getenv("VIRUS_TOTAL_API_KEY")


def scan_url(url): 
    URL_ENDPOINT = "https://www.virustotal.com/api/v3/urls"
    try:
        response = requests.post(
            URL_ENDPOINT, 
            headers = {
                'accept': 'application/json',
                'content-type': 'application/x-www-form-urlencoded',
                'x-apikey': VIRUS_TOTAL_API_KEY, 
            }, 
            data = {'url': url}
        )

        if response.status_code == 200:
            analysis_id = response.json()['data']['id']
            analysis_response = requests.get(
                f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
                headers={
                    "accept": "application/json",
                    "x-apikey": VIRUS_TOTAL_API_KEY
                }
            )
            print(analysis_response.json())
            return analysis_response.json()
        else: 
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"


def scan_file(file_path):
    FILE_ENDPOINT = "https://www.virustotal.com/api/v3/files"
    HEADER = {
        'accept': 'application/json',
        'x-apikey': VIRUS_TOTAL_API_KEY,
    }

    try: 

        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(FILE_ENDPOINT, headers=HEADER, files=files)
        
        if response.status_code != 200:
            raise Exception(f"VT Upload Error: {response.text}")

        analysis_id = response.json()["data"]["id"]
        print(f"File uploaded successfully. Analysis ID: {analysis_id}")
        analysis_endpoint = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"

        for _ in range(30): 
            result = requests.get(analysis_endpoint, headers={'accept': 'application/json', 'x-apikey': VIRUS_TOTAL_API_KEY})
            data = result.json()

            status = data["data"]["attributes"]["status"]
            if status == "completed":
                stats = data["data"]["attributes"]["stats"]
                return stats

            time.sleep(1)

        raise Exception("VirusTotal file scan timed out")
    except Exception as e:
        return f"An error occurred: {e}" 

report = scan_file("./src/app/services/CCS 7 Ideation.pdf")
print(report)