from passlib.context import CryptContext
from db import SessionLocal, User
import secrets

# Configurer le contexte pour le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fonction pour hacher un mot de passe
def get_password_hash(password):
    return pwd_context.hash(password)

# Fonction pour vérifier un mot de passe
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Fonction pour valider un token de réinitialisation
def validate_reset_token(token):
    db = SessionLocal()
    user = db.query(User).filter(User.reset_token == token).first()
    db.close()
    if user:
        return user.username
    return None

# Fonction pour générer un token de réinitialisation de mot de passe
def generate_reset_token(username):
    token = secrets.token_urlsafe(16)
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if user:
        user.reset_token = token
        db.commit()
    db.close()
    return token

# Fonction pour authentifier un utilisateur
def authenticate_user(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if user and verify_password(password, user.hashed_password):
        return user
    return None





