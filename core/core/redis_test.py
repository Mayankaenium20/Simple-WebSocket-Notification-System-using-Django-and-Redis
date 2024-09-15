import redis

# Connect to Redis
r = redis.Redis(host='127.0.0.1', port=6379, db=0)

# Set a key-value pair in Redis
r.set('foo', 'bar')

# Get the value associated with the key
value = r.get('foo')

# Print the value
print(value)  # Should output: b'bar'