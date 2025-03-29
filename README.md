1) S3 creates an event when a new file is uploaded.
2)The S3 event triggers an AWS Lambda function.   
3)The Lambda function uses the Databricks Jobs API to start a Databricks job, passing the S3 file path as a parameter.
The Databricks job processes the file.

4)This is the most direct and versatile way to start Databricks jobs programmatically. You'll need to make HTTP POST requests to the API endpoint.
curl -n -X POST \
  -H "Authorization: Bearer <your_databricks_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": 123,
    "notebook_params": {
      "input_date": "2025-03-26",
      "data_source": "s3://your-bucket/data/"
    },
    "run_name": "Programmatic Run - March 26"
  }' \
  "https://<your_databricks_workspace>/api/2.1/jobs/run-now"

5) Get information about a specific job run
curl -n -X GET \
  -H "Authorization: Bearer <your_databricks_token>" \
  "https://<your_databricks_workspace>/api/2.1/jobs/runs/get?run_id=456"




import boto3
import json
import requests
import os

def lambda_handler(event, context):
    # Databricks instance details and job configuration
    databricks_host = os.environ['DATABRICKS_HOST']
    databricks_token = os.environ['DATABRICKS_TOKEN']
    job_id = os.environ['DATABRICKS_JOB_ID']

    # API endpoint for running Databricks job
    api_version = '/api/2.1'
    api_command = '/jobs/run-now'
    url = f"https://{databricks_host}{api_version}{api_command}"

    # Request headers
    headers = {
        "Authorization": f"Bearer {databricks_token}",
        "Content-Type": "application/json"
    }

    # Request payload
    data = json.dumps({"job_id": job_id})

    try:
        # Make the API request
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Databricks job triggered successfully',
                'response': response.json()
            })
        }
    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to trigger Databricks job',
                'error': str(e),
                'response': response.text
            })
        }



```python
import boto3
import json
from pyspark.sql import SparkSession

s3 = boto3.client('s3')
dbracks = boto3.client('databricks')

def lambda_handler(event, context):
    # Get the file name from the S3 event
    file_name = event['Records'][0]['s3']['key']

    # Start the Databricks job
    try:
        dbracks.run_job(
            job_id='your_job_id',
            cluster_id='your_cluster_id',
            node_type='standard_xlarge',
            num_workers=1,
            spark_history_location='dbfs:/FileStore/historic Jobs'
        )
    except Exception as e:
        print(f"Error starting Databricks job: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    # Get the status of the Databricks job
    try:
        response = dbracks.get_job(job_id='your_job_id')
        job_status = response['jobStatus']
        print(f"Job status: {job_status}")
        return {
            'statusCode': 200,
            'body': json.dumps({'status': job_status})
        }
    except Exception as e:
        print(f"Error getting Databricks job status: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    # Wait for the job to finish
    while True:
        try:
            response = dbracks.get_job(job_id='your_job_id')
            job_status = response['jobStatus']
            if job_status == 'completed':
                break
        except Exception as e:
            print(f"Error checking job status: {e}")
            time.sleep(10)

    return {
        'statusCode': 200,
        'body': json.dumps({'status': job_status})
    }
```
**Step 6: Create an S3 event**

Create an S3 event that triggers the Lambda function when a file is uploaded to the S3 bucket. You can 
do this by going to the Events section in the Lambda console and creating a new event with the 
following settings:

* Event type: Object created
* Event source: Your S3 bucket name
* Prefix: Your file prefix (e.g., `my-files/`)
* Suffix: Your file suffix (e.g., `.csv`)

**Step 7: Deploy and test**

Deploy your Lambda function and wait for the file to 


import boto3
import json
import requests
import os

def lambda_handler(event, context):
    # Databricks instance details and job configuration
    databricks_host = os.environ['DATABRICKS_HOST']
    databricks_token = os.environ['DATABRICKS_TOKEN']
    job_id = os.environ['DATABRICKS_JOB_ID']

    # API endpoint for running Databricks job
    api_version = '/api/2.1'
    api_command = '/jobs/run-now'
    url = f"https://{databricks_host}{api_version}{api_command}"

    # Request headers
    headers = {
        "Authorization": f"Bearer {databricks_token}",
        "Content-Type": "application/json"
    }

    # Request payload
    data = json.dumps({"job_id": job_id})

    try:
        # Make the API request
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Databricks job triggered successfully',
                'response': response.json()
            })
        }
    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to trigger Databricks job',
                'error': str(e),
                'response': response.text
            })
        }
