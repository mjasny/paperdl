import requests
import re


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}

    

class Downloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def set_proxy(self, proxy):
        self.session.proxies.update(proxy.get_proxies())


    def get(self, url, save=True, fname=None):
        # if save=True -> return filename, else bytes

        r = self.session.get(url)
        print(f'[{r.status_code}] {r.url}')

        if not r.headers['content-type'].startswith('application/pdf'):
            raise Exception(f'ACM/IEEE No access? Try to use --sshhost. Resolved to: {r.url}')
        
        if save:
            fname = self.__get_filename(r) if fname is None else fname
            with open(fname, 'wb') as f:
                f.write(r.content)
            return fname
        
        return r.content


    def __get_filename(self, r):
        cd = r.headers.get('content-disposition')
        fname = re.findall('filename\*?=([^;]+)', cd, flags=re.IGNORECASE)
        return fname[0].strip().strip('"')
