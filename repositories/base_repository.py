from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic, List

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def save(self, entity: T) -> T:
        try:
            self.session.add(entity)
            self.session.commit()
            return entity
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, entity: T) -> T:
        try:
            self.session.merge(entity)
            self.session.commit()
            return entity
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, entity: T) -> None:
        try:
            self.session.delete(entity)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def find_by_id(self, id: int) -> T:
        try:
            return self.session.query(self.model).get(id)
        except Exception as e:
            raise e

    def find_all(self) -> List[T]:
        try:
            return self.session.query(self.model).all()
        except Exception as e:
            raise e
