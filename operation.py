import datetime
import re

class Operation:
    def __init__(self):
        pass

    # Assumptions
    # All years:BE, All inputs: '%m/%d/%Y'
    # Concern: In fact, year may be both AD and BE, Date input can be in different format.
    @staticmethod
    def iso_date_converter(date_str, key="date"):
        try:
            be_date = datetime.datetime.strptime(date_str, '%m/%d/%Y').date()
            ad_date = datetime.date(
                be_date.year-543, be_date.month, be_date.day)
            iso_date = ad_date.isoformat()
            return (key, iso_date)
        except Exception as e:
            return e

    # Assume that each record has only firstname and lastname
    @staticmethod
    def separate_firstname_lastname(fullname, key=["firstname", "lastname"]):
        arr_name_splitted = fullname.split()
        if len(arr_name_splitted) >= 3:
            return Exception("Invalid Name")
        elif len(arr_name_splitted) == 1:
            return ((key[0], arr_name_splitted[0]), (key[1], ""))
        elif len(arr_name_splitted) == 2:
            return ((key[0], arr_name_splitted[0]), (key[1], arr_name_splitted[1]))

    # Use 4 * to mask all emails
    # Does not handle the case like t@gmail.com
    @staticmethod
    def masking_email(email, key="email"):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email) is None:
            return Exception("Invalid Email")
        splitted_email = email.split("@")
        email_name = splitted_email[0]
        splitted_email[0] = email_name[0] + ("*"*4) + email_name[-1]
        return (key, "@".join(splitted_email))

# Demonstrating how to extend the functionality by using inheritance.


class MoreOperation(Operation):
    @staticmethod
    def masking_phonenumber(phonenumber, key="phonenumber"):
        if not re.match(r'^[\d_\- ]+$', phonenumber):
            return Exception("Invalid Phone Number")
        phone_digits_only = re.sub(r"\D", "", phonenumber)
        if len(phone_digits_only) == 10:
            return (key, f"{phonenumber[:3]}{'*' * 5}{phonenumber[-2:]}")
        else:
            return Exception("Invalid Phone Number")
