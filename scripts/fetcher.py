import requests
import json

def data_fetcher():
    url = "https://www.publicprocurement.be/api/sea/search/publications?include-organisation-children=true&page=1&page-size=25"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "nl",
        "Account-Type": "public",
        "Authorization":  "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJCMlhadHh1aXhwcUlzbm9tbUdQWVE1TjdodC1WblZDN0pqTnBMYlBQNmpFIn0.eyJleHAiOjE3MTk4NzQ4MzAsImlhdCI6MTcxOTg3MTIzMCwianRpIjoiMjIxYmE5OWMtOTQ3My00YTAwLWFiNjItZTVmYjQ4Y2YwYTQ3IiwiaXNzIjoiaHR0cHM6Ly93d3cucHVibGljcHJvY3VyZW1lbnQuYmUvYXV0aC9yZWFsbXMvc3VwcGxpZXIiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiOTMzOTgwYTUtMTQ5NS00NTg1LTlkYjMtNGRiMDc0ZTQ0ODQwIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZnJvbnRlbmQtcHVibGljIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy1zdXBwbGllciIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImNsaWVudEhvc3QiOiI5MS4xNzguMTA1LjIxNyIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiY2xpZW50SWQiOiJmcm9udGVuZC1wdWJsaWMiLCJyZWFsbSI6InB1YmxpYyIsInByZWZlcnJlZF91c2VybmFtZSI6InNlcnZpY2UtYWNjb3VudC1mcm9udGVuZC1wdWJsaWMiLCJjbGllbnRBZGRyZXNzIjoiOTEuMTc4LjEwNS4yMTcifQ.mr-pMoxvCSsTXJ2ryjcXrl5D3tcWSd0xEgXVbcMKGBYHqDqYKseClmvXOS32KNr57mpvlEZMuTRoUyeMwLIWaQcGhakdHW5w2IyU9CHKIE0Ngy918XR-Ofi819gyw4IbUJ0I-mXNQPN9RtETzPebRRoUv7YBj_TRfF7xvd31ojqR8mk7hLSQmgRptECEGEY87a_fP1fE9rMxWCpX1jBvGh0UZYRA9JezDj_O4OIapsu8fkcpVmln00xrpoHfWtsTGV-F-CwiXFF_Th33YCTLFDV41b1T9cyLbSapJUOqGvGCtvnj8evyhG15IkLzVVMpmW4CW8dTSe5tomYxuVrMRA",
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
