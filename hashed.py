from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed = pwd_context.hash("holacomoestas")  # Contraseña que vas a usar para ambos usuarios
print(hashed)