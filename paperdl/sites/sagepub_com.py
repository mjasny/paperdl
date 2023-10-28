import re
from ..utils import AttrDict
from ..exceptions import NotSupportedURL
from ..downloaders import PlaywrightDownloader


class SagePubGenerator:
    @staticmethod
    def extract(url):
        m = re.match(
            r'https:\/\/journals\.sagepub\.com\/doi\/(\d{2}\.\d{4}\/\d+)', url)
        if not m:
            raise NotSupportedURL()
        
        doi = m.group(1) # 10.1177/08850666221116594
        pdf_url = f'https://journals.sagepub.com/doi/pdf/{doi}?download=true'
        return AttrDict(url=pdf_url)

    @staticmethod
    def get_dl():
        return PlaywrightDownloader()