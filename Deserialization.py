import pika
import payment_request_pb2

def callback(ch, method, properties, body):
    request = payment_request_pb2.PaymentRequest()
    request.ParseFromString(body)
    print("Payment received:")
    print("Sender:", request.sender_id)
    print("Amount:", request.amount)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a fanout exchange and bind a unique queue
channel.exchange_declare(exchange='payment_fanout', exchange_type='fanout')
queue = channel.queue_declare(queue='', exclusive=True)  # Unique, temporary queue
queue_name = queue.method.queue
channel.queue_bind(exchange='payment_fanout', queue=queue_name)

# Start consuming
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print("Waiting for messages...")
channel.start_consuming()
