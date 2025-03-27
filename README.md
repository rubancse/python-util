S3 creates an event when a new file is uploaded.
The S3 event triggers an AWS Lambda function.   
The Lambda function uses the Databricks Jobs API to start a Databricks job, passing the S3 file path as a parameter.
The Databricks job processes the file.
