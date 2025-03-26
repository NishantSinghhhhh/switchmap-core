
def resolve_cpu_history(device, info, limit=100):
    records = DeviceStats.query.filter_by(device_id=device.id) \
                               .order_by(DeviceStats.timestamp.desc()) \
                               .limit(limit)
    return [CPUPointType(timestamp=r.timestamp, usage=r.cpu_usage_percent) for r in records]

@app.route('/api/v1/devices/<dev_id>/cpu')
def get_cpu(dev_id):
    data = query_device_stats(dev_id, limit=request.args.get('limit', 1))
    return jsonify(cpu_usage=data)

# GraphQL query

query {
  device(name: "SW1") {
    cpuHistory(limit: 2) {
      timestamp
      usage
    }
    cpuUsage
  }
}

# REST response
{
  "data": {
    "device": {
      "cpuHistory": [
        { "timestamp": "2025-03-26T02:00:00Z", "usage": 35.0 },
        { "timestamp": "2025-03-26T01:00:00Z", "usage": 30.5 }
      ],
      "cpuUsage": 35.0
    }
  }
}
