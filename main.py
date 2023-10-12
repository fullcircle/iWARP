import simpy

# Define a simple network node
class NetworkNode:
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.queue = simpy.Store(env)

    def send(self, data, dest):
        yield self.queue.put(data)
        #print(f'{self.name} sent: {data}')
        print(f'{self.env.now:.2f}: {self.name} sent: {data}')
        yield self.env.timeout(1)  # Simulate transmission time
       # Call the receive function of the destination node
        yield self.env.process(dest.receive(data)) 

    def receive(self, data):
        print(f'{self.env.now:.2f}: {self.name} received: {data}')
        yield self.env.timeout(1)  # Simulate processing time

# Define a simulation process
def data_transfer(env, node1, node2, duration):
    data = "Hello, iWARP!"
    start_time = env.now
    while env.now - start_time < duration:
        yield env.process(node1.send(data, node2))

# Create the simulation environment
env = simpy.Environment()

# Create network nodes
node_A = NetworkNode(env, "Node A")
node_B = NetworkNode(env, "Node B")

# Get user-defined simulation duration
simulation_duration = float(input("Enter simulation duration (in seconds): "))

# Start the data transfer process
env.process(data_transfer(env, node_A, node_B, simulation_duration))

# Run the simulation
env.run(until=simulation_duration)
