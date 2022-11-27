import argparse
import time

from gusamon.queue_workers import Producer, Consumer


def run_producer():
    producer = Producer()
    for _ in range(60):
        producer.produce_one()
        time.sleep(1)


def run_consumer():
    consumer = Consumer(subscribe=True)
    consumer.start()


def main():
    arguments = argparse.ArgumentParser()
    arguments.add_argument("--produce", action="store_true")
    arguments.add_argument("--consume", action="store_true")
    args = arguments.parse_args()

    should_produce: bool = args.produce
    should_consume: bool = args.consume

    if not should_produce and not should_consume:
        print("No producer/consumer mode specified")
        arguments.print_help()
        return

    if should_produce and should_consume:
        print("Cannot produce and consume at the same node.")
        return

    if should_produce:
        run_producer()

    if should_consume:
        run_consumer()


if __name__ == "__main__":
    main()
