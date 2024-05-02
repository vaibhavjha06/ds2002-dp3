#!/usr/bin/env python3

import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/fhy5uh"
sqs = boto3.client('sqs')

answer_dict = {}

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

def get_message():
    for m in range(0,10):
        try:
        # Receive message from SQS queue. Each message has two MessageAttributes: order and word
        # You want to extract these two attributes to reassemble the message
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ]
            )
            # Check if there is a message in the queue or not
            if "Messages" in response:
                # extract the two message attributes you want to use as variables
                # extract the handle for deletion later
                order = response['Messages'][0]['MessageAttributes']['order']['StringValue']
                word = response['Messages'][0]['MessageAttributes']['word']['StringValue']
                handle = response['Messages'][0]['ReceiptHandle']

                # Print the message attributes - this is what you want to work with to reassemble the message
                print(f"Order: {order}")
                print(f"Word: {word}")

                # Insert in dictionary
                answer_dict[order] = word

                # Delete
                delete_message(handle)

            # If there is no message in the queue, print a message and exit    
            else:
                print("No message in the queue")
                exit(1)
                
        # Handle any errors that may occur connecting to SQS
        except ClientError as e:
            print(e.response['Error']['Message'])

# Trigger the function
if __name__ == "__main__":
    get_message()
print(answer_dict)

# Order dictionary by keys
sorted_dict = dict(sorted(answer_dict.items()))
print(sorted_dict)

# Pull values and form sentence
sentence = " ".join(str(v) for v in sorted_dict.values())
print(sentence)


# Sentence formed!: People who know what they're talking about don't need PowerPoint.


# Delete message
# Called delete_message within get_message function to to delete the message using its handle.
# Got confirmation "Message deleted" for each message in queue

