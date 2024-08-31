from enum import Enum  
from sqlalchemy import ForeignKey, String, func, Enum as sqlEnum
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship
from datetime import datetime

#...

table_registry = registry()

#...

@table_registry.mapped_as_dataclass
class User:
    
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, default=func.now(), onupdate=func.now())

    transactions: Mapped[list['Transaction']] = relationship(
        init=False, back_populates='user', cascade='all, delete-orphan'
    )


class TransactionType(Enum):
    BUY = 'compra'
    SELL = 'venda'


@table_registry.mapped_as_dataclass
class Transaction:
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    
    ativo: Mapped[str] = mapped_column(String(50), nullable=False)
    quantidade: Mapped[int] = mapped_column(nullable=False)
    preco: Mapped[float] = mapped_column(nullable=False)
    transaction: Mapped[TransactionType] = mapped_column(sqlEnum(TransactionType), nullable=False)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

    user: Mapped[User] = relationship(init=False, back_populates='transactions')
