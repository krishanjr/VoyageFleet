import json
import APIFunctions
import restAPIhelper
from restAPIhelper import Response



def validate_register_customer_form(inputs : dict):
    print("Validation: input", inputs["user"])

    #validate if password is empty
    if len(inputs["user"]["password"])<7:
        return "Too short Password"
    # validate if password and re type password is same or not
    if inputs["user"]["password"] != inputs["user"]["retype_password"]:
        return "Passwords do not match."
    
    inputs["user"].pop("retype_password")
    return inputs

def validate_register_staff_form(inputs : dict):
    print("Validation: input", inputs["user"])

    #validate if password is empty
    if len(inputs["user"]["password"])<7:
        return "Too short Password"

    return inputs

def validate_register_driver_form(inputs : dict):
    print("Validation: input", inputs["user"])

    #validate if password is empty
    if len(inputs["user"]["password"])<7:
        return "Too short Password"

    return inputs

def validate_vehicle_form(inputs: dict):
    return inputs

def loginCustomer(credential) -> Response:
    return APIFunctions.login_api(user_type="customer", auth=credential)

def loginStaff(credential) -> Response:
    return APIFunctions.login_api(user_type="support", auth=credential)