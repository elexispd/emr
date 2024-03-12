from datetime import date
import os
import random
import time
from cryptography.fernet import Fernet

from hospital import settings


def generate_invoice_id():
    # Generate a random 4-digit number
    random_number = random.randint(1000, 9999)  
    # Get current timestamp (in milliseconds)
    invoice_id = int(time.time()) + random_number
    return invoice_id

def generate_card_number():
    random_number = random.randint(10, 99)
    num = int(time.time()) + random_number
    return num

def generate_unique_numbers():
    random_number = random.randint(10, 99)
    num = int(time.time()) + random_number
    return num

def ethnic_groups():
    ETHNIC_GROUPS = (
        ('igbo', 'Igbo'),
        ('hausa', 'Hausa'),
        ('yoruba', 'Yoruba'),
        ('afemai', 'Afemai'),
        ('akwa-ibom', 'Akwa Ibom'),
        ('akwaja', 'Akwaja'),
        ('afo', 'Afo'),
        ('anang', 'Anang'),
        ('basa', 'Basa'),
        ('bokyi', 'Bokyi'),
        ('ebira', 'Ebira'),
        ('ebonyi', 'Ebonyi'),
        ('edo', 'Edo'),
        ('efik', 'Efik'),
        ('fulani', 'Fulani'),
        ('gobirawa', 'Gobirawa'),
        ('gbagyi', 'Gbagyi'),
        ('gbaya', 'Gbaya'),
        ('idoma', 'Idoma'),
        ('igala', 'Igala'),
        ('igalla', 'Igalla'),
        ('ijaw', 'Ijaw'),
        ('ijebu', 'Ijebu'),
        ('ijaw', 'Ijaw'),
        ('igede', 'Igede'),
        ('ikwerre', 'Ikwerre'),
        ('isoko', 'Isoko'),
        ('itsekiri', 'Itsekiri'),
        ('ijaw', 'Ijaw'),
        ('jukun', 'Jukun'),
        ('kaje', 'Kaje'),
        ('kanuri', 'Kanuri'),
        ('koro', 'Koro'),
        ('kuteb', 'Kuteb'),
        ('maghavul', 'Maghavul'),
        ('mbembe', 'Mbembe'),
        ('ngas', 'Ngas'),
        ('nupe', 'Nupe'),
        ('ogba', 'Ogba'),
        ('ogoja', 'Ogoja'),
        ('ogoni', 'Ogoni'),
        ('oromo', 'Oromo'),
        ('tiv', 'Tiv'),
        ('urhobo', 'Urhobo'),
    )
    
    return ETHNIC_GROUPS


def is_card_expired(expiration_date):

    today = date.today()
    return expiration_date < today


def encrypt_data(data):
    key = settings.FIELD_ENCRYPTION_KEY
    cipher = Fernet(key)
    if isinstance(data, int):
        data = str(data)
    
    # Encode the data as bytes using UTF-8 encoding
    data_bytes = data.encode('utf-8')
    encrypted_data = cipher.encrypt(data_bytes)
    return encrypted_data.decode('utf-8')


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


def file_upload(uploaded_file, location):
    valid_extensions = ['.pdf', '.docx']
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
    if file_ext not in valid_extensions:
        return 0   
    file_path = os.path.join(settings.MEDIA_ROOT, 'labresults', uploaded_file.name)
    with open(file_path, 'wb') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    
    return os.path.join(location, uploaded_file.name)
