import datetime
import argparse
import re
import csv

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
