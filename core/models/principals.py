from core import db
from core.libs import helpers


class Principal(db.Model):
    """
    Model class representing a collection of principals.

    Attributes:
        id (int): The primary key of the principal.
        user_id (int): The foreign key referencing the associated user.
        created_at (datetime): The timestamp when the principal was created.
        updated_at (datetime): The timestamp when the principal was last updated.
    """
    __tablename__ = 'principals'
    id = db.Column(db.Integer, db.Sequence('principals_id_seq'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

    def __repr__(self) -> str:
        """
        Returns a string representation of the principal.

        Returns:
            str: A string representation of the principal.
        """
        # return f"Principal {self.id}"
