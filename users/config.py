from django.conf import settings

ACCESS_TOKEN_LIFETIME =  "300s",
REFRESH_TOKEN_LIFETIME = "1209600s",
TOKEN_TYPE_CLAIM = "token_type",
JTI_CLAIM = "jti"
USER_ID_CLAIM = "user_id"
USER_ID_FIELD = "id"
ALGORITHM = "HS256"
SIGNING_KEY=settings.SECRET_KEY, 
VERIFYING_KEY="",
AUDIENCE=None , 
JWK_URL=None 
LEEWAY=0
ISSUER= None
ALLOWED_ALGORITHMS = (
    "HS256",
)
