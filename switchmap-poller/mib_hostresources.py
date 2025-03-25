# New class in mib_hostresources.py
class HostResourcesQuery(Query):
    def cpu_load(self):
        oid = "1.3.6.1.2.1.25.3.3.1.2"  # hrProcessorLoad
        results = self.snmp_object.walk(oid, normalized=True)
        loads = [int(v) for v in results.values()]
        if loads:
            return sum(loads) / len(loads)  # average CPU %
        return None

# Pseudocode in core/ingest pipeline
stats = data.get('cpu')  # from parsed YAML
if stats is not None:
    DeviceStatsTable.insert(device_id=device.id, 
                            timestamp=ingest_time, 
                            cpu_usage_percent=stats)

CREATE TABLE device_stats (
    id SERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL REFERENCES device(id),  -- FK to the device table
    timestamp TIMESTAMPTZ NOT NULL,                   -- Time of the CPU reading
    cpu_usage_percent REAL,                           -- Average CPU usage across cores (0–100%)
    mem_used_bytes BIGINT,                            -- Optional: used memory (bytes)
    mem_total_bytes BIGINT                            -- Optional: total memory (bytes)
);
