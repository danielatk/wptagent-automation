from sqlalchemy import String, update, create_engine
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
import pandas as pd

DATABASE_PATH = '/data/data_gathering.db'
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'

VIDEOS_FILE_PATH = '/app/resources/videos'
PAGES_FILE_PATH = '/app/resources/top_100_brasil.csv'

Base = declarative_base()

engine = None

class Video(Base):
    __tablename__ = "video"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    seen: Mapped[bool]

    def get_url(self):
        return f'https://www.youtube.com/watch?v={self.id}'

class Page(Base):
    __tablename__ = "page"

    rank: Mapped[int] = mapped_column(primary_key=True)
    domain: Mapped[str] = mapped_column(String(100))
    monthly_traffic: Mapped[str] = mapped_column(String(10))
    pages_per_visit: Mapped[float]
    time_on_site: Mapped[str] = mapped_column(String(5))
    seen: Mapped[bool]

def get_random_instance(clazz):
    engine = get_database_engine()
    with Session(engine, expire_on_commit=False) as session, session.begin():
        not_seen = session.query(clazz).filter_by(seen=False).count()
        if not_seen <= 0:
            session.execute(update(clazz).values(seen=False))
        instance = session.query(clazz).filter_by(seen=False).order_by(func.random()).limit(1).one()
        instance.seen = True
        return instance

def get_random_page():
    page = get_random_instance(Page)
    return page.domain

def get_random_video():
    video = get_random_instance(Video)
    return video.get_url()

def get_all_videos_from_file():
    videos = pd.read_csv(VIDEOS_FILE_PATH, header=None)
    return [Video(id=video_id, seen=False) for video_id in videos.iloc[0]]

def get_all_pages_from_file():
    pages = pd.read_csv(PAGES_FILE_PATH)
    return [Page(rank=p['Posicionamento'],
                domain=p['Domínio'],
                monthly_traffic=p['Tráfego mensal'],
                pages_per_visit=p['páginas por visitas'],
                time_on_site=p['tempo no site (min)'],
                seen=False) for _, p in pages.iterrows()]

def get_database_engine():
    global engine
    if engine:
        return engine
    engine = create_engine(DATABASE_URL, echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(engine)
        with Session(engine) as session, session.begin():
            session.add_all(get_all_videos_from_file())
            session.add_all(get_all_pages_from_file())
    return engine
