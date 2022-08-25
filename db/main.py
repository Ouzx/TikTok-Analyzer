import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey

engine = create_engine('sqlite:///db/tiktok.db')
Base = declarative_base()


class Page(Base):
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    following = Column(Integer)
    followers = Column(Integer)
    likes = Column(Integer)
    bio = Column(String)
    post_count = Column(Integer)
    create_date = Column(DateTime)
    update_date = Column(DateTime)
    link = Column(String, unique=True)

    def __repr__(self):
        return f"Page(name='{self.name}', following={self.following}, followers={self.followers}, likes={self.likes}, bio='{self.bio}', post_count={self.post_count}, create_date={self.create_date}, update_date={self.update_date}, link='{self.link}')"


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    page_id = Column(Integer, ForeignKey('pages.id'))
    name = Column(String)
    link = Column(String, unique=True)
    create_date = Column(DateTime)
    update_date = Column(DateTime)

    def __repr__(self):
        return f"Post(id={self.id}, page_id={self.page_id}, name={self.name}, link={self.link}, create_date={self.create_date}, update_date={self.update_date})"


class PostActivity(Base):
    __tablename__ = 'post_activities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    view = Column(Integer)
    like = Column(Integer)
    comment = Column(Integer)
    create_date = Column(DateTime)

    def __repr__(self):
        return f"PostActivity(id={self.id}, post_id={self.post_id}, view={self.view}, like={self.like}, comment={self.comment}, create_date={self.create_date})"


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def create_page(page_data):
    session = Session()

    page = session.query(Page).filter(Page.link == page_data['link']).first()
    if page is None:
        page = Page(
            name=page_data['name'],
            following=page_data['following'],
            followers=page_data['followers'],
            likes=page_data['likes'],
            bio=page_data['bio'],
            post_count=page_data['post_count'],
            create_date=datetime.datetime.now(),
            update_date=datetime.datetime.now(),
            link=page_data['link']
        )
        session.add(page)
        session.commit()
    else:
        page.name = page_data['name']
        page.following = page_data['following']
        page.followers = page_data['followers']
        page.likes = page_data['likes']
        page.bio = page_data['bio']
        page.post_count = page_data['post_count']
        page.update_date = datetime.datetime.now()
        session.commit()

    session.close()


def create_post(post_data):
    session = Session()
    post = session.query(Post).filter(Post.link == post_data['link']).first()
    if post is None:
        post = Post(
            page_id=session.query(Page).filter(
                Page.link == post_data['page_link']).first().id,
            name=post_data['name'],
            link=post_data['link'],
            create_date=datetime.datetime.now(),
            update_date=datetime.datetime.now()
        )
        session.add(post)
        session.commit()
    else:
        post.update_date = datetime.datetime.now()
        session.commit()
    session.close()


def create_post_activity(post_activity_data):
    session = Session()
    post_id = session.query(Post).filter(
        Post.link == post_activity_data['post_link']).first().id
    post_activity = PostActivity(
        post_id=post_id,
        view=post_activity_data['view'],
        like=post_activity_data['like'],
        comment=post_activity_data['comment'],
        create_date=datetime.datetime.now()
    )
    session.add(post_activity)
    session.commit()
    session.close()
