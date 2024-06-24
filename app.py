from flask import *
from flask_restful import Api
app = Flask(__name__)

api = Api(app)

from datetime import timedelta
from flask_jwt_extended import JWTManager

# set up JWT
app.secret_key = "12badjekwkwkkwkkwkwkd"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)
# endpoints / Routes
from views.views import MemberSignup, MemberSignin, MemberProfile,AddDependant, ViewDependants, Laboratories, LabTests, MakeBooking, MyBookings, Payment, Location
from views.views_dashboard import LabProfile, LabSignin, LabSignup, ViewLabTest, Addlabtest, Viewlabookings, AddNurse, ViewNurses, taskallocation
from views.view_nurse import NurseSignin, changepassword
api.add_resource(MemberSignup, '/api/member_signup')
api.add_resource(MemberSignin, '/api/member_signin')
api.add_resource(MemberProfile, '/api/member_profile')
api.add_resource(AddDependant, '/api/add_dependant')
api.add_resource(ViewDependants, '/api/view_dependants')
api.add_resource(Laboratories, '/api/laboratories')
api.add_resource(LabTests, '/api/lab_tests')
api.add_resource(MakeBooking, '/api/makebooking')
api.add_resource(MyBookings, '/api/mybookings')
api.add_resource(Payment, '/api/payment')
api.add_resource(Location, '/api/locations')
# Dashboard
api.add_resource(LabSignup, '/api/labsignup')
api.add_resource(LabSignin, '/api/labsignin' )
api.add_resource(LabProfile, '/api/labprofile')
api.add_resource(Addlabtest, '/api/addlabtests')
api.add_resource(ViewLabTest, '/api/viewlabtests')
api.add_resource(Viewlabookings, '/api/viewlabookings')
api.add_resource(AddNurse, '/api/addnurse')
api.add_resource(ViewNurses, '/api/viewnurses')
api.add_resource(taskallocation, '/api/taskallocation')
api.add_resource(NurseSignin, '/api/nursesignin')
api.add_resource(changepassword, '/api/changepassword')


if __name__ == '__main__':
    app.run(debug=True)
