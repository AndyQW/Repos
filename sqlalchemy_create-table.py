from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from sqlalchemy import Column, MetaData, Table, create_engine
from sqlalchemy import String, Integer, Float, BigInteger, DateTime

from sqlalchemy.schema import DropTable, CreateTable
from sqlalchemy.orm import scoped_session, sessionmaker


from contextlib import contextmanager


@contextmanager
def Session(*args, **kwargs):
    Session = scoped_session(sessionmaker(
        bind=create_engine(*args, **kwargs)))

    try:
        session = Session()
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def main():
    DB = 'postgresql:///example'

    TABLE_SPEC = [
        ('id', BigInteger),
        ('name', String),
        ('t_modified', DateTime),
        ('whatever', String)
    ]

    TABLE_NAME = 'sample_table'

    columns = [Column(n, t) for n, t in TABLE_SPEC]
    table = Table(TABLE_NAME, MetaData(), *columns)

    with Session(DB, echo=True) as s:
        # this is just here to make the script idempotent
        s.execute('drop table if exists {}'.format(TABLE_NAME))

        table_creation_sql = CreateTable(table)
        s.execute(table_creation_sql)


if __name__ == '__main__':
    main()
