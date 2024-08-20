### Steps
1. Create Virtual Environment
2. Install Django
```bash 
pip install Django==4.2.9
```
3. Install Django Rest Framework
```bash
pip install djangorestframework
```
4. SuperUserPassword 
* Creating Superuser
```bash
python manage.py createsuperuser --username admin --email admin@voyagefleet.com
```
* Changing password
```bash
python manage.py changepassword
```
* Default Credintial for SuperUser 
```
    username = admin 
    password = SudinKri
```
5. add groups
[Add new Group](http://127.0.0.1:8000/admin/auth/group/add/)
* staff_driver
* customer
* staff_support
* admin

### Notes

#### Roles in VoyageFleet
In the **VoyageFleet** system, the user groups can be organized to reflect the different roles within the system. Here are some possible user groups:

1. **Customer**
   - **Role:** Users who book rides using the system.
   - **Permissions:**
      - Can view available vehicles.
      - Can book rides.
      - Can view their booking history and status.
      - Can cancel bookings before they start.

2. **Driver**
   - **Role:** Users who are responsible for driving the vehicles.
   - **Permissions:**
      - Can view assigned bookings.
      - Can update the status of bookings (e.g., mark as `RUNNING`, `COMPLETED`).
      - Can update location of ther Vechicle

3. **Administrator**
   - **Role:** Users who manage the entire system.
   - **Permissions:**
      - Can manage users (add, remove, assign groups).
      - Can manage vehicles (add, update, remove).
      - Can view all bookings and their statuses.
      - Can assign vehicles to drivers.
      - Can view and manage system settings.

5. **Support Staff**
   - **Role:** Users who provide customer support.
   - **Permissions:**
      - Can view and manage customer bookings.
      - Can assist with booking issues, cancellations, and modifications.
      - Can view customer and driver profiles.


##### Summary

- **Customer**: Books and manages their rides.
- **Driver**: Manages rides they are assigned to.
- **Administrator**: Full control over the system.
- **Support Staff**: Assists customers and manages booking-related issues.

These groups help in organizing the permissions and roles, ensuring that each user has access only to the functionality they need.


### API
1. User Management
a. Customer Management
<details>
<summary><code>POST</code> <code><b>/</b></code> <code>(overwrites all in-memory stub and/or proxy-config)</code></summary>
url: http://127.0.0.1:8000/userMgmt/customer/
* To create New Customer
  method: POST
  Body:
  ```json
  {
      "user": {
          "username": "abhinas",
          "email": "abhinas@gmail.com",
          "first_name": "Abhinas",
          "last_name": "Poudel",
          "password": "poudelAbhi"
      },
      "phone_number": "9843568166",
      "address": "Namobuddha, Nepal",
      "date_of_birth": "1998-02-05",
      "gender": "M"
  }
  ```
</details>

#### User Management

##### Customer Management

<details>
  <summary>
    <code>POST</code> 
    <code><b>/userMgmt/customer/</b></code> <code>Create New Customer</code>
  </summary>

###### Parameters

> | name      |  type     | data type               | description                                                           |
> |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
> | None      |  required | JSON   | N/A  |


##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `201`         | `text/plain;charset=UTF-8`        | `Configuration created successfully`                                |
> | `400`         | `application/json`                | `{"code":"400","message":"Bad Request"}`                            |
> | `405`         | `text/html;charset=utf-8`         | None                                                                |

##### Example cURL

> ```javascript
>  curl -X POST -H "Content-Type: application/json" --data @post.json http://localhost:8889/
> ```

</details>

URL: http://127.0.0.1:8000/userMgmt/customer/
Method: POST
Body: 
    1. {
        "user": {
            "username": "abhinas",
            "email": "abhinas@gmail.com",
            "first_name": "Abhinas",
            "last_name": "Poudel",
            "password": "poudelAbhi"
        },
        "phone_number": "9843568166",
        "address": "Namobuddha, Nepal",
        "date_of_birth": "1998-02-05",
        "gender": "M"
    }

    2. {
        "user": {
            "username": "nishal",
            "email": "nishal@gmail.com",
            "first_name": "Nishal",
            "last_name": "Shrestha",
            "password": "nishalPassword"
        },
        "phone_number": "9843626886",
        "address": "Banepa, Nepal",
        "date_of_birth": "1998-05-08",
        "gender": "M"
    }
    3. {
        "user": {
            "username": "sidhartha",
            "email": "sidhartha@gmail.com",
            "first_name": "Sidhartha",
            "last_name": "Shrestha",
            "password": "password"
        },
        "phone_number": "9843000000",
        "address": "Panauti, Nepal",
        "date_of_birth": "1998-05-18",
        "gender": "M"
    }