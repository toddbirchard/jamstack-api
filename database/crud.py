from datetime import datetime
from typing import Optional

from clients.log import LOGGER
from database.models import Account, Comment, CommentUpvote, Donation
from database.schemas import NetlifyAccount, NewComment, NewDonation
from sqlalchemy.engine.result import ResultProxy
from sqlalchemy.orm import Session


def get_donation(db: Session, donation_id: int) -> Optional[ResultProxy]:
    """
    Fetch BuyMeACoffee donation by ID.

    :param db: ORM database session.
    :type db: Session
    :param donation_id: Primary key for donation record.
    :type donation_id: int
    :returns: Optional[ResultProxy]
    """
    return db.query(Donation).filter(Donation.coffee_id == donation_id).first()


def create_donation(db: Session, donation: NewDonation) -> Donation:
    """
    Create new BuyMeACoffee donation record.

    :param db: ORM database session.
    :type db: Session
    :param donation: Donation schema object.
    :type donation: NewDonation
    :returns: Donation
    """
    db_item = Donation(
        email=donation.email,
        name=donation.name,
        count=donation.count,
        message=donation.message,
        link=donation.link,
        coffee_id=donation.coffee_id,
        created_at=datetime.now(),
    )
    db.add(db_item)
    db.commit()
    return db_item


def get_comment(db: Session, comment_id: str) -> Optional[ResultProxy]:
    """
    Fetch comment ID.

    :param db: ORM database session.
    :type db: Session
    :param comment_id: Primary key for user comment record.
    :type comment_id: int
    :returns: Optional[ResultProxy]
    """
    return db.query(Comment).filter(Comment.id == comment_id).first()


def create_comment(db: Session, comment: NewComment) -> Comment:
    """
    Create new user-submitted comment.

    :param db: ORM database session.
    :type db: Session
    :param comment: User comment object.
    :type comment: NewComment
    :returns: NewComment
    """
    new_comment = Comment(
        user_name=comment.user_name,
        user_avatar=comment.user_avatar,
        user_id=comment.user_id,
        user_email=comment.user_email,
        user_role=comment.user_role,
        body=comment.body,
        created_at=datetime.now(),
        post_slug=comment.post_slug,
        post_id=comment.post_id,
    )
    db.add(new_comment)
    db.commit()
    LOGGER.success(
        f"New comment submitted by user `{new_comment.user_name}` on post `{new_comment.post_slug}`"
    )
    return new_comment


def submit_comment_upvote(db: Session, user_id: str, comment_id: int) -> CommentUpvote:
    """
    Create a record of a user's upvote for a given comment.

    :param db: ORM database session.
    :type db: Session
    :param user_id: Primary key for account record.
    :type user_id: str
    :param comment_id: Unique ID of comment user attempted to upvote.
    :type comment_id: int
    :returns: CommentUpvote
    """
    upvote = CommentUpvote(user_id=user_id, comment_id=comment_id)
    db.add(upvote)
    db.commit()
    LOGGER.success(
        f"Upvote submitted for comment `{comment_id}` from user `{user_id}`."
    )
    return upvote


def remove_comment_upvote(db: Session, user_id: str, comment_id: int):
    """
    Delete a record of a user's upvote for a given comment.

    :param db: ORM database session.
    :type db: Session
    :param user_id: Primary key for account record.
    :type user_id: str
    :param comment_id: Unique ID of comment user attempted to upvote.
    :type comment_id: int
    :returns: CommentUpvote
    """
    upvote = CommentUpvote(user_id=user_id, comment_id=comment_id)
    db.delete(upvote)
    db.commit()
    LOGGER.success(f"Removed upvote for comment `{comment_id}` from user `{user_id}`.")


def get_comment_upvote(
    db: Session, user_id: str, comment_id: int
) -> Optional[ResultProxy]:
    """
    Validate whether a user has upvoted a given comment.

    :param db: ORM database session.
    :type db: Session
    :param user_id: Primary key for account record.
    :type user_id: str
    :param comment_id: Unique ID of comment user attempted to upvote.
    :type comment_id: int
    :returns: Optional[ResultProxy]
    """
    return (
        db.query(CommentUpvote)
        .filter(
            CommentUpvote.user_id == user_id and CommentUpvote.comment_id == comment_id
        )
        .first()
    )


def get_account(db: Session, account_email: str) -> Optional[ResultProxy]:
    """
    Fetch account by email address.

    :param db: ORM database session.
    :type db: Session
    :param account_email: Primary key for account record.
    :type account_email: str
    :returns: Optional[ResultProxy]
    """
    return db.query(Account).filter(Account.email == account_email).first()


def create_account(db: Session, account: NetlifyAccount) -> Optional[NetlifyAccount]:
    """
    Create new account record sourced from Netlify.

    :param db: ORM database session.
    :type db: Session
    :param account: User comment schema object.
    :type account: NetlifyAccount
    :returns: Optional[NetlifyAccount]
    """
    new_account = Account(
        id=account.id,
        full_name=account.user_metadata.full_name,
        avatar_url=account.user_metadata.avatar_url,
        email=account.email,
        role=account.role,
        provider=account.app_metadata.provider,
        created_at=account.created_at,
        updated_at=account.updated_at,
    )
    db.add(new_account)
    db.commit()
    account_confirmation = get_account(db, new_account.email)
    if account_confirmation:
        LOGGER.success(f"New account created `{account.email}`")
        return account
    LOGGER.error(f"Failed to create user account for `{account.email}`")
