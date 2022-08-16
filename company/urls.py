from django.urls import path  
from .views import *
urlpatterns = [  

    path("",home),
    #path("test",test.as_view()),
#transaction account
    # path("createtransactionAccount",CreateTransactionAccountView.as_view()),
    # path("updatetransactionAccount",UpdateTransactionAccountView.as_view()),
    # path("listtransactionAccount",ListtransactionAccountView.as_view()),
    # path("deletetransactionAccount",DeletetransactionAccountView.as_view()),
#end    
#Login
    path("companyRegistration",CompanyRegistration.as_view()),
    path("companyLogin",CompanyLogin.as_view()),
    path("companyVarification",varificationView.as_view()),
    path("resendOtp",resendOtpView.as_view()),
    path("forgetPasswordOtp",ResetPasswordView.as_view()),
    path("VerifyOtp",resetPassvarificationView.as_view()),
    path("changeForgetPassword",passwordVerifyView.as_view()),
    path("ChangePassword",UpdatePasswordView.as_view()),
    
#User
    path("createUser",CreateUser.as_view()),
    path("userLogin",UserLogin.as_view()),
    path("allUsers",AllUsers.as_view()),
    path("updateUser",UpdateUser.as_view()),
    path("deleteUser",DeleteUser.as_view()),
    
#Group master
    path("groupMaster",GroupMasterView.as_view()),
    path("listGroupMaster",ListGroupMasterView.as_view()),
    path("getGroupUnder",ListGroupMasterDefault.as_view()),
    path("updateGroupMaster",UpdateGroupMaster.as_view()),
    path("deleteGroupMaster",DeleteGroupMaster.as_view()),
  
#ledger
    path("createLedgerMaster",LedgerMasterView.as_view()),
    path("listLedgerMaster",ListLedgerMasterView.as_view()),
    path("updateLedgerMaster",UpdateLedgerMasterView.as_view()),
    path("deleteLedgerMaster",DeleteLedgerMasterView.as_view()),
#end

#transaction transaction
    path("createTransaction",CreateTransactionsView.as_view()),
    path("updateTransaction",UpdateTransactionsView.as_view()),
    path("listTransaction",ListTransactionsView.as_view()),
    path("userListTransaction",UserListTransactionsView.as_view()),
    path("deleteTransaction",DeleteTransactionsView.as_view()),
    path("transactionDetails/",transactionsDetailsView.as_view()),
#end
#user details 
    path("userDetails/",userDetailsView.as_view()),
    path("getUserPermissions",getUserPermissions.as_view()),
    path("groupMasterDetails/",groupMasterDetailsView.as_view()),
    path("LedgerMasterDetails/",LedgerMasterDetailsView.as_view()),
    
]


