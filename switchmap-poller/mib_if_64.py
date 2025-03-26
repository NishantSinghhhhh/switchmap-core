class If64Query(Query):
    # existing methods for ifHCInOctets, ifHCOutOctets, etc.
    def if_in_errors(self, oidonly=False):
        oid = ".1.3.6.1.2.1.2.2.1.14"  # ifInErrors
        if oidonly: 
            return oid
        results = self.snmp_object.walk(oid, normalized=True)
        return {int(k): int(v) for k, v in results.items()}
    def if_out_errors(self, oidonly=False):
        oid = ".1.3.6.1.2.1.2.2.1.20"  # ifOutErrors
        # similar to above
    def if_in_discards(self, oidonly=False):
        oid = ".1.3.6.1.2.1.2.2.1.13"  # ifInDiscards
        # similar implementation
    def if_out_discards(self, oidonly=False):
        oid = ".1.3.6.1.2.1.2.2.1.19"  # ifOutDiscards
        # similar implementation
