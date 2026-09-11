from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint, Enum as SAEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from enum import Enum

# =====================
# BASE
# =====================

class Base(DeclarativeBase):
    pass


# =====================
# ENUMS
# =====================

class OrderStatus(str, Enum):
    DELIVERED = "delivered"
    APPROVED = "approved"
    CANCELED = "canceled"
    CREATED = "created"
    INVOICED = "invoiced"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    UNAVAILABLE = "unavailable"

class PaymentType(str, Enum):
    BOLETO = "boleto"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    NOT_DEFINED = "not_defined"
    VOUCHER = "voucher"


# =====================
# TABLES
# =====================
class States(Base):
    __tablename__ = "states"
    __table_args__ = {
        "schema": "core"
    }

    sta_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sta_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    sta_uf: Mapped[str] = mapped_column(String, nullable=False, unique=True)

class Cities(Base):
    __tablename__ = "cities"
    __table_args__ = (
        UniqueConstraint(
            "cit_normalize_name",
            "cit_sta_id",
            name="uq_cities_name_state"
        ),
        {
            "schema": "core"
        }
    )
    
    cit_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cit_name: Mapped[str] = mapped_column(String, nullable=False)
    cit_normalize_name: Mapped[str] = mapped_column(String, nullable=False)
    cit_sta_id: Mapped[int] = mapped_column(ForeignKey("core.states.sta_id"), nullable=False)

class Locations(Base):
    __tablename__ = "locations"
    __table_args__ = {
        "schema": "core"
    }

    loc_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    loc_code_prefix: Mapped[str] = mapped_column(String, nullable=False)
    loc_lat: Mapped[float] = mapped_column(Numeric(10, 8), nullable=False)
    loc_lng: Mapped[float] = mapped_column(Numeric(11, 8), nullable=False)
    loc_cit_id: Mapped[int] = mapped_column(ForeignKey("core.cities.cit_id"), nullable=False)

class Customers(Base):
    __tablename__ = "customers"
    __table_args__ = {
        "schema": "core"
    }

    cus_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cus_unique_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)

class Sellers(Base):
    __tablename__ = "sellers"
    __table_args__ = {
        "schema": "core"
    }

    sel_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sel_external_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    sel_loc_id: Mapped[int] = mapped_column(ForeignKey("core.locations.loc_id"), nullable=False)

class Categories(Base):
    __tablename__ = "categories"
    __table_args__ = {
        "schema": "core"
    }

    cat_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cat_name: Mapped[str] = mapped_column(String, nullable=False)
    cat_name_english: Mapped[str] = mapped_column(String, nullable=True)

class Products(Base):
    __tablename__ = "products"
    __table_args__ = {
        "schema": "core"
    }

    pro_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pro_external_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    pro_photo_count: Mapped[int] = mapped_column(Integer, nullable=False)
    pro_weight: Mapped[int] = mapped_column(Integer,nullable=False)
    pro_width: Mapped[float] = mapped_column(Numeric(8, 2), nullable=False)
    pro_height: Mapped[float] = mapped_column(Numeric(8, 2), nullable=False)
    pro_length: Mapped[float] = mapped_column(Numeric(8, 2), nullable=False)
    pro_cat_id: Mapped[int] = mapped_column(ForeignKey("core.categories.cat_id"), nullable=False)

class Orders(Base):
    __tablename__ = "orders"
    __table_args__ = {
        "schema": "core"
    }

    ord_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ord_external_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    ord_status: Mapped[OrderStatus] = mapped_column(SAEnum(OrderStatus, name="order_status"), nullable=False)
    ord_purchase_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ord_approved_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    ord_shipped_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    ord_delivered_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    ord_estimated_delivery_date: Mapped[date] = mapped_column(Date, nullable=False)
    ord_cus_id: Mapped[int] = mapped_column(ForeignKey("core.customers.cus_id"), nullable=False)
    ord_customer_external_id: Mapped[str] = mapped_column(String, nullable=False)
    ord_loc_id: Mapped[int] = mapped_column(ForeignKey("core.locations.loc_id"), nullable=False)

class OrderItems(Base):
    __tablename__ = "order_items"
    __table_args__ = {
        "schema": "core"
    }

    ori_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ori_external_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    ori_pro_id: Mapped[int] = mapped_column(ForeignKey("core.products.pro_id"), nullable=False)
    ori_ord_id: Mapped[int] = mapped_column(ForeignKey("core.orders.ord_id"), nullable=False)
    ori_sel_id: Mapped[int] = mapped_column(ForeignKey("core.sellers.sel_id"), nullable=False)
    ori_shipment_limit_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ori_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    ori_freight_value: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

class Payments(Base):
    __tablename__ = "payments"
    __table_args__ = {
        "schema": "core"
    }

    pay_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pay_ord_id: Mapped[int] = mapped_column(ForeignKey("core.orders.ord_id"), nullable=False)
    pay_sequential: Mapped[int] = mapped_column(Integer, nullable=False)
    pay_type: Mapped[PaymentType] = mapped_column(SAEnum(PaymentType, name="payment_type"), nullable=False)
    pay_installments: Mapped[int] = mapped_column(Integer,  nullable=False)

class Reviews(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        CheckConstraint(
            "rev_score BETWEEN 1 AND 5",
            name="ck_reviews_score_range"
        ),
        {
            "schema": "core"
        }
    )

    rev_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rev_external_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    rev_ord_id: Mapped[int] = mapped_column(ForeignKey("core.orders.ord_id"), nullable=False)
    rev_score: Mapped[int] = mapped_column(Integer, nullable=False)
    rev_title: Mapped[str] = mapped_column(String, nullable=True)
    rev_comment: Mapped[str] = mapped_column(String, nullable=True)
    rev_creation_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    rev_answered_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)