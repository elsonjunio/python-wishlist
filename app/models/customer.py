from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from core.models import TimestampMixin, SoftDeleteMixin

from sqlalchemy.dialects.postgresql import UUID
import uuid


class Customer(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'customers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    user = relationship('User', back_populates='customer')
