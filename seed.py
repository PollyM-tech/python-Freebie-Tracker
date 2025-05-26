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

    # Creating Companies
    company1 = Company(name="TechPolly", founding_year=2023)
    company2 = Company(name="Lintech", founding_year=2020)
    session.add_all([company1, company2])
    session.commit()

    # Creating Developers
    dev1 = Dev(name="Kylian")
    dev2 = Dev(name="Daniel")
    session.add_all([dev1, dev2])
    session.commit()

    # Creating Freebies
    freebie1 = company1.give_freebie(dev1, "backpack", 10, session)
    freebie2 = company1.give_freebie(dev2, "waterbottle", 4, session)
    freebie3 = company2.give_freebie(dev1, "mug", 8, session)

    session.commit()
