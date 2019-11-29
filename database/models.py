from database.base import CodecovBaseModel
from sqlalchemy import Column, types, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from sqlalchemy import UniqueConstraint, Index


class Owner(CodecovBaseModel):
    __tablename__ = 'owners'
    ownerid = Column(types.Integer, primary_key=True)
    service = Column(types.String(100), nullable=False)
    service_id = Column(types.Text, nullable=False)

    name = Column(types.String(100))
    email = Column(types.String(300))
    username = Column(types.String(100))
    plan_activated_users = Column(postgresql.ARRAY(types.Integer))
    admins = Column(postgresql.ARRAY(types.Integer))
    permission = Column(postgresql.ARRAY(types.Integer))
    organizations = Column(postgresql.ARRAY(types.Integer))
    free = Column(types.Integer, nullable=False, default=0)
    integration_id = Column(types.Integer)
    yaml = Column(postgresql.JSON)
    oauth_token = Column(types.Text)
    avatar_url = Column(types.Text)
    updatestamp = Column(types.DateTime)
    parent_service_id = Column(types.Text)
    plan_provider = Column(types.Text)
    bot_id = Column('bot', types.Integer, ForeignKey('owners.ownerid'))

    bot = relationship('Owner', remote_side=[ownerid])

    __table_args__ = (
        Index('owner_service_ids', 'service', 'service_id', unique=True),
        Index('owner_service_username', 'service', 'username', unique=True),
    )


class Repository(CodecovBaseModel):

    __tablename__ = 'repos'

    repoid = Column(types.Integer, primary_key=True)
    ownerid = Column(types.Integer, ForeignKey('owners.ownerid'))
    bot_id = Column('bot', types.Integer, ForeignKey('owners.ownerid'))
    service_id = Column(types.Text)
    name = Column(types.Text)
    private = Column(types.Boolean)
    updatestamp = Column(types.DateTime)
    yaml = Column(postgresql.JSON)
    branch = Column(types.Text)
    language = Column(types.Text)
    hookid = Column(types.Text)
    using_integration = Column(types.Boolean)

    owner = relationship(Owner, foreign_keys=[ownerid])
    bot = relationship(Owner, foreign_keys=[bot_id])

    __table_args__ = (UniqueConstraint('ownerid', 'name', name='repos_slug'),)

    @property
    def service(self):
        return self.owner.service


class Commit(CodecovBaseModel):

    __tablename__ = 'commits'

    commitid = Column(types.Text, primary_key=True)
    repoid = Column(types.Integer, ForeignKey('repos.repoid'), primary_key=True)
    author_id = Column('author', types.Integer, ForeignKey('owners.ownerid'))
    message = Column(types.Text)
    ci_passed = Column(types.Boolean)
    pullid = Column(types.Integer)
    totals = Column(postgresql.JSON)
    report_json = Column("report", postgresql.JSON)
    branch = Column(types.Text)
    parent_commit_id = Column('parent', types.Text)
    state = Column(types.String(256))

    author = relationship(Owner)
    repository = relationship(Repository)
