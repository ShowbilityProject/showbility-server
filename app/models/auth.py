# from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from app.models.base import Base
#
# class VerificationCode(Base):
#     __tablename__ = "verification_codes"
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
#     code = Column(String(6), nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     verified = Column(Boolean, default=False)
#     auth_hash = Column(String(39), nullable=True)
#     is_valid = Column(Boolean, default=True)
#
#     user = relationship("ExtendUser", back_populates="codes")
