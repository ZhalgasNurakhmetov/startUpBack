from services.database.database_service import Base


class UserModel(Base):
    from sqlalchemy.orm import relationship, Session
    from sqlalchemy import Column, String, Text

    __tablename__ = 'users'

    id = Column(String, primary_key=True, unique=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    birthDate = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    city = Column(String, nullable=False)
    about = Column(Text, nullable=True, default=None)
    photo = Column(String, nullable=True, default=None)
    resourceList = relationship('ResourceModel', back_populates='owner')
    # followed
    # likedResources

    def save_to_db(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)

    @staticmethod
    def get_user_by_username(username: str, db: Session):
        return db.query(UserModel).filter(UserModel.username == username).first()

    @staticmethod
    def get_user_by_id(id: str, db: Session):
        return db.query(UserModel).filter(UserModel.id == id).first()


class ResourceModel(Base):
    from sqlalchemy.orm import relationship, Session
    from sqlalchemy import Column, String, Text, Integer, Boolean, ForeignKey

    __tablename__ = 'resources'

    id = Column(String, primary_key=True, unique=True)
    personal = Column(Boolean, nullable=False)
    available = Column(Boolean, nullable=False, default=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(String, nullable=True, default=None)
    pageCount = Column(String, nullable=True, default=None)
    literature = Column(String, nullable=False)
    cover = Column(String, nullable=True, default=None)
    language = Column(String, nullable=False)
    composition = Column(String, nullable=False)
    format = Column(String, nullable=True, default=None)
    description = Column(Text, nullable=True, default=None)
    condition = Column(String, nullable=True, default=None)
    likes = Column(Integer, nullable=False, default=0)
    ownerId = Column(String, ForeignKey('users.id'))
    owner = relationship('UserModel', back_populates='resourceList')

    def save_to_db(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)

    def delete_from_db(self, db: Session):
        db.delete(self)
        db.commit()
        db.refresh()

    @staticmethod
    def get_resource_by_id(id: str, db: Session):
        return db.query(ResourceModel).filter(ResourceModel.id == id).first()
