from redis.asyncio import Redis
from app.common.configuration import config
from Crypto.Cipher import AES
import base64
import json

redis_connector = None

def get_redis_connector():
    global redis_connector
    if redis_connector is None:
        redis_connector = RedisConnector(host=config.REDIS_HOST, port=config.REDIS_PORT, prefix="fastapi")
    return redis_connector

class RedisConnector:
    def __init__(self, host: str, port: int, db: str = '', prefix: str = "cache") -> None:
        self.client = Redis(host=host, port=port, db=db)
        self.prefix = prefix
        # Ensure key is 32 bytes for AES-256
        self.key = self._prepare_key(config.REDIS_KEY)

    def _prepare_key(self, key: str) -> bytes:
        """Prepare the encryption key to be 32 bytes."""
        if isinstance(key, str):
            key = key.encode('utf-8')
        # Pad or truncate to 32 bytes
        return key[:32].ljust(32, b'\0')

    def get_key(self, key: str):
        return f"{self.prefix}:{key}"
    
    def encrypt_value(self, value: any) -> str:
        """Encrypt the value using AES-256 in EAX mode."""
        # Convert value to JSON string and encode to bytes
        value_bytes = json.dumps(value).encode('utf-8')
        
        # Create cipher
        cipher = AES.new(self.key, AES.MODE_EAX)
        nonce = cipher.nonce
        
        # Encrypt and get tag
        ciphertext, tag = cipher.encrypt_and_digest(value_bytes)
        
        # Combine nonce, tag, and ciphertext
        encrypted_data = nonce + tag + ciphertext
        
        # Convert to base64 for storage
        return base64.b64encode(encrypted_data).decode('utf-8')
    
    def decrypt_value(self, encrypted_value: str) -> any:
        """Decrypt the value using AES-256 in EAX mode."""
        # Decode from base64
        encrypted_data = base64.b64decode(encrypted_value)
        
        # Extract nonce, tag, and ciphertext
        nonce = encrypted_data[:16]  # AES nonce is 16 bytes
        tag = encrypted_data[16:32]  # AES tag is 16 bytes
        ciphertext = encrypted_data[32:]
        
        # Create cipher
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        
        # Decrypt and verify
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        
        # Convert back to Python object
        return json.loads(decrypted_data.decode('utf-8'))
    
    async def read(self, key: str):
        encrypted_value = await self.client.get(self.get_key(key))
        if encrypted_value:
            return self.decrypt_value(encrypted_value)
        return None
    
    async def write(self, key: str, value: any, ttl: int = 60 * 60 * 24 * 14):
        encrypted_value = self.encrypt_value(value)
        return await self.client.set(self.get_key(key), encrypted_value, ex=ttl)
    
    async def delete(self, key: str):
        return await self.client.delete(self.get_key(key))