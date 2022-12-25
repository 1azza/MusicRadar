import json
client_data = {}
with open('data/radar_data.json', 'r') as handle:
    radar_data = json.load(handle)
for i in radar_data:
    client_data[i['title']] = {
        "owned" : True,
        "site_data": i
    }

with open('data/client_data.json', 'w') as handle:
    json.dump(client_data, handle, indent=4)