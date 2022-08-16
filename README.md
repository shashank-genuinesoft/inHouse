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

* **Sample Call:**

  ```javascript
        var request = require('request');
        var options = {
        'method': 'POST',
        'url': 'https://inhouse-api.herokuapp.com/companyRegistration',
        'headers': {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "company_name": "GENUINE",
            "company_address": "309,abv,rajendra nagar indore",
            "tax_number": "1224535432345",
            "commercial_year": "2022",
            "company_email": "abc@gmail.com",
            "mobile_number": "7685457690",
            "password": "auweguiybvjdfhbvjb"
        })

        };
        request(options, function (error, response) {
        if (error) throw new Error(error);
        console.log(response.body);
        });
  ```
