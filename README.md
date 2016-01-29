# devconf-2016-atomic-workshop
Demos for our Atomic workshop at DevConf 2016

## Docker News

### 1.8

#### `docker cp`

You can copy files and directories between (even stopped) containers and your host system.

```shell
docker create -ti --name=banana fedora bash
docker cp LICENSE banana:/
docker attach banana
```

In other terminal:

```shell
docker cp banana:/ LICENSE
cat LICENSE
```


#### `docker daemon`

```shell
man docker
man docker-daemon
```


### 1.9

#### `docker volume`

```shell
docker volume ls
docker volume create --name mango
docker run -ti -v mango:/mango fedora bash
docker volume inspect mango
docker volume rm mango
```

`inspect` doesn't say which conatiners use the volume.


#### build arguments

https://docs.docker.com/engine/reference/builder/#arg

```shell
docker build --build-arg fruit=watermelon --tag=watermelon ./build_args
docker inspect watermelon | less
```


#### concurrent image pulls

Run concurrently and ^c the latter one

```shell
docker pull centos:7
```


#### `STOPSIGNAL` instruction

Comment `STOPSIGNAL` first.

```shell
docker build --tag=signal .
docker run --name=signal signal
```

in another terminal

```shell
docker kill --signal=int signal
docker kill --signal=term signal
docker kill --signal=usr1 signal
```


#### `docker stats`

```shell
docker stats
```

