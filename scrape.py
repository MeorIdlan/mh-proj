from playwright.sync_api import sync_playwright, TimeoutError, expect
import redis
import json

class cacheSetError(Exception):
    def __init__(self, code, message='Something went wrong when setting new cache data.') -> None:
        self.code = code
        self.message = message
        super().__init__(self.message)

class Scraper:
    def __init__(self):
        self.cache = redis.Redis(host='localhost', port=6379, db=0)
        self.ttl = 300     # cache ttl at 30 minutes (1800), 5 mins for debug (300)
        
    def scrape_subway_site(self, query=None):
        with sync_playwright() as p:
            # start browser and create new page
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            # go to url
            page.goto('https://subway.com.my/find-a-subway')
            all_locations_list = []
            try:
                # wait for page load
                page.locator('#t3-content').wait_for()
                
                # get all locations and extract latitude longitude in a list
                if (query is None):
                    all_locations = page.locator('.fp_listitem').all()
                    all_locations_list = [(float(loc.get_attribute('data-latitude')),float(loc.get_attribute('data-longitude'))) for loc in all_locations]
                else:
                    # setup error dialog handling
                    errFound = False
                    def handleDialogError(dialog):
                        nonlocal errFound
                        errFound = True
                        dialog.dismiss()
                    
                    # enter specific location on search bar and click search
                    page.locator('#fp_searchAddress').fill(query)
                    page.once('dialog', handleDialogError)
                    try:
                        with page.expect_event('dialog',timeout=1000) as event_info:
                            page.locator('#fp_searchAddressBtn').click()
                    except TimeoutError:
                        # if no error dialog, move on with script
                        pass
                    
                    if not errFound:
                        all_locations = page.locator('.fp_listitem').all()
                        
                        def checkCSS(loc):
                            try:
                                expect(loc).not_to_have_css('display','none',timeout=5)
                                return True
                            except AssertionError:
                                return False
                        all_locations_list = [(float(loc.get_attribute('data-latitude')),float(loc.get_attribute('data-longitude'))) for loc in all_locations if checkCSS(loc)]
                    else:
                        return -2
            except TimeoutError as e:
                print(f'Timeout error: {e}')
                return -1
            
            # set cache
            if (query is None):
                self.cache.set('all', json.dumps(all_locations_list), ex=self.ttl)
            else:
                self.cache.set(f"{query.replace(' ','').lower()}", json.dumps(all_locations_list), ex=self.ttl)
            return 1
            
    # todo get restaurant details
    def getLocations(self, query=None):
        # check search query in cache
        if query is None:
            cached_loc = self.cache.get('all')
        else:
            cached_loc = self.cache.get(f"{query.replace(' ','').lower()}")
          
        # if cache exists return data, else do scrape and then return 
        if cached_loc:
            return json.loads(cached_loc)
        else:
            try:
                result = self.scrape_subway_site(query=query)
                if result < 0:
                    raise cacheSetError(code=result)
            except cacheSetError as e:
                print(f'Error code: {e.code}')
                return None
                
            if query is None:
                return json.loads(self.cache.get('all'))
            else:
                return json.loads(self.cache.get(f"{query.replace(' ','').lower()}"))
    
if __name__ == '__main__':
    scraper = Scraper()
    # scraper.getLocations()
    print(scraper.getLocations('penang'))
    print(len(scraper.getLocations('penang')))