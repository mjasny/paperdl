import re
from ..exceptions import NotSupportedURL
from ..utils import AttrDict
from ..downloaders import RequestsDownloader


class ACMURLGenerator:
    @staticmethod
    def extract(url):
        m = re.match(
            r'https:\/\/dl\.acm\.org\/doi\/abs\/(10\.\d{4,9}\/[-._;()\/:A-Z0-9]+)', url)
        if not m:
            raise NotSupportedURL()
        pdf_url = f'https://dl.acm.org/doi/pdf/{m.group(1)}'
        return AttrDict(url=pdf_url,)


    @staticmethod
    def get_dl():
        return RequestsDownloader()