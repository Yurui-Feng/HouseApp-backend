import pika, json, os

rabbitmq_url = os.environ.get('CLOUDAMQP_URL')
params = pika.URLParameters(rabbitmq_url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='config', body=json.dumps(body), properties=properties)