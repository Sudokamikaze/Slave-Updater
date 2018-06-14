Slave-updater - Python script that does things! Also with docker support :D
==========

Table of contents
-----------------
- [Installation](#installation)

#### Run docker build

```
    docker build \
    --no-cache \
    -t slave-updater:latest .
``` 

#### Issue `run` command

```
   docker run -d \
   -v /var/run/docker.sock:/var/run/docker.sock \
   --name=Slave-Updater \
   --restart=always \
   slave-updater:latest
```

That's it! You've made it!

