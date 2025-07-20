import json
from scrapy.exceptions import DropItem
from webcrawler.items import QuotesItem
import logging as log

class StreamingQuotesPipeline:

    def open_spider(self, spider):
        self.quotes_file = open('quotes.jsonl', 'w', encoding='utf-8')
        log.info("File opened")

    def close_spider(self, spider):
        self.quotes_file.close()
        log.info("File closed")

    def process_item(self, item, spider):
        log.info("Item processing")
        if isinstance(item, QuotesItem):
            if not item.get("title") or not item.get("author"):
                raise DropItem("Missing title or author in quote")
            line = json.dumps(dict(item), ensure_ascii=False)
            self.quotes_file.write(line + "\n")
            return item

        else:
            raise DropItem(f"Unknown item type: {type(item)}")
