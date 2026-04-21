import db_models
from database import Base, engine
from crud import create_user, get_user_by_id

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

user_id = create_user(name="Ali", email="ali@test.com", age=25, role="user")
print(f"Created user with id: {user_id}")

user = get_user_by_id(user_id)
print(f"Fetched user: {user.name}, {user.email}")
