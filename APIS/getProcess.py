import requests
import os
import json

def getProcess(Config:dict,bearerKey:str):
    try:
        processUrl=Config.get("base_url")+Config.get("Processurl")
        if not processUrl:
            print("Error: 'Folder_URL' is missing in the configuration.")
            return None
        header={
            "accept": "application/json",
            "authorization": f"Bearer {bearerKey}"
        }
        response=requests.get(processUrl,headers=header)
        if response:
            data=json.loads(response.text)
            print(f"Successfully retrieved {data.get('@odata.count', 0)} folders.")
            return data
    except requests.exceptions.HTTPError as err:
        print(f"❌ Failed to fetch folders (HTTP Error: {err.response.status_code}).")
        # Attempt to print the detailed UiPath error message
        try:
            error_details = err.response.json()
            print(f"Error Message: {error_details.get('message', 'No specific message.')}")
        except json.JSONDecodeError:
            raise(f"Raw Error Response: {err.response.text}")
        
    except requests.exceptions.RequestException as e:
        raise(f"⚠️ An error occurred during the API call: {e}")