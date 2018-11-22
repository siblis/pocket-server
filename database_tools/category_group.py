from database_tools.alchemy import CCategoryGroup
from sqlalchemy.orm import sessionmaker


def add_category(engine):

    Session = sessionmaker(bind=engine)
    session = Session()

    session.add_all([CCategoryGroup(category_name='Single'),
                     CCategoryGroup(category_name='Multi')])
    session.commit()
