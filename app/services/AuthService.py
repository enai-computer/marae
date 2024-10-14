from devicecheck import DeviceCheck
from datetime import datetime, timedelta, timezone
import jwt
from app.rest.models.AuthModels import Token
from app.SecretsService import secretsStore


class AuthService:
    def __init__(self):
        self.device_check = DeviceCheck(
            team_id=secretsStore.secrets["TEAM_ID"],
            bundle_id=secretsStore.secrets["BUNDLE_ID"],
            key_id=secretsStore.secrets["KEY_ID"], 
            private_key=secretsStore.secrets["PRIVATE_KEY_PATH"],
            dev_environment=False, 
        )

    def validate_device_token(self, apple_device_token: str):
        return self.device_check.validate_device_token(apple_device_token)
    
    def get_jwt_token(self, apple_device_token: str) -> Token:
        access_token_expires = timedelta(minutes=int(secretsStore.secrets["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"]))
        access_token = self.create_access_token(
            data={"sub": apple_device_token}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
    
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secretsStore.secrets["JWT_SECRET_KEY"], algorithm=secretsStore.secrets["JWT_ALGORITHM"])
        return encoded_jwt
