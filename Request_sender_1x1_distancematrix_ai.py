import csv
import datetime
import logging
import requests
import time
import os.path
import sys


BASE_URL = "https://api.distancematrix.ai"

DATA_FILE_PATH = "data.csv"
RESULT_FILE_PATH = "result.csv"
TOKEN_FILE_PATH = "token.txt"

if(os.path.exists(TOKEN_FILE_PATH)!=True):
    print('No token.txt file with API token. Please contact alina.lysykh@distancematrix.ai for help \n')
    exit=input("press close to exit")
    sys.exit()

if(os.path.exists(DATA_FILE_PATH)!=True):
    print('No data.csv file with raw data. Please contact alina.lysykh@distancematrix.ai for help \n')
    exit=input("press close to exit")
    sys.exit()

with open(TOKEN_FILE_PATH, "r") as file:
    API_KEY = file.read()
    print(f'Your API KEY is: "{API_KEY}"')

with open(DATA_FILE_PATH) as f:
   count_data_rows = sum(1 for _ in f) - 1

def load_data():
    count_rows = 0
    data = []
    with open(DATA_FILE_PATH, newline='') as csvfile:
        rows = csv.reader(csvfile, delimiter=';', quotechar='"')
        for idx, row in enumerate(rows):
            if not idx:
                continue

            origin, destination, mode, traffic_model, departure_time = row

            data.append({
                "origin": "%s" % origin.replace('&', ' '),
                "destination": "%s" % destination.replace('&', ' '),
                "mode": "%s" % mode.replace('&', ' '),
                "traffic_model": "%s" % traffic_model.replace('&', ' '),
                "departure_time": "%s" % departure_time.replace('&', ' ')
            })
            count_rows+=1
        print(" \nTotal rows in CSV = %s \n" % (count_rows))
        return data

def make_request(base_url, api_key, origin, destination, mode, traffic_model, departure_time):
    url = "{base_url}/maps/api/distancematrix/json" \
          "?key={api_key}" \
          "&origins={origin}" \
          "&destinations={destination}" \
          "&mode={mode}" \
          "&traffic_model={traffic_model}" \
          "&departure_time={departure_time}".format(base_url=base_url,
                                                    api_key=api_key,
                                                    origin=origin,
                                                    destination=destination,
                                                    mode=mode,
                                                    traffic_model=traffic_model,
                                                    departure_time=departure_time)
    # logging.info("URL: %s" % url)
    result = requests.get(url)
    return result.json()

def main():
    data = load_data()
    n=0
    with open(RESULT_FILE_PATH, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(
            ['request_time', 'origin', 'destination', 'origin addresses', 'destination addresses', 'mode','traffic_model', 'Departure time', 'Distance (meters)', 'Distance (text)', 'Duration (seconds)', 'Duration (text)', 'Duration in traffic (seconds)', 'Duration in traffic (text)'])

        for t in data:
            time.sleep(0)
            request_time = datetime.datetime.now()
            dm_res = make_request(BASE_URL, API_KEY, t['origin'], t['destination'], t['mode'], t['traffic_model'], t['departure_time'])
       
            if dm_res['status'] == 'REQUEST_DENIED':
                if dm_res['error_message'] == 'The provided API key is invalid or token limit exceeded.':
                    print(dm_res['error_message'])
                    break
            n+=1
            try:
                dm_distance = dm_res['rows'][0]['elements'][0]['distance']
                dm_duration = dm_res['rows'][0]['elements'][0]['duration']
                dm_duration_in_traffic = dm_res['rows'][0]['elements'][0]['duration_in_traffic']
                origin_addresses = dm_res['origin_addresses']
                destination_addresses = dm_res['destination_addresses']

            except Exception as exc:
                print("%s) Please check if the address or coordinates in this line are correct" % n)
                # logging.error(str(exc))
                continue

            csvwriter.writerow([
                request_time,
                t['origin'],
                t['destination'],
                origin_addresses,    
                destination_addresses,
                t['mode'],
                t['traffic_model'],
                t['departure_time'],                
                dm_distance['value'],
                dm_distance['text'],
                dm_duration['value'],
                dm_duration['text'],
                dm_duration_in_traffic['value'],
                dm_duration_in_traffic['text'],        
            ])
            print("%s) %s -> %s : [dist: %s] <> [dur: %s]" % (n, t['origin'], t['destination'], dm_distance['text'], dm_duration_in_traffic['text']))

if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    main()

with open(RESULT_FILE_PATH) as f:
   count_result_rows = sum(1 for _ in f) - 1

print(f' \n{count_result_rows} / {count_data_rows} -> Calculated correctly')
print(' \nHelp is needed? Please contact alina.lysykh@distancematrix.ai \n')
exit=input("press close to exit")