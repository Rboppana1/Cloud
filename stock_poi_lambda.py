from pprint import pprint
import boto3
import json
import csv
import datetime
import os
import random
import base64
from decimal import Decimal
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    
    AWS_REGION = 'us-east-1'
    print(event)
    
    dynamodb_res = boto3.resource('dynamodb', region_name=AWS_REGION)
    stock_poi_table = dynamodb_res.Table('stock_poi_data')

    sns_client = boto3.client('sns', region_name=AWS_REGION)
    topic_arn = "arn:aws:sns:us-east-1:755358636241:stock_poi"

    for record in event['Records']:
        data_point = base64.b64decode(record['kinesis']['data'])
        data_point = str(data_point, 'utf-8')
        #pprint(data_point, sort_dicts=False)
        data_point = json.loads(data_point)

        poi_type = ''

        if data_point["stockPrice"] <= (1.2 * int(data_point["fiftyTwoWeekLow"])):
            poi_type = "Low PoI"
        elif data_point["stockPrice"] >= (0.8 * int(data_point["fiftyTwoWeekHigh"])):
            poi_type = "High PoI"

        if (poi_type):
            search_data = {'stockName': data_point["stockName"], 'poiDate': data_point["timestamp"][0:10]}
            response = stock_poi_table.get_item(Key=search_data)
            if ('Item' not in response):
                poi_data = {'stockName': data_point["stockName"], 
                            'poiDate': data_point["timestamp"][0:10], 
                            'timestamp': data_point["timestamp"], 
                            'stockPrice': data_point["stockPrice"],
                            'poiType': poi_type}
                
                poi_data = json.loads(json.dumps(poi_data), parse_float=Decimal)
                response = stock_poi_table.put_item(Item=poi_data)
                #pprint("DB Response Data: ", response)
                sns_client.publish(TopicArn=topic_arn, 
                                    Message=str("On the date of " + poi_data["poiDate"] + " In " + poi_data["stockName"] + " Stock, "  + poi_data["poiType"] + " is detected, because of hitting the value of : " + str(poi_data["stockPrice"])) , 
                                    Subject=str(poi_data["poiType"] + " in " + poi_data["stockName"]))
            

    return 1