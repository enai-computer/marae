import boto3
import hashlib
import json
from datetime import datetime
from uuid import UUID
from app.rest.models.ShareModels import SharePayload, ShareResponse


class SharingService:
    
    """
    Service for sharing data with other users
    """
    def __init__(self):
        self.dynamodb = boto3.client('dynamodb')
        self.table_name = 'v1-mac-app-group-share'

    def store_shared_obj(self, user_id: UUID, payload: SharePayload) -> str:
        # hash payload
        payload_dict = payload.model_dump()
        key = self.gen_key(payload_dict)
        self.dynamodb.put_item(
            TableName=self.table_name,
            Item={
                'id': {'S': key},
                'user_id': {'S': str(user_id)},
                'payload': {'S': payload.model_dump_json()},
                'created_at': {'S': datetime.now().isoformat()}
            }
        )
        return key
    
    def fetch_shared_obj(self, user_id: UUID, share_id: str) -> SharePayload:
        response = self.dynamodb.get_item(
            TableName=self.table_name,
            Key={'id': {'S': share_id}}
        )
        return SharePayload(**json.loads(response['Item']['payload']['S']))

    def gen_key(self, payload: dict) -> str:
        # hash payload
        # Convert payload to string and encode to bytes
        payload_str = str(payload)
        hash_bytes = hashlib.sha256(payload_str.encode()).digest()
        
        # Convert to base62
        ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        base62_key = ""
        num = int.from_bytes(hash_bytes[:8], byteorder='big')  # Use first 8 bytes for shorter key
        
        while num:
            num, rem = divmod(num, 62)
            base62_key = ALPHABET[rem] + base62_key
        
        # Ensure minimum length of 8 characters
        base62_key = base62_key.zfill(8)
        return base62_key
