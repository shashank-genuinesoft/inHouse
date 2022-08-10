import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . models import *
from . serializers import *
from rest_framework import permissions
from . import models
from . myauth import *
from . otpgen import *
from . test import *
from . utility import generateKey,verify_otp
from . email import send_email
from rest_framework import status
TOKENEXPTIME=86400
# Create your views here.
def home(request):
    #send_otp(6,"shashankpawar8082@gmail.com")
    return render(request,"otp.html")
# start of company registration
class CompanyRegistration(APIView):
    def post(self,request):
        data=request.data     

#validation
        try: 
            company_name=data["company_name"]
        except:   
            val_error={
                "status": 201,
                "message":"Company Name is Required.",
                        }
            return Response(val_error)
        try: 
            data["company_address"]
        except:   
            val_error={
                "status": 201,
                "message":"Company Address is Required.",
                        }
            return Response(val_error)
        try: 
            data["tax_number"]
        except:   
            val_error={
                "status": 201,
                "message":"Tax Number is Required.",
                        }
            return Response(val_error)
        try: 
            data["commercial_year"]
        except:   
            val_error={
                "status": 201,
                "message":"Commercial Year is Required.",
                        }
            return Response(val_error)
        try: 
            company_email=data["company_email"]
        except:   
            val_error={
                "status": 201,
                "message":"Company Email is Required.",
                        }
            return Response(val_error)       
        try: 
            data["mobile_number"]
        except:   
            val_error={
                "status": 201,
                "message":"Mobile Number is Required.",
                        }
            return Response(val_error)
        try: 
            data["password"]
        except:   
            val_error={
                "status": 201,
                "message":"Password is Required.",
                        }
            return Response(val_error)
        try:
            instance=Companies.objects.get(company_email=company_email)    
            status= instance.isVerified
            print(status)
            if status == True:
                try: 
                    company_email=data["company_email"]    
                    Companies.objects.get(company_email=company_email)
                    val_error={
                        "status": 201,
                        "message":"Company With This Email Already Exists.",
                                }
                    return Response(val_error)
                except :
                    print("hello.......................")
                    serializer = CompaniesSerializer(data=data)
            else: 
                print("hello 1.....................")
                serializer = CompaniesSerializer(instance,data=data,partial=True)  
        except :
            print("hello 2.....................")
            serializer = CompaniesSerializer(data=data)

            
#end validation                         
        if serializer.is_valid():
            serializer.save()
            key = generateKey()
            user = Companies(company_id=serializer.data['company_id'])
            user.otp=key['OTP']
            user.activation_key=key['totp']
            user.save(update_fields=['otp','activation_key'])
            send_email('otp.html',"Otp Verification",serializer.data['company_email'],otp = key['OTP'],username = serializer.data['company_name'])
            response_data={
                    "status": 200,
                    "message": "Registered Successfully",
                    "data":"Otp has been send!!",
                    "otp":key['OTP']
                          }
            return Response (response_data)
        response_data={
                    "status": 201,
                    "message": serializer.errors
                      }   
        return Response(response_data)
#end of company registration

#resend otp
class resendOtpView(APIView):
    def post(self,request):
#validation
        try:            
            email=request.data["company_email"]           
        except: 
            data={
                "status": 201,
                "message":"Company Email is Required"
                 }
            return Response(data)
#validation        
        email = request.data["company_email"]
        try:
            user = Companies.objects.get(company_email = email)
            key = generateKey()
            user.otp = key['OTP']
            user.activation_key = key['totp']
            user.save(update_fields=['otp','activation_key'])      
            send_email('otp.html','Otp Verification',email,otp = key['OTP'],username = user.company_name)
            data={
                "status": 200,
                "message":"Otp successfully send!!"
                 }
            return Response(data)
        except:
            data={
                    "status": 201,
                    "message":"No Inactive account found for this given email!!"
                 }
            return Response(data)
#end or resend otp

# reset password
class ResetPasswordView(APIView):
    def post(self,request):
#validation
        try:            
            email=request.data["company_email"]           
        except: 
            data={
                "status": 201,
                "message":"Company Email is Required"
                 }
            return Response(data)
#validation        
        email = request.data["company_email"]
        try:
            user = Companies.objects.get(company_email = email)
            key = generateKey()
            user.otp = key['OTP']
            user.activation_key = key['totp']
            user.save(update_fields=['otp','activation_key'])      
            send_email('otp.html','Otp Verification',email,otp = key['OTP'],username = user.company_name)
            data={
                "status": 200,
                "message":"Otp successfully send!!"
                 }
            return Response(data)
        except:
            data={
                "status": 201,
                "message":"No account found for this given email!!"
                 }
            return Response(data)
#end of reset password 

#password reset 
#verification
class resetPassvarificationView(APIView):
    def post(self,request):
        data=request.data
#validation
        try:            
            company_email=request.data["company_email"]           
        except: 
            data={
                "status": 201,
                "message":"Company Email is Required."
                 }
            return Response(data)
        try:            
            company_email=request.data["company_email"]
            Companies.objects.get(company_email=company_email)           
        except: 
            data={
                "status": 201,
                "message":"Company dose not exists with this company email "
                 }
            return Response(data)
        try:            
            otp=request.data["otp"]           
        except: 
            data={
                "status": 201,
                "message":"OTP is Required."
                 }
            return Response(data)
       
