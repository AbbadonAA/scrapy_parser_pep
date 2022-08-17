import csv
from collections import Counter
from datetime import datetime as dt
from pathlib import Path

BASE_DIR = Path(__file__).parents[1]
COUNT_STATUS = Counter()


class PepParsePipeline:

    def __init__(self) -> None:
        self.results_dir = BASE_DIR / 'results'
        self.results_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        time = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f'status_summary_{time}.csv'
        file_path = self.results_dir / file_name
        self.file = csv.writer(open(file_path, 'w'))
        self.file.writerow(['Статус', 'Количество'])

    def close_spider(self, spider):
        COUNT_STATUS['Total'] = sum(COUNT_STATUS.values())
        self.file.writerows(COUNT_STATUS.items())

    def process_item(self, item, spider):
        COUNT_STATUS[item['status']] += 1
        return item
