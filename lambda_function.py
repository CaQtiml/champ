from operation import MoreOperation
from data_source import DataSource

def lambda_handler(event, context):
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
    data_source.upload_csv_to_s3()