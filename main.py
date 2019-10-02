#!/usr/bin/env python3
import speedtest
import time
import json
import jsonpickle
from datetime import datetime


def main():
    while True:
        servers = []
        threads = None
        # If you want to use a single threaded test
        # threads = 1

        s = speedtest.Speedtest()
        s.get_servers(servers)
        s.get_best_server()
        print("Starting Download Test")
        s.download(threads=threads)
        print("Starting Upload Test")
        s.upload(threads=threads)
        write_results(s.results)
        print('Test Results:\nDownload: {}\nUpload: {}'.format(s.results.download,s.results.upload))
        print("Sleeping 10 Minutes Now")
        time.sleep(600)

def write_results(results):
    file_name = datetime.now().strftime('%m-%d_%H%M%S.json')
    with open('./results/{}'.format(file_name),mode='w') as f:
        f.write('{}'.format(jsonpickle.encode(results)))


if __name__ == '__main__':
    main()