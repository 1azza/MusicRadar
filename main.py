from struct import pack
from musicradar import Client
import json
import requests
import os
from multiprocessing.pool import ThreadPool as Pool
from pprint import pprint

PACK_FOLDER_LOCAL = 'D:\dev\python\Projects\MusicRadar'


def sync():
    client = Client()
    client.get_all_samples()
    print("Writing to json . . .")
    with open('data/radar_data.json', 'w') as handle:
        json.dump(client.samples, handle, indent=4)
    print("Success!")





def check():
    samples_owned = []
    for filename in os.listdir(PACK_FOLDER_LOCAL):
        name = filename
        samples_owned.append(name)
    return samples_owned

def download(url):
    local_filename = url.split('https://cdn.mos.musicradar.com/audio/samples/')[1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk:
                f.write(chunk)
    return local_filename

def compare(packs_owned):
    owned = []
    with open('data/radar_data.json', 'r') as handle:
        radar_data = json.load(handle)
        
    missing = []
    owned = {}
    for pack in packs_owned:
        pack = f'https://cdn.mos.musicradar.com/audio/samples/{pack}'
        owned[pack] = True
    for i in radar_data.keys():
        if owned.get(i) is None:
            missing.append(i)
    print(f'Owned {len(owned)} packs')
    print(f'Missing {len(missing)} packs')
            
            
    return missing
# sync()
owned = check()
missing = compare(owned)
# pprint(missing)
yn = input('Would you like to download the missing packs?  y/n')
if yn.upper() == 'Y':
    pool = Pool(2)
    for i in missing:
        print(f'Downloading from {i} . . .')
        pool.apply_async(download, (i,))
    pool.close()
    pool.join()
