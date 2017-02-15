## AMQP library for Robotframework

## Installation

### Using pip

:warning: Not implemeted yet
```
pip install robotframework-amqp
```

### Using the install script
```
python setup.py install
```

## Usage
In the settings section
```robotframework
*** Settings ***
Test Teardown     After tests
Test Setup        Before tests
Library           RmqMsgSend

```

In the keywords section
```robotframework
*** Keywords ***
Before tests
    Init AMQP connection    ${amqp_host}  ${amqp_port}   ${amqp_user}  ${amqp_pass}   ${amqp_vhost}
    Set amqp destination    ${amqp_exchange}        ${amqp_routing_key}

After tests
    close amqp connection
```