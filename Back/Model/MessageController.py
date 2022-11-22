import pika
from pika import exchange_type
from .config import *



# unused 

# Maybe, for Future

class ServerRabbit:
    
    exchange_ : str = 'direct_faces'
    exchange_type : str = 'direct'
    rmq_channel = None
    
    @staticmethod
    def channelCreating():
        rmq_parameters = pika.URLParameters(f'amqp://{rmq_user}:{rmq_password}@{rmq_host}:{rmq_port}')
        rmq_connection = pika.BlockingConnection(rmq_parameters)
        ServerRabbit.rmq_channel = rmq_connection.channel()
        ServerRabbit.rmq_channel.exchange_declare(ServerRabbit.exchange_, exchange_type=ServerRabbit.exchange_type)

    @staticmethod
    def sendData(message, key, channel=None):
        if channel == None:
            ServerRabbit.channelCreating()

        ServerRabbit.rmq_channel.basic_publish(exchange=ServerRabbit.exchange_, routing_key=key, body=message)

    @staticmethod
    def clearQueue():
            ServerRabbit.channelCreating()

            queue_ = ServerRabbit.rmq_channel.queue_declare(queue='', durable=True).method.queue
            ServerRabbit.rmq_channel.queue_delete(queue=queue_)
    
    @staticmethod
    def declareFunc(severity, callback) -> None: 
        ServerRabbit.channelCreating()
        
        queue_ = ServerRabbit.rmq_channel.queue_declare(queue='').method.queue
        ServerRabbit.rmq_channel.queue_bind(queue=queue_, exchange=ServerRabbit.exchange_, routing_key=severity)
        ServerRabbit.rmq_channel.basic_consume(queue=queue_, on_message_callback=callback, auto_ack=True)
    
    @staticmethod
    def startConsuming():
        ServerRabbit.channelCreating()

        ServerRabbit.rmq_channel.start_consuming()
