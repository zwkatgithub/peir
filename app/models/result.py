from app.models import db
from sqlalchemy import Column, Integer, String, and_, Float


class Record(db.Model):
    id = Column(Integer(), primary_key=True, autoincrement=True)

    pn = Column(Integer(), nullable=False)

    topic_id = Column(Integer(), nullable=False)

    doc_id = Column(String(11), nullable=False)

    score = Column(Float(), nullable=False)

    @classmethod
    def records(cls, topic, pn):
        return cls.query.filter(and_(Record.topic_id==topic, Record.pn==pn)).all()

    @classmethod
    def save_all(cls, records):
        db.session.add_all(records)
        db.session.commit()
