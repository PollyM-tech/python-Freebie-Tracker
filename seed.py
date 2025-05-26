#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Clearing existing data
    session.query(Freebie).delete()
    session.query(Dev).delete()
    session.query(Company).delete()
    session.commit()

    company1 = Company(name="TechPolly", founding_year=2023)
    company2 = Company(name="Lintech", founding_year=2020)
    session.add_all([company1, company2])

    dev1 = Dev(name="Kylian")
    dev2 = Dev(name="Daniel")
    session.add_all([dev1, dev2])

    freebie1 = Freebie(item_name="backpack", value=10, dev=dev1, company=company1)
    freebie2 = Freebie(item_name="waterbottle", value=4, dev=dev1, company=company2)
    freebie3 = Freebie(item_name="Mug", value=8, dev=dev2, company=company1)
    session.add_all([freebie1, freebie2, freebie3])

    session.commit()