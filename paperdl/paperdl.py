#!/usr/bin/env python3

import paramiko
import requests
import re
import os
import argparse
import itertools
import sys


ASCII_LOGO = """\
  _____                      _____  _      
 |  __ \                    |  __ \| |     
 | |__) |_ _ _ __   ___ _ __| |  | | |     
 |  ___/ _` | '_ \ / _ \ '__| |  | | |     
 | |  | (_| | |_) |  __/ |  | |__| | |____ 
 |_|   \__,_| .__/ \___|_|  |_____/|______|
            | |                            
            |_|                            
"""


SOCKS_HOST = '127.0.0.1'
SOCKS_PORT = 34579


def main():
    print(ASCII_LOGO)

    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='SSH Host to use for download')
    parser.add_argument(
        '--interactive', action='store_true', help='Interactive mode, script will ask for urls')
    parser.add_argument('urls', nargs='*', help='List of IEEE/ACM urls')
    args = parser.parse_args()

    urls = args.urls
    if args.interactive:
        def read_urls():
            try:
                while True:
                    url = input('Enter URL: ')
                    yield url
            except KeyboardInterrupt:
                pass

        urls = itertools.chain(urls, read_urls())

    if not urls:
        print('No URLs specified')
        sys.exit(1)

    ssh_config = paramiko.SSHConfig()
    user_config_file = os.path.expanduser('~/.ssh/config')
    if os.path.exists(user_config_file):
        with open(user_config_file) as f:
            ssh_config.parse(f)

    user_config = ssh_config.lookup(args.host)
    cfg = {
        'hostname': user_config.get('hostname', args.host),
        'port': user_config.get('port'),
        'username': user_config.get('user'),
        'key_filename': user_config.get('identityfile')
    }
    cfg = {k: v for k, v in cfg.items() if v is not None}

    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    # print(cfg)
    ssh_client.connect(**cfg)

    proxy = ssh_client.open_socks_proxy(
        bind_address=SOCKS_HOST,
        port=SOCKS_PORT,
    )

    proxies = {
        'http': f'socks5://{SOCKS_HOST}:{SOCKS_PORT}',
        'https': f'socks5://{SOCKS_HOST}:{SOCKS_PORT}',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }

    session = requests.Session()
    session.proxies.update(proxies)
    session.headers.update(headers)

    for url in urls:
        try:
            article_no = re.match(
                r'https:\/\/ieeexplore\.ieee\.org\/document\/(\d+)', url).group(1)
            print(f'Extracted: {article_no}')
            pdf_url = f'https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&isnumber=&arnumber={article_no}'

        except:
            doi = re.match(
                r'https:\/\/dl\.acm\.org\/doi\/abs\/(10\.\d{4,9}\/[-._;()\/:A-Z0-9]+)', url).group(1)
            print(f'Extracted: {doi}')
            pdf_url = f'https://dl.acm.org/doi/pdf/{doi}'

        r = session.get(pdf_url)
        print(f'[{r.status_code}] {r.url}')

        def get_filename(r):
            cd = r.headers.get('content-disposition')
            fname = re.findall('filename\*?=([^;]+)', cd, flags=re.IGNORECASE)
            return fname[0].strip().strip('"')

        fname = get_filename(r)
        with open(fname, 'wb') as f:
            f.write(r.content)

        print(f'Downloaded to: {fname}')

    proxy.close()
    ssh_client.close()
