import requests
import json
from .getuipathreleases import getRelease
from .getuipathfolders import getFolders

def triggerUiPathJob(process_name: str, config: dict, bearerKey: str) -> dict:
    releaseData={}
    base_url = config.get("base_url") # Ensure this is in your Config.json
    trigger_job_url = config.get("triggerJob") # Ensure this is in your Config.json
    start_job_url=base_url+trigger_job_url
    tenant_name = config.get("tenant_name") # Ensure this is in your Config.json
    try:
        releaseData=getFolders(Config=config,bearerKey=bearerKey,process_name=process_name)
    except:
        raise 
    organization_unit_id=releaseData.get("organization_unit")
    ReleaseId=releaseData.get("ReleaseId")

    if not all([start_job_url, tenant_name, organization_unit_id]):
        return {"status": "error", "message": "Missing required URL or config parameters in Config.json."}

    # 1. Define the API Headers
    headers = {
        "Authorization": f"Bearer {bearerKey}",
        "X-UIPATH-OrganizationUnitId": organization_unit_id,
        "Content-Type": "application/json",
        "Accept":"application/json"
    }

    
    payload = {
        "startInfo": {
            "ReleaseKey": ReleaseId,
            "Strategy": "ModernJobsCount",
            "JobsCount": 1,
            "InputArguments": "{\"in_TestCaseData\":\"Initial Test Run\"}"
        }
    }

    try:
        # 3. Make the POST request to start the job
        response = requests.post(
            start_job_url,
            headers=headers,
            json=payload
        )
        if response.status_code==201:
            return {f"Job f{process_name} Trigge successfully."}
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

    except requests.exceptions.HTTPError as err:
        return {"message": f"HTTP Error triggering job: {err}. Response: {response.text}"}
    except Exception as e:
        return {"message": f"An unexpected error occurred: {str(e)}"}