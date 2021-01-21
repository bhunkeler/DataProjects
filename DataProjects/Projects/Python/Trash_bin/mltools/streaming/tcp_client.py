import socket
import json


class TCP_Client():

    def __init__(self, host, port, request_type):

        self._host = host           # The server's hostname or IP address
        self._port = port           # The port used by the server
        self._message_size = 10240  # message size

        self._request_type = request_type  # 'send' or 'update'

        # instantiate socket
        self._client_socket = socket.socket()
        # connect to the server
        self._client_socket.connect((self._host, self._port))

        pass

    def initialize(self, path):
        '''
        initializing allows to tell the server which location data has to be used. 
        This is either switzerland or winterthur

        arguments:
        ----------
        path - definition containing the respective location file for switzerland or winterthur
        '''
        # 'data/sz_sensor_dummy.json'
        message = ['init', path]
        message = json.dumps(message)

        # send message
        self._client_socket.send(message.encode())

        # receive response
        received_data = self._client_socket.recv(
            self._message_size).decode()

        print('Received from server: ' + received_data)

        # close the connection
        self._client_socket.close()
        pass

    def request_sensor_data(self):
        '''
        Request sensor data sends a request to the server, which on that request sends a data feed containing öocation-, 
        filling level and IoT component status data.

        arguments:
        ----------
        none
        '''

        message = ['send', '']
        message = json.dumps(message)

        # send message
        self._client_socket.send(message.encode())

        # receive response
        data = self._client_socket.recv(
            self._message_size).decode()
        json_data = json.loads(data)
        received_data = json.dumps(json_data, indent=4, sort_keys=True)

        # print('Received from server: ' + received_data)

        # close the connection
        self._client_socket.close()
        return received_data

    def update_sensor_data(self, sensor_data):
        '''
        Update sensor data, sends changed data back to the server. Data is kept in memory 
        and will be updated. 

        arguments:
        ----------
        sensor_data - sends changed sensor data to the server to update
        '''

        sensor_data = json.dumps(sensor_data)
        message = ['update', sensor_data]
        sensor_data = json.dumps(message)

        # send message
        self._client_socket.send(sensor_data.encode())

        # receive response
        state = self._client_socket.recv(
            self._message_size).decode()

        print('Sensor data state: {}'.format(state))

        # close the connection
        self._client_socket.close()

    def assign_random_values(self):
        '''
        Ask the server to create random data. On that the server will create random values for different locations.

        arguments:
        ----------
        none
        '''

        message = ['random', '']
        message = json.dumps(message)

        # send message
        self._client_socket.send(message.encode())

        # receive response
        state = self._client_socket.recv(
            self._message_size).decode()

        print('Sensor data state: {}'.format(state))

        # close the connection
        self._client_socket.close()


def get_sensor_data():
    '''
    Initial test data - not used latter on
    '''
    data = [
        {
            "id": 0,
            "street": "Street 0",
            "city": "Winterthur",
            "country": "Switzerland",
            "country_code": "CH",
            "canton": "Zurich",
            "canton_code": "ZH",
            "point": [47.505637, 8.724139],
            "lat": 47.505637,
            "lon": 8.724139,
            "filling_level": 0,
            "timestamp": "2020-11-17T14:00:00.000Z",
            "maintenance": False,
            "update": False
        },
        {
            "id": 1,
            "street": "Street 0",
            "city": "Zurich",
            "country": "Switzerland",
            "country_code": "CH",
            "canton": "Zurich",
            "canton_code": "ZH",
            "point": [47.505637, 8.724139],
            "lat": 47.505637,
            "lon": 8.724139,
            "filling_level": 0,
            "timestamp": "2020-11-17T14:00:00.000Z",
            "maintenance": False,
            "update": True
        },
        {
            "id": 2,
            "street": "Street 2",
            "city": "Bern",
            "country": "Switzerland",
            "country_code": "CH",
            "canton": "Bern",
            "canton_code": "BE",
            "point": [
                            46.948384,
                            7.439946
            ],
            "lat": 46.948384,
            "lon": 7.439946,
            "filling_level": 15,
            "timestamp": "2020-11-17T16:00:00.000Z",
            "maintenance": False,
            "update": False
        }]
    return data


if __name__ == '__main__':

    host = '192.168.0.151'  # The server's hostname or IP address
    port = 65432            # The port used by the server
    sensor_data = 'data/sz_sensor_dummy.json'

    client = TCP_Client(host, port, request_type='init')
    client.initialize(sensor_data)

    client = TCP_Client(host, port, request_type='send')
    received_data = client.request_sensor_data()
    print(received_data)

    client = TCP_Client(host, port, request_type='update')
    sensor_data = get_sensor_data()
    client.update_sensor_data(sensor_data)

    client = TCP_Client(host, port, request_type='send')
    received_data = client.request_sensor_data()
    print(received_data)

    client = TCP_Client(host, port, request_type='random')
    received_data = client.assign_random_values()
    print(received_data)

    client = TCP_Client(host, port, request_type='send')
    received_data = client.request_sensor_data()
    print(received_data)

    end = 'end'
