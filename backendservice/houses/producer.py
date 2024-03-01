import pika, json
import os

rabbitmq_url = os.environ.get('CLOUDAMQP_URL')
params = pika.URLParameters(rabbitmq_url)

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='core', body=json.dumps(body), properties=properties)