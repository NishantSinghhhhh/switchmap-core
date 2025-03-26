class HostResourcesQuery(Query):
    # ... (cpu_load as above)
    def memory_stats(self):
        # Walk hrStorageType to find index of physical memory
        types = self.snmp_object.walk("1.3.6.1.2.1.25.2.3.1.2")
        ram_index = None
        for oid_suffix, val in types.items():
            # val might be something like '...25.2.1.2' indicating hrStorageRam
            if val.endswith("25.2.1.2"):  # matches hrStorageRam OID
                ram_index = oid_suffix.split('.')[-1]  # get index number
                break
        if ram_index is None:
            return None  # no RAM info
        # Now getting size, used, allocationUnits for that index
        base = f"1.3.6.1.2.1.25.2.3.1"
        size = self.snmp_object.get(f"{base}.5.{ram_index}")
        used = self.snmp_object.get(f"{base}.6.{ram_index}")
        alloc = self.snmp_object.get(f"{base}.4.{ram_index}")
        if size and used and alloc:
            total_bytes = int(size) * int(alloc)
            used_bytes = int(used) * int(alloc)
            return {"total": total_bytes, "used": used_bytes}
        return None
