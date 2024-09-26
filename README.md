# flagged-crypto-scraping

## Introduction
This project involves the collection of cryptocurrency addresses flagged for involvement in activities such as dark web operations, scams, hacking, and other malicious activities. The primary focus is on major cryptocurrencies including Bitcoin, Ethereum, Litecoin, Tron, Solana, and any other significant ones where possible. The collected data will be used for transaction pre-screening to identify and mitigate risks associated with flagged addresses before processing transactions.

## Data Source
**Chainabuse.com**: Chainabuse.com is a community-driven platform that features reported and flagged cryptocurrency addresses associated with scams, fraud, hacking, and other malicious activities. Users can report suspicious addresses and track flagged crypto addresses to stay informed and avoid potential threats.

## Data Collection Process
- **Tools Used**: Scrapy, Selenium
- **Process**: The data collection involved analyzing the CSS used on Chainabuse.com to create CSS selectors for data extraction. Scrapy was used to extract content from the pages, while Selenium was employed to navigate through the pages as Chainabuse.com is a JavaScript-driven, dynamic website.
- **Data Preprocessing**: The data underwent cleaning through pipelines to remove duplicates and ensure the uniqueness of addresses. This step was crucial to maintain the integrity and reliability of the dataset.

## Data Description
The dataset consists of the following columns:
- `crypto_address`: The cryptocurrency address that has been flagged.
- `crypto_name`: The name of the cryptocurrency, which can be one of the following categories:
  - Bitcoin
  - Ethereum
  - Polygon
  - Solana
  - Litecoin
  - Tron
- `flagging_reason`: The reason for the flagging, which can be one of the following categories:
  - Blackmail Scam
  - Sextortion Scam
  - Ransomware
  - Other
  - Romance Scam
  - Phishing Scam
  - Hacking
  - Pigbutchering Scam
  - Fake Project Scam
  - Impersonation Scam
  - Fake Returns Scam
  - SIM Swap Scam
  - Rug Pull Scam
  - Donation Impersonation Scam
  - Contract Exploit Scam
  - NFT Airdrop Scam
  - Investment Scam

## Scraper Usage 
1. Ensure that chromedriver is set up on your system according to your chrome version.
2. Clone the repository:
   ```
   git clone https://github.com/umairsiddique3171/multi-lang-invoice-data-extractor.git
   cd multi-lang-invoice-data-extractor
   ```
3. Create and activate a virtual environment:
   ```
   python -m venv env
   .\env\Scripts\activate
   ```
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
5. If you prefer to use **incognito mode (recommended)**, no changes are necessary. However, if you wish to use your Chrome profile, update the **config.yaml** file with the path to your profile, which you can find by entering **chrome://version/** in the address bar. Additionally, uncomment the following lines in **cryptospider.py**:
   ```
   # chrome_options.add_argument("incognito")    # using incognito
   chrome_options.add_argument(f"user-data-dir={utils.profile_directory}")     # chrome profile directory 
   chrome_options.add_argument(f"--profile-directory={utils.profile_name}")      # chrome profile name
   ```
   Using your standard profile for scraping may cause conflicts due to the profile's port being in use. It's recommended to copy the profile you want to use into a different folder, and then use that copy for scraping. This way, the profile will always be available for use without conflicts. Therefore, it's better to use incognito mode so you don't have to deal with these issues.
6. Add the values for the number of pages to be scraped for the corresponding cryptocurrencies in the config.yaml file.
7. Run the scraper:
   ```
   cd cryptoscraper/cryptoscraper/spiders
   scrapy crawl cryptospider -o data.csv
   ```

## License
This project is licensed under the [MIT License](https://github.com/umairsiddique3171/flagged-crypto-scraping/blob/main/LICENSE).

## Author 
[@umairsiddique3171](https://github.com/umairsiddique3171)
