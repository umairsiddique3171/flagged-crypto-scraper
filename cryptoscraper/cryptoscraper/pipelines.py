import scrapy
from itemadapter import ItemAdapter

class CryptoscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        for field_name, value in adapter.items():
            if value is None or str(value).strip() == "":
                spider.logger.info(f"Discarded item due to null or empty field: {field_name}")
                raise scrapy.exceptions.DropItem(f"Item has a null or empty field: {field_name}")
        
        crypto_address = adapter.get('crypto_address').strip()
        if len(crypto_address) < 15:
            spider.logger.info(f"Discarded item due to invalid crypto_address: {crypto_address}")
            raise scrapy.exceptions.DropItem(f"Crypto address {crypto_address} is invalid.")
        
        flagging_reason = adapter.get('flagging_reason').strip()
        if flagging_reason == 'Other Blackmail Scam':
            adapter['flagging_reason'] = 'Blackmail Scam'
        elif flagging_reason == 'Other:':
            adapter['flagging_reason'] = 'Other'
        elif flagging_reason == 'Hack - Other':
            adapter['flagging_reason'] = 'Hacking'
        elif flagging_reason == 'Other Investment Scam':
            adapter['flagging_reason'] = 'Investment Scam'

        spider.logger.info(f"Processed item with flagging_reason: {adapter['flagging_reason']}")
        
        return item

