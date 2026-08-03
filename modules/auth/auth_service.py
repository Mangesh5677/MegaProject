import bcrypt

from modules.database.models import User


# ==========================
# Register User
# ==========================

def register_user(db, name, email, password):

    existing = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing:
        return False, "Email already exists."

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    user = User(
        name=name,
        email=email,
        password=hashed
    )

    db.add(user)
    db.commit()

    return True, "Registration Successful."


# ==========================
# Login User
# ==========================

def login_user(db, email, password):

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        return None

    if bcrypt.checkpw(
        password.encode(),
        user.password.encode()
    ):
        return user

    return None