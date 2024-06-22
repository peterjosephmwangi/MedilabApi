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

