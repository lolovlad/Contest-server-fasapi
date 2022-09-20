from sqlalchemy import Column, Integer, String, LargeBinary, \
    DateTime, ForeignKey, Boolean, Text, Float

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

base = declarative_base()


class User(base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)
    type = Column(Integer, default=1)

    name = Column(String, nullable=True)
    sename = Column(String, nullable=True)
    secondname = Column(String, nullable=False, default="")
    type_learning = Column(Integer,  nullable=True)
    place_of_study = Column(String, nullable=True)
    learning_stage = Column(String, nullable=True)
    foto = Column(String, nullable=False, default="Photo/default.png")

    teams = relationship("TeamRegistration", back_populates="user", collection_class=list)
    contests = relationship("ContestRegistration", back_populates="user",
                            collection_class=list, join_depth=2)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, val):
        self.hashed_password = generate_password_hash(val)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class ContestRegistration(base):
    __tablename__ = "contest_registration"

    id = Column(Integer, autoincrement=True, primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id'))
    id_contest = Column(Integer, ForeignKey('contest.id'))
    id_team = Column(Integer, ForeignKey('team.id'), default=0)
    state_contest = Column(Integer, nullable=False, default=1)

    user = relationship('User', lazy='joined', join_depth=2, back_populates="contests")
    contest = relationship('Contest', lazy='joined', join_depth=2, back_populates="users")
    team = relationship('Team', lazy='joined', join_depth=2, back_populates="contests")


class TeamRegistration(base):
    __tablename__ = "team_registration"
    id = Column(Integer, autoincrement=True, primary_key=True)
    id_user = Column(Integer, ForeignKey("user.id"))
    id_team = Column(Integer, ForeignKey("team.id"))

    user = relationship("User", back_populates="teams")
    team = relationship("Team", back_populates="users")


class Team(base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_team = Column(String, nullable=True)
    is_solo = Column(Boolean, nullable=False, default=True)

    users = relationship("TeamRegistration", back_populates="team")
    contests = relationship("ContestRegistration", back_populates="team",
                            collection_class=list, join_depth=2)


class Contest(base):
    __tablename__ = "contest"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_contest = Column(String, nullable=True)
    datetime_start = Column(DateTime, nullable=True)
    datetime_end = Column(DateTime, nullable=True)

    datetime_registration = Column(DateTime, default=datetime.now())

    type = Column(Integer, default=1)

    state_contest = Column(Integer, default=0)

    users = relationship("ContestRegistration", back_populates="contest",
                         collection_class=list, join_depth=2)
    tasks = relationship('Task', backref='task')


class TypeCompilation(base):
    __tablename__ = "type_compilation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_compilation = Column(String, nullable=True)
    path_compilation = Column(String, nullable=True)
    path_commands = Column(String, nullable=True)


class EducationalOrganizations(base):
    __tablename__ = "educational_organizations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_organizations = Column(String, nullable=False)
    type_organizations = Column(Integer, nullable=False)


class Task(base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_contest = Column(Integer, ForeignKey('contest.id'))
    time_work = Column(Integer, nullable=False)
    size_raw = Column(Integer, nullable=False)
    type_input = Column(Integer, nullable=False, default=1)
    type_output = Column(Integer, nullable=False, default=1)
    name_task = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    description_input = Column(String, nullable=False)
    description_output = Column(String, nullable=False)

    path_test_file = Column(String, nullable=False)

    type_task = Column(Integer, nullable=False, default=1)
    number_shipments = Column(Integer, nullable=False, default=100)

    #answers = relationship("Answer", backref="task", lazy=True)


class Answer(base):
    __tablename__ = "answer"

    date_send = Column(DateTime, nullable=False, default=datetime.now())
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_team = Column(Integer, ForeignKey('team.id'), default=0)
    id_user = Column(Integer, ForeignKey('user.id'))
    id_task = Column(Integer, ForeignKey('task.id'))
    id_contest = Column(Integer, ForeignKey('contest.id'))
    type_compiler = Column(Integer, ForeignKey('type_compilation.id'), default=1)
    total = Column(String, nullable=False, default="-")
    time = Column(String, nullable=False, default="-")
    memory_size = Column(Float, nullable=False, default=0)
    number_test = Column(Integer, nullable=False, default=0)
    points = Column(Integer, nullable=False, default=0)

    path_report_file = Column(String, nullable=False, default="None")
    path_programme_file = Column(String, nullable=False)

    user = relationship('User', backref='user', lazy=True)
    team = relationship('Team', backref='Team', lazy=True)
    compilation = relationship('TypeCompilation', backref='type_compilation', lazy=True)