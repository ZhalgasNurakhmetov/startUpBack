from sqlalchemy import Table, Column, String, ForeignKey, select

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
    photoPath = Column(String, nullable=True, default=None)
    resourceList = relationship('ResourceModel', back_populates='owner')
    favoriteResourceList = relationship('ResourceLikeModel', foreign_keys='ResourceLikeModel.userId')
    following = relationship(
        'UserModel', lambda: user_following,
        primaryjoin=lambda: UserModel.id == user_following.c.userId,
        secondaryjoin=lambda: UserModel.id == user_following.c.followingId,
        backref='followers'
    )
    # chats = relationship(
    #     'ChatModel', lambda: ChatModel,
    #     primaryjoin=lambda: UserModel.id == ChatModel.firstUserId,
    #     secondaryjoin=lambda: UserModel.id == ChatModel.secondUserId,
    # )

    def json(self):
        return {
            "id": self.id,
            "photoPath": self.photoPath,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "birthDate": self.birthDate,
            "city": self.city,
            "about": self.about,
            "username": self.username
        }

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
    imagePath = Column(String, nullable=True, default=None)
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

    @staticmethod
    def delete_like_by_resource_id(resource_id: str, db: Session):
        db.delete(db.query(ResourceLikeModel).filter(ResourceLikeModel.resourceId == resource_id).all())
        db.commit()


user_following = Table(
    'user_following', Base.metadata,
    Column('userId', String, ForeignKey(UserModel.id), primary_key=True),
    Column('followingId', String, ForeignKey(UserModel.id), primary_key=True)
)


class ChatModel(Base):
    from sqlalchemy.orm import relationship, Session
    from sqlalchemy import Column, String

    __tablename__ = 'chats'

    id = Column(String, primary_key=True, unique=True)
    firstUserId = Column(String, nullable=False)
    secondUserId = Column(String, nullable=False)
    firstUserInfo = Column(String, nullable=False)
    secondUserInfo = Column(String, nullable=False)
    firstUserPhotoPath = Column(String, nullable=True)
    secondUserPhotoPath = Column(String, nullable=True)
    messages = relationship('MessageModel', foreign_keys='MessageModel.chatId')

    def save_to_db(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)

    @staticmethod
    def get_all_chats(user_id: str, db: Session):
        from sqlalchemy import or_

        return db.query(ChatModel).where(or_(
            ChatModel.firstUserId == user_id,
            ChatModel.secondUserId == user_id
        )).all()


class MessageModel(Base):
    from sqlalchemy import Column, String, ForeignKey, Text, Boolean
    from sqlalchemy.orm import relationship, Session

    __tablename__ = 'messages'

    id = Column(String, primary_key=True, unique=True)
    chatId = Column(String, ForeignKey('chats.id'))
    userId = Column(String, ForeignKey('users.id'))
    userInfo = relationship('UserModel')
    message = Column(Text, nullable=False)
    isRed = Column(Boolean, nullable=False)
    dateTime = Column(String, nullable=False)

    def json(self):
        return {
            "id": self.id,
            "chatId": self.chatId,
            "userId": self.userId,
            "userInfo": self.userInfo.json(),
            "message": self.message,
            "isRed": self.isRed,
            "dateTime": self.dateTime
        }

    def save_to_db(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)
