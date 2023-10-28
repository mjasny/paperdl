from playwright.sync_api import sync_playwright


class PlaywrightDownloader:
    def __init__(self):        
        self.playwright = sync_playwright().start()
        self.browser = None
        self.page = None
        self._proxy = None

    def _setup(self):
        self.browser = self.playwright.firefox.launch(
            proxy=self._proxy
        )
        self.page = self.browser.new_page()

    def set_proxy(self, proxy):
        self._proxy = {
            "server": proxy.get_proxies()['http'],
        }


    def get(self, url, save=True, fname=None):
        if self.browser is None:
            self._setup()
        assert(save==True)

        # Start waiting for the download
        with self.page.expect_download() as download_info:
            # Perform the action that initiates download
            try:
                self.page.goto(url)
            except Exception as e: # https://stackoverflow.com/questions/73652378/download-files-with-goto-in-playwright-python
                # print(e)
                pass
        download = download_info.value

        if fname is None:
            fname = download.suggested_filename
        download.save_as(fname)

        return fname


    def __get_filename(self, r):
        cd = r.headers.get('content-disposition')
        fname = re.findall('filename\*?=([^;]+)', cd, flags=re.IGNORECASE)
        return fname[0].strip().strip('"')



# with sync_playwright() as p:
#     browser = p.firefox.launch(
#         proxy={"server": "socks5://127.0.0.1:9052"},
#     )

#     page = browser.new_page()

#     url = 'https://journals.sagepub.com/doi/pdf/10.1177/08850666221116594?download=true'

#     # Start waiting for the download
#     with page.expect_download() as download_info:
#         # Perform the action that initiates download
#         try:
#             page.goto(url)
#         except Exception as e: # https://stackoverflow.com/questions/73652378/download-files-with-goto-in-playwright-python
#             # print(e)
#             pass
#     download = download_info.value

#     # Wait for the download process to complete and save the downloaded file somewhere
#     download.save_as(download.suggested_filename)
#     print(download.suggested_filename)

#     browser.close()

