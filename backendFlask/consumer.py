import pika, json, os

from core import House, db

rabbitmq_url = os.environ.get('CLOUDAMQP_URL')
params = pika.URLParameters(rabbitmq_url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='core')

def callback(ch, method, properties, body):
    print('Received in core')
    data = json.loads(body)
    print(data)

    # Check the content type and perform the appropriate action
    # For example, if the content type is 'house_created', then create a new house
    # the content type is equal to the name of the method in the producer
    # why? because the producer sends the content type as the method
    # and pika.BasicProperties's first argument is the content type
    if properties.content_type == 'house_created':
        house = House(id=data['id'], name=data['name'], image=data['image'], description=data['description'])
        db.session.add(house)
        db.session.commit()
        print('House Created')

    elif properties.content_type == 'house_updated':
        house = House.query.get(data['id'])
        house.name = data['name']
        house.image = data['image']
        house.description = data['description']
        db.session.commit()
        print('House Updated')

    elif properties.content_type == 'product_deleted':
        house = House.query.get(data)
        db.session.delete(house)
        db.session.commit()
        print('House Deleted')
    
channel.basic_consume(queue='core', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()