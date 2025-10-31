import requests
import json
from .getuipathreleases import getRelease
from .getfolders import getFolders

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

if __name__ == "__main__":
    triggerUiPathJob("GenerateExcelFile",{'auth_url': 'https://cloud.uipath.com/identity_/connect/token', 'scope': 'Orchestrator.Jobs.ReadWrite', 'base_url': 'https://cloud.uipath.com/anjalqeebhkv/DefaultTenant/orchestrator_/',
'Folderurl': 'odata/Folders?$filter=contains(tolower(FullyQualifiedName),$processName)',
'Releaseurl': "odata/Releases?$filter=tolower(ProcessKey) eq '$processName'", 'Processurl': 'odata/Processes', 'triggerJob': 'odata/Jobs/UiPath.Server.Configuration.OData.StartJob', 'tenant_name': 'DefaultTenant'},'eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg2QTY0RjI2NTA3MzY4MkQ4NTFGMDFBRUFEMTQxNjgyNUFEOTNDNTciLCJ4NXQiOiJocVpQSmxCemFDMkZId0d1clJRV2dsclpQRmMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2Nsb3VkLnVpcGF0aC5jb20vaWRlbnRpdHlfIiwibmJmIjoxNzYxODAyMzIyLCJpYXQiOjE3NjE4MDI2MjIsImV4cCI6MTc2MTgwNjIyMiwiYXVkIjoiVWlQYXRoLk9yY2hlc3RyYXRvciIsInNjb3BlIjpbIk9SLkFkbWluaXN0cmF0aW9uIiwiT1IuQWRtaW5pc3RyYXRpb24uUmVhZCIsIk9SLkFkbWluaXN0cmF0aW9uLldyaXRlIiwiT1IuQW5hbHl0aWNzIiwiT1IuQW5hbHl0aWNzLlJlYWQiLCJPUi5BbmFseXRpY3MuV3JpdGUiLCJPUi5Bc3NldHMiLCJPUi5Bc3NldHMuUmVhZCIsIk9SLkFzc2V0cy5Xcml0ZSIsIk9SLkF1ZGl0IiwiT1IuQXVkaXQuUmVhZCIsIk9SLkF1ZGl0LldyaXRlIiwiT1IuQXV0b21hdGlvblNvbHV0aW9ucy5BY2Nlc3MiLCJPUi5CYWNrZ3JvdW5kVGFza3MiLCJPUi5CYWNrZ3JvdW5kVGFza3MuUmVhZCIsIk9SLkJhY2tncm91bmRUYXNrcy5Xcml0ZSIsIk9SLkV4ZWN1dGlvbiIsIk9SLkV4ZWN1dGlvbi5SZWFkIiwiT1IuRXhlY3V0aW9uLldyaXRlIiwiT1IuRm9sZGVycyIsIk9SLkZvbGRlcnMuUmVhZCIsIk9SLkZvbGRlcnMuV3JpdGUiLCJPUi5IeXBlcnZpc29yIiwiT1IuSHlwZXJ2aXNvci5SZWFkIiwiT1IuSHlwZXJ2aXNvci5Xcml0ZSIsIk9SLkpvYnMiLCJPUi5Kb2JzLlJlYWQiLCJPUi5Kb2JzLldyaXRlIiwiT1IuTGljZW5zZSIsIk9SLkxpY2Vuc2UuUmVhZCIsIk9SLkxpY2Vuc2UuV3JpdGUiLCJPUi5NYWNoaW5lcyIsIk9SLk1hY2hpbmVzLlJlYWQiLCJPUi5NYWNoaW5lcy5Xcml0ZSIsIk9SLk1MIiwiT1IuTUwuUmVhZCIsIk9SLk1MLldyaXRlIiwiT1IuTW9uaXRvcmluZyIsIk9SLk1vbml0b3JpbmcuUmVhZCIsIk9SLk1vbml0b3JpbmcuV3JpdGUiLCJPUi5RdWV1ZXMiLCJPUi5RdWV1ZXMuUmVhZCIsIk9SLlF1ZXVlcy5Xcml0ZSIsIk9SLlJvYm90cyIsIk9SLlJvYm90cy5SZWFkIiwiT1IuUm9ib3RzLldyaXRlIiwiT1IuU2V0dGluZ3MiLCJPUi5TZXR0aW5ncy5SZWFkIiwiT1IuU2V0dGluZ3MuV3JpdGUiLCJPUi5UYXNrcyIsIk9SLlRhc2tzLlJlYWQiLCJPUi5UYXNrcy5Xcml0ZSIsIk9SLlRlc3REYXRhUXVldWVzIiwiT1IuVGVzdERhdGFRdWV1ZXMuUmVhZCIsIk9SLlRlc3REYXRhUXVldWVzLldyaXRlIiwiT1IuVGVzdFNldEV4ZWN1dGlvbnMiLCJPUi5UZXN0U2V0RXhlY3V0aW9ucy5SZWFkIiwiT1IuVGVzdFNldEV4ZWN1dGlvbnMuV3JpdGUiLCJPUi5UZXN0U2V0cyIsIk9SLlRlc3RTZXRzLlJlYWQiLCJPUi5UZXN0U2V0cy5Xcml0ZSIsIk9SLlRlc3RTZXRTY2hlZHVsZXMiLCJPUi5UZXN0U2V0U2NoZWR1bGVzLlJlYWQiLCJPUi5UZXN0U2V0U2NoZWR1bGVzLldyaXRlIiwiT1IuVXNlcnMiLCJPUi5Vc2Vycy5SZWFkIiwiT1IuVXNlcnMuV3JpdGUiLCJPUi5XZWJob29rcyIsIk9SLldlYmhvb2tzLlJlYWQiLCJPUi5XZWJob29rcy5Xcml0ZSJdLCJzdWJfdHlwZSI6InNlcnZpY2UuZXh0ZXJuYWwiLCJwcnRfaWQiOiIzYTk5YmUwZi00NDdjLTQ5YTgtYmY1ZC02NWQ0NzcyNTQ2MTAiLCJjbGllbnRfaWQiOiI0NTBmMGFkNC1mYTE4LTRiMGItYTQ5OC05YWQ3ZWM0OTBmMDYiLCJqdGkiOiI2Mzg5MTA1RTREOUQ1MENGMEM2MjE2Q0RDNjBCNDM5NCJ9.R2O6iux1ohUAVPu17vV4J-qdYoGtomYtphun5TRgV2y7oQytwK4Ie8A8uBOnb0ULSaHazTHoeoVJbhgT4gaDpxHGjB0xt9su-SAjEgW-jeKcqj1CQtgO7zb2VTkXzr5vv6z44KdBHgTUsy-PNxT4ewBX2kSSpAZIz8_n7LGnqpYizQuRq9U76BlFSp4TqoA3LFkuXeDcl4j6zdh7XGcX3HbdyK6VN8-oTXB6DGaLqlNy00Avsk9C_CnW-qjMM8IfC2PfILB5TStISiAyGZlkSNRe8mTAJhx4VIBpP59mXfgowTPUGcNpZADEH8Fl_foMpTImgWLcbRxBjmNrovKNVQ')