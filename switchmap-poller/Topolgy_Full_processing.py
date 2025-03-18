import graphene

def generate_topology_data(interface_data):
    nodes = set()
    links = []

    for entry in interface_data:
        local_device = f"Device-{entry['idx_device']}"
        remote_device = entry['lldpRemSysName']

        nodes.add(local_device)
        nodes.add(remote_device)

        links.append({
            'source': local_device,
            'target': remote_device,
            'localPort': entry['ifname'],
            'remotePort': entry['lldpRemPortDesc']
        })

    topology_data = {
        'nodes': [{'id': device} for device in nodes],
        'links': links
    }

    return topology_data


class Query(graphene.ObjectType):
    network_topology = graphene.JSONString()

    def resolve_network_topology(parent, info):
        # Simulate fetching raw data (in real life, this comes from your DB)
        interface_data = [
            {
                'idx_device': 1001,
                'ifname': 'Gig0/1',
                'lldpRemSysName': 'Switch-B',
                'lldpRemPortDesc': 'Gig0/24'
            },
            {
                'idx_device': 1001,
                'ifname': 'Gig0/2',
                'lldpRemSysName': 'Switch-C',
                'lldpRemPortDesc': 'Gig0/12'
            },
            {
                'idx_device': 1002,
                'ifname': 'Gig1/1',
                'lldpRemSysName': 'Switch-D',
                'lldpRemPortDesc': 'Gig1/24'
            }
        ]

        topology = generate_topology_data(interface_data)
        return topology

schema = graphene.Schema(query=Query)
