#!/usr/bin/env python3


import argparse
import itertools
import sys

from .ssh_proxy import SSHProxy
from .downloader import Downloader
from .sites import SITES
from .exceptions import NotSupportedURL



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






def main():
    print(ASCII_LOGO)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--sshhost', required=False, help='SSH Host to use for download. Needed for constitutional access.')
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
            except (KeyboardInterrupt, EOFError):
                pass

        urls = itertools.chain(urls, read_urls())

    if not urls:
        print('No URLs specified')
        sys.exit(1)



    dl = Downloader()

    if args.sshhost:
        ssh_proxy = SSHProxy(args.sshhost)
        dl.set_proxy(ssh_proxy)
        

    
    for url in urls:
        for site in SITES:
            try:
                pdf_info = site.extract(url)
                print(f'Extracted URL: {pdf_info.url}')
                fname = dl.get(**pdf_info, save=True)
                print(f'Downloaded to: {fname}')
                break
            except NotSupportedURL:
                continue
            except Exception as e:
                raise e



