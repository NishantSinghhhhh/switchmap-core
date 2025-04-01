def insert_movement_events(items, test=False):
    """
    Insert processed movement events into the database.

    Args:
        items: A list of dictionaries representing processed movement events.
               Each dictionary should contain keys like "ip", "fromLocation", "toLocation", and "timestamp".
        test: If True, I insert rows sequentially. Bulk inserts might not give predictable primary keys.

    Returns:
        None
    """
    # I initialize an empty list to collect new DB rows.
    rows = []

    # I ensure that 'items' is a list; if not, I wrap it in a list.
    if not isinstance(items, list):
        items = [items]

    # I process each movement event.
    for item in items:
        # I check if the event already exists in the database.
        # I assume _movement.exists is a helper function that checks for an event by IP and timestamp.
        event_exists = _movement.exists(item["ip"], item["timestamp"])
        if not event_exists:
            # I create a new DB record for the movement event.
            # IMovementEvent is my DB model for movement events.
            rows.append(
                IMovementEvent(
                    ip=item["ip"],
                    from_location=item["fromLocation"],
                    to_location=item["toLocation"],
                    timestamp=item["timestamp"]
                )
            )

    # I insert the new rows into the database.
    if not test:
        _movement.insert_row(rows)
    else:
        # In test mode, I sort the rows by IP and timestamp before inserting.
        from operator import attrgetter
        sorted_rows = sorted(rows, key=attrgetter("ip", "timestamp"))
        _movement.insert_row(sorted_rows)
