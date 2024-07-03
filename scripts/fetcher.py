import requests
import json

def data_fetcher():
    url = "https://www.publicprocurement.be/api/sea/search/publications?include-organisation-children=true&page=1&page-size=25"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "nl",
        "Account-Type": "public",
        "Authorization":  "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJCMlhadHh1aXhwcUlzbm9tbUdQWVE1TjdodC1WblZDN0pqTnBMYlBQNmpFIn0.eyJleHAiOjE3MjAwMDQ3NzYsImlhdCI6MTcyMDAwMTE3NiwianRpIjoiNmMxMjVlNWUtNzVkZS00MWU3LThhMzAtMGEyODFkYjE1Y2I0IiwiaXNzIjoiaHR0cHM6Ly93d3cucHVibGljcHJvY3VyZW1lbnQuYmUvYXV0aC9yZWFsbXMvc3VwcGxpZXIiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiOTMzOTgwYTUtMTQ5NS00NTg1LTlkYjMtNGRiMDc0ZTQ0ODQwIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZnJvbnRlbmQtcHVibGljIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy1zdXBwbGllciIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImNsaWVudEhvc3QiOiI5MS4xNzguMTA1LjIxNyIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiY2xpZW50SWQiOiJmcm9udGVuZC1wdWJsaWMiLCJyZWFsbSI6InB1YmxpYyIsInByZWZlcnJlZF91c2VybmFtZSI6InNlcnZpY2UtYWNjb3VudC1mcm9udGVuZC1wdWJsaWMiLCJjbGllbnRBZGRyZXNzIjoiOTEuMTc4LjEwNS4yMTcifQ.J4f0tz3I0RL-B6w7FhLWWxLvWsUms4DzYF_aaLxe9zD8EJ_pt5iqOAmLPSRlbhJSJwIj04NZynPj7JtY7RGYToXs0M1zto9h_Xc5-x39yK64EhJ1zkuAs2h0UZ0bbDRPtxOJX2BAdDYeWZ8A8UH_jE_iAmpSWWAP-Ktgqph1jTk7Z_uuLACuu_-XRlX269wnNXuVzkZCTdFHy8bxpw9I4rACs2MEKbF7fs4M_hdvrwfBTGrzkrKnOxESePsewtYgjRKqPeoZi-KKaO_s9BhWTrF5k8OPK-X0BNCwYeWGc6jrFcOq4KOzq8858jYr3-mQeoCtrAWurxuI14UxYKC-Vw",
        "BelGov-Trace-Id": "3c32731d-4cc7-4bb4-a2d2-c42905f5f4af",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "expires": "0",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }


    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        json_data = json.dumps(response.json())
        print(type(json_data))
        with open('/opt/airflow/data/raw/raw.json', "w") as raw:
            print(json_data[0])
            raw.write(str(json_data))
    else:
        print(f"Failed to fetch data: {response.status_code}")
