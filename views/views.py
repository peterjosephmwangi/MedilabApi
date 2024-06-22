from functions import *
# import JWT packages
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

# Add a member class
# member_signup and member_signin
class MemberSignup(Resource):
    def post(self):
        # get data from client
        data = request.json
        surname= data["surname"]
        others= data["others"]
        gender= data["gender"]
        email= data["email"]
        phone= data["phone"]
        dob= data["dob"]
        status= data["status"]
        password= data["password"]
        location_id= data["location_id"]

        # check if password is valid
        response = passwordValidity(password)
        if response == True:
            # connect to DB
            connection  = pymysql.connect(host='pebu.mysql.pythonanywhere-services.com', user='pebu',password='peter1234',database='pebu$default')
            cursor  = connection.cursor()
            # instert into database
            sql = "insert into members (surname, others, gender, email, phone, dob, status, password, location_id) values(%s, %s, %s, %s, %s, %s, %s, %s,%s)"
            data = (surname, others, gender, email, encrypt(phone), dob, status, hash_password(password), location_id)
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
        

class MemberSignin(Resource):
    def post(self):
        # get request from client
        data = request.json
        email= data["email"]
        password= data["password"]
        # connect to DB
        connection  = pymysql.connect(host='pebu.mysql.pythonanywhere-services.com',user='pebu', password='peter1234', database='pebu$default' )

        # check if email exists
        sql = "select * from members where email = %s"
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
            
class MemberProfile(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        member_id = data["member_id"]
        # connect to DB
        connection  = pymysql.connect(host='pebu.mysql.pythonanywhere-services.com',user='pebu', password='peter1234', database='pebu$default' )
        sql = "SELECT * FROM members WHERE member_id = %s"
        cursor  = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, member_id)
        count = cursor.rowcount
        if  count == 0:
            return jsonify({  "message":"Member does not exist!"  })
        else:
            member = cursor.fetchone()
            return jsonify({  "message": member })
        
class AddDependant(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data =  request.json
        member_id = data["member_id"]
        surname = data["surname"]
        others = data["others"]
        dob = data["dob"]
        connection  = pymysql.connect(host='pebu.mysql.pythonanywhere-services.com',user='pebu', password='peter1234', database='pebu$default' )
        cursor = connection.cursor()
        # insert into dependants table
        sql = "insert into dependants (member_id, surname, others, dob) values(%s, %s, %s, %s)"
        data = (member_id , surname, others, dob)
        try:
            cursor.execute(sql, data)
            connection.commit( )
            return jsonify({ "message": "POST SUCCESSFUL. Dependant SAVED"  })

        except:
            connection.rollback()
            return jsonify({ "message": "POST FAILED. Dependant NOT SAVED"  })


class ViewDependants(Resource):
     @jwt_required(fresh=True)
     def post(self):
          json = request.json
          member_id = json['member_id']
          sql = "select * from dependants where member_id = %s"
          connection = pymysql.connect(host='pebu.mysql.pythonanywhere-services.com',
                                                user='pebu',
                                                password='peter1234',
                                                database='pebu$default')

          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute(sql, member_id)
          count = cursor.rowcount
          if count == 0:
               return jsonify({'message': 'Member does Not exist'})
          else:
               dependants = cursor.fetchall()
               return jsonify(dependants)
          

class Laboratories(Resource):
    def get(self):
         connection  = pymysql.connect(host='pebu.mysql.pythonanywhere-services.com',user='pebu', password='peter1234', database='pebu$default' )
         sql = "SELECT * FROM laboratories"
         cursor  = connection.cursor(pymysql.cursors.DictCursor)
         cursor.execute(sql)
         if cursor.rowcount == 0:
             return jsonify({ "message": "No Laboratories" })
         else:
             labs = cursor.fetchall()
             return jsonify(labs)
         
class Location(Resource):
    def post(self):
         connection  = pymysql.connect(host='pebu.mysql.pythonanywhere-services.com',user='pebu', password='peter1234', database='pebu$default' )
         sql = "SELECT * FROM locations"
         cursor  = connection.cursor(pymysql.cursors.DictCursor)
         cursor.execute(sql)
         if cursor.rowcount == 0:
             return jsonify({ "message": "No Locations" })
         else:
             locations = cursor.fetchall()
             return jsonify(locations)

class LabTests(Resource):
    def post(self):
        data = request.json
        lab_id = data["lab_id"]
        connection  = pymysql.connect(host='pebu.mysql.pythonanywhere-services.com',user='pebu', password='peter1234', database='pebu$default' )
        sql = "SELECT * FROM lab_tests WHERE lab_id = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, lab_id)
        if cursor.rowcount == 0:
            return jsonify({ "message": "No Lab Tests Found" })
        else:
            lab_tests = cursor.fetchall()
            return jsonify(lab_tests)





