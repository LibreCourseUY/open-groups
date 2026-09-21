"""
Database Configuration and Models

This file defines the database schema using SQLAlchemy ORM (Object-Relational Mapping).
It creates the tables for storing groups and important links.

Key Concepts:
- SQLAlchemy: A Python library that provides database abstraction
- ORM: Maps Python classes to database tables
- SQLite: A simple file-based database (for development)
- The database URL can be changed via DATABASE_URL environment variable
"""

import os
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
    event,
    text,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker

ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV")

_db_url = os.getenv("DATABASE_URL")
if ENVIRONMENT == "PROD":
    if not _db_url:
        raise RuntimeError("DATABASE_URL is required when ENVIRONMENT=PROD")
    _sync_db_url = _db_url.replace("postgresql+asyncpg://", "postgresql://", 1)
    DATABASE_URL = _db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
else:
    # Accept plain "sqlite://" from .env and normalize it to the async driver.
    if not _db_url:
        DATABASE_URL = "sqlite+aiosqlite:///./groups.db"
    elif _db_url.startswith("sqlite://"):
        DATABASE_URL = _db_url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    else:
        DATABASE_URL = _db_url
    _sync_db_url = DATABASE_URL.replace("sqlite+aiosqlite://", "sqlite://", 1)

from dbwarden import database_config

database_config(
    database_name="primary",
    default=True,
    database_type="postgresql" if ENVIRONMENT == "PROD" else "sqlite",
    database_url_sync=_sync_db_url,
    migrations_dir="migrations",
    model_paths=["database.py"],
)

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

_sync_engine = create_engine(_sync_db_url, echo=False, future=True)
SessionLocal = sessionmaker(bind=_sync_engine, expire_on_commit=False)


# ============================================================================
# DATABASE MODELS
# ============================================================================


class Base(DeclarativeBase):
    """
    Base class for all database models.
    SQLAlchemy will create tables for all classes that inherit from this.
    """


class GroupTag(Base):
    """Association table linking groups and tags."""

    __tablename__ = "group_tags"

    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)


class Group(Base):
    """
    Model representing a student group or project.

    Fields:
    - id: Unique identifier (auto-incremented)
    - name: Group name (required)
    - description: Optional description of the group
    - url: Link to the group's website or repository
    - pinned: Whether this group appears at the top of listings
    - created_at: Timestamp when the group was added
    """

    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    url = Column(String(500))
    pinned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    tags = relationship("Tag", secondary="group_tags", lazy="selectin")


class ImportantLink(Base):
    """
    Model representing important links for students.
    These are displayed on the frontend for quick access.

    Fields:
    - id: Unique identifier
    - title: Link title (required)
    - description: Optional description
    - url: The actual URL (required)
    - created_at: Timestamp when the link was added
    """

    __tablename__ = "important_links"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500))
    url = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now)


# Ensure IDs are set when SERIAL doesn't auto-increment (SQLite)
@event.listens_for(Group, "before_insert", propagate=True)
def _group_before_insert(mapper, connection, target):
    if target.id is None:
        result = connection.execute(text("SELECT COALESCE(MAX(id), 0) + 1 FROM groups"))
        target.id = result.scalar()


@event.listens_for(Tag, "before_insert", propagate=True)
def _tag_before_insert(mapper, connection, target):
    if target.id is None:
        result = connection.execute(text("SELECT COALESCE(MAX(id), 0) + 1 FROM tags"))
        target.id = result.scalar()


# ============================================================================
# DATABASE SESSION HELPER
# ============================================================================


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
