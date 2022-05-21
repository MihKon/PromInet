import datetime
from time import sleep
from opcua import Server
from random import randint
import random

server = Server()

url = 'opc.tcp://0.0.0.0:8001/opcua/server/'
server.set_endpoint(url)
server.set_server_name('OPC UA SIMULATION SERVER')

uri = 'http://vertical.farm.ru'
space = server.register_namespace(uri)

node = server.get_objects_node()

params = node.add_object(space, 'Parameters')

temperature = params.add_variable(space, 'Temperature', 0)
humidity = params.add_variable(space, 'Humidity', 0)
H20_Level = params.add_variable(space, 'H20_Level', 20)
illumination = params.add_variable(space, 'Illumination', 0)
time = params.add_variable(space, 'Time', 0)

temperature.set_writable()
humidity.set_writable()
H20_Level.set_writable()
illumination.set_writable()
time.set_writable()

server.start()
print(f'Server has been started at {url}')

try:

    count = 0
    while True:
        count += 1
        t = randint(15, 25)
        h = randint(50, 80)
        h2 = H20_Level.get_value() - 1
        i = randint(2500, 4000)
        temp_time = datetime.datetime.now().strftime("%H:%M:%S")
        if h2 == -1:
            h2 = 20
        if count % 10 == 0:
            lst = [10, 30, 28, 12]
            t = random.choice(lst)
        if count % 7 == 0:
            lst = [1900, 5000, 4200, 2200, 1500, 6000]
            i = random.choice(lst)
        print(t, h, h2, i, temp_time)

        temperature.set_value(t)
        humidity.set_value(h)
        H20_Level.set_value(h2)
        illumination.set_value(i)
        time.set_value(temp_time)

        sleep(10)

finally:
    server.stop()
