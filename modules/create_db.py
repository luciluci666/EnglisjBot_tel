from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import DATABASE_URL
from models import connect_db, Topic

def create_db():
    session = connect_db()

    session.execute("""create table topics(
        id integer not null primary key,
        name varchar(256),
        desc varchar(256),
        created_at datetime
    );
    """)

    session.execute("""create table words(
        id integer not null primary key,
        word varchar(256),
        translation varchar(256),
        topic_id integer references topics
    );
    """)

    session.execute("""create table phrases(
        id integer not null primary key,
        phrase varchar(512),
        translation varchar(512),
        topic_id integer references topics
    );
    """)

    session.execute("""create table chats(
        id integer not null primary key,
        user_tg_id varchar(256),
        chat_tg_id varchar(256),
        interval varchar(256),
        amount integer,
        topic_id integer references topics
    );
    """)

    
    topic = Topic(
        name = 'General',
        desc = 'Here you can see words and phrases not tied to any topic.'
    )
    session.add(topic)
    session.commit()
    session.close()

    print("Database successfully created")


if __name__ == '__main__':
    create_db()



    