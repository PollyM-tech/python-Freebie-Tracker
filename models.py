# models.py

from sqlalchemy import Column, Integer, String, ForeignKey, MetaData, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

#alembic naming convention
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    founding_year = Column(Integer, nullable=False)

    freebies = relationship('Freebie', back_populates='company')
    devs = association_proxy('freebies', 'dev')

    def give_freebie(self, dev, item_name, value, session):
        existing = next((fb for fb in self.freebies
                         if fb.dev == dev and fb.item_name == item_name), None)
        if existing:
            return existing

        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        session.add(freebie)
        return freebie

    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()

    def __repr__(self):
        return f'<Company {self.name}>'


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    freebies = relationship('Freebie', back_populates='dev')
    companies = association_proxy('freebies', 'company')

    def received_one(self, item_name):
        return any(fb.item_name == item_name for fb in self.freebies)

    def give_away(self, new_dev, freebie, session):
        if freebie.dev == self:
            freebie.dev = new_dev
            session.commit()
            return True
        return False

    def __repr__(self):
        return f'<Dev {self.name}>'


class Freebie(Base):
    __tablename__ = 'freebies'
    __table_args__ = (
        UniqueConstraint('dev_id', 'company_id', 'item_name', name='uq_freebie_per_dev_company_item'),
    )

    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    dev_id = Column(Integer, ForeignKey('devs.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)

    dev = relationship('Dev', back_populates='freebies')
    company = relationship('Company', back_populates='freebies')

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"

    def __repr__(self):
        return f'<Freebie {self.item_name}>'
    
