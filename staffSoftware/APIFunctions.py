from restAPIhelper import RestConsumer, append_to_url

class CustomerAPI:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/userMgmt/customer/"

    def create_customer(self, new_customer_data):
        """Register new customer data."""
        rest_consumer = RestConsumer(self.base_url)
        return rest_consumer.post(json=new_customer_data)

    def get_customer(self, customer_id, **kwargs):
        """Get customer data by ID."""
        get_url = append_to_url(self.base_url, str(customer_id))
        rest_consumer = RestConsumer(get_url)
        return rest_consumer(**kwargs)

    def get_all_customers(self, **kwargs):
        """Get all customers detail"""
        rest_consumer = RestConsumer(self.base_url)
        return rest_consumer(**kwargs)

    def update_customer(self, customer_id, customer_data, **kwargs):
        """Update customer data by ID."""
        _url = append_to_url(self.base_url, str(customer_id))
        rest_consumer = RestConsumer(_url)
        return rest_consumer.patch(json=customer_data, **kwargs)

    def delete_customer(self, customer_id, **kwargs):
        """Delete customer data by ID."""
        _url = append_to_url(self.base_url, str(customer_id))
        rest_consumer = RestConsumer(_url)
        return rest_consumer.delete(**kwargs)

class StaffAPI:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/userMgmt/support/"

    def create_staff(self, new_staff_data):
        """Register new staff data."""
        rest_consumer = RestConsumer(self.base_url)
        return rest_consumer.post(json=new_staff_data)

    def get_staff(self, staff_id, **kwargs):
        """Get staff data by ID."""
        get_url = append_to_url(self.base_url, str(staff_id))
        rest_consumer = RestConsumer(get_url)
        return rest_consumer(**kwargs)

    def get_all_staffs(self, **kwargs):
        """Get all staffs detail"""
        rest_consumer = RestConsumer(self.base_url)
        return rest_consumer(**kwargs)

    def update_staff(self, staff_id, staff_data, **kwargs):
        """Update staff data by ID."""
        _url = append_to_url(self.base_url, str(staff_id))
        rest_consumer = RestConsumer(_url)
        return rest_consumer.patch(json=staff_data, **kwargs)

    def delete_staff(self, staff_id, **kwargs):
        """Delete staff data by ID."""
        _url = append_to_url(self.base_url, str(staff_id))
        rest_consumer = RestConsumer(_url)
        return rest_consumer.delete(**kwargs)

class DriverAPI:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/userMgmt/driver/"

    def create_driver(self, new_driver_data):
        """Register new driver data."""
        rest_consumer = RestConsumer(self.base_url)
        return rest_consumer.post(json=new_driver_data)
    
    def get_driver(self, driver_id, **kwargs):
        """Get driver data by ID."""
        get_url = append_to_url(self.base_url, str(driver_id))
        rest_consumer = RestConsumer(get_url)
        return rest_consumer(**kwargs)

    def get_all_drivers(self, **kwargs):
        """Get all drivers detail"""
        rest_consumer = RestConsumer(self.base_url)
        return rest_consumer(**kwargs)

    def update_driver(self, driver_id, driver_data, **kwargs):
        """Update driver data by ID."""
        _url = append_to_url(self.base_url, str(driver_id))
        rest_consumer = RestConsumer(_url)
        return rest_consumer.patch(json=driver_data, **kwargs)

    def delete_driver(self, driver_id, **kwargs):
        """Delete driver data by ID."""
        _url = append_to_url(self.base_url, str(driver_id))
        rest_consumer = RestConsumer(_url)
        return rest_consumer.delete(**kwargs)
    
class VehicleAPI:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/vehicleMgmt/vehicles/"

    def create(self, new_driver_data, **kwargs):
        """Register new driver data."""
        rest_consumer = RestConsumer(self.base_url)
        return rest_consumer.post(json=new_driver_data, **kwargs)
    
    def get(self, driver_id, **kwargs):
        """Get driver data by ID."""
        get_url = append_to_url(self.base_url, str(driver_id))
        rest_consumer = RestConsumer(get_url)
        return rest_consumer(**kwargs)

    def get_all(self, **kwargs):
        """Get all drivers detail"""
        rest_consumer = RestConsumer(self.base_url)
        return rest_consumer(**kwargs)

    def update(self, driver_id, driver_data, **kwargs):
        """Update driver data by ID."""
        _url = append_to_url(self.base_url, str(driver_id))
        rest_consumer = RestConsumer(_url)
        return rest_consumer.patch(json=driver_data, **kwargs)

    def delete(self, driver_id, **kwargs):
        """Delete driver data by ID."""
        _url = append_to_url(self.base_url, str(driver_id))
        rest_consumer = RestConsumer(_url)
        return rest_consumer.delete(**kwargs)

class BookingAPI:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/vehicleMgmt/booking/"

    def create(self, new_driver_data, **kwargs):
        """Register new Booking data."""
        rest_consumer = RestConsumer(self.base_url)
        return rest_consumer.post(json=new_driver_data, **kwargs)
    
    def get(self, driver_id, **kwargs):
        """Get booking data by ID."""
        get_url = append_to_url(self.base_url, str(driver_id))
        rest_consumer = RestConsumer(get_url)
        return rest_consumer(**kwargs)

    def get_all(self, **kwargs):
        """Get all booking detail"""
        rest_consumer = RestConsumer(self.base_url)
        return rest_consumer(**kwargs)

    def update(self, driver_id, driver_data, **kwargs):
        """Update booking data by ID."""
        _url = append_to_url(self.base_url, str(driver_id))
        rest_consumer = RestConsumer(_url)
        return rest_consumer.patch(json=driver_data, **kwargs)

    def delete(self, driver_id, **kwargs):
        """Delete booking data by ID."""
        _url = append_to_url(self.base_url, str(driver_id))
        rest_consumer = RestConsumer(_url)
        return rest_consumer.delete(**kwargs)

def login_api(user_type, **kwargs):
    match user_type:
        case "customer":
            _url = "http://127.0.0.1:8000/userMgmt/users/customer/login/"
        case "support":
            _url = "http://127.0.0.1:8000/userMgmt/users/support/login/"
        case "driver":
            _url = "http://127.0.0.1:8000/userMgmt/users/driver/login/"
    rest_consumer = RestConsumer(_url)
    return rest_consumer(**kwargs)


if __name__=='__main__':
    customerAPI = CustomerAPI()
    newCustomerData = {
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
    #print(customerAPI.create_customer(newCustomerData)) 

    print(customerAPI.get_customer(10, auth=("sidhartha","password")))

    print(customerAPI.get_all_customers(auth=("sidhartha","password")))

    credential = ("sidhartha","password")
    ret = customer_login_api(auth=credential)
    print(ret, type(ret))