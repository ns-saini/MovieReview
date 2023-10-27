# import cursor as cursor
import time

import pandas
import pika
import sys



# SENDING DATA FROM HERE:
# Defining Credentials
credentials = pika.PlainCredentials('myuser', 'mypassword')

# Define Connection Parameters
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='35.168.68.133',
                              port=5672,
                              credentials=credentials, virtual_host='/'))
channel = connection.channel()

#
print("Reading The TSV File....................")
df = pandas.read_csv('data.tsv', usecols=['nconst', 'primaryName', 'birthYear', 'deathYear', 'primaryProfession'],
                     header=0, sep='\t')

print("Converting To JSON The TSV File....................")
# df.to_json('file.json', orient='records')#file.json file name where jason records are written
df.replace(to_replace='\\N', value=None, inplace=True)
df.rename(columns={"nconst": "id", "primaryName": "name", "birthYear": "birth_year", "deathYear": "death_year"},
          inplace=True)

count = 1

for index, row in df.iterrows():
    op = row.to_json()
    channel.basic_publish(exchange='name_exchange', routing_key='crud_service_name_queue', body=op)
    print(" [x] Sent %r" % op)
    count = count + 1
    if count % 1000 == 0:
        time.sleep(5)
        print("sleeping for 5 seconds")
# After This Send JSON Data Line By Line from file.json to Message QUEUE of RabbitMQ

#DEFINE LOGIC TO READ FILE WITH JSON DATA HERE.

# print(" [x] Sent %r" % message)
connection.close()
