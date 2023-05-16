import datetime
from sqlalchemy import create_engine, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

engine = create_engine(f"sqlite:///tokens_db.sqlite", echo=False)
connection = engine.connect()


class Base(DeclarativeBase):
    pass


class Token(Base):
    __tablename__ = 'tokens'
    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True,
                                    comment='Первичный ключ')
    date: Mapped[str] = mapped_column(default=str(datetime.datetime.now()))
    token: Mapped[str] = mapped_column()
    token_url: Mapped[str] = mapped_column()
    weth: Mapped[int] = mapped_column()
    score: Mapped[str] = mapped_column(nullable=True, default='')

    def __repr__(self):
        return f'{self.id}. {self.token} {self.score}'

Base.metadata.create_all(engine)
