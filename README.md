# Smart-Classroom-Assistant-AWS-Lambda
Our cloud app will implement a smart classroom assistant for educators. This assistant takes videos from the user’s classroom, performs face recognition on the collected videos using AWS Lambda, looks up the recognized students in the Dynamo DB database, and returns the relevant academic information of each student back to the user and also stores it in AWS S3.

![Alt text](https://github.com/priyaavijay/Smart-Classroom-Assistant-AWS-Lambda/blob/main/Smart%20Classroom%20Architecture.png)

Steps to setup:
Created input and output S3 buckets.
Created the dynamo_db table and loaded the data from the “student.json” to the table.
Docker Desktop is installed.
Image is created by using the command “docker build.”
After the image is created, by using command “docker images” get the latest image and
tag the image using “docker tag 353e3d63ff4c 067895197847.dkr.ecr.us-east-
1.amazonaws.com/cc_project_2“command. By using the command “docker push
067895197847.dkr.ecr.us-east-1.amazonaws.com/cc_project_2” push the image to ECR
repository
Lambda function is created with the S3_input_bucket event trigger and then deployed
the image from the ECR Repository.
In the workload generator set the input and output bucket names accordingly and run the
workload generator for both the test cases.
