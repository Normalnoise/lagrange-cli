import os
import requests

from swan.common import get_dir_data, COMMITS, FILES, LAGRANGE_API_URL, get_config, STATUS_200_OK
from swan.config import get_api_token

#get hash of latest (most recent) commit
def get_latest_commit(data, cwd):
    latest_commit = None
    cwd_commits = data[cwd][COMMITS]

    for commit in cwd_commits:
        if latest_commit is None or cwd_commits[latest_commit]["CreatedAt"] < cwd_commits[commit]["CreatedAt"]:
            latest_commit = commit

    return latest_commit

def push(dataset_name):
    api_token = get_api_token()
    if api_token == None:
        print("Please set your api token with \"swan config --api-token <YOUR_TOKEN>\"")
        return

    cwd = os.getcwd()
    data = get_dir_data(cwd)

    latest_commit = get_latest_commit(data, cwd)
    files = data[cwd][COMMITS][latest_commit][FILES]

    files_data = []
    for filename in files:
        with open(filename, 'rb') as f:
            files_data.append(('file', (filename, f.read())))
    
    print("Uploading files to dataset...")
    res = requests.put(
        LAGRANGE_API_URL + "/datasets/" + dataset_name + "/files", 
        files=files_data,
        headers = {"Authorization" : "Bearer " + api_token}
        )

    if res.status_code != STATUS_200_OK:
        print(f"An error occured when pushing the files. Status code {res.status_code}")