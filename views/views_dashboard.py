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


# view lab profile using lab_id
class LabProfile(Resource):
  @jwt_required(fresh=True)
  def post(self):
      data = request.json
      lab_id = data["lab_id"]
      connection = pymysql.connect(host="pebu.mysql.pythonanywhere-services.com", user="pebu", password="peter1234", database="pebu$default")
      sql = "select * from laboratories where lab_id = %s"
      cursor = connection.cursor(pymysql.cursors.DictCursor)
      cursor.execute(sql, lab_id)
      if cursor.rowcount == 0:
          return jsonify({"message":"lab does not exist"})
      else:
          lab = cursor.fetchone()
          return jsonify({"message":lab})
      

# add lab tests
class Addlabtest(Resource):
    # @jwt_required(fresh=True)
    def post(self):
         data = request.json
         lab_id=data["lab_id"]
         test_name=data["test_name"]
         test_description=data["test_description"]
         test_cost=data["test_cost"]
         test_discount=data["test_discount"]

        #  connection
         connection = pymysql.connect(host="pebu.mysql.pythonanywhere-services.com", user="pebu", password="peter1234", database="pebu$default")
         cursor=connection.cursor()
         sql="INSERT INTO lab_tests(lab_id,test_name,test_description,test_cost,test_discount) values(%s,%s,%s,%s,%s)"
         data=(lab_id,test_name,test_description,test_cost,test_discount)

         try:
            cursor.execute(sql,data)
            connection.commit()
            return jsonify({"message":"Labposted"})
         except:
             connection.rollback()
             return jsonify({"massage":"Lab not posted"})
         

    # view lab tests
class ViewLabTest(Resource):
        @jwt_required(fresh=True)
        def post(self):
            data = request.json
            lab_id = data["lab_id"]

            connection = pymysql.connect(host="pebu.mysql.pythonanywhere-services.com",user="pebu",password="peter1234",database="pebu$default")
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT * FROM lab_tests WHERE lab_id =%s"
            data = (lab_id)

            cursor.execute(sql,data)
            count = cursor.rowcount
            if count == 0:
                return jsonify ({"mesage":"Lab test does not exist."})
            else:
                labtest = cursor.fetchall()
                return jsonify ({"message": labtest})
            
# view lab bookings
class Viewlabookings(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        lab_id = data["lab_id"]
        connection = pymysql.connect(host='localhost',user='root',password='',database='Medilab')
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "select* from bookings where lab_id=%s"
        cursor.execute(sql,lab_id)
        count = cursor.rowcount
        if count == 0:
            return jsonify({"message":"No bookings"})
        else:
            bookings = cursor.fetchall()
            # associate member_id with the booking
            # we want to loop all the bookings
            for booking in bookings:
                member_id = booking["member_id"]
                # return jsonify(member_id)
                sql = "SELECT * FROM members WHERE member_id = %s"
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                cursor.execute(sql, member_id)
                member = cursor.fetchone()
                # result is attached to booking dictionary under key
                booking['key'] = member
                # return jsonify(member)


            import json
            booking = json.dumps(bookings,indent=1, sort_keys= True,default=str)
            return json.loads(booking)

class AddNurse(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        surname = data["surname"]
        others = data["others"]
        gender = data["gender"]
        phone = data["phone"]
        password = data["password"]
        lab_id = data["lab_id"]

        connection = pymysql.connect(host="pebu.mysql.pythonanywhere-services.com", user="pebu", password="peter1234", database="pebu$default")
        sql = "insert into nurses(surname, others, gender,phone, password,  lab_id) values(%s, %s, %s, %s,  %s, %s)"
        cursor = connection.cursor()

        # try:
        cursor.execute(sql, (surname, others, gender,phone,hash_password(password), lab_id))
        connection.commit()
        return jsonify({"message": "Nurse added"})
        # except:
        #     connection.rollback()
        #     return jsonify({"message": "Nurse not added"})
    

# view nusers
class ViewNurses(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        nurse_id = data["nurse_id"]

        connection = pymysql.connect(host="pebu.mysql.pythonanywhere-services.com", user="pebu", password="peter1234", database="pebu$default")
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        sql = "SELECT * FROM nurses WHERE nurse_id =%s"
        data = (nurse_id)
        cursor.execute(sql, data)
        if cursor.rowcount == 0:
            return jsonify({"message": "Nurse does not exist"})
        else:
            nurse = cursor.fetchone()
            return jsonify({"message": nurse})



# task allocations
class taskallocation (Resource):
    @jwt_required(fresh=True)
    def post(self):
        data=request.json
        nurse_id=data["nurse_id"]
        invoice_no=data["invoice_no"]

        connection = pymysql.connect(host="pebu.mysql.pythonanywhere-services.com", user="pebu", password="peter1234", database="pebu$default")
        sql = "select * from bookings where status = 'Pending' "
        cursor=connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        count=cursor.rowcount
        if count == 0:
            return jsonify({"message":"No pending tasks"})

        else:
            sql1="insert into nurse_lab_allocations (nurse_id,invoice_no) values(%s,%s)"
            data=(nurse_id,invoice_no)
            cursor1 = connection.cursor()
            try:
                cursor1.execute(sql1, data)
                connection.commit()
                return jsonify({"message":"Task allocated"})
            except:
                connection.rollback()
                return jsonify({"message":"Task not allocated"})



