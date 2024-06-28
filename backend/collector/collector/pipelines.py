from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import psycopg2


class SavingToPostgresqlPipeline:

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        conn = psycopg2.connect(
                # host='collector',
                host='localhost',
                user='collector',
                password='c011lect',
                database='ingredients',
                port=5432,
                )
        self.conn = conn
        self.cursor = conn.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        keys = ['shop', 'name', 'volume', 'volume_unit', 'price', 'price_unit', 'img', 'description']
        holders = ','.join(['%s']*len(keys))
        values = tuple([item[field] for field in keys])
        keys = ','.join(keys)
        self.cursor.execute(f"""
        INSERT INTO products({keys}) VALUES({holders}) ON CONFLICT DO NOTHING""", values
                            )
        self.conn.commit()


class DuplicatesPipeline:

    def __init__(self):
        self.names_seen = dict()

    def process_item(self, item, spider):
        if spider.name not in self.names_seen.keys():
            self.names_seen[spider.name] = set()
        adapter = ItemAdapter(item)
        if adapter['name'] in self.names_seen[spider.name]:  # нам не нужно, чтобы один и тот же паук смотрел тот же товар
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.names_seen[spider.name].add(adapter['name'])
            return item
