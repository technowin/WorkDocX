
import msal
import requests

from Masters.models import para_master



TENANT_ID = (para_master.objects.filter(para_name='PB Dashboard', para_details='TENANT_ID').values_list('description', flat=True).first())
CLIENT_ID = (para_master.objects.filter(para_name='PB Dashboard', para_details='CLIENT_ID').values_list('description', flat=True).first())
CLIENT_SECRET = (para_master.objects.filter(para_name='PB Dashboard', para_details='CLIENT_SECRET').values_list('description', flat=True).first())
WORKSPACE_ID = (para_master.objects.filter(para_name='PB Dashboard', para_details='WORKSPACE_ID').values_list('description', flat=True).first())
REPORT_ID = (para_master.objects.filter(para_name='PB Dashboard', para_details='REPORT_ID').values_list('description', flat=True).first())
REPORT_ID2 = (para_master.objects.filter(para_name='PB Dashboard', para_details='REPORT_ID2').values_list('description', flat=True).first())
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]
POWER_BI_API = "https://api.powerbi.com/v1.0/myorg"

# def get_powerbi_embed_info():
#     app = msal.ConfidentialClientApplication(
#         CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
#     )
#     token_response = app.acquire_token_for_client(scopes=SCOPE)

#     if "access_token" not in token_response:
#         raise Exception(f"Token acquisition failed: {token_response}")
#     access_token = token_response["access_token"]

#     headers = {"Authorization": f"Bearer {access_token}"}
#     report_url = f"{POWER_BI_API}/groups/{WORKSPACE_ID}/reports/{REPORT_ID}"
#     report_response = requests.get(report_url, headers=headers).json()

#     embed_token_url = f"{POWER_BI_API}/groups/{WORKSPACE_ID}/reports/{REPORT_ID}/GenerateToken"
#     embed_token_response = requests.post(
#         embed_token_url,
#         headers={**headers, "Content-Type": "application/json"},
#         json={"accessLevel": "view"},
#     ).json()

#     return {
#         "embedUrl": report_response["embedUrl"],
#         "embedToken": embed_token_response["token"],
#         "reportId": REPORT_ID,
#     }

def get_powerbi_embed_info(report_id):
    app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )
    token_response = app.acquire_token_for_client(scopes=SCOPE)

    if "access_token" not in token_response:
        raise Exception(f"Token acquisition failed: {token_response}")
    access_token = token_response["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    report_url = f"{POWER_BI_API}/groups/{WORKSPACE_ID}/reports/{report_id}"
    report_response = requests.get(report_url, headers=headers).json()

    embed_token_url = f"{POWER_BI_API}/groups/{WORKSPACE_ID}/reports/{report_id}/GenerateToken"
    embed_token_response = requests.post(
        embed_token_url,
        headers={**headers, "Content-Type": "application/json"},
        json={"accessLevel": "view"},
    ).json()

    return {
        "embedUrl": report_response["embedUrl"],
        "embedToken": embed_token_response["token"],
        "reportId": report_id,
    }
