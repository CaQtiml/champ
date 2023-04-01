import datetime
import argparse
import re
import csv


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
        pattern = r'^[\d_\- ]+$'
        if re.match(pattern, phonenumber) is None:
            return Exception("Invalid Phone Number")
        phone_digits_only = re.sub(r"\D", "", phonenumber)
        if len(phone_digits_only) == 10:
            return (key, phonenumber[0:3] + ("*"*5) + phonenumber[-2] + phonenumber[-1])
        else:
            return Exception("Invalid Phone Number")

# Not sure how to make DataSource to receive data from another source.


class DataSource:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Enter the data source information')
        parser.add_argument('-i', '--input', type=str, help='Input Filename')
        parser.add_argument('-vo', '--voutput', type=str,
                            help='Valid Output Filename')
        parser.add_argument('-io', '--ioutput', type=str,
                            help='Invalid Output Filename')
        self.args = parser.parse_args()
        self.input_filename = self.args.input
        self.valid_output_filename = self.args.voutput
        self.invalid_output_filename = self.args.ioutput

    def get_data_from_input(self, field_names):
        arr_data = []
        with open(self.input_filename, mode='r', encoding='utf8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                data = {field_names[i]: row[i]
                        for i in range(0, len(field_names))}
                arr_data.append(data)
        return arr_data

    def write_csv_from_dict(self, filename, arr):
        with open(filename, mode='w', encoding='utf8', newline='') as csv_file:
            valid_fieldnames = list(arr[0].keys())
            writer = csv.DictWriter(csv_file, fieldnames=valid_fieldnames)
            writer.writeheader()
            for data in arr:
                writer.writerow(data)

    def give_result_csv(self, arr_valid_data, arr_invalid_data):
        self.write_csv_from_dict(self.valid_output_filename, arr_valid_data)
        self.write_csv_from_dict(
            self.invalid_output_filename, arr_invalid_data)


if __name__ == '__main__':
    data_source = DataSource()
    input_field_names = ['date', 'fullname', 'email', 'phonenumber']
    arr_valid_output = []
    arr_invalid_output = []
    cleaning_functions = [
        (MoreOperation.iso_date_converter, "date"),
        (MoreOperation.separate_firstname_lastname, "fullname"),
        (MoreOperation.masking_email, "email"),
        (MoreOperation.masking_phonenumber, "phonenumber")
    ]

    all_input_data = data_source.get_data_from_input(input_field_names)
    for input_data in all_input_data:
        print(input_data)
        valid_flag = True
        dict_cleaned_input_data = {}
        for function, key in cleaning_functions:
            results = function(input_data[key])
            if isinstance(results, Exception):
                arr_invalid_output.append(input_data)
                valid_flag = False
                break
            if key != "fullname":
                dict_cleaned_input_data[results[0]] = results[1]
            else:
                for result in results:
                    dict_cleaned_input_data[result[0]] = result[1]
        if valid_flag:
            arr_valid_output.append(dict_cleaned_input_data)

    data_source.give_result_csv(arr_valid_output, arr_invalid_output)
