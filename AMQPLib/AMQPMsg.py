"""
Connect to an AMQP server and sent messages to a certain queue
"""
import pika
from robot.api import logger


def _receive_callback(chan, method, properties, body):
    print("AMQP received: {}".format(body))
    return body


class AMQPMsg(object):
    """
    Connect to an AMQP server and receive messages or send messages in Robotframework
    """
    def __init__(self, heartbeat=10, timeout=5):
        self.amqp_addr = ""
        self.amqp_connection = None
        self.amqp_channel = None
        self.exchange = ""
        self.routing_key = ""
        self.queue = ""
        # self.amqp_heartbeat = heartbeat
        self.amqp_timeout = timeout

    def init_amqp_connection(self, amqp_host, amqp_port, amqp_user, amqp_pass, amqp_vhost):
        """
        Init the connection to the amqp server

        Example:

        *** Keywords ***
        Before tests
            Init AMQP connection    ${amqp_host}  ${amqp_port}   ${amqp_user}  ${amqp_pass}   ${amqp_vhost}
        """
        self.amqp_addr = "amqp://{user}:{passwd}@{host}:{port}/{vhost}".format(user=amqp_user,
                                                                               passwd=amqp_pass,
                                                                               host=amqp_host,
                                                                               port=amqp_port,
                                                                               vhost=amqp_vhost)

        logger.debug("AMQP connect to: {}".format(self.amqp_addr))
        params = pika.URLParameters(self.amqp_addr)
        self.amqp_connection = pika.BlockingConnection(parameters=params)
        self.amqp_channel = self.amqp_connection.channel()

    def close_amqp_connection(self):
        """
        Close the amqp connection
        Usage:

        *** Keywords ***
        After tests
            close amqp connection
        """
        self.amqp_connection.close()

    def set_amqp_destination(self, exchange, routing_key):
        """
        Set destination for subsequent send_amqp_msg calls

        :param exchange:    amqp exchange name
        :param routing_key: amqp routing_key
        """
        self.exchange = exchange
        self.routing_key = routing_key

    def set_amqp_queue(self, amqp_queue):
        """
        Set queue to listen to and declare it on AMQP server for the subsequent get_amqp_msg calls

        :param amqp_queue string:
        """
        self.queue = amqp_queue
        self.amqp_channel.queue_declare(queue=self.queue)

    def send_amqp_msg(self, msg, exchange=None, routing_key=None):
        """
        Send one message via AMQP

        :param msg:
        :param exchange: name of the exchange to send the message to; default: self.exchange
        :param routing_key: the routing key to use; default is self.routing_key
        """
        amqp_exchange = exchange if exchange is not None else self.exchange
        amqp_routing_key = routing_key if routing_key is not None else self.routing_key

        logger.debug("AMQP send ---> ({} / {})".format(amqp_exchange, amqp_routing_key))
        logger.debug("AMQP msg to send: {}".format(msg))

        self.amqp_channel.basic_publish(exchange=amqp_exchange,
                                        routing_key=amqp_routing_key,
                                        body=msg)

    def get_amqp_msg(self, msg_number=1, queue=None):
        """
        Get at least 1 message from the configured queue
        :param msg_number:  number of messages to consume form the queue
        :param queue:   queue_name to listen to; if missing listen to the queue configured via set_amqp_queue
        :return:
        """

        queue_name = queue if queue is not None else self.queue
        received_messages = []

        # variant with basic_get
        for ev_method, ev_prop, ev_body in self.amqp_channel.consume(self.queue_name,
                                                                     inactivity_timeout=self.amqp_timeout):
            if ev_method:
                logger.debug("AMQP received <-- {}".format(ev_body))
                self.amqp_channel.basic_ack(ev_method.delivery_tag)
                received_messages.append(ev_body)
            if ev_method.delivery_tag == msg_number:
                break

        requeued_messages = self.amqp_channel.cancel()
        logger.debug("AMQP requeued after {} received: {}".format(msg_number, requeued_messages))
        return received_messages
