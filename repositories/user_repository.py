from typing import Optional
from models.user import User
from sqlalchemy.orm import Session
from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def find_by_email(self, email: str) -> Optional[User]:
        try:
            return self.session.query(User).filter_by(email=email).first()
        except Exception as e:
            raise e
