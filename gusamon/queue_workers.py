import random

import pika
from pydantic import parse_raw_as

from gusamon.messages import Message
from gusamon.settings import Settings


TypeOptions = [True, False]
NounOptions = [
    "V1", "Zero", "Sora", "Gregorius Techneticies", "Gordon Freeman"
]
AdjectiveOptions = [
    "Funny", "Cool", "Sus", "Aggressive", "Greggy"
]


class QueueWorker:
    def __init__(self) -> None:
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=Settings.rabbitmq.host,
                credentials=pika.PlainCredentials(
                    username=Settings.rabbitmq.username,
                    password=Settings.rabbitmq.password
                )
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(Settings.rabbitmq.queue)

    def __del__(self) -> None:
        self.connection.close()


class Producer(QueueWorker):
    def __init__(self) -> None:
        super().__init__()

    def produce_one(self):
        is_epic = random.choice(TypeOptions)

        noun = random.choice(NounOptions)
        adjective = random.choice(AdjectiveOptions)
        text = f"{noun} is {adjective}"

        message = Message(is_epic=is_epic, payload=text)
        self.channel.basic_publish(
            exchange="", routing_key=Settings.rabbitmq.queue, body=message.json()
        )


class Consumer(QueueWorker):
    def __init__(self, subscribe: bool = False) -> None:
        super().__init__()
        if subscribe:
            self.subscribe()

    def subscribe(self):
        self.channel.basic_consume(
            queue=Settings.rabbitmq.queue,
            on_message_callback=self.consume,
            auto_ack=True
        )

    def start(self):
        self.channel.start_consuming()

    def consume(self, ch, method, peoperties, body):
        message = parse_raw_as(Message, body)
        print(f"{message.is_epic=}, {message.payload=}")
