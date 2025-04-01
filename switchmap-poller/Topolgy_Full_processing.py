import os
import log  
import files  
import update_topology 

# This function takes raw interface data and converts it into a topology dictionary.
def generate_topology_data(interface_data):
    nodes = set()
    links = []

    for entry in interface_data:
        # I create a unique identifier for the local device based on its index
        local_device = f"Device-{entry['idx_device']}"
        # The remote device is identified by its system name in the LLDP data
        remote_device = entry['lldpRemSysName']

        nodes.add(local_device)
        nodes.add(remote_device)

        # I build a link representing the connection between the local and remote devices,
        # including the relevant port details.
        links.append({
            'source': local_device,
            'target': remote_device,
            'localPort': entry['ifname'],
            'remotePort': entry['lldpRemPortDesc']
        })

    # I compile the topology information into a dictionary with nodes and links.
    topology_data = {
        'nodes': [{'id': device} for device in nodes],
        'links': links
    }

    return topology_data

# This function ingests a single file to update the network topology.
def ingest_topology_data(argument):
    """
    Ingest a single file for network topology updates.

    Args:
        argument: An object containing the file path, configuration details, etc.

    Returns:
        None
    """
    # I extract the necessary parameters from the argument object.
    (idx_zone, data, filepath, config, dns) = _get_arguments(argument)

    # I check for the presence of a skip file. If it exists, I log a message and abort the ingestion.
    skip_file = files.skip_file(AGENT_INGESTER, config)
    if os.path.isfile(skip_file):
        log_message = (
            f"Skip file {skip_file} found. Aborting ingesting {filepath}. "
            "A daemon shutdown request was probably issued."
        )
        log.log2debug(1049, log_message)
        return

    # I convert the raw interface data into a structured topology format.
    topology = generate_topology_data(data)

    # Finally, I update the database with the new topology data.
    update_topology.process(topology, idx_zone, dns=dns)
