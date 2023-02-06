import json
import boto3
import sys
import yfinance as yf
import time
import random
import datetime


# Your goal is to get per-hour stock price data for a time range for the ten stocks specified in the doc.
# Further, you should call the static info api for the stocks to get their current 52WeekHigh and 52WeekLow values.
# You should craft individual data records with information about the stockid, price, price timestamp, 52WeekHigh and 52WeekLow values and push them individually on the Kinesis stream




KINESIS_DATA_STREAM = "stock_data_stream"

kinesis_handle = boto3.client('kinesis', region_name = "us-east-1")


# Function to push data in the kinesis stream, partition key of kinesis stream is stock_name itself
def insert_kinesis_stream(message, partition_key):
        response = kinesis_handle.put_record(
                                StreamName=KINESIS_DATA_STREAM,
                                Data = message,
                                PartitionKey=partition_key
                        )
        return response



# name of all the stocks which data eeds to be pulled from the yfinance library
stock_list = ["MSFT", "MVIS", "GOOG", "SPOT", "INO", "OCGN", "ABML", "RLLCF", "JNJ", "PSFE"]

stock_list_str = ' '.join(stock_list)

today = datetime.date.today()
yesterday = today - datetime.timedelta(1)

# Code to pull the data for the stocks specified in the doc
stocks_data = yf.download(stock_list_str, start= yesterday, end= today, interval = '1h' )
print("Print the downloaded data: ")
print((stocks_data))

# iterating over each data points we got by making the download API call 
for stocks_data_point in stocks_data.index:
        collected_timestamp = stocks_data_point.strftime("%Y-%m-%d %H:%M:%S%z")
        collected_date = stocks_data_point.strftime("%Y-%m-%d")

        # Iterating over ech stock to access more relevant information for each stock
        for stock_item in stock_list:

                # Getting data for each stock 
                stock_info = yf.Ticker(stock_item)
                 # Collating all the necessary information into a dictionary, same dictinary will be later pushed in the kinesis stream 
                stock_item_data = {}
                stock_item_data["stockName"] = stock_item
                stock_item_data["timestamp"] = collected_timestamp
                stock_item_data["date"] = collected_date

                stock_item_data["stockPrice"] = stocks_data.loc[stocks_data_point]['Close'][stock_item]

                stock_item_data["fiftyTwoWeekHigh"] = stock_info.info["fiftyTwoWeekHigh"]
                stock_item_data["fiftyTwoWeekLow"] = stock_info.info["fiftyTwoWeekLow"]


                message = {}
                
                # Coverting the dictionary data into indiviudal JSON object
                message = json.dumps(stock_item_data)
                # Doing final check to ignore data points which has Noe in them  
                if stock_item_data["stockPrice"] != None:
                        response = insert_kinesis_stream(message, stock_item)
                        print(response)


