import re
from ..exceptions import NotSupportedURL
from ..utils import AttrDict
from  ..downloaders import RequestsDownloader

class IEEEURLGenerator:
    @staticmethod
    def extract(url):
        m = re.match(
            r'https:\/\/ieeexplore\.ieee\.org\/document\/(\d+)', url)
        if not m:
            raise NotSupportedURL()
        pdf_url = f'https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&isnumber=&arnumber={m.group(1)}'
        return AttrDict(url=pdf_url)
    

    @staticmethod
    def get_dl():
        return RequestsDownloader()