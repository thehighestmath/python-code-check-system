```console
docker build -t docker-inside-docker .

docker run -v /var/run/docker.sock:/var/run/docker.sock -i -t docker-inside-docker:latest 
```

```python
import docker
client = docker.from_env()
f = open('Dockerfile', 'rb')
out = client.images.build(path='.', fileobj=f, dockerfile='Dockerfile')
client.containers.run(image=out[0].id, command="""python3 -c 'print("Hi")'""") # b'Hi\n'
```
