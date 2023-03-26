from uuid import uuid4
from dataclasses import dataclass, asdict
from datetime import datetime
from sqlalchemy.orm import registry, Session
from sqlalchemy import Table, Column, String, DateTime
from sqlalchemy.engine import create_engine
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import IntegrityError
DB_NAME = 'TEST.db'

@dataclass
class Record:
    primary_key: str
    info: str
    start_time: datetime
    end_time: datetime = datetime.now()


mapper_registry = registry()

record_table = Table(
    "record",
    mapper_registry.metadata,
    Column("primary_key", String, primary_key=True),
    Column("info", String),
    Column("start_time", DateTime),
    Column("end_time", DateTime),
)

mapper_registry.map_imperatively(Record, record_table)


class NotFoundException(Exception):
    pass


class DuplicatedPrimaryKeyException(Exception):
    pass


class TableClient:
    def __init__(self, class_: type, in_memory: bool = False, echo: bool = True):
        db_name = ':memory:' if in_memory else DB_NAME
        self._engine = create_engine(f'sqlite:///{db_name}', echo=echo)   # Sqlite in memory
        self._class = class_
        mapper_registry.metadata.create_all(self._engine) 
    
    def get(self, primary_key):
        with Session(self._engine) as session:
            result = session.get(self._class, primary_key)
        
        if result is None:
            raise NotFoundException(f'Entity with primary key \"{primary_key}\" not found.')

        return result

    def insert(self, entity):
        with Session(self._engine) as session:
            try:
                session.add(entity)
                session.commit()
            except IntegrityError as ex:
                raise DuplicatedPrimaryKeyException() from ex
    
    def upsert(self, entity):
        with Session(self._engine) as session:
            session.merge(entity)
            session.commit()
    
    def list_all(self):
        with Session(self._engine) as session:
            return session.query(self._class).all()


def main():
    table_client = TableClient(Record, in_memory=False, echo=False)
    primary_key = str(uuid4())
    try:
        record = table_client.get(primary_key)
    except NotFoundException:
        print('Not found!')

    record = Record(primary_key, 'info', datetime.now())
    print(f'Record = {record}')
   
    # Insert.
    table_client.insert(record)
    print('Insert first time succeeded!')

    # Insert again with the same instance.
    # No exception will be thrown
    table_client.insert(record)
    print('Insert same instance succeeded!')

    # Insert again with a new instance with same primary key.
    # Expect to fail due to primary key conflict
    record2 = Record(primary_key, 'info_new', datetime.now())
    try:
        table_client.insert(record2)
    except DuplicatedPrimaryKeyException:
        print('Failed to insert due to duplicated primary key!')
        print('Insert different instance same primary key failed!')

    # Upsert with same primary key. Succeed.
    table_client.upsert(record2)
    print('Upsert succeeded!')
    new_record = table_client.get(primary_key)
    print(f'Retrieved entity type = {type(new_record)}; value = {new_record}')

    # Upsert a new primary key. Succeed.
    key_2 = str(uuid4())
    record3 = Record(key_2, 'info', datetime.now())
    table_client.upsert(record3)
    new_record = table_client.get(key_2)
    print(f'Retrieved entity type = {type(new_record)}; value = {new_record}')

    # Insert a nullable. Succeed
    key_4 = str(uuid4())
    record4 = Record(key_4, None, datetime.now())
    table_client.insert(record4)
    new_record = table_client.get(key_4)
    print(f'value = {new_record}')

    # # List all.
    results = table_client.list_all()
    for r in results:
        print(f'Row = {r}')


if __name__ == '__main__':
    main()