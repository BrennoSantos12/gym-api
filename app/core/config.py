import os
from datetime import timedelta


SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY não definida. Configure no .env ou export SECRET_KEY=...")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = timedelta(minutes=60)
