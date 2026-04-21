from sqlalchemy import select, update
from db_models import User, Product
from database import SessionLocal


# ── CREATE ──────────────────────────────────────────
def create_user(name: str, email: str, age: int, role: str):
    with SessionLocal() as session:
        with session.begin():
            user = User(name=name, email=email, age=age, role=role)
            session.add(user)
        session.refresh(user)
        return user.id


def create_product(name: str, category: str, price: float):
    with SessionLocal() as session:
        with session.begin():
            product = Product(name=name, category=category, price=price)
            session.add(product)
        session.refresh(product)
        return product.id


# ── READ ────────────────────────────────────────────
def get_user_by_id(user_id: int):
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if user:
            session.expunge(user)
        return user


def get_all_users():
    with SessionLocal() as session:
        stmt = select(User)
        return session.execute(stmt).scalars().all()


def get_users_by_role(role: str):
    with SessionLocal() as session:
        stmt = select(User).where(User.role == role)
        return session.execute(stmt).scalars().all()


def get_products_in_stock():
    with SessionLocal() as session:
        stmt = select(Product).where(Product.in_stock == True).order_by(Product.price)
        return session.execute(stmt).scalars().all()


# ── UPDATE ──────────────────────────────────────────
def update_user_role(user_id: int, new_role: str):
    with SessionLocal() as session:
        with session.begin():
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(role=new_role)
                .execution_options(synchronize_session="fetch")
            )
            session.execute(stmt)


# ── DELETE ──────────────────────────────────────────
def delete_user(user_id: int):
    with SessionLocal() as session:
        with session.begin():
            user = session.get(User, user_id)
            if user:
                session.delete(user)
