# Wake On Lan (WoL) server in Docker

## About
It is super simple Python (FastAPI) server that sends magic packets to wake up another machine.
Docker container is based on python-alpine base image and rely on awake linux script.

## Usage

```
docker run -p 8080:8080 daamian3/wake-on-lan:latest
```

It will run on port 8080.

### Endpoints

#### Wake on Lan - POST `/`

Example body:

```
{
    "mac": "02:42:5b:3a:a8:9a"
}
```

#### Health check - GET `/`

Example response:

```
{
    "status": "OK"
}
```

### Testing

```
docker run --rm daamian3/wake-on-lan:latest python -m unittest
```

## License

MIT