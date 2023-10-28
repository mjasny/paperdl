
class Socks5Proxy:
    def __init__(self, proxy_url):
        self.proxy_url = proxy_url


    def get_proxies(self):
        return  {
            'http': f'socks5://{self.proxy_url}',
            'https': f'socks5://{self.proxy_url}',
        }