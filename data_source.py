import datetime
import argparse
import re
import csv
import pandas as pd
import os
from s3 import S3Service
import datetime

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
        self.s3_service = S3Service()
        self.input_filename = self.args.input
        self.valid_output_filename = self.args.voutput
        self.invalid_output_filename = self.args.ioutput

    def csv_to_dataframe(self):
        df = pd.read_csv(self.input_filename)

    def download_file(self, bucket_path, local_path):
        self.s3_service.download(bucket_path, local_path)

    def get_data_from_input(self, field_names):
        arr_data = []
        bucket_path = "/".join(["input", self.input_filename])
        local_path = "sample.csv"
        self.s3_service.download(bucket_path, local_path)
        with open(local_path, mode='r', encoding='utf8') as csv_file:
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
        self.write_csv_from_dict(self.invalid_output_filename, arr_invalid_data)
    
    def upload_csv_to_s3(self):
            now = datetime.datetime.now()
            date_str = now.strftime("%d%b%y")
            self.s3_service.upload(self.valid_output_filename, f"output/good_{date_str}.csv")
            self.s3_service.upload(self.invalid_output_filename, f"output/bad_{date_str}.csv")
