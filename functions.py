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
