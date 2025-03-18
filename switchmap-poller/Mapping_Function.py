def generate_topology_data(interface_data):
    nodes = set()
    links = []

    for entry in interface_data:
        local_device = f"Device-{entry['idx_device']}"
        remote_device = entry['lldpRemSysName']

        # Add unique devices to nodes set
        nodes.add(local_device)
        nodes.add(remote_device)

        # Build link between local and remote device interfaces
        link = {
            'source': local_device,
            'target': remote_device,
            'localPort': entry['ifname'],
            'remotePort': entry['lldpRemPortDesc']
        }
        links.append(link)

    # Prepare final structured data
    topology_data = {
        'nodes': [{'id': device} for device in nodes],
        'links': links
    }

    return topology_data
