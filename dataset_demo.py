import dataset
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Record:
    primary_key: str
    index_1: str
    index_2: str
    info: str
    start_time: datetime
    end_time: datetime = datetime.now()


def main():
    db = dataset.connect('sqlite:///:memory:')
    primary_key = 'primary_key'
    record = Record(primary_key, 'index-1', 'index-2', 'info', datetime.now())
    table = db.create_table('test_table', primary_id='primary_key', primary_type=db.types.string)
    # print(table.table)
    table.insert(asdict(record))
    table.create_index(['index_1'])
    table.create_index(['index_2'])
    print(table.columns)
    print(table.has_index(['index_1']))  # True
    print(table.has_index(['index_2']))  # True

if __name__ == '__main__':
    main()