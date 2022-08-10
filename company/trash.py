

class test(APIView):
    def post(self,request):
        data=request.data
        
#validation
        try: 
            data["company_name"]
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
            data["company_email"]
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
#end validation
        return Response("thanks")



# create transection account
class CreateTransactionAccountView(APIView):
    def post(self,request):
#permission 
        try:
            auth=permission_create(request.META["HTTP_AUTHORIZATION"])
            if not auth["status"]==200:
                return Response (auth)
        except:
            data={
                "status": 201,
                "message": "Unauthorized"
                 }
            return Response(data)
#permission
        data=request.data
        ser = TransectionAccountSerializer(data=data)
        if ser.is_valid():
            ser.save()
            response_data={
                    "status": 200,
                    "message": "Transection Account created successfully"
                      }
            return Response (response_data)
        response_data={
                    "status": 201,
                    "message":ser.errors,
                      }   
        return Response(response_data)
# end

#update transection
class UpdateTransactionAccountView(APIView):
    def put(self,request):
#permission 
        try:
            auth=permission_update(request.META["HTTP_AUTHORIZATION"])
            if not auth["status"]==200:
                return Response (auth)
        except:
            data={
                "status": 201,
                "message": "Unauthorized"
                 }
            return Response(data)
#permission
        data=request.data
        try:
            account_id  = data["account_id"]
        except :
                data = {
                    "status": 201,
                    "message":{
                         "account_id": 
                                    "This field is required."
                                    
                    }}
                return Response(data)
       
        if not  TransectionAccount.objects.filter(account_id=account_id).exists():
                errdata= {
                        "status": 201,
                        "message":'Transection account dose not exist'
                        }
                return Response(errdata)
        else:
            user= TransectionAccount.objects.get(account_id=account_id)
            ser = TransectionAccountSerializer(user,data=data,partial=True)
            if ser.is_valid(raise_exception=True):
                ser.save()
                data= {
                        "status": 200,
                        "message":'Transection account updated successfully'
                        }
                return Response(data)
            else:
                data={
                    "status":201,
                    "message":ser.errors
                }                 
                return Response(data)    
#end

#List transection account   
class ListTransectionAccountView(APIView):
    def get(self,request):
#permission 
        try:
            auth=permission_view(request.META["HTTP_AUTHORIZATION"])
            if not auth["status"]==200:
                return Response (auth)
        except:
            data={
                "status": 201,
                "message": "Unauthorized"
                 }
            return Response(data)
#permission 
        data= TransectionAccount.objects.all()
        ser = TransectionAccountSerializer(data, many=True)
        
        if not data:
            data={
                    "status": 201,
                    "message": "Transection account not found",
                        }
            return Response (data)
        errdata= {
                    "status": 200,
                    "message":"success",
                    "data":ser.data
                        }
        return Response(errdata)  
#end

# Delete transection account
class DeleteTransectionAccountView(APIView):
    def delete(self,request):
#params
        try:
            data=request.query_params
            account_id=data["account_id"]
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
            if not auth["status"]==200:
                return Response (auth)
        except:
            data={
                "status": 201,
                "message": "Unauthorized"
                 }
            return Response(data)
#permission
        if not  TransectionAccount.objects.filter(account_id=account_id).exists():
                errdata= {
                        "status": 201,
                        "message":'Transection account dose not exist'
                        }
                return Response(errdata)
        else:
            user= TransectionAccount.objects.get(account_id=account_id)
            user.delete()
            data={
                "status":200,
                "message":"Transection account deleted succesfully"
                }
            return Response(data)
#end