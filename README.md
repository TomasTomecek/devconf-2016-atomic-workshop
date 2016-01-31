# DevConf 2016 Atomic Workshop

Run several containers:

 * OpenShift origin
 * `cat`
 * bash with nested process

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


#### `docker network`


```
docker build --tag=networking-demo ./networks
docker run --name=netw networking-demo
docker exec -ti netw bash
curl -v -XHEAD 0.0.0.0:8000
```

https://github.com/docker/docker/issues/19448

```
docker network create -d bridge kiwi
docker run --name=pomelo --net=kiwi networking-demo
docker run -ti --rm --net=kiwi --name orange fedora bash
```

or

```
docker network connect kiwi orange
docker network connect kiwi pomelo
```


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


### 1.10

#### seccomp

https://github.com/jfrazelle/docker/blob/831af89991edd442ef4eeb29fd01da576b04bcfc/docs/security/seccomp.md
https://github.com/opencontainers/specs/blob/master/config-linux.md#seccomp

```
vim seccomp/policy.json
docker run --rm -it --security-opt seccomp:seccomp/policy.json fedora bash
useradd asdqwe
touch /tmp/change_me
chown root:root /tmp/change_me
```


#### User Namespaces

https://github.com/docker/docker/blob/7992b353c04b4214c28d5be6195b2703a52defb1/docs/reference/commandline/daemon.md#daemon-user-namespace-options

Run `docker daemon` with `--userns-remap=default`.

```
time="2016-01-31T01:07:15.321694705+01:00" level=info msg="User namespaces: ID ranges will be mapped to subuid/subgid ranges of: dockremap:dockremap" 
time="2016-01-31T01:07:15.321787749+01:00" level=fatal msg="Error starting daemon: Can't create ID mappings: open /etc/subuid: no such file or directory" 
```

Fix `/etc/sub{uid,gid}

```
$ cat /etc/subuid
user1:100000:65536
dockremap:165536:65536

$ cat /etc/subgid
user1:100000:65536
dockremap:165536:65536
```

```
time="2016-01-31T01:08:30.143584027+01:00" level=info msg="User namespaces: ID ranges will be mapped to subuid/subgid ranges of: dockremap:dockremap" 
time="2016-01-31T01:08:30.143661722+01:00" level=debug msg="Creating user namespaced daemon root: /var/lib/docker/165536.165536" 
```

```
docker run -it --rm -v /:/host fedora bash
getent passwd
cat etc/shadow
```


#### daemon config
