import scrapy
from cryptoscraper.items import CryptoscraperItems
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
import time

class CryptospiderSpider(scrapy.Spider):
    name = "cryptospider"
    allowed_domains = ["chainabuse.com"]
    cryptos = [
        ["Bitcoin","BTC"],
        ["Ethereum","ETH"]
        ["Polygon","POLYGON"],
        ["Solana","SOL"],
        ["Litecoin","LITECOIN"],
        ["Tron","TRON"]]
    pages = {
        "BTC":1500,
        "ETH":1500,
        "POLYGON":60,
        "SOL":45,
        "LITECOIN":25,
        "TRON":50
        }
    

    def __init__(self, *args, **kwargs):
        super(CryptospiderSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        # chrome_options.add_argument("--headless") 
        chrome_options.add_argument(r"user-data-dir=C:\Users\US593\OneDrive\Desktop\user_data")   # chrome profile path  
        chrome_options.add_argument("--profile-directory=Default")   # profile directory
        chrome_options.add_argument("--remote-debugging-pipe")
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.seen_addresses = set()  
        self.prev_html = ""  

    def start_requests(self):
        for crypto in self.cryptos:
            name, symbol = crypto
            count = 0
            for page in range(self.pages[symbol]):
                # url = f"https://www.chainabuse.com/chain/{symbol}?page={page}"
                url = f"https://www.chainabuse.com/chain/{symbol}?page={page}&sort=most-comments"
                count+=1
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    meta={'crypto_name': name, 'page': page, 'count':count}
                )

    def parse(self, response):
        crypto_name = response.meta.get('crypto_name')
        page = response.meta.get('page')
        count = response.meta.get('count')
        url = response.url
        self.driver.get(url)
        if count==1:
            time.sleep(45)
        
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.create-ScamReportCard'))
            )
        except Exception as e:
            self.logger.error(f"Error waiting for page load on {url}: {e}")
            return

        html = self.driver.page_source

        if html == self.prev_html:
            self.logger.info(f"Page {page} for {crypto_name} is identical to the previous one, skipping.")
            return
        self.prev_html = html  

        response = HtmlResponse(url=url, body=html, encoding='utf-8')

        containers = response.css("div.create-ScamReportCard")
        for container in containers:
            try:
                flagging_reason = container.css('p.create-Text.type-body-lg-heavy.create-ScamReportCard__category-label::text').get()
                crypto_address = container.css(f'img[alt^="{crypto_name}"] + div.create-ResponsiveAddress .create-ResponsiveAddress__text::text').get()
                if crypto_address in self.seen_addresses:
                    continue
                self.seen_addresses.add(crypto_address)

                crypto_items = CryptoscraperItems()
                crypto_items['crypto_name'] = crypto_name
                crypto_items['flagging_reason'] = flagging_reason
                crypto_items['crypto_address'] = crypto_address

                yield crypto_items
            except Exception as e:
                self.logger.error(f"Error parsing item on page {page} for {crypto_name}: {e}")

    def closed(self, reason):
        self.driver.quit()


