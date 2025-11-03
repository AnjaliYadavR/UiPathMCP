import requests
import json
from .getuipathreleases import getRelease
from .getuipathfolders import getFolders
from .getToken import getToken

async def triggerUiPathJob(process_name: str, config: dict, bearerKey: str) -> dict:
    releaseData={}
    base_url = config.get("base_url") # Ensure this is in your Config.json
    trigger_job_url = config.get("triggerJob") # Ensure this is in your Config.json
    start_job_url=base_url+trigger_job_url
    tenant_name = config.get("tenant_name") # Ensure this is in your Config.json
    try:
        releaseData=await getFolders(Config=config,bearerKey=bearerKey,process_name=process_name)
    except:
        raise 
    organization_unit_id=releaseData.get("organization_unit")
    ReleaseId=releaseData.get("ReleaseId")
    inputArguments=releaseData.get("InputArguments")

    if not all([start_job_url, organization_unit_id]):
        return {"status": "error", "message": "Missing required URL or config parameters."}
    if inputArguments is None:
        return {"status": "error", "message": f"Kindly pass the value for following arguments : {inputArguments}"}

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
            "InputArguments": str(inputArguments)
        }
    }

    try:
        # 3. Make the POST request to start the job
        response = await requests.post(
            start_job_url,
            headers=headers,
            json=payload
        )
        if response.status_code==201:
            return {f"Job {process_name} Trigge successfully."}
        if response.status_code==401:
            try:
                bearerKey = await getToken(config=config)
                print("token generated successfully")
                await triggerUiPathJob(process_name=process_name, config=config, bearerKey=bearerKey)
            except Exception as e:
                raise SystemError("Failed to generate the Token.")
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

    except requests.exceptions.HTTPError as err:
        return {"message": f"HTTP Error triggering job: {err}. Response: {response.text}"}
    except Exception as e:
        return {"message": f"An unexpected error occurred: {str(e)}"}