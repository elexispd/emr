# custom_filters.py

from datetime import date
from django import template
from django.conf import settings
from cryptography.fernet import Fernet

register = template.Library()

@register.filter
def is_card_expired(expiration_date):
    if expiration_date:
        today = date.today()
        return expiration_date < today
    return False


# def encrypt_date(date_value):
#     key = settings.FIELD_ENCRYPTION_KEY
#     cipher = Fernet(key.encode('utf-8'))
#     date_str = date_value.strftime('%Y-%m-%d %H:%M:%S')
#     encrypted_date = cipher.encrypt(date_str.encode('utf-8')).decode('utf-8')
#     return encrypted_date

# def decrypt_date(encrypted_date_str):
#     key = settings.FIELD_ENCRYPTION_KEY
#     cipher = Fernet(key.encode('utf-8'))
#     decrypted_date_str = cipher.decrypt(encrypted_date_str.encode('utf-8')).decode('utf-8')
#     return timezone.datetime.strptime(decrypted_date_str, '%Y-%m-%d %H:%M:%S')



@register.filter
def encrypt_data(data):
    key = settings.FIELD_ENCRYPTION_KEY
    cipher = Fernet(key)
    if isinstance(data, int):
        data = str(data)
    
    # Encode the data as bytes using UTF-8 encoding
    data_bytes = data.encode('utf-8')
    encrypted_data = cipher.encrypt(data_bytes)
    return encrypted_data.decode('utf-8')


@register.filter
def decrypt_data(encrypted_data):
    key = settings.FIELD_ENCRYPTION_KEY
    cipher = Fernet(key)
    
    # Decode the encrypted data
    encrypted_data_bytes = encrypted_data.encode('utf-8')
    
    # Decrypt the data
    decrypted_data_bytes = cipher.decrypt(encrypted_data_bytes)
    
    # Decode the decrypted data bytes as string
    decrypted_data = decrypted_data_bytes.decode('utf-8')
    
    return decrypted_data
