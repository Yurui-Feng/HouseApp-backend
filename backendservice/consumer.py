import os, django, pika, json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from houses.models import House

rabbitmq_url = os.environ.get('CLOUDAMQP_URL')
params = pika.URLParameters(rabbitmq_url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='config')

def callback(ch, method, properties, body):
    print('Received in config')
    id = json.loads(body)
    print(id)

    house = House.objects.get(id=id)
    if house.likes:
        house.likes = house.likes + 1
        house.save()
        print('House likes increased')
    else:
        house.checks += 1
        house.save()
        print('House checks increased')

channel.basic_consume(queue='config', on_message_callback=callback, auto_ack=True)

print('Started consuming')

channel.start_consuming()

channel.close()
