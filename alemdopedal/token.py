from itsdangerous import URLSafeTimedSerializer
from alemdopedal import app

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


def gerar_token(email):
    return serializer.dumps(email, salt=app.config['SECRET_KEY'])


def verificar_token(token, expiration=3600):
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECRET_KEY'],
            max_age=expiration
        )
    except:
        return None
    return email
