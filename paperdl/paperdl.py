#!/usr/bin/env python3


import argparse
import itertools
import sys

from .ssh_proxy import SSHProxy
from .socks5_proxy import Socks5Proxy
from .sites import SITES
from .exceptions import NotSupportedURL
from .utils import open_pdf



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
        '--socks5', required=False, help='Socks5 Proxy to use for download. Needed for constitutional access.')
    parser.add_argument(
        '--interactive', action='store_true', help='Interactive mode, script will ask for urls')
    parser.add_argument(
        '--autoopen', required=False, action='store_true', help='Automatically open pdf after download using system-viewer')
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


    proxy = None
    if args.sshhost:
        proxy = SSHProxy(args.sshhost)
    if args.socks5:
        proxy = Socks5Proxy(args.socks5)
        

    
    for url in urls:
        for site in SITES:
            try:
                pdf_info = site.extract(url)
                print(f'Extracted URL: {pdf_info.url}')
                dl = site.get_dl()
                if proxy:
                    dl.set_proxy(proxy)
                fname = dl.get(**pdf_info, save=True)
                print(f'Downloaded to: {fname}')
                if args.autoopen:
                    open_pdf(fname)
                break
            except NotSupportedURL:
                continue
            except Exception as e:
                raise e



if __name__ == '__main__':
    main()