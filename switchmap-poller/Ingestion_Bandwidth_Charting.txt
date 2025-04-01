def insert_bandwidth_data(items, test=False):
    """
    Insert calculated bandwidth data into the database.

    Args:
        items: A list of dictionaries representing calculated bandwidth data.
               Each dictionary should contain keys like "in_mbps", "out_mbps", "timestamp",
               and optionally "interface" if available.
        test: If True, I insert rows sequentially since bulk inserts might not provide
              predictable primary keys.

    Returns:
        None
    """
    # I initialize an empty list to collect new DB rows.
    rows = []

    # I ensure that 'items' is a list; if it's not, I wrap it in a list.
    if not isinstance(items, list):
        items = [items]

    # I process each bandwidth record.
    for item in items:
        # I check if the record already exists in the database.
        # I assume _bandwidth.exists is a helper function that checks for a record by timestamp
        # and optionally by interface.
        record_exists = _bandwidth.exists(item["timestamp"], item.get("interface"))
        if not record_exists:
            # I create a new DB record for the calculated bandwidth data.
            rows.append(
                IBandwidth(
                    in_mbps=item["in_mbps"],
                    out_mbps=item["out_mbps"],
                    timestamp=item["timestamp"],
                    interface=item.get("interface")
                )
            )

    # I insert the new rows into the database.
    if not test:
        _bandwidth.insert_row(rows)
    else:
        from operator import attrgetter
        sorted_rows = sorted(rows, key=attrgetter("timestamp"))
        _bandwidth.insert_row(sorted_rows)
