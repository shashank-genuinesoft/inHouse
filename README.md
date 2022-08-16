
# API LIST

Complete api list with doc refrence link.

##  
**Gaming**
* [/companyRegistration](https://github.com/shashank-genuinesoft/inHouse/tree/main#company-registration) -   Creates company login account.
* [/companyVarification](https://github.com/shashank-genuinesoft/inHouse/tree/main#company-verification) - API for Company login.
* [/companyLogin](https://github.com/shashank-genuinesoft/inHouse/tree/main#company-login) - API for Company login.




----
**Company Registration**
----
  Creates company login account.

* **URL**

  /companyRegistration

* **Method:**

  `POST`
  
*  **URL Params**

   **Required:**
 
     None

* **Data Params**

  **Required:**

    `
    "company_name":"GENUINE",
    "company_address":"309,abv,rajendra nagar indore",
    "tax_number":"1224535432345",
    "commercial_year":"2022",
    "company_email":"abc@gmail.com",
    "mobile_number":"7685457690",
    "password":"auweguiybvjdfhbvjb"
                `


**Optional:**
 
    NONE

* **Success Response:**

* **Code:** 200 

  **Content:**
  
        {

        "status": 200,

        "message": "Registered Successfully",

        "data": "Otp has been send!!"

        }

* **Error Response:**

  * **Code:** 404 NOT FOUND
  
    **Content:** 
    
    `{ error : "Wrong url." }`



----
**Company Verification**
----
  Otp verification of company account.

* **URL**

  /companyVarification

* **Method:**

  `POST`
  
*  **URL Params**

   **Required:**
 
     None

* **Data Params**

  **Required:**

      "company_email":"shashankpathe@gmail.com",

      "otp": "123245"

**Optional:**
 
    NONE

* **Success Response:**

* **Code:** 200 

  **Content:**
  
              {
          "status": "200",
          "Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NjA3MjExMzMsIlVzZXIiOnsiY29tcGFueV9pZCI6MSwiY29tcGFueV9uYW1lIjoic3RzIiwiY29tcGFueV9hZGRyZXNzIjoiMzA2LCBqYXdhaGFyIG5hZ2FyIGluZG9yZSIsInRheF9udW1iZXIiOiIxMjMzMSIsImNvbW1lcmNpYWxfeWVhciI6IjIwMjIiLCJjb21wYW55X2VtYWlsIjoic2hhc2hhbmtwYXRoZUBnbWFpbC5jb20iLCJtb2JpbGVfbnVtYmVyIjoiNzU2NDM0NTY1NCIsImlzVmVyaWZpZWQiOnRydWV9fQ.joYSZYV6WuqwG236LHwZL5lOrE03ygvrB6f9DP5FZPo",
          "data": {
                  "company_id": 1
                    }
             }

* **Error Response:**

  * **Code:** 404 NOT FOUND
  
    **Content:** 
    
    `{ error : "Wrong url." }`


----
**Company Login**
----
  Company Login module.

* **URL**

  /companyLogin

* **Method:**

  `POST`
  
*  **URL Params**

   **Required:**
 
     None

* **Data Params**

  **Required:**

      "company_email":"shashankpathe@gmail.com",

      "password": "doremon"

**Optional:**
 
    NONE

* **Success Response:**

* **Code:** 200 

  **Content:**
  
              {
          "status": "200",
          "Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NjA3MjExMzMsIlVzZXIiOnsiY29tcGFueV9pZCI6MSwiY29tcGFueV9uYW1lIjoic3RzIiwiY29tcGFueV9hZGRyZXNzIjoiMzA2LCBqYXdhaGFyIG5hZ2FyIGluZG9yZSIsInRheF9udW1iZXIiOiIxMjMzMSIsImNvbW1lcmNpYWxfeWVhciI6IjIwMjIiLCJjb21wYW55X2VtYWlsIjoic2hhc2hhbmtwYXRoZUBnbWFpbC5jb20iLCJtb2JpbGVfbnVtYmVyIjoiNzU2NDM0NTY1NCIsImlzVmVyaWZpZWQiOnRydWV9fQ.joYSZYV6WuqwG236LHwZL5lOrE03ygvrB6f9DP5FZPo",
          "data": {
                  "company_id": 1
                    }
             }

* **Error Response:**

  * **Code:** 404 NOT FOUND
  
    **Content:** 
    
    `{ error : "Wrong url." }`

