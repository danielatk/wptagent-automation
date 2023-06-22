from sqlalchemy import String, update
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.expression import func

class Video(DeclarativeBase):
    __tablename__ = "video"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    seen: Mapped[bool]

    def get_url(self):
        return f'https://www.youtube.com/watch?v={self.id}'

class Page(DeclarativeBase):
    __tablename__ = "page"

    rank: Mapped[int] = mapped_column(primary_key=True)
    domain: Mapped[str] = mapped_column(String(100))
    monthly_traffic: Mapped[str] = mapped_column(String(10))
    pages_per_visit: Mapped[float]
    time_on_site: Mapped[str] = mapped_column(String(5))
    seen: Mapped[bool]

def get_random_instance(engine, clazz):
    with Session(engine) as session:
        not_watched = session.query(clazz).where(not clazz.seen).count()
        if not_watched <= 0:
            with session.begin():
                session.scalars(update(clazz).values(seen=False))
        instance = session.query(clazz).where(not clazz.seen).order_by(func.random()).limit(1).one()
        instance.seen = True
        return instance

def get_random_page(engine):
    page = get_random_instance(engine, Page)
    return page.domain

def get_random_video(engine):
    video = get_random_instance(engine, Video)
    return video.get_url()
