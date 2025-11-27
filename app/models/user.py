from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import UUID
import uuid
from core.database import Base
from core.models import TimestampMixin, SoftDeleteMixin


class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default='customer')
    active = Column(Boolean, default=True)

    customer = relationship("Customer", back_populates="user", uselist=False)