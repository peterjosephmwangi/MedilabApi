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

































