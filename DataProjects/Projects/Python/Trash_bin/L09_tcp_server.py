


import socketserver
import json
import random


class Handler(socketserver.BaseRequestHandler):
    '''
    The request handler class for our server.

    It is instantiated once per connection to the server. The handler() has been implemented to 
    fulfill several tasks.
    client.
    '''
    
    def __init__(self, request, client_address, server):
        
        global sensor_data
        # if ONCE == False:
        #    sensor_data = self.initialize('data/sz_sensor.json')
        
        self._message_size = 10240
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)

    def receive(self, data):
        '''
        receive a message from a client application and process the 
        respective data 

        arguments:
        ----------
        data      - sensor data to client or update sensor data
        '''
        
        sen_data = json.loads(data[1])
        self.update_sensor_data(sen_data)
        state = 'updated'
        print('Sensor data state: {}'.format(state))
        
        return state

    def submit(self):
        '''
        send sensor data to the client 
        '''
        sen_data = self.process_sensor_data()
        self.request.sendall(sen_data.encode())
        print('Sensor data state: {}'.format('submitted'))
        pass

    def acknowledge(self, state):
        
        self.request.sendall(state.encode())
        pass        

    def update_sensor_data(self, sen_data):
        '''
        update received client sensor data 

        arguments:
        ----------
        sensor_data - sensor data in json format
        '''
        global sensor_data
        
        do_not_update = []

        for i in range(len(sen_data)):
            if sen_data[i]['update']:
                sensor_data[i]['filling_level'] = sen_data[i]['filling_level']
                sensor_data[i]['maintenance']   = False
                sensor_data[i]['update']        = False
                do_not_update.append(i)

        print('Sensor data state: {}'.format('updated'))
        pass

    def handle(self):
        '''
        central request handler which receives and sends data
        '''
        global sensor_data
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(self._message_size).strip()
        data = self.data.decode()
        data = json.loads(data)

        request_type = data[0]
        
        if request_type == 'init':
            sensor_data, state = self.initialize(data[1])
            self.acknowledge(state)

        if request_type == 'send':
            self.submit()

        if request_type == 'update':        
            state = self.receive(data)
            self.acknowledge(state)

        if request_type == 'random':
            state = self.assign_random_values() 
            self.acknowledge(state)

    def process_sensor_data(self):
        '''
        Load the initial sensor data and keep it in memory
        '''
        data = sensor_data
        return json.dumps(data)

    def assign_random_values(self):
        '''
        Create random numbers to simulate the changeing filling level
        '''
        global sensor_data

        for i in range(len(sensor_data)):
            if i != 0:
                sensor_data[i]['filling_level'] = random.randint(5, 10) + sensor_data[i]['filling_level']  

        state = 'assigned randomly'
        return state

    def initialize(self, path):
        
        with open(path) as f:
            data = json.load(f)
        
        state = 'initialized'
        global ONCE
        ONCE = True
        print('Server state: {}'.format('initialized'))

        return data, state


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 65432
    ONCE = False
    sensor_data = None 

    # Create the server, binding to localhost on port 65432
    with socketserver.TCPServer((HOST, PORT), Handler) as server:
        '''
        Activate the server. 
        This will keep running until I interrupt the program with Ctrl-C
        '''
        
        print(' ')
        print('TCP_Server running - listening on port: {}'.format(PORT))
        server.serve_forever()            


