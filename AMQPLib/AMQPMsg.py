"""
Connect to an AMQP server and sent messages to a certain queue
"""
import puka


def _receive_callback(chan, method, properties, body):
    print("AMQP received: {}".format(body))
    return body


class AmqpMsg(object):
    """
    Connect to an AMQP server and receive messages or send messages in Robotframework
    """
    def __init__(self):
        self.amqp_addr = ""
        self.amqp_client = None
        self.exchange = ""
        self.routing_key = ""
        self.queue = ""

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

        self.amqp_client = puka.Client(self.amqp_addr)
        amqp_promise = self.amqp_client.connect()
        self.amqp_client.wait(amqp_promise)

    def close_amqp_connection(self):
        """
        Close the amqp connection
        Usage:

        *** Keywords ***
        After tests
            close amqp connection
        """
        amqp_promise = self.amqp_client.close()
        self.amqp_client.wait(amqp_promise)

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
        Set queue to listen to for the subsequent get_amqp_msg calls

        :param amqp_queue:
        :return:
        """
        self.queue = amqp_queue

    def send_amqp_msg(self, msg, exchange=None, routing_key=None):
        """
        Send one message via AMQP

        :param msg:
        :param exchange: name of the exchange to send the message to; default: self.exchange
        :param routing_key: the routing key to use; default is self.routing_key
        """
        amqp_exchange = exchange if exchange is not None else self.exchange
        amqp_routing_key = routing_key if routing_key is not None else self.routing_key
        promise = self.amqp_client.basic_publish(exchange=amqp_exchange,
                                                 routing_key=amqp_routing_key,
                                                 body=msg)
        self.amqp_client.wait(promise)

    def get_amqp_msg(self, msg_number=1, queue=None):
        """
        Get at least 1 message from the configured queue
        :param msg_number:  number of messages to consume form the queue
        :param queue:   queue_name to listen to; if missing listen to the queue configured via set_amqp_queue
        :return:
        """

        queue_name = queue if queue is not None else self.queue
        consume_promise = self.amqp_client.basic_consume(queue=queue_name)
        received_messages = []
        for _ in xrange(0, msg_number):
            msg = self.amqp_client.wait(consume_promise)
            print("received: {}".format(msg))
            received_messages.append(msg)
            self.amqp_client.basic_ack(msg)

        promise = self.amqp_client.basic_cancel(consume_promise)
        self.amqp_client.wait(promise)

        return received_messages
