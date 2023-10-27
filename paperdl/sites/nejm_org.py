import re
from ..utils import AttrDict
from ..exceptions import NotSupportedURL

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
