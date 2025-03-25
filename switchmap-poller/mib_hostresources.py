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
