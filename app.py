import json
import datetime
import requests


class Logger(object):
    @staticmethod
    def log(data, level="INFO"):
        #print("[%s] %s:> %s" % (level, datetime.datetime.now(), data))
        pass

class HttpClient(object):
    def __init__(self, username, password, base_url):
        self.username = username
        self.password = password
        self.base_url = base_url

    def get(self, param):
        response = requests.get(self.build_url(param), auth=(self.username, self.password))
        Logger.log(response)
        return response

    def build_url(self, param):
        url = "%s%s" % (self.base_url, param)
        Logger.log(url)
        return url

    def get_json(self, param):
        response = self.get(param)
        json_data = json.loads(response.content)
        return json_data

    def post_json(self, url, data):
        response = self.post(url, data=data)
        json_data = json.loads(response.content)
        return json_data

    def post(self, path, data):
        response = requests.post(self.build_url(path), data=data, auth=(self.username, self.password))
        Logger.log(response)
        return response


class Adapter(object):
    def __init__(self, username, password, url):
        self.http_client = HttpClient(username, password, url)

    def build_path(self, number, backend, path=""):
        return "/%s/%s%s" % (backend, number, path)

    def number_exists(self, number):
        response = self.http_client.get_json(self.build_path(number, "console"))
        return response["success"]

    def get_current_poll(self, number):
        response = self.http_client.get_json(self.build_path(number, "console", "/polls/current"))
        Logger.log(response)
        return response['poll']

    def respond_to_poll(self, number, poll, user_response):
        data = {}
        data["response"] = user_response
        response = self.http_client.post_json(self.build_path(number, "console", "/poll/%s/responses" % poll["id"]),
                                              json.dumps(data))
        return response

#
# class Fetcher(object):
#     def __init__(self, number):
#         self.number = number
#
#     def

class App(object):
    def __init__(self, username, password, url):
        self.adapter = Adapter(username, password,
                               url)

    def start(self):
        number = self.get_input("Phone Number :")
        registered = self.adapter.number_exists(number)
        Logger.log("number registered %s " % registered)

        current_poll = self.adapter.get_current_poll(number)
        while (current_poll):
            Logger.log(current_poll)
            # print current_poll["question"]
            if current_poll['type'] != 'none':
                user_response = self.get_input(": ")
                post_response = self.adapter.respond_to_poll(number, current_poll, user_response)
                Logger.log(post_response)
                print(post_response["result"]["response"])
            current_poll = self.adapter.get_current_poll(number)

    def get_input(self, prompt):
        return raw_input(prompt)


if __name__ == "__main__":
    app = App("test", "nakulabye", "http://2.2.2.2/api/v1/ureporters")
    app.start()
