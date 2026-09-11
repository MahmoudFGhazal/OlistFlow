"""create locations table

Revision ID: d5025c03c23d
Revises: 8deaf3785b26
Create Date: 2026-08-05 12:39:57.819183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5025c03c23d'
down_revision: Union[str, Sequence[str], None] = '8deaf3785b26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('categories', sa.Column('cat_id', sa.Integer(), autoincrement=True, nullable=False), schema='core')
    op.drop_constraint(op.f('categories_cat_name_english_key'), 'categories', schema='core', type_='unique')

    op.alter_column('cities', 'cit_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True,
               postgresql_using='cit_id::integer',
               schema='core')
    op.alter_column('cities', 'cit_sta_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               postgresql_using='cit_sta_id::integer',
               schema='core')

    op.add_column('customers', sa.Column('cus_external_id', sa.String(), nullable=False), schema='core')
    op.alter_column('customers', 'cus_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True,
               postgresql_using='cus_id::integer',
               schema='core')
    op.alter_column('customers', 'cus_loc_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               postgresql_using='cus_loc_id::integer',
               schema='core')
    op.create_unique_constraint(None, 'customers', ['cus_external_id'], schema='core')

    op.alter_column('locations', 'loc_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True,
               postgresql_using='loc_id::integer',
               schema='core')
    op.alter_column('locations', 'loc_cit_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               postgresql_using='loc_cit_id::integer',
               schema='core')

    op.add_column('order_items', sa.Column('ori_external_id', sa.String(), nullable=False), schema='core')
    op.alter_column('order_items', 'ori_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True,
               postgresql_using='ori_id::integer',
               schema='core')
    op.alter_column('order_items', 'ori_pro_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               postgresql_using='ori_pro_id::integer',
               schema='core')
    op.alter_column('order_items', 'ori_ord_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               postgresql_using='ori_ord_id::integer',
               schema='core')
    op.alter_column('order_items', 'ori_sel_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               postgresql_using='ori_sel_id::integer',
               schema='core')
    op.create_unique_constraint(None, 'order_items', ['ori_external_id'], schema='core')

    op.add_column('orders', sa.Column('order_external_id', sa.String(), nullable=False), schema='core')
    op.alter_column('orders', 'ord_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True,
               postgresql_using='ord_id::integer',
               schema='core')
    op.alter_column('orders', 'ord_cus_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               postgresql_using='ord_cus_id::integer',
               schema='core')
    op.create_unique_constraint(None, 'orders', ['order_external_id'], schema='core')

    op.alter_column('payments', 'pay_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True,
               postgresql_using='pay_id::integer',
               schema='core')
    op.alter_column('payments', 'pay_ord_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               postgresql_using='pay_ord_id::integer',
               schema='core')

    op.add_column('products', sa.Column('pro_external_id', sa.String(), nullable=False), schema='core')
    op.add_column('products', sa.Column('pro_cat_id', sa.Integer(), nullable=False), schema='core')
    op.alter_column('products', 'pro_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True,
               postgresql_using='pro_id::integer',
               schema='core')
    op.create_unique_constraint(None, 'products', ['pro_external_id'], schema='core')
    op.drop_constraint(op.f('products_pro_cat_name_fkey'), 'products', schema='core', type_='foreignkey')
    op.create_foreign_key(None, 'products', 'categories', ['pro_cat_id'], ['cat_id'], source_schema='core', referent_schema='core')
    op.drop_column('products', 'pro_cat_name', schema='core')

    op.add_column('reviews', sa.Column('rev_external_id', sa.String(), nullable=False), schema='core')
    op.alter_column('reviews', 'rev_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True,
               postgresql_using='rev_id::integer',
               schema='core')
    op.alter_column('reviews', 'rev_ord_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               postgresql_using='rev_ord_id::integer',
               schema='core')
    op.create_unique_constraint(None, 'reviews', ['rev_external_id'], schema='core')

    op.add_column('sellers', sa.Column('sel_external_id', sa.String(), nullable=False), schema='core')
    op.alter_column('sellers', 'sel_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True,
               postgresql_using='sel_id::integer',
               schema='core')
    op.alter_column('sellers', 'sel_loc_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               postgresql_using='sel_loc_id::integer',
               schema='core')
    op.create_unique_constraint(None, 'sellers', ['sel_external_id'], schema='core')

    op.alter_column('states', 'sta_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True,
               postgresql_using='sta_id::integer',
               schema='core')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('locations', schema='core')
    # ### end Alembic commands ###
