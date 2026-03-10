import requests, os
from dotenv import load_dotenv
load_dotenv()

TENANT_ID = os.getenv("FABRIC_TENANT_ID")
CLIENT_ID = os.getenv("FABRIC_CLIENT_ID")
CLIENT_SECRET = os.getenv("FABRIC_CLIENT_SECRET")
DATASET_ID = os.getenv("FABRIC_DATASET_ID")
WORKSPACE_ID = os.getenv("FABRIC_WORKSPACE_ID")

url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
r = requests.post(url, data={"grant_type":"client_credentials","client_id":CLIENT_ID,"client_secret":CLIENT_SECRET,"scope":"https://analysis.windows.net/powerbi/api/.default"}, timeout=15)
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
url2 = f"https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/datasets/{DATASET_ID}/executeQueries"

# Nigeria
print("=== NIGERIA ===")
ng_dax = "EVALUATE SELECTCOLUMNS(FILTER('Nigeria - Chemist', 'Nigeria - Chemist'[latitude] <> BLANK()), \"Shop Name\", 'Nigeria - Chemist'[name], \"latitude\", 'Nigeria - Chemist'[latitude], \"longitude\", 'Nigeria - Chemist'[longitude], \"Retailer Subtype\", 'Nigeria - Chemist'[retailer_subtype], \"YTD Retailing Value\", 0)"
r2 = requests.post(url2, headers=headers, json={"queries":[{"query":ng_dax}],"serializerSettings":{"includeNulls":True}}, timeout=30)
data = r2.json()
rows = data['results'][0]['tables'][0].get('rows',[])
print(f"Status: {r2.status_code} | Rows: {len(rows)}")
if rows: print(f"Sample: {rows[0]}")

# Angola
print("\n=== ANGOLA ===")
ao_dax = "EVALUATE SELECTCOLUMNS(FILTER('Angola - Chemist', 'Angola - Chemist'[Lat] <> BLANK()), \"Shop Name\", 'Angola - Chemist'[Retailer/Chemist Name], \"latitude\", 'Angola - Chemist'[Lat], \"longitude\", 'Angola - Chemist'[Long], \"Retailer Subtype\", 'Angola - Chemist'[Type new], \"YTD Retailing Value\", 'Angola - Chemist'[YTD Sales Value])"
r3 = requests.post(url2, headers=headers, json={"queries":[{"query":ao_dax}],"serializerSettings":{"includeNulls":True}}, timeout=30)
data3 = r3.json()
rows3 = data3['results'][0]['tables'][0].get('rows',[])
print(f"Status: {r3.status_code} | Rows: {len(rows3)}")
if rows3: print(f"Sample: {rows3[0]}")