#validation            
        try:    
            user = Companies.objects.get(otp = otp)
            verify = verify_otp(user.activation_key,otp) 
            if verify:
                user.otp = None
                user.save(update_fields=['otp'])
                payload={"company_id":user.company_id,"company_name":user.company_name,"company_address":user.company_address,"tax_number":user.tax_number,"commercial_year":user.commercial_year,"company_email":user.company_email,"mobile_number":user.mobile_number,"isVerified":user.isVerified}
                encoded = jwt.encode({"exp": datetime.now(tz=timezone.utc) + timedelta(seconds=TOKENEXPTIME),"User": payload}, "secret", algorithm="HS256")          
                data={
                "status": 200,
                "message": "Otp verified successfully.",
                # "token":encoded,
                # "data":{
                # "company_id":user.company_id
                #         }
                 }
                return Response(data)
            else:
                data={
                "status": 201,
                "message": "Given otp is expired!!"
                 }
                return Response(data)
        except:
            data={
                "status": 201,
                "message": "Invalid otp OR No any inactive user found for given otp"
                 }
            return Response(data)
#end of varification
class passwordVerifyView(APIView):
    def post(self,request):
        data=request.data
#validation
        try:            
            company_email=request.data["company_email"]           
        except: 
            data={
                "status": 201,
                "message":"Company Email is Required."
                 }
            return Response(data)
        try:            
            company_email=request.data["company_email"]
            Companies.objects.get(company_email=company_email)           
        except: 
            data={
                "status": 201,
                "message":"Company dose not exists with this company email "
                 }
            return Response(data)
        try:            
            new_password=request.data["new_password"]           
        except: 
            data={
                "status": 201,
                "message":"New Password is Required."
                 }
            return Response(data)
#validation 
        if Companies.objects.get(company_email=company_email):
            instance=Companies.objects.get(company_email=company_email)
            instance.password=make_password(new_password)
            instance.save()
            data={
                "status": 200,
                "message":"Password reset Success."
                 }
            return Response(data)
        else:
            data={
                "status": 201,
                "message":"company dose not exists with this company email."
                 }
            return Response(data)
#password reset 

#verification
class varificationView(APIView):
    def post(self,request):
        data=request.data
#validation
        try:            
            company_email=request.data["company_email"]           
        except: 
            data={
                "status": 201,
                "message":"Company Email is Required."
                 }
            return Response(data)
        try:            
            company_email=request.data["company_email"]
            Companies.objects.get(company_email=company_email)           
        except: 
            data={
                "status": 201,
                "message":"Company dose not exists with this company email "
                 }
            return Response(data)
        try:            
            otp=request.data["otp"]           
        except: 
            data={
                "status": 201,
                "message":"OTP is Required."
                 }
            return Response(data)
#validation            
        try:    
            user = Companies.objects.get(otp = otp)
            verify = verify_otp(user.activation_key,otp) 
            if verify:
                user.otp = None
                user.isVerified=True
                user.save(update_fields=['isVerified','otp'])
                payload={"company_id":user.company_id,"company_name":user.company_name,"company_address":user.company_address,"tax_number":user.tax_number,"commercial_year":user.commercial_year,"company_email":user.company_email,"mobile_number":user.mobile_number,"isVerified":user.isVerified}
                encoded = jwt.encode({"exp": datetime.now(tz=timezone.utc) + timedelta(seconds=TOKENEXPTIME),"User": payload}, "secret", algorithm="HS256")          
                data={
                "status": 200,
                "message": "Account successfully activated",
                "token":encoded,
                "data":{
                "company_id":user.company_id
            }
                 }
                return Response(data)
            else:
                data={
                "status": 201,
                "message": "Given otp is expired!!"
                 }
                return Response(data)
        except:
            data={
                "status": 201,
                "message": "Invalid otp OR No any inactive user found for given otp"
                 }
            return Response(data)
#end of varification
from django.contrib.auth.hashers import make_password
#update password
# class UpdatePasswordView(APIView):
#     def post(self,request):
#         data= request.data
#         try:
#             company_email  = data["company_email"]
#         except :
#             val_error={
#                 "status": 201,
#                 "message":"Company Email is Required.",
#                         }
#             return Response(val_error)
#         try: 
#            old_password= data["old_password"]
#         except:   
#             val_error={
#                 "status": 201,
#                 "message":"old Password is Required.",
#                         }
#             return Response(val_error)
#         try: 
#             data["new_password"]
#         except:   
#             val_error={
#                 "status": 201,
#                 "message":"New Password is Required.",
#                         }
#             return Response(val_error)
#         try:
#             Companies.objects.get(company_email=data["company_email"])
#         except:
#             val_error={
#                 "status": 201,
#                 "message":"Company With This Company Email is Not Exists.",
#                         }
#             return Response(val_error)
#         try:
#             oldPassword=make_password(data["old_password"])
#             print(oldPassword)
#             Companies.objects.get(company_email=data["company_email"],password=oldPassword)
#         except:
#             val_error={
#                 "status": 201,
#                 "message":"Wrong Password.",
#                         }
#             return Response(val_error)
# #validation
#         data=request.data
#         company_email  = data["company_email"]
#         if not Companies.objects.filter(company_email=company_email).exists():
#                 errdata= {
#                         "status": 201,
#                         "message":'Account dose not exist'
#                         }
#                 return Response(errdata)
#         else:
#             data={"password":make_password(data["new_password"])}
#             user=Companies.objects.get(company_email=company_email)
#             ser = CompaniesSerializer(user,data=data,partial=True)
#             if ser.is_valid(raise_exception=True):
#                 ser.save()
#                 data= {
#                         "status": 200,
#                         "message":'Password Has been successfully reset'
#                         }
#                 return Response(data)
#             else:
#                 data={
#                     "status":201,
#                     "message":ser.errors
#                 }                 
#                 return Response(data)    
# #end


from datetime import datetime, timedelta,timezone
import time

