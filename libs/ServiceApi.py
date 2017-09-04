import requests


class ServiceApi():
    def __init__(self,service_api_url):
        self.service_api_url = service_api_url

    def put_data(self, body):
        response = requests.put(self.service_api_url, data=body)
        return response.text

    def post_data(self, body):
        response = requests.post(self.service_api_url, data=body)
        return response.json()

    def check_data_exist(self, params):
        query_data = requests.get(self.service_api_url, params=params)
        #print query_data.text
        if eval(query_data.text)["data"]:
            return True
        else:
            return False

    def query_data(self, params):
        query_data = requests.get(self.service_api_url, params=params)
        print(query_data.json())
        return query_data.json()

    def query_id(self, params):
        query_data = requests.get(self.service_api_url, params=params)
        #print(query_data.text)
        repo_id = eval(query_data.text)["data"]["id"]
        return repo_id