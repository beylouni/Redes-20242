import socket
import time
from routing_table import RoutingTable

class Router:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.routing_table = RoutingTable(self.ip_address)
        self.neighbors = self.load_neighbors()
        self.last_received_time = {}  # Track last update from each neighbor

    def load_neighbors(self):
        neighbors = []
        with open('routers.txt', 'r') as f:
            for line in f:
                neighbors.append(line.strip())
        return neighbors

    def broadcast_routing_table(self):
        message = self.routing_table.format_for_sending()
        for neighbor in self.neighbors:
            self.send_message(f"@{self.ip_address}", neighbor, message)

    def send_message(self, prefix, dest_ip, message):
        full_message = f"{prefix}{message}"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(full_message.encode(), (dest_ip, 9000))

    def receive_updates(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.ip_address, 9000))
        while True:
            data, addr = sock.recvfrom(1024)
            message = data.decode()
            self.process_message(message, addr[0])

    def process_message(self, message, sender_ip):
        if message.startswith('@'):
            # Process route update message
            self.update_routing_table(sender_ip, message)
        elif message.startswith('*'):
            # Process router announcement
            new_router_ip = message[1:]
            self.routing_table.add_route(new_router_ip, 1, new_router_ip)
        elif message.startswith('!'):
            # Process text message
            _, dest_ip, text = message[1:].split(';', 2)
            self.route_message(sender_ip, dest_ip, text)

    def update_routing_table(self, sender_ip, message):
        routes = message.split('@')[1:]
        for route in routes:
            dest_ip, metric = route.split('-')
            metric = int(metric) + 1
            self.routing_table.update_route(dest_ip, metric, sender_ip)
        self.routing_table.display()

    def route_message(self, source_ip, dest_ip, text):
        if dest_ip == self.ip_address:
            print(f"Received message from {source_ip}: {text}")
        elif dest_ip in self.routing_table.table:
            next_hop = self.routing_table.table[dest_ip][1]
            self.send_message(f"!{source_ip};{dest_ip};", next_hop, text)
        else:
            print(f"Cannot route message to {dest_ip} - no route available.")

    def monitor_neighbors(self):
        while True:
            current_time = time.time()
            for neighbor, last_time in self.last_received_time.items():
                if current_time - last_time > 35:
                    print(f"Lost connection to {neighbor}")
                    self.routing_table.remove_route(neighbor)
            time.sleep(10)

    def run(self):
        # Start broadcasting routing table and receiving messages
        from threading import Thread
        Thread(target=self.broadcast_routing_table).start()
        Thread(target=self.receive_updates).start()
        Thread(target=self.monitor_neighbors).start()