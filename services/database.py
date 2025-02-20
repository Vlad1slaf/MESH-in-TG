from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, select, BigInteger, Text
from config.settings import settings

Base = declarative_base()


class Homework(Base):
    __tablename__ = "homework"
    school_id = Column(Integer, primary_key=True)
    class_name = Column(String(10), primary_key=True)
    subject = Column(String(100), primary_key=True)
    homework = Column(Text)


class User(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True)  # Telegram User ID
    yandex_token = Column(String(255), nullable=True)  # Yandex OAuth Token


engine = create_async_engine(settings.DB_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_homework(school_id: int, class_name: str, subject: int) -> str:
    async with AsyncSessionLocal() as session:
        result = await session.get(Homework, (school_id, class_name, subject))
        return result.homework if result else None


async def update_homework(school_id: int, class_name: str, subject: int, text: str):
    async with AsyncSessionLocal() as session:
        homework = Homework(
            school_id=school_id,
            class_name=class_name,
            subject=subject,
            homework=text
        )
        await session.merge(homework)
        await session.commit()


async def save_yandex_token(user_id: int, yandex_token: str):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if user:
            user.yandex_token = yandex_token
        else:
            user = User(user_id=user_id, yandex_token=yandex_token)
            session.add(user)
        await session.commit()
