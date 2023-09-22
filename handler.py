from boto3 import client as boto3_client
import boto3
import face_recognition
import pickle
import os

input_bucket = "cc-input-p2"
output_bucket = "cc-output-p2"

access_key = '#######'
secret_key = '###############'
region_name = 'us-east-1'

s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region_name)
dynamodb = boto3.resource('dynamodb', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region_name)


# Function to read the 'encoding' file
def open_encoding(filename):
    file = open(filename, "rb")
    data = pickle.load(file)
    file.close()
    return data

def face_recognition_handler(event, context):
    print("Hello")
    #get the event details from lambda function (s3)
    #s3 bucket name
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    print(s3_bucket)
    s3_object_key = event['Records'][0]['s3']['object']['key']
    print(s3_object_key)
    #Dowload files from S3_input
    # local_file_path = '/Users/venkatasai/Downloads/s3_videos'
    path = '/tmp/'
    video_file_path = str(path) + s3_object_key
    s3.download_file(s3_bucket, s3_object_key, video_file_path)
    print("video_downloaded")
    # Create frames directory if it does not exist
    frames_path = "/tmp/frames/"
    if not os.path.exists(frames_path):
        os.makedirs(frames_path)
    # Execute FFmpeg command to extract frames
    os.system("ffmpeg -i " + str(video_file_path) + " -r 1 " + str(frames_path) + "image-%3d.jpeg")
    print("extracted frames")
    #get the first frame
    # List all files in the frames directory
    files = os.listdir(frames_path)
    #get the first frame
    for frame in files:
        image = face_recognition.load_image_file(os.path.join(frames_path, frame))
        faces_array = face_recognition.face_encodings(image)
        #if faces detected
        if(len(faces_array)>0):
            result_image=faces_array[0]
            break
    print(result_image)
    print("extracted face in first frame")

    #assigning encoding file with path to variable
    encoding_file='/home/app/encoding'
    known_face_encodings=open_encoding(encoding_file)
    boolean_values=face_recognition.compare_faces(known_face_encodings['encoding'], result_image)
    #getting the index of the first occurrence of True in the list boolean_values
    index=0
    for value in boolean_values:
        if value==True:
            break
        index += 1
    person_name = list(known_face_encodings['name'])[index]
    print(person_name)
    csv_content=dynamo_db(person_name,s3_object_key)
    return csv_content


def dynamo_db(person_name,s3_object_key):
# Specify the table name and the key of the item to retrieve
    table_name = 'cc-p2-student-info'
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'name': person_name})
    if 'Item' in response:
        item = response['Item']
        csv_content = f"{item['name']},{item['major']},{item['year']}"
        s3.put_object(Bucket=output_bucket, Key=s3_object_key.replace(".mp4", ".csv"), Body=csv_content)
        return csv_content



