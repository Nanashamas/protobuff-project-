import pika
import payment_request_pb2

# Create a PaymentRequest object
request = payment_request_pb2.PaymentRequest()
request.sender_id = "user123"
request.receiver_id = "merchant456"
request.amount = 100.50
request.currency = "USD"
request.description = "Payment for services"
request.timestamp = "2024-12-06T12:00:00Z"

# Serialize the object
serialized_request = request.SerializeToString()

# Connect to RabbitMQ and declare a fanout exchange
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='payment_fanout', exchange_type='fanout')

# Publish the message to the fanout exchange
channel.basic_publish(exchange='payment_fanout', routing_key='', body=serialized_request)

print("Payment request broadcasted.")
connection.close()
