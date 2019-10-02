#!/usr/bin/env python3
import speedtest
import time
import json
import argparse
import os
from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from gooey import Gooey, GooeyParser

@dataclass
class Client:
    ispdlavg: Optional[int] = None
    ispulavg: Optional[int] = None
    loggedin: Optional[int] = None
    rating: Optional[int] = None
    country: Optional[str] = None
    ip: Optional[str] = None
    isp: Optional[str] = None
    isprating: Optional[str] = None
    lat: Optional[str] = None
    lon: Optional[str] = None


@dataclass
class Server:
    id: Optional[int] = None
    cc: Optional[str] = None
    country: Optional[str] = None
    d: Optional[float] = None
    host: Optional[str] = None
    lat: Optional[str] = None
    latency: Optional[float] = None
    lon: Optional[str] = None
    name: Optional[str] = None
    sponsor: Optional[str] = None
    url: Optional[str] = None


@dataclass
class SpeedtestResults:
    bytes_received: Optional[int] = None
    bytes_sent: Optional[int] = None
    client: Optional[Client] = None
    download: Optional[str] = None
    ping: Optional[float] = None
    server: Optional[Server] = None
    timestamp: Optional[datetime] = None
    upload: Optional[str] = None

    def new(self,client,download,ping,server,timestamp,upload,bytes_received,bytes_sent):
        self.bytes_received = bytes_received
        self.bytes_sent = bytes_sent
        self.client = client
        self.download = download
        self.ping = ping
        self.server = server
        self.timestamp = timestamp
        self.upload = upload

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


@Gooey(dump_build_config=True, program_name="Speedtest Application")
def main():
    desc = "Simple Speedtest Application"
    parser = GooeyParser(description=desc)
    parser.add_argument('-o', '--Output_Directory', help="Directory to store output", widget="DirChooser", default=os.getcwd())
    parser.add_argument('-f', '--Format', widget="Dropdown", nargs="*", choices=['kBit/s', 'mBit/s'], default='mBit/s')
    args = parser.parse_args()

    while True:
        servers = []
        threads = None

        s = speedtest.Speedtest()
        s.get_servers(servers)
        s.get_best_server()
        print("Starting Download Test")
        s.download(threads=threads)
        print("Starting Upload Test")
        s.upload(threads=threads)

        results = SpeedtestResults()

        upload = f"{s.results.upload} Bits/s"
        download = f"{s.results.download} Bits/s"

        if args.Format == ['mBit/s']:
            upload = f"{str(s.results.upload / 1_000_000)} mBit/s"
            download = f"{str(s.results.download / 1_000_000)} mBit/s"
        if args.Format == ['kBit/s']:
            upload = f"{str(s.results.upload / 1_000)} kBit/s"
            download = f"{str(s.results.download / 1_000)} kBit/s"


        results.new(
            client=s.results.client,
            download=download,
            ping=s.results.ping,
            server=s.results.server,
            timestamp=s.results.timestamp,
            upload=upload,
            bytes_received=s.results.bytes_received,
            bytes_sent=s.results.bytes_sent
        )

        write_results(results, args)
        print(f"Test Results:\nDownload: {download}\nUpload: {upload}")
        print("Sleeping 10 Minutes Now")
        time.sleep(600)


def write_results(results, args):
    file_path = args.Output_Directory
    file_name = datetime.now().strftime('%m-%d_%H%M%S.json')

    if file_path == os.getcwd():
        if not os.path.exists(f"{file_path}/results"):
            os.mkdir(f"{file_path}/results")

        with open(f"{file_path}/results/{file_name}",mode='w') as f:
            f.write(results.to_JSON())
            print(f"Wrote results to: {file_path}/results/{file_name}")
    else:
        with open(f"{file_path}/{file_name}",mode='w') as f:
            f.write(results.to_JSON())
            print(f"Wrote results to: {file_path}/{file_name}")


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


if __name__ == '__main__':
    main()

# TODO: cleanup print statements to suit current system, round some speed results, dynamically determine suitable format for speed
