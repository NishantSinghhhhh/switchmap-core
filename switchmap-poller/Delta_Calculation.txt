from datetime import datetime

def calculate_bandwidth(
    current_in_octets: int,
    current_out_octets: int,
    prev_in_octets: int,
    prev_out_octets: int,
    interval_seconds: float
) -> (float, float):
    """
    Calculates inbound/outbound bandwidth in Mbps.

    :param current_in_octets: Current 'ifHCInOctets' from SNMP
    :param current_out_octets: Current 'ifHCOutOctets' from SNMP
    :param prev_in_octets: Previous 'ifHCInOctets'
    :param prev_out_octets: Previous 'ifHCOutOctets'
    :param interval_seconds: Time (in seconds) between the two polls
    :return: (in_mbps, out_mbps)
    """

    # Calculate the difference (delta) in bytes
    delta_in_bytes = current_in_octets - prev_in_octets
    delta_out_bytes = current_out_octets - prev_out_octets

    # Convert bytes to bits
    delta_in_bits = delta_in_bytes * 8
    delta_out_bits = delta_out_bytes * 8

    # Calculate bits per second
    in_bps = delta_in_bits / interval_seconds
    out_bps = delta_out_bits / interval_seconds

    # Convert to Megabits per second (Mb/s)
    in_mbps = in_bps / 1_000_000
    out_mbps = out_bps / 1_000_000

    return in_mbps, out_mbps
