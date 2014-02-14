import time
from app import Adapter, Logger

steps = ['sms', 'Kampala', '23', 'M', 'Kampala']


class Load(object):
    def __init__(self, username, password, url):
        self.adapter = Adapter(username, password,
                               url)

    def process(self, number='90'):
        registered = self.adapter.number_exists(number)
        Logger.log("number registered %s " % registered)
        count = 0
        current_poll = self.adapter.get_current_poll(number)
        while (current_poll):
            Logger.log(current_poll)
            # print current_poll["question"]
            if current_poll['type'] != 'none':
                user_response = steps[count]
                count += 1
                post_response = self.adapter.respond_to_poll(number, current_poll, user_response)
                Logger.log(post_response)
                # print(post_response["result"]["response"])
            current_poll = self.adapter.get_current_poll(number)

    def start(self):
        user_count = int(self.get_input("User Count :"))
        for n in range(0, user_count):
            number = "%s%s" % (str(time.time()), str(n))
            number = number.replace(".", "")
            # print(".")
            self.process(number)

    def get_input(self, prompt):
        return raw_input(prompt)


if __name__ == "__main__":
    app = Load("test", "nakulabye", "http://2.2.2.2/api/v1/ureporters")
    app.start()