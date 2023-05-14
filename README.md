# Python Microservices with redis and FastAPI

Microservice one:

- product registration

Microservice two:

- purchase a product

```
docker exec -it pg_py_db psql -U tyler -d pyauthdb
```

## REDIS

A key-value store database.

In general, to **delete** a data structure:

- DELETE <key>

Manipulate **strings**:

- SET <key> <value>
- GET <value>

Manipulate **hashes**:

- HSET <key> <field> <value>
- HGET <key> <field>
- HDEL <key> <field>
- HGETALL <key>

Manipulate **lists**:

- LPUSH/RPUSH
- LPOP/RPOP
- LINDEX
- LRANGE
- DEL

```
# Display all elements inside the LIST
LRANGE <element> 0 -1
```

Manipulate **pub/sub**:

- SUBSCRIBE <channels>
- PUBLISH <channel> <message>
