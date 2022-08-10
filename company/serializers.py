from rest_framework import serializers
from . models import *
from . helpers import *
from django.contrib.auth.hashers import make_password, check_password

# used to create company account
class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Companies
        fields="__all__" 
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        
        return super(CompaniesSerializer, self).create(validated_data)
# used to create user

# user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields="__all__"
        fields=fields = ['user_id', 'company_id', 'first_name', 'last_name', 'email', 'mobile_number','permission_view','permission_create','permission_update','permission_delete',"password"]       
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)   
#end   
class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields=fields = ['user_id', 'company_id', 'first_name', 'last_name', 'email', 'mobile_number','permission_view','permission_create','permission_update','permission_delete']
        #extra_kwargs = {"first_name": {"error_messages": {"required": "Give yourself a username"}},"company_id": {"error_messages": {"required": "Give yourself a username"}}}

# serializer for company login
class LoginSerializer(serializers.Serializer):
    company_email = serializers.CharField( label="company_email", write_only=True)
    password = serializers.CharField(label="Password",style={'input_type': 'password'}, trim_whitespace=False, write_only=True)

    def validate(self, attrs):
        # Take username and password from request
        company_email = attrs.get('company_email')
        password = attrs.get('password')
        try:
            Companies.objects.get(company_email=company_email)
        except:
           
            data={
                "status": 201,
                "message": "Wrong Company Email",
                }
            return data
        if not company_email:
            data={
                "status": 201,
                "message": "Wrong Email",
                }
            return data
        else:
            pass    
        if company_email and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(self,request=self.context.get('request'),company_email=company_email, password=password)
            
            if not user:
                data={
                "status": 201,
                "message": "Wrong Password",
                }
                return data
        else:
            data={
            "status": 201,
            "message": "Password is Required.",
            }
            return data
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs
class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField( label="email", write_only=True)
    password = serializers.CharField(label="Password",style={'input_type': 'password'}, trim_whitespace=False, write_only=True)

    def validate(self, attrs):
        # Take username and password from request
        email = attrs.get('email')
        password = attrs.get('password')
        if not email:
            data={
                "status": 201,
                "message": " Email is Required ",
                }
            return data

        if email and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticateMyUser(self,request=self.context.get('request'),email=email, password=password)
            
            if not user:
                # If we don't have a regular user, raise a ValidationError
                data={
                "status": 201,
                "message": " Wrong Password",
                }
                return data
        else:
            data={
            "status": 201,
            "message": "Password is Required.",
            }
            return data
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs

#group master serializer
class GroupMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=GroupMaster
        fields="__all__"
#end
#group master serializer
class GetGroupMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=GroupMaster
        fields=("group_master_id","company_id","group_name")
#end
#group master serializer
class GetGroupMasterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=GroupMaster
        fields=("group_master_id","company_id","group_under","group_name","group_nature","pl_affect")
    def to_representation(self, instance):
        rep = super(GetGroupMasterviewSerializer, self).to_representation(instance)
        rep['group_under'] = instance.group_under.group_name
        return rep
#end
#Ledger master serializer
class LedgerMasterDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=LedgerMaster
        fields="__all__"

class LedgerMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=LedgerMaster
        fields="__all__"
    def to_representation(self, instance):
        rep = super(LedgerMasterSerializer, self).to_representation(instance)
        rep['group_under'] = instance.group_under.group_name
        return rep    
#end
#transactionAccount master serializer
class transactionAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=transactionAccount
        fields="__all__"
#end
from datetime import datetime
import time
#transaction master serializer
class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transactions
        fields=("transaction_id","company_id","transaction_name","voucher_number","remarks","transaction_date","created_at")
    
#end
#transaction master serializer
class getTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transactions
        fields=("transaction_id","company_id","transaction_name","voucher_number","remarks","transaction_date","created_at")
    def to_representation(self, instance):
        representation = super(getTransactionsSerializer, self).to_representation(instance)
        representation['transaction_date'] = instance.transaction_date.strftime("%d/%m/%Y")
        return representation
#end

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Users()
#         fields ="__all__"
#         def create(self, validated_data):
#             validated_data['password'] = make_password(validated_data['password'])
#             return super(UserSerializer, self).create(validated_data)
        
class CtreateTransactionSerializer(serializers.ModelSerializer):
    accounts= transactionAccountSerializer(many=True)

    class Meta:
        model=Transactions
        fields="__all__"

    def create(self, validated_data):
        accounts = validated_data.pop('accounts')
        transaction_instance = Transactions.objects.create(**validated_data)
        for account in accounts:
            transactionAccount.objects.create(transaction_id=transaction_instance,**account)
        return transaction_instance

    def update(self, instance, validated_data):
        accounts=validated_data.pop("accounts")
        instance.voucher_number = validated_data.get('voucher_number', instance.voucher_number)
        instance.transaction_name = validated_data.get('transaction_name', instance.transaction_name)
        instance.transaction_date = validated_data.get('transaction_date', instance.transaction_date)
        instance.remarks = validated_data.get('remarks', instance.remarks)
        instance.save()
        user_hobby_with_same_instance=transactionAccount.objects.filter(transaction_id=instance.pk).values_list('account_id', flat=True)
        hobbies_id_pool = []
        temp=0
        for hobby in accounts:  
            if user_hobby_with_same_instance:
                inst=user_hobby_with_same_instance
                try:
                    transactionAccount.objects.filter(pk=inst[temp]).exists()
                    hobby_instance = transactionAccount.objects.get(pk=inst[temp])
                    hobby_instance.account_name = hobby.get('account_name', hobby_instance.account_name)
                    hobby_instance.account_debit_amount = hobby.get('account_debit_amount', hobby_instance.account_debit_amount)
                    hobby_instance.account_credit_amount = hobby.get('account_credit_amount', hobby_instance.account_credit_amount)
                    hobby_instance.save()
                    
                    hobbies_id_pool.append(hobby_instance.account_id)
                except:
                    hobbies_instance = transactionAccount.objects.create(transaction_id=instance, **hobby)
                    hobbies_id_pool.append(hobbies_instance.account_id)
            else:
                hobbies_instance = transactionAccount.objects.create(transaction_id=instance, **hobby)
                hobbies_id_pool.append(hobbies_instance.account_id)
            temp += 1
        for hobby_id in user_hobby_with_same_instance:
            if hobby_id not in hobbies_id_pool:
                transactionAccount.objects.filter(pk=hobby_id).delete() 
        return instance


