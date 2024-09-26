import os 
import yaml
import math


script_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.abspath(os.path.join(script_dir, '..', '..','..', 'config.yaml'))
with open(config_file_path, 'r') as file:
    config = yaml.safe_load(file)

profile_directory = config['PROFILE_DIRECTORY']
profile_name = config['PROFILE_NAME']


def load_crypto_config():
    cryptos = []
    pages = {}

    crypto_names = {
        "BTC": "Bitcoin",
        "ETH": "Ethereum",
        "POLYGON": "Polygon",
        "SOL": "Solana",
        "LITECOIN": "Litecoin",
        "TRON": "Tron"
    }

    for symbol, num_pages in config['CRYPTO'].items():

        num_pages = abs(num_pages) 
        num_pages = math.floor(num_pages)  

        if num_pages > 0:
            cryptos.append([crypto_names[symbol], symbol])
            pages[symbol] = num_pages

    return cryptos, pages



# testing 
if __name__ == "__main__":
    cryptos, pages = load_crypto_config()
    print("Profile Directory", config['PROFILE_DIRECTORY'])
    print("Profile_Name", config['PROFILE_NAME'])
    print("Cryptos:", cryptos)
    print("Pages:", pages)
