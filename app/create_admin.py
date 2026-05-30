from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

username = "hiroki"
password = "M2MWVwnXNkCZ"

existing_user = db.query(User).filter(User.username == username).first()

if existing_user:
    print("管理者ユーザーはすでに存在します")
else:
    user = User(
        username=username,
        password_hash=pwd_context.hash(password),
        role="admin"
    )
    db.add(user)
    db.commit()
    print("管理者ユーザーを作成しました")

db.close()