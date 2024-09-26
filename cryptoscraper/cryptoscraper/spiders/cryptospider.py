import scrapy
from cryptoscraper.items import CryptoscraperItems
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from . import secret, utils
import time



class CryptospiderSpider(scrapy.Spider):
    name = "cryptospider"
    allowed_domains = ["chainabuse.com"]
    cryptos,page = utils.load_crypto_config()

    def __init__(self, *args, **kwargs):
        super(CryptospiderSpider, self).__init__(*args, **kwargs)

        chrome_options = Options()
        # chrome_options.add_argument("--headless")   # if u want to run in headless mode, then u can uncomment it.
        chrome_options.add_argument("incognito")    # using incognito
        # chrome_options.add_argument(f"user-data-dir={utils.profile_directory}")     # chrome profile directory 
        # chrome_options.add_argument(f"--profile-directory={utils.profile_name}")      # chrome profile name
        chrome_options.add_argument("--disable-gpu")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.seen_addresses = set()
        self.prev_html = ""

    def start_requests(self):
        self.login()        # login process automation
        time.sleep(2)
        for crypto in self.cryptos:         # scraping procedure after login
            name, symbol = crypto
            for page in range(self.pages[symbol]):
                url = f"https://www.chainabuse.com/chain/{symbol}?page={page}&sort=most-comments"
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    meta={'crypto_name': name, 'page': page}
                )


    def login(self):  # login functionality
        login_url = "https://www.chainabuse.com/api/auth/login?"
        self.driver.get(login_url)

        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.NAME, "username"))  
            )
            email_input = self.driver.find_element(By.NAME, "username")   
            email_input.send_keys(secret.EMAIL) 
            continue_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            continue_button.click()
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.NAME, "password"))  
            )
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(secret.PASSWORD)
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            while True:
                try:
                    WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.create-ProfileDropdown"))
                    )
                    self.logger.info("Login successful.")
                    break
                except:
                    self.logger.info("Waiting for login to complete.")
                    time.sleep(2)

        except Exception as e:
            self.logger.error(f"Error during login: {e}")


    def parse(self, response):
        crypto_name = response.meta.get('crypto_name')
        page = response.meta.get('page')
        url = response.url
        self.driver.get(url)

        try:
            WebDriverWait(self.driver, 15).until(
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
                flagging_reason = container.css(
                    'p.create-Text.type-body-lg-heavy.create-ScamReportCard__category-label::text').get()
                crypto_address = container.css(
                    f'img[alt^="{crypto_name}"] + div.create-ResponsiveAddress .create-ResponsiveAddress__text::text').get()
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