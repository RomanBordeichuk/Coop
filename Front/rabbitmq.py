import pika
from .config import *

# queue_ = config.rmq_queue

class ClientRabbit:
    def __init__(self) -> None:
        self.exchange_ = 'direct_faces'
        self.exchange_type = 'direct'
        self.rmq_channel = None

    def channelCreating(self):
        rmq_parameters = pika.URLParameters(f'amqp://{rmq_user}:{rmq_password}@{rmq_host}:{rmq_port}')
        rmq_connection = pika.BlockingConnection(rmq_parameters)
        self.rmq_channel = rmq_connection.channel()
        self.rmq_channel.exchange_declare(self.exchange_, exchange_type=self.exchange_type)

    
    def sendData(self, message, key):
        self.channelCreating()

        self.rmq_channel.basic_publish(exchange=self.exchange_, routing_key=key, body=message)

    def clearQueue(self):
            self.channelCreating()

            queue_ = self.rmq_channel.queue_declare(queue='', durable=True).method.queue
            self.rmq_channel.queue_delete(queue=queue_)

    def declareFunc(self, severity, callback) -> None: 
        self.channelCreating()
        
        queue_ = self.rmq_channel.queue_declare(queue='', durable=True).method.queue
        self.rmq_channel.queue_bind(queue=queue_, exchange=self.exchange_, routing_key=severity)
        self.rmq_channel.basic_consume(queue=queue_, on_message_callback=callback, auto_ack=True)
    
    def startConsuming(self):
        self.channelCreating()

        self.rmq_channel.start_consuming()

    


# def receive(key):
#     exchange_ = "direct_faces"

#     rmq_parameters = pika.URLParameters(f'amqp://{config.rmq_user}:{config.rmq_password}@{config.rmq_host}:{config.rmq_port}')
#     rmq_connection = pika.BlockingConnection(rmq_parameters)
#     rmq_channel = rmq_connection.channel()


#     result = rmq_channel.queue_declare(queue='', durable=True)
#     queue_name = result.method.queue
#     print("queue name: ", queue_name)
#     rmq_channel.queue_bind(queue=queue_name, exchange=exchange_, routing_key=key)

#     method_frame, header_frame, body = rmq_channel.basic_get(queue = queue_name)        
    
#     rmq_channel.basic_ack(method_frame.delivery_tag)
#     rmq_connection.close() 
#     return body