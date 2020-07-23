from amqp_handler import AMQPHandler
from telnet_device_operator import IOSTelnetOperator
import asyncio
import json
import datetime
import logging
import json
import os

logger = logging.getLogger('rmq_telnet_operator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
bf = logging.Formatter('{asctime} {name} {levelname:8s} {message}', style='{')
handler.setFormatter(bf)
logger.addHandler(handler)

# with open('config.json') as jcf:
#     config = json.load(jcf)

config = {}

config['rmq_host'] = os.environ.get('RMQ_HOST', '')
config['rmq_exchange'] = os.environ.get('RMQ_TELNET_OPERATOR_RMQ_EXCHANGE', '')
config['rmq_queue_in'] = os.environ.get('RMQ_TELNET_OPERATOR_RMQ_QUEUE_IN', '')

config['redirect_to_exchange'] = os.environ.get('RMQ_TELNET_OPERATOR_REDIRECT_TO_EXCHANGE', '')
config['redirect_to_queue'] = os.environ.get('RMQ_TELNET_OPERATOR_REDIRECT_TO_QUEUE', '')

    
def rmq_msg_proc(msg):
    redir_message = \
    {
        "main_output" : None,
        "device_id" : None,
        "datetime" : None
    }

    msg = msg.decode('utf-8')
    msg = json.loads(msg)

        
    ITO = IOSTelnetOperator(msg['telnet_ipv4'], msg['telnet_username'], msg['telnet_password'])
    status = ITO.connect()

    # send wrong status instead payload
    # it can demand more time due timeout delay
    if status is not None:
        name, message = status.popitem()
        redir_message['main_output'] = '{} {}'.format(name, message)
        redir_message['device_id'] = msg['device_id']
        redir_message['datetime'] = '{}'.format(datetime.datetime.now())
        redir_message['device_name'] = '[None]'
        return (True, json.dumps(redir_message))

    output = ITO.show_operation(msg['operation'])

    redir_message['main_output'] = output.decode('utf-8')
    redir_message['device_id'] = msg['device_id']
    redir_message['datetime'] = '{}'.format(datetime.datetime.now())
    redir_message['device_name'] = ITO.get_device_name().decode('utf-8')
    return (True, json.dumps(redir_message))

def main():
    
    loop = asyncio.get_event_loop()

    AMQPH = AMQPHandler(loop)

    loop.run_until_complete(AMQPH.connect(amqp_connect_string=config['rmq_host']))

    loop.run_until_complete(
        AMQPH.receive(
            config['rmq_exchange'], 
            config['rmq_queue_in'], 
            rmq_msg_proc, 
            redirect_to_exchange=config['redirect_to_exchange'], 
            redirect_to_queue=config['redirect_to_queue']
        )
    )
    loop.close()

if __name__ == '__main__':
    main()
