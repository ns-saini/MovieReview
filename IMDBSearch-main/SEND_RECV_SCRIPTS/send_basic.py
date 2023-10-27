# import cursor as cursor
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
df = pandas.read_csv('data_basic.tsv', usecols=['tconst', 'primaryTitle', 'runtimeMinutes', 'genres'],
                     header=0, sep='\t')

print("Converting To JSON The TSV File....................")
# df.to_json('file.json', orient='records')#file.json file name where jason records are written
df.replace(to_replace='\\N', value=None, inplace=True)
df.rename(columns={"tconst": "id", "primaryTitle": "primary_title", "runtimeMinutes": "runtime_minutes", "genres": "genres"},
          inplace=True)

for index, row in df.iterrows():
    op = row.to_json()
    channel.basic_publish(exchange='basic_exchange', routing_key='crud_service_basic_queue', body=op)
    print(" [x] Sent %r" % op)

# After This Send JSON Data Line By Line from file.json to Message QUEUE of RabbitMQ

#DEFINE LOGIC TO READ FILE WITH JSON DATA HERE.

# print(" [x] Sent %r" % message)
connection.close()
