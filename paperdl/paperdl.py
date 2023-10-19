#!/usr/bin/env python3


import re
import argparse
import itertools
import sys

from .ssh_proxy import SSHProxy
from .downloader import Downloader
from .utils import AttrDict



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


class NotSupportedURL(Exception):
    pass

class IEEEURLGenerator:
    @staticmethod
    def extract(url):
        m = re.match(
            r'https:\/\/ieeexplore\.ieee\.org\/document\/(\d+)', url)
        if not m:
            raise NotSupportedURL()
        pdf_url = f'https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&isnumber=&arnumber={m.group(1)}'
        return AttrDict(url=pdf_url)

class ACMURLGenerator:
    @staticmethod
    def extract(url):
        m = re.match(
            r'https:\/\/dl\.acm\.org\/doi\/abs\/(10\.\d{4,9}\/[-._;()\/:A-Z0-9]+)', url)
        if not m:
            raise NotSupportedURL()
        pdf_url = f'https://dl.acm.org/doi/pdf/{m.group(1)}'
        return AttrDict(url=pdf_url)

class NEJMURLGenerator:
    @staticmethod
    def extract(url):
        m = re.match(
            r'https:\/\/www\.nejm\.org\/doi\/full/10.1056/([A-z0-9]+)', url)
        if not m:
            raise NotSupportedURL()
        
        fname = f'{m.group(1)}.pdf'
        pdf_url = f'https://mediacenteratypon.nejmgroup-production.org/{fname}'
        return AttrDict(url=pdf_url, fname=fname)



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
        

    generators = [IEEEURLGenerator, ACMURLGenerator, NEJMURLGenerator]
    
    for url in urls:
        for generator in generators:
            try:
                pdf_info = generator.extract(url)
                print(f'Extracted URL: {pdf_info.url}')
                fname = dl.get(**pdf_info, save=True)
                print(f'Downloaded to: {fname}')
                break
            except NotSupportedURL:
                continue
            except Exception as e:
                raise e



