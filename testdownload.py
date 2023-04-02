from s3 import S3Service

s3 = S3Service()

s3.download("output/bad_02Apr23.csv", "download_test\\bad_02Apr23.csv")