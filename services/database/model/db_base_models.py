from sqlalchemy import Table, Column, String, ForeignKey

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
    favoriteResourceList = relationship('ResourceLikeModel', foreign_keys='ResourceLikeModel.userId')
    following = relationship(
        'UserModel', lambda: user_following,
        primaryjoin=lambda: UserModel.id == user_following.c.userId,
        secondaryjoin=lambda: UserModel.id == user_following.c.followingId,
        backref='followers'
    )

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
    image = Column(String, nullable=True, default=None)
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
    favoriteUserList = relationship('ResourceLikeModel', back_populates='resource')

    def save_to_db(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)

    def delete_from_db(self, db: Session):
        db.delete(self)
        db.commit()

    @staticmethod
    def get_resource_by_id(id: str, db: Session):
        return db.query(ResourceModel).filter(ResourceModel.id == id).first()

    @staticmethod
    def get_non_personal_resource_list(current_user_id: str, criteria: str, search_text: str, db: Session):
        if criteria == 'title':
            return db.query(ResourceModel).filter(
                (ResourceModel.ownerId != current_user_id) &
                (ResourceModel.available == True) &
                (ResourceModel.personal == True) &
                (ResourceModel.title.ilike('%{}%'.format(search_text)))
            ).all()
        return db.query(ResourceModel).filter(
            (ResourceModel.ownerId != current_user_id) &
            (ResourceModel.available == True) &
            (ResourceModel.personal == True) &
            (ResourceModel.author.ilike('%{}%'.format(search_text)))
        ).all()


class ResourceLikeModel(Base):
    from sqlalchemy import Column, String, ForeignKey
    from sqlalchemy.orm import relationship, Session

    __tablename__ = 'resource_like'

    id = Column(String, primary_key=True, unique=True)
    userId = Column(String, ForeignKey('users.id'))
    resourceId = Column(String, ForeignKey('resources.id'))
    user = relationship('UserModel', back_populates='favoriteResourceList')
    resource = relationship('ResourceModel', back_populates='favoriteUserList')

    def save_to_db(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)

    def delete_from_db(self, db: Session):
        db.delete(self)
        db.commit()

    @staticmethod
    def get_like_by_id(user_id: str, resource_id: str, db: Session):
        return db.query(ResourceLikeModel).filter(ResourceLikeModel.userId == user_id,
                                                  ResourceLikeModel.resourceId == resource_id).first()

    # @staticmethod
    # def get_like_by_resource_id(resource_id: str, db: Session):
    #     return db.query(ResourceLikeModel).filter(ResourceLikeModel.resourceId == resource_id).all()


user_following = Table(
    'user_following', Base.metadata,
    Column('userId', String, ForeignKey(UserModel.id), primary_key=True),
    Column('followingId', String, ForeignKey(UserModel.id), primary_key=True)
)
