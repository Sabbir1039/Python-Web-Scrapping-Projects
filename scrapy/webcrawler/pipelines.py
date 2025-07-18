import json
from scrapy.exceptions import DropItem
from webcrawler.items import QuotesItem

class StreamingQuotesPipeline:

    def open_spider(self, spider):
        self.quotes_file = open('quotes.jsonl', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.quotes_file.close()

    def process_item(self, item, spider):
        if isinstance(item, QuotesItem):
            if not item.get("title") or not item.get("author"):
                raise DropItem("Missing title or author in quote")
            line = json.dumps(dict(item), ensure_ascii=False)
            self.quotes_file.write(line + "\n")
            return item

        else:
            raise DropItem(f"Unknown item type: {type(item)}")
