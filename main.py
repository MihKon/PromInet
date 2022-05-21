from opcua import Client
import paho.mqtt.client as mqtt


broker = "demo.thingsboard.io"
port = 1883
topic = "v1/devices/me/telemetry"
temperature_sensor_token = "vQfPG2riPfzh4EREBAZW"
illumination_sensor_token = "A1NqX37eFPOASnA6T27T"
level_sensor_token = "Xtc5RupkQ6Q1wv5BqyLq"
payload1 = dict()
payload2 = dict()
payload3 = dict()

if __name__ == "__main__":

    client = Client("opc.tcp://localhost:8001/opcua/server/")

    mqtt_client1 = mqtt.Client("temperature_client")
    mqtt_client1.username_pw_set(temperature_sensor_token)
    mqtt_client1.connect(broker, port)

    mqtt_client2 = mqtt.Client("illumination_client")
    mqtt_client2.username_pw_set(illumination_sensor_token)
    mqtt_client2.connect(broker, port)

    mqtt_client3 = mqtt.Client("h20_level_client")
    mqtt_client3.username_pw_set(level_sensor_token)
    mqtt_client3.connect(broker, port)

    try:
        while True:
            client.connect()
            root = client.get_root_node()
            # print("Root node is: ", root)
            objects = client.get_objects_node()
            # print("Objects node is: ", objects)

            uri = "http://vertical.farm.ru"
            idx = client.get_namespace_index(uri)

            children = root.get_children()
            # print("Children of root is: ", children)

            var_temperature = root.get_child(["0:Objects", "{}:Parameters".format(idx), "{}:Temperature".format(idx)])
            var_humidity = root.get_child(["0:Objects", "{}:Parameters".format(idx), "{}:Humidity".format(idx)])
            var_h20 = root.get_child(["0:Objects", "{}:Parameters".format(idx), "{}:H20_Level".format(idx)])
            var_light = root.get_child(["0:Objects", "{}:Parameters".format(idx), "{}:Illumination".format(idx)])
            var_time = root.get_child(["0:Objects", "{}:Parameters".format(idx), "{}:Time".format(idx)])

            temperature = client.get_node(var_temperature).get_value()
            humidity = client.get_node(var_humidity).get_value()
            h20_level = client.get_node(var_h20).get_value()
            illumination = client.get_node(var_light).get_value()
            time = client.get_node(var_time).get_value()
            print(temperature, humidity, h20_level, illumination, time)

            payload1.update({"temperature": temperature, "humidity": humidity})
            payload2.update({"illumination": illumination})
            payload3.update({"level": h20_level})

            mqtt_client1.publish(topic, str(payload1))
            mqtt_client2.publish(topic, str(payload2))
            mqtt_client3.publish(topic, str(payload3))

            print(str(payload1), str(payload2), str(payload3))

    finally:
        client.disconnect()
