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
