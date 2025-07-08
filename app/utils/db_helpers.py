from app import db
from sqlalchemy.exc import SQLAlchemyError

def commit_session():
    try:
        db.session.commit()
        return True, None
    except SQLAlchemyError as e:
        db.session.rollback()
        return False, str(e)

def add_and_commit(instance):
    db.session.add(instance)
    return commit_session()

def get_by_id(model, id_):
    return db.session.query(model).get(id_)
