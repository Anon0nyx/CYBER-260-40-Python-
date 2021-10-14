from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from cryptography.fernet import Fernet

def generate_secret_keys(username):
	key = RSA.generate(2048)

	private_key = key.export_key()
	file_out = open(f"./client/keys/{username}/{username}_priv.pem", "wb")
	file_out.write(private_key)
	file_out.close()
	private_key = private_key.decode()

	public_key = key.publickey().export_key()
	file_out = open(f"./client/keys/{username}/{username}_pub.pem", "wb")
	file_out.write(public_key)
	file_out.close()
	public_key = public_key.decode()

	sym_key = Fernet.generate_key()

	return [public_key, private_key, sym_key]

def write_key_to_file(priv_key, rsa_key):
	to_encrypt = priv_key.encode("utf-8")
	encryptor = PKCS1_OAEP.new(rsa_key)

	encrypted = encryptor.encrypt(msg)
	print(encrypted)

def encrypt_key(priv_key, rsa_key):
	pr_key = RSA.import_key(rsa_key)
	encryptor = PKCS1_OAEP.new(pr_key)

	encrypted = encryptor.encrypt(priv_key)
	return encrypted

def decrypt_key(priv_key, rsa_key):
	pr_key = RSA.import_key(rsa_key)
	decryptor = PKCS1_OAEP.new(pr_key)

	decrypted = decryptor.decrypt(priv_key)

	return decrypted

def encrypt_data(data, key):
	fernet = Fernet(key)
	
	encrypted = fernet.encrypt(data)
	return encrypted

def decrypt_data(data, key):
	fernet = Fernet(key)
	
	decrypted = fernet.decrypt(data)
	return decrypted
