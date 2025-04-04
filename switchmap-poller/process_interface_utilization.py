from datetime import datetime
from sqlalchemy.orm import Session
from models import InterfaceTrafficHistory
from sqlalchemy import desc

def calculate_interface_utilization(session: Session, interface_id: int, data: dict, timestamp: datetime):
    """
    Calculates interface utilization percentage using the last known traffic record.

    Args:
        session: SQLAlchemy DB session
        interface_id: The interface ID in question
        data: Dictionary with 'in_octets', 'out_octets', 'if_speed'
        timestamp: Current timestamp of the sample

    Returns:
        Utilization percentage (float) or None if insufficient data
    """
    in_octets = data.get("in_octets")
    out_octets = data.get("out_octets")
    if_speed = data.get("if_speed")

    if None in (in_octets, out_octets, if_speed):
        return None

    # Fetch the last traffic snapshot from DB
    last = (
        session.query(InterfaceTrafficHistory)
        .filter_by(interface_id=interface_id)
        .order_by(desc(InterfaceTrafficHistory.timestamp))
        .first()
    )

    if not last:
        return None

    # Calculate deltas
    delta_t = (timestamp - last.timestamp).total_seconds()
    delta_in = in_octets - last.in_bytes
    delta_out = out_octets - last.out_bytes

    if delta_t <= 0 or delta_in < 0 or delta_out < 0:
        return None

    # Calculate bits per second and utilization
    in_bps = (delta_in * 8) / delta_t
    out_bps = (delta_out * 8) / delta_t
    utilization_pct = max((in_bps / if_speed) * 100, (out_bps / if_speed) * 100)

    return utilization_pct
