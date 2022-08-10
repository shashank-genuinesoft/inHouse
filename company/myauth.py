from rest_framework.response import Response
from datetime import datetime, timedelta,timezone
import time
from rest_framework import status
import jwt
# to verify token       
PREFIX = 'Bearer '
def is_company_user(header):
    if not header.startswith(PREFIX):
        data={
            "status": 201,
            "message": "Invalid token",

             }
        code=401
        return data,code
    token=header[len(PREFIX):] 
    try:
        myobj=jwt.decode(token, "secret", algorithms=["HS256"])
        try:
            myobj["User"]["company_name"]
            data={
            "status": 200,
            "is_company_user": myobj,
             }
            return data
        
        except:
            try:
                myobj["User"]["permission_update"]
                data={
                "status": 204,
                "message": "You dont have permission for this action",
                }
                code=401
                return data,code
            except:
                pass    
        data={
            "status": 200,
            "is_company_user": myobj,
             }
        
        return data
    except :
        data={
            "status": 202,
            "message": "token expired"
             }
        code=401
        return data,code

#to verify token  

# to verify token view permission       
PREFIX = 'Bearer '
def permission_view(header):
    if not header.startswith(PREFIX):
        data={
            "status": 202,
            "message": "Invalid token",
             }
        code=401
        return data,code
    token=header[len(PREFIX):] 
    try:
        myobj=jwt.decode(token, "secret", algorithms=["HS256"])
        try:
            print(myobj["User"]["company_name"])
            data={
            "status": 200,
            "is_company_user": myobj,
             }
           
            return data
        
        except:
            try:
                myobj["User"]["permission_view"] 
                if not myobj["User"]["permission_view"] == "YES":
                    data={
                    "status": 204,
                    "message": "You dont have permission for this action",
                    }
                else:
                    data={
                    "status": 200,
                    "message": "ok",
                    "data":myobj
                    }
            
                return data
            except:
                pass    
        data={
            "status": 200,
            "is_company_user": myobj,
             }
        
        return data
    except :
        data={
            "status": 202,
            "message": "token expired",
             }
        code=401
        return data,code 

#to verify token view permission      
# to verify token create permission       
PREFIX = 'Bearer '
def permission_create(header):
    if not header.startswith(PREFIX):
        data={
            "status": 203,
            "message": "Invalid token",
             }
        code=401
        return data,code
    token=header[len(PREFIX):] 
    try:
        myobj=jwt.decode(token, "secret", algorithms=["HS256"])
        try:
            myobj["User"]["company_name"]
            data={
            "status": 200,
            "is_company_user": myobj,
             }
            
            return data
        
        except:
            try:
                myobj["User"]["permission_create"] 
                
                if not myobj["User"]["permission_create"] == "YES":
                    data={
                    "status": 204,
                    "message": "You dont have permission for this action",
                    }
                else:
                    data={
                    "status": 200,
                    "message": "ok",
                    "data":myobj
                    }
                return data
            except:
                pass    
        data={
            "status": 200,
            "is_company_user": myobj,
             }
       
        return data
    except :
        data={
            "status": 202,
            "message": " token expired",
             }
        code=401
        return data,code 

#to verify token view permission      
# to verify token create permission       
PREFIX = 'Bearer '
def permission_update(header):
    if not header.startswith(PREFIX):
        data={
            "status": 203,
            "message": "Invalid token",

             }
        code=401
        return data,code
    token=header[len(PREFIX):] 
    try:
        myobj=jwt.decode(token, "secret", algorithms=["HS256"])
        try:
            myobj["User"]["company_name"]
            data={
            "status": 200,
            "is_company_user": myobj,
             }
            return data
        
        except:
            try:
                myobj["User"]["permission_update"] 
                if not myobj["User"]["permission_update"] == "YES":
                    data={
                    "status": 204,
                    "message": "You dont have permission for this action",
                    }
                else:
                    data={
                    "status": 200,
                    "message": "ok",
                    }
                return data
            except:
                pass    
        data={
            "status": 200,
            "is_company_user": myobj,
             }
       
        return data
    except :
        data={
            "status": 202,
            "message": " token expired",
             }
        code=401
        return data,code 

#to verify token view permission      
# to verify token create permission       
PREFIX = 'Bearer '
def permission_delete(header):
    if not header.startswith(PREFIX):
        data={
            "status": 203,
            "message": "Invalid token",

             }
        code=401
        return data,code
    token=header[len(PREFIX):] 
    try:
        myobj=jwt.decode(token, "secret", algorithms=["HS256"])
        try:
            myobj["User"]["company_name"]
            data={
            "status": 200,
            "is_company_user": myobj,
             }
           
            return data
        
        except:
            try:
                myobj["User"]["permission_delete"] 
                if not myobj["User"]["permission_delete"] == "YES":
                    data={
                    "status": 204,
                    "message": "You dont have permission for this action",
                    }
                else:
                    data={
                    "status": 200,
                    "message": "ok",
                    }
                return data
            except:
                pass    
        data={
            "status": 200,
            "is_company_user": myobj,
             }
        return data
    except :
        data={
            "status": 202,
            "message": "token expired",
             }
        code=401
        return data,code

#to verify token view permission      

# to verify token view permission       
PREFIX = 'Bearer '
def permission_all(header):
    if not header.startswith(PREFIX):
        data={
            "status": 202,
            "message": "Invalid token",
             }
        code=401
        return data,code
    token=header[len(PREFIX):] 
    try:
        myobj=jwt.decode(token, "secret", algorithms=["HS256"])
        try:
            data={
            "status": 200,
            "is_company_user": myobj,
             }
            
            return data
        except:
            try:
                myobj["User"]["permission_view"] 
                data={
                "status": 200,
                "message": "ok",
                "data":myobj
                }
                
                return data
            except:
                pass    
        data={
            "status": 200,
            "is_company_user": myobj,
             }
     
        return data
    except :
        data={
            "status": 202,
            "message": "token expired",
             }
        code=401
        return data,code

#to verify token view permission 