import json
from datetime import datetime

# These dictionaries are just for demo purposes.
# In a real-world scenario, I'd probably query a database or use a more robust method.
MAC_TO_DEVICE = {
    "00:11:22:33:44:55": "Dell XPS",
    "AA:BB:CC:DD:EE:FF": "iPhone 15"
}
MAC_TO_TAG = {
    "00:11:22:33:44:55": "Workstation",
    "AA:BB:CC:DD:EE:FF": "Mobile"
}

def process_json_data(json_file_path):
    """
    This function reads a JSON file with raw movement events,
    then transforms the data into a format that's easier for me to use
    in the Device Movement History table.
    """
    # First, I open and load the JSON data.
    with open(json_file_path, 'r') as f:
        raw_events = json.load(f)

    processed = []
    # Now, I loop through each event and reformat the data.
    for event in raw_events:
        mac = event.get("mac", "")
        from_switch = event.get("from_switch", "")
        from_port = event.get("from_port", "")
        to_switch = event.get("to_switch", "")
        to_port = event.get("to_port", "")
        ts = event.get("timestamp", "")

        # I use the stub dictionaries to find a friendly device name and a tag.
        device_name = MAC_TO_DEVICE.get(mac, "Unknown Device")
        device_tag = MAC_TO_TAG.get(mac, "Unknown Tag")

        # I put together the "From" and "To" locations as strings.
        from_location = f"{from_switch}:{from_port}"
        to_location = f"{to_switch}:{to_port}"

        # I try to convert the timestamp into a nicer format.
        try:
            dt = datetime.fromisoformat(ts.replace("Z", ""))  # Remove the "Z" if it's there.
            ts_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            # If it can't be parsed, I'll just use the original string.
            ts_str = ts

        # I create a final record for this event.
        record = {
            "device": device_name,
            "tag": device_tag,
            "fromLocation": from_location,
            "toLocation": to_location,
            "timestamp": ts_str
        }
        processed.append(record)

    return processed
