import json

import requests

def get_registration_code(mobile_number, invitee_mobile_number):
    payload = {
        "Request":{
            "mobile_number": mobile_number,
            "invitee_mobile_number":invitee_mobile_number
        }
    }

    res = requests.post("https://mobiloantest.mfs.co.ke/api/v1/registration_code",
                  json=payload)

    res_json_str = res.content.decode('utf-8')
    res_json = json.loads(res_json_str)


def estatement_opt_in(mobile_number, customer_email, customer_id_number):
    payload = {
        "Request":{
            "mobile_number": mobile_number,
            "customer_email": customer_email,
            "customer_id_number": customer_id_number
        }
    }