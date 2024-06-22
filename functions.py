# generate random number
# function defination, takes no argument
def gen_random():
    import random
    # random is used to generat numbers and make randomm selections
    import string
    # provides a collections o string constants, including digits, letters
    # initialized the size of string
    N = 6
    # N is set to 6 , specifies the length of string
    # generate random strings
    res = ''.join(random.choices(string.digits, k=N))
    # ''.join() it concatenates the random strings to single string
    # print the result
    print("The generated string is: " + str(res))
    return str(res)


# gen_random()

# check phone validity
import re
# its a module which provides support for working with regular expressions
def  check_phone(phone):
    # the function takes one argument phone
    regex = "^\+254\d{9}"
    # ^ it asserts the start of the string
    # \+254 ir matches the literal string +254
    # \d{9} matches exactly 9 digits
    if not re.match(regex, phone) or len(phone) != 13:
        print("Phone is not valid")
        return False
    else:
        print("Phone is valid, OK")
        return True
# phone_number = input("Enter your number")
# check_phone(phone_number)


# check password validity
import re
def passwordValidity(password):
    if len (password) < 8 :
        return ("Password is too short")
    elif not re.search ("[A-Z]", password):
        return ("Password must have atleast 1 uppercase")
    elif not re.search("[a-z]", password):
     return("Password must have atleast 1 lowercase")
    elif not re.search("[0-9]", password):
        return ("password must contain atleast a number")
    elif not re.search("[_@$]", password):
        return ("password must contain atleast a special character")
    else:
        return True

# passwordValidity(input("Enter your password: "))

# sending an sms
import africastalking
africastalking.initialize(
username="joe2022",
api_key="aab3047eb9ccfb3973f928d4ebdead9e60beb936b4d2838f7725c9cc165f0c8a"
#justpaste.it/1nua8
)
sms = africastalking.SMS
def send_sms(phone, message):
    recipients = [phone]
    sender = "AFRICASTALKING"
    try:
        response = sms.send(message, recipients)
        print(response)
    except Exception as error:
        print("Error is",  error )
# send_sms("+254716988147", "This is my message")



# hash password
import bcrypt
# bcrypt its a module for hashing and checking passwords
# its very secure
def hash_password(password):
    bytes = password.encode("utf-8")
    # password is encoded into bytes
    # it is necessary because bcrypt library works well with byte data
    # print(bytes)
    salt  = bcrypt.gensalt()
    # using a unique salt for each password ensures that even if two users have same password,
    # their hased password will be different
    # print(salt)
    hash = bcrypt.hashpw(bytes, salt)
    # print(hash)
    return hash.decode()

# hash_password(input("Enter your password: "))

# verify password
def hash_verify(password,  hashed_password):
    bytes = password.encode('utf-8')
    result = bcrypt.checkpw(bytes, hashed_password.encode())
    print(result)
    return result



# hash_verify("1234", "$2b$12$d8FWh.IqQE/MTgncFUm6k.tRqbkdzCyQA5QELRj63MzMsJ6aHzvcG")

# encrypt data
from cryptography.fernet import Fernet
# we import Fernet class
# the module is used for encryption and decryption
def gen_key():
# function used to generate an new encryption key
    key = Fernet.generate_key()
    # print(key)
    with open("key.key", "wb") as key_file:
    # with open it opens a new file if it exists
    # creates a new file if it doesnt exist
    # wb- write binary ensures the file is properly closed after writing on it
        key_file.write(key)


# gen_key()
# load key
def load_key():
    return open("/home/pebu/mysite/key.key", "rb").read()
# it reads the entire content of the file

# load_key()

# encrypt data
def encrypt(data):
    key = load_key()
    f = Fernet(key)
    # print(f)
    # this creates a fernet object 4 encryption
    encrypt_data = f.encrypt(data.encode())
    return (encrypt_data.decode())

# encrypt("1234")

# decrypt data
def decrypt(encrypted_data):
    key = load_key()
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data.encode())
    return (decrypted_data.decode())

# decrypt("gAAAAABmUEKLyoQfQCEd_Tns1oPpWFt2nFQABB0VxuUiahophFWcgLSQoHv1FAJpIeaH-HkGyX7kyLh-Gsk-M7uiFtXVcT950g==")
import requests
import base64
import datetime
from requests.auth  import HTTPBasicAuth
def mpesa_payment(amount, phone, invoice_no):
        # GENERATING THE ACCESS TOKEN
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)




































