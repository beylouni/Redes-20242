import time

class RoutingTable:
    def __init__(self, router_ip):
        self.router_ip = router_ip
        self.table = {}  # {destination_ip: (metric, next_hop)}

    def add_route(self, destination_ip, metric, next_hop):
        self.table[destination_ip] = (metric, next_hop)

    def update_route(self, destination_ip, metric, next_hop):
        current_metric, _ = self.table.get(destination_ip, (float('inf'), None))
        if metric < current_metric:
            self.table[destination_ip] = (metric, next_hop)

    def remove_route(self, destination_ip):
        if destination_ip in self.table:
            del self.table[destination_ip]

    def format_for_sending(self):
        return ''.join([f"@{dest}-{metric}" for dest, (metric, _) in self.table.items()])

    def display(self):
        print(f"Routing table for {self.router_ip}:")
        for dest, (metric, next_hop) in self.table.items():
            print(f"Destination: {dest}, Metric: {metric}, Next Hop: {next_hop}")