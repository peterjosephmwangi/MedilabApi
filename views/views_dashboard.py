# import required modules
import pymysql
from flask_restful import *
from flask import *
from functions import *
import pymysql.cursors

# JWT packages
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
# lab signup resource
class LabSignup(Resource):
    def post(self):
        data = request.json

        lab_name = data["lab_name"]
        email = data["email"]
        phone = data["phone"]
        permit_id = data["permit_id"]
        password = data["password"]

        connection = pymysql.connect(host="pebu.mysql.pythonanywhere-services.com",user="pebu",password="peter1234",database="pebu$default")
        cursor = connection.cursor()
                   # check if password is valid
        response = passwordValidity(password)
        if response == True:
            # connect to DB
            # connection  = pymysql.connect(host='localhost', user='root',password='',database='Medilab')
            # cursor  = connection.cursor()
            # instert into database
            # sql = "insert into members (surname, others, gender, email, phone, dob, status, password, location_id) values(%s, %s, %s, %s, %s, %s, %s, %s,%s)"
            sql = "INSERT INTO laboratories (lab_name,permit_id,email,phone,password) values (%s,%s,%s,%s,%s)"
            # data = (surname, others, gender, email, phone, dob, status, hash_password(password), location_id)
            data = (lab_name,permit_id,email,phone,hash_password(password))
            try:
                cursor.execute(sql, data)
                connection.commit( )
                send_sms(phone, "Registration successful")
                return jsonify({ "message": "POST SUCCESSFUL. MEMBER SAVED"  })

            except:
                connection.rollback()
                return jsonify({ "message": "POST FAILED. MEMBER NOT SAVED"  })

        else:
            return jsonify({  "message": response })
        


class LabSignin(Resource):
    def post(self):
        # get request from client
        data = request.json
        email= data["email"]
        password= data["password"]
        # connect to DB
        connection  = pymysql.connect(host='localhost',user='root', password='', database='Medilab' )

        # check if email exists
        sql = "select * from laboratories where email = %s"
        cursor  = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, email)
        if cursor.rowcount == 0:
            return jsonify({  "message":"Email does not exist!"  })
        else:
            # check password
            member = cursor.fetchone()
            hashed_password = member['password']
            is_matchpassword = hash_verify(password, hashed_password)
            if  is_matchpassword  == True:
                access_token = create_access_token(identity=member, fresh=True)
                return jsonify({  'access_token': access_token,

                                'member':member
                                })
            elif is_matchpassword == False:
                return jsonify({  "message":"LOGIN FAILED"  })
            else:
                return jsonify({  "message": "Something went wrong" })