# start of company login
class CompanyLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self,request):
#validation        
        try:            
            mail=request.data["company_email"]           
        except: 
            data={
                "status": 201,
                "message":"Company Email is Required."
                 }
            return Response(data)
        try:            
            mail=request.data["password"]           
        except: 
            data={
                "status": 201,
                "message":"Password is Required."
                 }
            return Response(data)
        try:
            mail=request.data["company_email"]
            cdata=Companies.objects.get(company_email=mail) 
        except:       
            data={
                "status": 201,
                "message":  "Wrong Company Email."
                 }
            return Response(data)     
        if cdata.isVerified == True:
            pass
        else:
            data={
                "status": 201,
                "message": "Account not verified please verify first!!"
                 }
            return Response(data) 

#end validation                 
            
        serializer = LoginSerializer(data=self.request.data,context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.validated_data['user']
        except:
            return Response(serializer.validated_data)        
        payload={"company_id":user.company_id,"company_name":user.company_name,"company_address":user.company_address,"tax_number":user.tax_number,"commercial_year":user.commercial_year,"company_email":user.company_email,"mobile_number":user.mobile_number,"isVerified":user.isVerified}
        encoded = jwt.encode({"exp": datetime.now(tz=timezone.utc) + timedelta(seconds=TOKENEXPTIME),"User": payload}, "secret", algorithm="HS256")
        data={
            "status": "200",
            "Token": encoded,
            "data":{
                "company_id":user.company_id
            }
                }
        return Response(data, status=200)
#end of company login

class UpdatePasswordView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self,request):
#permission 
        try:
            auth=is_company_user(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission 
#validation      
        
        try:            
            mail=request.data["old_password"]           
        except: 
            data={
                "status": 201,
                "message":"Old Password is Required."
                 }
            return Response(data)
        try:            
            mail=request.data["new_password"]           
        except: 
            data={
                "status": 201,
                "message":"New Password is Required."
                 }
            return Response(data)
        try:
            mail=auth["is_company_user"]["User"]["company_email"]
            cdata=Companies.objects.get(company_email=mail) 
        except:       
            data={
                "status": 201,
                "message":  "Wrong password!"
                 }
            return Response(data)     
#end validation         
        compamy_mail=auth["is_company_user"]["User"]["company_email"]        
        data={"company_email":compamy_mail,"password":request.data["old_password"]}
        serializer = LoginSerializer(data=data,context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.validated_data['user']
        except:
            return Response(serializer.validated_data)    
        company_pass=Companies.objects.get(company_email = compamy_mail)   
        company_pass.password= make_password(request.data["new_password"])    
        company_pass.save()
        payload={"company_id":user.company_id,"company_name":user.company_name,"company_address":user.company_address,"tax_number":user.tax_number,"commercial_year":user.commercial_year,"company_email":user.company_email,"mobile_number":user.mobile_number,"isVerified":user.isVerified}
        encoded = jwt.encode({"exp": datetime.now(tz=timezone.utc) + timedelta(seconds=TOKENEXPTIME),"User": payload}, "secret", algorithm="HS256")
        data={
            "status": "200",
            "Token": encoded,
            "data":{
                "company_id":user.company_id
            }
                }
        return Response(data, status=200)
#end of company login

#..............................................................................................................................
# start of company login
class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self,request):
#validation        
        try:            
            mail=request.data["email"]           
        except: 
            data={
                "status": 201,
                "message":"Email is Required."
                 }
            return Response(data)
        try:            
            mail=request.data["password"]           
        except: 
            data={
                "status": 201,
                "message":"Password is Required."
                 }
            return Response(data)
        try:
            mail=request.data["email"]
            cdata=Users.objects.get(email=mail) 
        except:       
            data={
                "status": 201,
                "message":  "Wrong  Email."
                 }
#end validation 
        serializer = UserLoginSerializer(data=self.request.data,context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.validated_data['user']
        except:
            return Response(serializer.validated_data)
        payload={"user_id":user.user_id,"company_id":str(user.company_id.company_id),"first_name":user.first_name,"last_name":user.last_name,"email":user.email,"mobile_number":user.mobile_number,"permission_view":user.permission_view,"permission_create":user.permission_create,"permission_update":user.permission_update,"permission_delete":user.permission_delete}
        encoded = jwt.encode({"exp": datetime.now(tz=timezone.utc) + timedelta(seconds=TOKENEXPTIME),"User": payload}, "secret", algorithm="HS256")    
        #decode=jwt.decode(encoded, "secret", algorithms=["HS256"])
        data={"status": "200 ",
            "Token": encoded,
            "data":{
                "company_id":str(user.company_id.company_id),
                "user_id":user.user_id,
                "permission_view":user.permission_view,
                "permission_create":user.permission_create,
                "permission_update":user.permission_update,
                "permission_delete":user.permission_delete
            }
             }
        return Response(data, status=200)
#end of  login

#start of create user
class CreateUser(APIView):
    def post(self,request):
#permission 
        auth=is_company_user(request.META["HTTP_AUTHORIZATION"]) 
        try:
            auth=is_company_user(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                
                return Response(data,401)
#permission   
#validation
        data=request.data
        try: 
            data["company_id"]
        except:   
            val_error={
                "status": 201,
                "message":"Company Id is Required.",
                        }
            return Response(val_error)
        try:
            Companies.objects.get(company_id=data["company_id"])
        except:
            val_error={
                "status": 201,
                "message":"Company With This Company Id is Not Exists.",
                        }
            return Response(val_error)
        try: 
            data["first_name"]
        except:   
            val_error={
                "status": 201,
                "message":"First Name is Required.",
                        }
            return Response(val_error)
        try: 
            data["last_name"]
        except:   
            val_error={
                "status": 201,
                "message":"Last Name is Required.",
                        }
            return Response(val_error)
        try: 
            data["email"]
        except:   
            val_error={
                "status": 201,
                "message":"Email is Required.",
                        }
            return Response(val_error)
        try:
            Users.objects.get(email=data["email"]) 
            val_error={
                "status": 201,
                "message":"User With This Email Already Exists.",
                        }
            return Response(val_error) 
        except:
            pass      
        try: 
            data["mobile_number"]
        except:   
            val_error={
                "status": 201,
                "message":"Mobile Number is Required.",
                        }
            return Response(val_error)
        try: 
            data["password"]
        except:   
            val_error={
                "status": 201,
                "message":"Password is Required.",
                        }
            return Response(val_error)
        try: 
            data["permission_view"]
        except:   
            val_error={
                "status": 201,
                "message":"Permission View is Required.",
                        }
            return Response(val_error)
        try: 
            data["permission_create"]
        except:   
            val_error={
                "status": 201,
                "message":"Permission Create is Required.",
                        }
            return Response(val_error)
        try: 
            data["permission_update"]
        except:   
            val_error={
                "status": 201,
                "message":"Permission Update is Required.",
                        }
            return Response(val_error)
        try: 
            data["permission_delete"]
        except:   
            val_error={
                "status": 201,
                "message":"Permission Delete is Required.",
                        }
            return Response(val_error)
#end validation        
        data=request.data
        serializer=UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            
            response_data={
                    "status": 200,
                    "message": "User Created Successfully",
                    # "data":{
                    #     "user_id":serializer.data["user_id"],
                    #     "company_id":serializer.data["company_id"],
                    # }
                      }
            return Response (response_data)
        response_data={
                    "status": 201,
                    "message":serializer.errors,
                      }   
        return Response(response_data)
#end of create user

#start of all users

class AllUsers(APIView):
    def get(self,request):
#permission 
        try:
            auth=permission_view(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission 
        try:
            company_id=auth["is_company_user"]["User"]["company_id"]
        except:
            data={
                "status": 201,
                "message": "You dont have permission for this action"
                 }
            return Response(data)
        data=Users.objects.filter(company_id=company_id)
        ser = GetUserSerializer(data, many=True)
        if not data:
            data={
                    "status": 201,
                    "message": "Users Not Found",
                        }
            return Response (data)
        data= {
                "status": 200,
                "message":"Success",
                "data":ser.data
                    }
        return Response(data)  
# end of get all users

# start of update user
class UpdateUser(APIView):
    def put(self,request):
    
#permission 
        try:
            auth=is_company_user(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission 
#validation
        data=request.data
        try: 
            user_id=data["user_id"]
        except:   
            val_error={
                "status": 201,
                "message":"User Id is Required.",
                        }
            return Response(val_error)
       
        try: 
            data["first_name"]
        except:   
            val_error={
                "status": 201,
                "message":"First Name is Required.",
                        }
            return Response(val_error)
        try: 
            data["last_name"]
        except:   
            val_error={
                "status": 201,
                "message":"Last Name is Required.",
                        }
            return Response(val_error)
        try: 
            data["email"]
        except:   
            val_error={
                "status": 201,
                "message":"Email is Required.",
                        }
            return Response(val_error)
        if not Users.objects.filter(user_id=user_id).exists():
                errdata= {
                        "status": 201,
                        "message":'User Dose Not Exist'
                        }
                return Response(errdata)
        user_mailid=Users.objects.get(user_id=user_id).email
        try: 
            data["email"]
            Users.objects.get(email=data["email"])
            val_error={
                "status": 201,
                "message":"User With This Email Already Exists.",
                        }
            if user_mailid == data["email"] :
                pass 
            else:      
                return Response(val_error)
        except: 
            pass  
            
        try: 
            data["mobile_number"]
        except:   
            val_error={
                "status": 201,
                "message":"Mobile Number is Required.",
                        }
            return Response(val_error)
        
        try: 
            data["permission_view"]
        except:   
            val_error={
                "status": 201,
                "message":"Permission View is Required.",
                        }
            return Response(val_error)
        try: 
            data["permission_create"]
        except:   
            val_error={
                "status": 201,
                "message":"Permission Create is Required.",
                        }
            return Response(val_error)
        try: 
            data["permission_update"]
        except:   
            val_error={
                "status": 201,
                "message":"Permission Update is Required.",
                        }
            return Response(val_error)
        try: 
            data["permission_delete"]
        except:   
            val_error={
                "status": 201,
                "message":"Permission Delete is Required.",
                        }
            return Response(val_error)
#end validation
        data=request.data
        user_id  = data["user_id"]
        if not Users.objects.filter(user_id=user_id).exists():
                errdata= {
                        "status": 201,
                        "message":'User Dose Not Exist'
                        }
                return Response(errdata)
        else:
            user=Users.objects.get(user_id=user_id)
            ser = GetUserSerializer(user,data=data)
            if ser.is_valid():
                ser.save()
                data= {
                        "status": 200,
                        "message":'User Updated Successfully'
                        }
                return Response(data)
            else:
                data={
                    "status":201,
                    "message":ser.errors
                }                 
                return Response(data)                
#end of update user

#start of Delete user

class DeleteUser(APIView):
    def delete(self,request):
#params
        try:
            data=request.query_params
            user_id=data["user_id"]
        except :
            data={
                "status": 201,
                "message": "Invalid header"
                 }
            return Response(data)      
#params 
#permission 
        try:
            auth=is_company_user(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission 

        if not Users.objects.filter(user_id=user_id).exists():
                errdata= {
                        "status": 201,
                        "message":'User Dose Not Exist'
                        }
                return Response(errdata)
        else:
            user=Users.objects.get(user_id=user_id)
            user.delete()
            data={
                "status":200,
                "message":"User Deleted Succesfully"
                }
            return Response(data)
# End of delete user
#user datails 
class userDetailsView(APIView):
    def get(self,request):
#params
        try:
            data=request.query_params
            user_id=data["user_id"]
        except :
            data={
                "status": 201,
                "message": "Invalid header"
                 }
            return Response(data)      
#params 
#permission 
        try:
            auth=permission_view(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission 
        try:
            Users.objects.get(user_id=user_id)
        except:
            errdata= {
                        "status": 201,
                        "message":'User Dose Not Exist'
                        }
            return Response(errdata)
        else:
            user=Users.objects.get(user_id=user_id)
            ser = GetUserSerializer(user)
            data= {
                    "status": 200,
                    "message":"success",
                    "data":ser.data
                        }
            data=json.dumps(data)            
            data=json.loads(data)            
            return Response(data)
#end user details

#.........................................


#user datails 
class getUserPermissions(APIView):
    def get(self,request): 
#permission 
        try:
            auth=permission_all(request.META["HTTP_AUTHORIZATION"])
            if not auth["status"]==200:
                return Response ("gfdxghfhjfghbcvgcfbhcvnv jmngv")
            try:
                auth["is_company_user"]["User"]["user_id"]
               
                data={
                    "status": 200,
                    "message": "success",
                    "data":{
                        "permission_view":auth["is_company_user"]["User"]["permission_view"],
                        "permission_create":auth["is_company_user"]["User"]["permission_create"],
                        "permission_update":auth["is_company_user"]["User"]["permission_update"],
                        "permission_delete":auth["is_company_user"]["User"] ["permission_delete"]
                    }
                    }
                
                return Response(data)
            except:
                data={
                    "status": 205,
                    "message": "user not found please login as user."
                    }
                return Response(data) 
        except:
            data={
                "status": 205,
                "message": "Unauthorized"
                }
            return Response(data)

#.......................................................................................................................................................


# create group master This Api is used to create the Group master by the company
class GroupMasterView(APIView):
    def post(self,request):
#permission 
        try:
            auth=permission_create(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission 
#validation
        data= request.data
        try: 
            data["company_id"]
        except:   
            val_error={
                "status": 201,
                "message":"Company Id is Required.",
                        }
            return Response(val_error)
        try:
            Companies.objects.get(company_id=data["company_id"])
        except:
            val_error={
                "status": 201,
                "message":"Company With This Company Id is Not Exists.",
                        }
            return Response(val_error)
        try: 
            data["group_name"]
        except:   
            val_error={
                "status": 201,
                "message":"Group Name is Required.",
                        }
            return Response(val_error)
        
        try: 
            data["group_nature"]
        except:   
            val_error={
                "status": 201,
                "message":"Group Nature is Required.",
                        }
            return Response(val_error)
        try: 
            data["group_under"]
        except:   
            val_error={
                "status": 201,
                "message":"Group under is Required.",
                        }
            return Response(val_error)
        try: 
            plaffect=data["pl_affect"]
        except:   
            val_error={
                "status": 201,
                "message":"Pl Affect is Required.",
                        }
            return Response(val_error)   
        if plaffect in ('YES', 'NO'):
            pass
        else:
            val_error={
                "status": 201,
                "message":"Invalid choice please select YES or NO",
                        }
            return Response(val_error)
#validation
        data=request.data
        ser = GroupMasterSerializer(data=data)
        if ser.is_valid():
            ser.save()
            response_data={
                    "status": 200,
                    "message": "Group created successfully"
                      }
            return Response (response_data)
        response_data={
                    "status": 201,
                    "message":ser.errors,
                      }   
        return Response(response_data)
#end

#list group master 
class ListGroupMasterView(APIView):
    def get(self,request):
#permission 
        try:
            auth=permission_view(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission 
        print(auth)
        try:
            company_id=auth["is_company_user"]["User"]["company_id"]
        except :
            company_id=auth["data"]["User"]["company_id"]
        data=GroupMaster.objects.filter(company_id=company_id,is_default_group=False)
        ser = GetGroupMasterviewSerializer(data, many=True)
        
        if not data:
            data={
                    "status": 201,
                    "message": "Group Not Found",
                        }
            return Response (data)
        errdata= {
                    "status": 200,
                    "message":"success",
                    "data":ser.data
                        }
        return Response(errdata)  
#end
class ListGroupMasterDefault(APIView):
    def get(self,request):
#permission 
        try:
            auth=permission_view(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission 
        print(auth)
        try:
            company_id=auth["is_company_user"]["User"]["company_id"]
        except :
            company_id=auth["data"]["User"]["company_id"]

        data_def =GroupMaster.objects.filter(is_default_group=True)
        ser_def = GetGroupMasterSerializer(data_def, many=True)
        data=GroupMaster.objects.filter(is_default_group=False)
        ser = GetGroupMasterSerializer(data, many=True)
        
        if not data_def:
            data={
                    "status": 201,
                    "message": "Group Not Found",
                        }
            return Response (data)
        errdata= {
                    "status": 200,
                    "message":"success",
                    "data":ser_def.data+ser.data
                        }
        return Response(errdata)  
#end

#update group master 
class UpdateGroupMaster(APIView):
    def put(self,request):
#permission 
        try:
            auth=permission_update(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission 
#validation
        data= request.data
        try: 
            data["group_master_id"]
        except:   
            val_error={
                "status": 201,
                "message":"Group Master Id is Required.",
                        }
            return Response(val_error)
        try: 
            data["group_name"]
        except:   
            val_error={
                "status": 201,
                "message":"Group Name is Required.",
                        }
            return Response(val_error)
        try: 
            data["group_under"]
        except:   
            val_error={
                "status": 201,
                "message":"Group Under is Required.",
                        }
            return Response(val_error)
        try: 
            data["group_nature"]
        except:   
            val_error={
                "status": 201,
                "message":"Group Nature is Required.",
                        }
            return Response(val_error)
        try: 
            data["pl_affect"]
        except:   
            val_error={
                "status": 201,
                "message":"Pl Affect is Required.",
                        }
            return Response(val_error)       
#validation
        group_master_id=data["group_master_id"]
        if not GroupMaster.objects.filter(group_master_id=group_master_id).exists():
                errdata= {
                        "status": 201,
                        "message":'Group Dose Not Exist'
                        }
                return Response(errdata)
        else:
            user=GroupMaster.objects.get(group_master_id=group_master_id)
            ser = GroupMasterSerializer(user,data=data,partial=True)
            if ser.is_valid(raise_exception=True):
                ser.save()
                data= {
                        "status": 200,
                        "message":'Group Updated Successfully'
                        }
                return Response(data)
            else:
                data={
                    "status":201,
                    "message":ser.errors
                }                 
                return Response(data)                            
#end of update user

#start Delete group master
class DeleteGroupMaster(APIView):
    def delete(self,request):
#params
        try:
            data=request.query_params
            group_master_id=data["group_master_id"]
        except :
            data={
                "status": 201,
                "message": "Invalid header"
                 }
            return Response(data)      
#params 
#permission 
        try:
            auth=permission_delete(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission
        if not GroupMaster.objects.filter(group_master_id=group_master_id).exists():
                errdata= {
                        "status": 201,
                        "message":'Group dose not exist'
                        }
                return Response(errdata)
        else:
            user=GroupMaster.objects.get(group_master_id=group_master_id)
            user.delete()
            data={
                "status":200,
                "message":"Group deleted succesfully"
                }
            return Response(data)
#end
#details 
class groupMasterDetailsView(APIView):
    def get(self,request):
#params
        try:
            data=request.query_params
            group_master_id=data["group_master_id"]
        except :
            data={
                "status": 201,
                "message": "Invalid header"
                 }
            return Response(data)      
#params 
#permission 
        try:
            auth=permission_view(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission         
        try:
            GroupMaster.objects.get(group_master_id=group_master_id)
        except:
            errdata= {
                        "status": 201,
                        "message":'Group Master dose not exist'
                        }
            return Response(errdata)
        else:
            user=GroupMaster.objects.get(group_master_id=group_master_id)
            ser = GroupMasterSerializer(user)
            data= {
                    "status": 200,
                    "message":"success",
                    "data":ser.data
                        }
            return Response(data)
#end details
#......................................................................................................................................................................

#start of ledger
class LedgerMasterView(APIView):
    def post(self,request):
#permission 
        try:
            auth=permission_create(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission
#validation
        data= request.data
        try: 
            data["company_id"]
        except:   
            val_error={
                "status": 201,
                "message":"Company Id is Required.",
                        }
            return Response(val_error)
        try:
            Companies.objects.get(company_id=data["company_id"])
        except:
            val_error={
                "status": 201,
                "message":"Company With This Company Id is Not Exists.",
                        }
            return Response(val_error)
        try: 
            data["ledger_name"]
        except:   
            val_error={
                "status": 201,
                "message":"Ledger Name is Required.",
                        }
            return Response(val_error)
        try: 
            data["group_under"]
        except:   
            val_error={
                "status": 201,
                "message":"Group Under is Required.",
                        }
            return Response(val_error)     
#validation

        data=request.data
        ser = LedgerMasterSerializer(data=data)
        if ser.is_valid():
            ser.save()
            response_data={
                    "status": 200,
                    "message": "Ledger Created Successfully"
                      }
            return Response (response_data)
        response_data={
                    "status": 201,
                    "message":ser.errors,
                      }   
        return Response(response_data)
# end

#update ledger
class UpdateLedgerMasterView(APIView):
    def put(self,request):
#permission 
        try:
            auth=permission_update(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission
#validation
        data= request.data
        try:
            ledger_master_id  = data["ledger_master_id"]
        except :
            val_error={
                "status": 201,
                "message":"Ledger Id is Required.",
                        }
            return Response(val_error)
        try: 
            data["ledger_name"]
        except:   
            val_error={
                "status": 201,
                "message":"Ledger Name is Required.",
                        }
            return Response(val_error)
        try: 
            data["group_under"]
        except:   
            val_error={
                "status": 201,
                "message":"Group Under is Required.",
                        }
            return Response(val_error)     
#validation
        data=request.data
        ledger_master_id  = data["ledger_master_id"]
        if not LedgerMaster.objects.filter(ledger_master_id=ledger_master_id).exists():
                errdata= {
                        "status": 201,
                        "message":'Ledger dose not exist'
                        }
                return Response(errdata)
        else:
            user=LedgerMaster.objects.get(ledger_master_id=ledger_master_id)
            ser = LedgerMasterSerializer(user,data=data,partial=True)
            if ser.is_valid(raise_exception=True):
                ser.save()
                data= {
                        "status": 200,
                        "message":'Ledger updated successfully'
                        }
                return Response(data)
            else:
                data={
                    "status":201,
                    "message":ser.errors
                }                 
                return Response(data)    
#end
#List ledger
class ListLedgerMasterView(APIView):
    def get(self,request):
#permission 
        try:
            auth=permission_view(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission 
        try:
            company_id=auth["is_company_user"]["User"]["company_id"]
        except:
            company_id=auth['data']['User']['company_id'] 
        data=LedgerMaster.objects.filter(company_id=company_id)
        ser=LedgerMasterSerializer(data,many=True)
        if not data:
            data={
                    "status": 201,
                    "message": "Ledger Not Found",
                        }
            return Response (data)
        errdata= {
                    "status": 200,
                    "message":"success",
                    "data":ser.data
                        }
        return Response(errdata) 
#end

#delete ledger
class DeleteLedgerMasterView(APIView):
    def delete(self,request):
#params
        try:
            data=request.query_params
            ledger_master_id=data["ledger_master_id"]
        except :
            data={
                "status": 201,
                "message": "Invalid header"
                 }
            return Response(data)      
#params 
#permission 
        try:
            auth=permission_delete(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission    

        if not LedgerMaster.objects.filter(ledger_master_id=ledger_master_id).exists():
                errdata= {
                        "status": 201,
                        "message":'Ledger Dose Not Exist'
                        }
                return Response(errdata)
        else:
            user=LedgerMaster.objects.get(ledger_master_id=ledger_master_id)
            user.delete()
            data={
                "status":200,
                "message":"Ledger Deleted Duccesfully"
                }
            return Response(data)
#end
class LedgerMasterDetailsView(APIView):
    def get(self,request):
#params
        try:
            data=request.query_params
            ledger_master_id=data["ledger_master_id"]
        except :
            data={
                "status": 201,
                "message": "Invalid header"
                 }
            return Response(data)      
#params          
#permission 
        try:
            auth=permission_view(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission        
        try:
            LedgerMaster.objects.get(ledger_master_id=ledger_master_id)
        except:
            errdata= {
                        "status": 201,
                        "message":'Ledger Master dose not exist'
                        }
            return Response(errdata)
        else:
            user=LedgerMaster.objects.get(ledger_master_id=ledger_master_id)
            ser = LedgerMasterDetailsSerializer(user)
            data= {
                    "status": 200,
                    "message":"success",
                    "data":ser.data
                        }
            return Response(data)
#................................................................................
# create transaction 
class CreateTransactionsView(APIView):
    def post(self,request):
#permission 
        try:
            auth=permission_create(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission
        
#validation
        data= request.data       
        # try: 
        #     data["company_id"]
        # except:   
        #     val_error={
        #         "status": 201,
        #         "message":"Company Id is Required."
        #                 }
        #     return Response(val_error)
        # try:
        #     Companies.objects.get(company_id=data["company_id"])
        # except:
        #     val_error={
        #         "status": 201,
        #         "message":"Company With This Company Id is Not Exists."
        #                 }
        #     return Response(val_error)
        try: 
            data["transaction_name"]
        except:   
            val_error={
                "status": 201,
                "message":"Transaction Name is Required."
                        }
            return Response(val_error)
        try: 
            data["voucher_number"]
        except:   
            val_error={
                "status": 201,
                "message":"Voucher Number is Required."
                        }
            return Response(val_error)
        try: 
            data["remarks"]
        except:   
            val_error={
                "status": 201,
                "message":"Remarks is Required."
                        }
            return Response(val_error)     
        try: 
            data["transaction_date"]
        except:   
            val_error={
                "status": 201,
                "message":"Transaction date is Required."
                        }
            return Response(val_error)     
        data=request.data
        try:
            uid=auth["data"]["User"]["user_id"]
            cid=auth["data"]["User"]["company_id"]
            user_data={"user_id":uid,"company_id":cid}
            data.update(user_data)
        except :
            cid=auth["is_company_user"]["User"]["company_id"]
            user_data={"company_id":cid}
            data.update(user_data)
        ser = CtreateTransactionSerializer(data=data)
        if ser.is_valid():
            ser.save()  
            response_data={
                    "status": 200,
                    "message": "Transaction Created Successfully",
                    "data":ser.data
                      }
            return Response(response_data)
        response_data={
                    "status": 201,
                    "message":ser.errors,
                      }   
        return Response(response_data)
# end
#update transaction
class UpdateTransactionsView(APIView):
    def put(self,request):
#permission 
        try:
            auth=permission_update(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission
#validation
        data= request.data
        try: 
            data["transaction_id"]
        except:   
            val_error={
                "status": 201,
                "message":"Transaction Id is Required."
                        }
            return Response(val_error)
        try: 
            data["transaction_name"]
        except:   
            val_error={
                "status": 201,
                "message":"Transaction Name is Required."
                        }
            return Response(val_error)
        try: 
            data["transaction_date"]
        except:   
            val_error={
                "status": 201,
                "message":"Transaction date is Required."
                        }
            return Response(val_error)    
        try: 
            data["voucher_number"]
        except:   
            val_error={
                "status": 201,
                "message":"Voucher Number is Required."
                        }
            return Response(val_error)
        try: 
            data["remarks"]
        except:   
            val_error={
                "status": 201,
                "message":"Remarks is Required."
                        }
            return Response(val_error)     
        try: 
            accounts=data["accounts"]
        except:   
            val_error={
                "status": 201,
                "message":"Accounts is Required."
                        }
            return Response(val_error) 
        for account in accounts:
            try:
                account["account_name"]
            except:
                val_error={
            "status": 201,
            "message":"Account Name is Required."
                    }
                return Response(val_error)                    
#validation
        data=request.data
        print(auth)
        print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,",data)
        try:
            cid=auth["data"]["User"]["company_id"]
            user_data={"company_id":cid}
            data.update(user_data)
        except :
            cid=auth["is_company_user"]["User"]["company_id"]
            user_data={"company_id":cid}
            data.update(user_data)
        
        transaction_id  = data["transaction_id"]
        if not  Transactions.objects.filter(transaction_id=transaction_id).exists():
                errdata= {
                        "status": 201,
                        "message":'Transaction  dose not exist'
                        }
                return Response(errdata)
        else:
            user= Transactions.objects.get(transaction_id=transaction_id)
            ser = CtreateTransactionSerializer(user,data=data,partial=True)
            if ser.is_valid(raise_exception=True):
                ser.save()
                data= {
                        "status": 200,
                        "message":'Transaction updated successfully'
                        }
                return Response(data)
            else:
                data={
                    "status":201,
                    "message":ser.errors
                }                 
                return Response(data)    
#end
#List transaction account   
class ListTransactionsView(APIView):
    def get(self,request):
#permission 
        try:
            auth=permission_all(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission 
#params
        try:
            data=request.query_params
            transaction_name=data["transaction_name"]
        except :
            data={
                "status": 206,
                "message": "Invalid header"
                 }
            return Response(data)      
#params 
        try:
            user_id=auth["is_company_user"]["User"]["user_id"]
            data=Transactions.objects.filter(user_id=user_id,transaction_name=transaction_name)
        except:
            company_id=auth["is_company_user"]["User"]["company_id"]
            data=Transactions.objects.filter(company_id=company_id,transaction_name=transaction_name) 
        try:       
            transection_data=[]
            for obj in data:
                ser = getTransactionsSerializer(obj)
                accountData=transactionAccount.objects.filter(transaction_id=ser.data["transaction_id"])
                accountser=transactionAccountSerializer(accountData, many=True)
                acdata={"accounts":accountser.data}
                serdata=ser.data
                serdata.update(acdata)
                transection_data.append(serdata)                   
            if not data:
                data={
                        "status": 201,
                        "message": "Transaction not found",
                            }
                return Response (data)
            errdata= {
                        "status": 200,
                        "message":"success",
                        "data":transection_data
                            }
            return Response(errdata)  
        except :
            data={
                        "status": 201,
                        "message": "Transaction not found",
                            }
            return Response (data)

#end
#List transaction account   
class UserListTransactionsView(APIView):
    def get(self,request):
#permission 
        try:
            auth=permission_all(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission 
#params
        try:
            data=request.query_params
            transaction_name=data["transaction_name"]
        except :
            data={
                "status": 206,
                "message": "Invalid header"
                 }
            return Response(data)      
#params 
        try:
            user_id=auth["is_company_user"]["User"]["user_id"]
        except:
            if auth["is_company_user"]["User"]["company_id"]:
                data={
                "status": 207,
                "message": "Not a user account please login as user first"
                 }
                return Response(data) 
            user_id=auth['data']['User']['user_id'] 
        try:       
            data=Transactions.objects.filter(user_id=user_id,transaction_name=transaction_name)
            transection_data=[]
            for obj in data:
                ser = TransactionsSerializer(obj)
                accountData=transactionAccount.objects.filter(transaction_id=ser.data["transaction_id"])
                accountser=transactionAccountSerializer(accountData, many=True)
                acdata={"accounts":accountser.data}
                serdata=ser.data
                serdata.update(acdata)
                transection_data.append(serdata)                   
            if not data:
                data={
                        "status": 201,
                        "message": "Transaction not found",
                            }
                return Response (data)
            errdata= {
                        "status": 200,
                        "message":"success",
                        "data":transection_data
                            }
            return Response(errdata)  
        except :
            data={
                        "status": 201,
                        "message": "Transaction not found",
                            }
            return Response (data)

#end
# Delete transaction account
class DeleteTransactionsView(APIView):
    def delete(self,request):
#params
        try:
            data=request.query_params
            transaction_id=data["transaction_id"]
        except :
            data={
                "status": 201,
                "message": "Invalid header"
                 }
            return Response(data)      
#params 

#permission 
        try:
            auth=permission_delete(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission
        if not  Transactions.objects.filter(transaction_id=transaction_id).exists():
                errdata= {
                        "status": 201,
                        "message":'transaction dose not exist'
                        }
                return Response(errdata)
        else:
            user= Transactions.objects.get(transaction_id=transaction_id)
            user.delete()
            data={
                "status":200,
                "message":"transaction deleted succesfully"
                }
            return Response(data)
#end
        
class transactionsDetailsView(APIView):

    def get(self,request):
#params
        try:
            data=request.query_params
            transaction_id=data["transaction_id"]
        except :
            data={
                "status": 201,
                "message": "Invalid header"
                 }
            return Response(data)      
#params             
#permission 
        try:
            auth=permission_view(request.META["HTTP_AUTHORIZATION"])
            if not auth[0]["status"]==200:
                return Response (auth[0],auth[1])
        except:
            if auth["status"]==200:
                pass
            else:
                data={
                    "status": 205,
                    "message": "Unauthorized"
                    }
                return Response(data)
#permission   
        try:
            Transactions.objects.get(transaction_id=transaction_id)
        except:
            errdata= {
                        "status": 201,
                        "message":'transaction Dose Not Exist'
                        }
            return Response(errdata)
        else:
            user=Transactions.objects.get(transaction_id=transaction_id)
            ser = TransactionsSerializer(user)
            accountData=transactionAccount.objects.filter(transaction_id=transaction_id)
            accountser=transactionAccountSerializer(accountData, many=True)
            acdata={"accounts":accountser.data}
            serdata=ser.data
            serdata.update(acdata)
            data= {
                    "status": 200,
                    "message":"success",
                    "data":serdata
                        }
            return Response(data)
#end of transaction