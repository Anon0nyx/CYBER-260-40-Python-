from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from cryptography.fernet import Fernet

# Generate a set of RSA keys using the provided functions from Crypto lib
def generate_secret_keys(username):
	key = RSA.generate(2048) # Generate key set

	# Handle private key
	private_key = key.export_key()
	file_out = open(f"./client/keys/{username}/{username}_priv.pem", "wb")
	file_out.write(private_key)
	file_out.close()
	private_key = private_key.decode()

	# Handle public key
	public_key = key.publickey().export_key()
	file_out = open(f"./client/keys/{username}/{username}_pub.pem", "wb")
	file_out.write(public_key)
	file_out.close()
	public_key = public_key.decode()

	# Create and handle symmetric encryption key
	sym_key = Fernet.generate_key()

	return [public_key, private_key, sym_key]

# Function to encrypt an symmetric key with an rsa key
def encrypt_key(priv_key, rsa_key):
	pr_key = RSA.import_key(rsa_key)
	encryptor = PKCS1_OAEP.new(pr_key)

	encrypted = encryptor.encrypt(priv_key)
	return encrypted

# Function to decrypt symmetric key with rsa key
def decrypt_key(priv_key, rsa_key):
	pr_key = RSA.import_key(rsa_key)
	decryptor = PKCS1_OAEP.new(pr_key)

	decrypted = decryptor.decrypt(priv_key)

	return decrypted

# Use symmetric key to encrypt data
def encrypt_data(data, key):
	fernet = Fernet(key)
	
	encrypted = fernet.encrypt(data)
	return encrypted

# Use symmetric key to decrypt data
def decrypt_data(data, key):
	fernet = Fernet(key)
	
	decrypted = fernet.decrypt(data)
	return decrypted
