import requests
import json


def load_json():
    with open('config.json') as json_file:
        data = json.load(json_file)
        return data


def authenticate(data):
    payload = {"grant_type": "refresh_token", "client_id": data['client_id'], "refresh_token": data['user_key']}
    payload = json.dumps(payload)
    url = data['url']
    headers = {
        'Content-Type': 'application/json',
        'X-UIPATH-TenantName': data['tenant_name']
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response = response.json()
    data['access_token'] = response['access_token']
    data['id_token'] = response['id_token']


def read_info(data):
    url = f"https://cloud.uipath.com/{data['account_name']}/{data['tenant_name']}"
    headers = {
        "Authorization": f"Bearer {data['access_token']}",
        'X-UIPATH-TenantName': data['tenant_name']
    }
    robots = requests.request("GET", url + "/orchestrator_/api/Stats/GetSessionsStats", headers=headers).json()
    robot_count = 0
    for robot in robots:
        robot_count += robot['count']

    jobs = requests.request("GET", url + "/orchestrator_/api/Stats/GetJobsStats", headers=headers).json()
    successful_jobs = jobs[0]['count']
    failed_jobs = jobs[1]['count']
    print("===============SUMARRY===============")
    print(f"Total number of robots: \t\t\t{robot_count}")
    print(f"Total number of successful jobs: \t{successful_jobs}")
    print(f"Total number of failed jobs: \t\t{failed_jobs}")


if __name__ == '__main__':
    data = load_json()
    authenticate(data)
    read_info(data)
