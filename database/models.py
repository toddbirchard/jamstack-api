"""Data models."""
from database.orm import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Comment(Base):
    """User-generated comment."""

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255), unique=False)
    user_avatar = Column(Text, unique=False)
    user_id = Column(String(255), ForeignKey("accounts.id"))
    user_email = Column(String(255), unique=False)
    user_role = Column(String(255), unique=False)
    body = Column(Text, unique=False)
    post_slug = Column(String(255), unique=False)
    post_id = Column(String(255), unique=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("Account", backref="user_id")


class CommentUpvote(Base):
    """Upvotes for user comments."""

    __tablename__ = "upvotes"

    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id"))
    user_id = Column(String(255), ForeignKey("accounts.id"))

    # Relationships
    comment = relationship("Comment", backref="comment_id")
    user = relationship("Account")


class Account(Base):
    """Netlify-managed user account."""

    __tablename__ = "accounts"

    id = Column(String(255), primary_key=True, index=True)
    full_name = Column(String(255), unique=False)
    avatar_url = Column(Text, unique=False)
    email = Column(String(255), unique=True)
    role = Column(String(255), unique=False)
    provider = Column(String(255), unique=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class Donation(Base):
    """BuyMeACoffee donation."""

    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=False)
    name = Column(String(255), unique=False)
    count = Column(Integer, unique=False)
    message = Column(Text, unique=False)
    link = Column(String(255))
    created_at = Column(DateTime)
    coffee_id = Column(Integer, unique=True, index=True)
