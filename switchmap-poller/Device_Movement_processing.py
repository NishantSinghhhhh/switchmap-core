import json
from datetime import datetime

def process_json_data(json_file_path):
    """
    This function reads a JSON file with raw movement events,
    then transforms the data into a format that's easier for me to use
    in the Device Movement History table.
    """
    # Open the JSON file and load the raw events.
    with open(json_file_path, 'r') as f:
        raw_events = json.load(f)

    processed = []
    # Loop through each event and reformat the data.
    for event in raw_events:
        # I now directly render the IP address from the event without any additional naming.
        ip = event.get("ip", "")
        # Get the source and destination switch and port details.
        from_switch = event.get("from_switch", "")
        from_port = event.get("from_port", "")
        to_switch = event.get("to_switch", "")
        to_port = event.get("to_port", "")
        ts = event.get("timestamp", "")

        # Construct the "From" and "To" location strings.
        from_location = f"{from_switch}:{from_port}"
        to_location = f"{to_switch}:{to_port}"

        # Try to convert the timestamp into a nicer, more readable format.
        try:
            dt = datetime.fromisoformat(ts.replace("Z", ""))  # Remove the "Z" if present.
            ts_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            # If parsing fails, I'll simply use the original timestamp.
            ts_str = ts

        # Create the final record for this event, now including only the raw IP.
        record = {
            "ip": ip,
            "fromLocation": from_location,
            "toLocation": to_location,
            "timestamp": ts_str
        }
        processed.append(record)

    return processed
