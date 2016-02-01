# DevConf 2016 Atomic Workshop

Run several containers:

 * OpenShift origin
   ```shell
   docker run -d --name "origin" \
     --privileged --pid=host --net=host \
     -v /:/rootfs:ro -v /var/run:/var/run:rw -v /sys:/sys -v /var/lib/docker:/var/lib/docker:rw \
     -v /var/lib/openshift/openshift.local.volumes:/var/lib/openshift/openshift.local.volumes \
     openshift/origin:v1.0.6 start
   ```

 * `cat`
   ```shell
   docker run -i fedora cat
   ```

 * bash with nested process
   ```shell
   docker run -ti fedora bash
   sleep 12345 &
   bash
   sleep 123456 &
   sleep 1234 &
   ```


## Docker News


### 1.8

Not much news on UI side, lots of work on backend and plugins.


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

`-d` turned into a command `daemon`, which means that `--help` can be found elsewhere:

```shell
man docker
man docker-daemon
```


### 1.9


#### `docker network`

Networking has its own UI now. The demo is about creating network and adding containers to it in runtime.

We will create `bridge` network, `overlay` networks are much more complicated.

We first create the network:

```
docker network create -d bridge fruits
```

Create webserver now:

```
docker build --tag=networking-demo ./networks
docker run --name=orange --net=fruits networking-demo
docker exec -ti orange bash
curl -v -XHEAD 0.0.0.0:8000
```

Let's create new container and try to connect to `orange`:

```
docker run -ti --rm --name pomelo fedora bash
curl -v -XHEAD http://orange:8000
```

how about now?

```
docker network connect fruits pomelo
```

Bumped into some issues?

```
docker network inspect fruits
```


#### `docker volume`

At the same time volumes have now UI too.

```shell
docker volume ls
docker volume create --name mango
docker run -ti -v mango:/mango fedora bash
docker volume inspect mango
docker cp mango:/mango .
docker volume rm mango
```

`inspect` doesn't say which conatiners use the volume. You also need to run
container if you want to know about content of a volume.


#### build arguments

https://docs.docker.com/engine/reference/builder/#arg

Build time arguments (as environment variables) which don't leak to final image

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

You can also specify stopsignal in `run`.


#### `docker stats`

```shell
docker stats
```


### 1.10

#### seccomp

seccomp is in place by default!


https://github.com/docker/docker/blob/master/docs/security/seccomp.md
https://github.com/opencontainers/specs/blob/master/config-linux.md#seccomp

Using custom profile:

```
vim seccomp/policy.json
docker run --rm -it --security-opt seccomp:seccomp/policy.json fedora bash
useradd asdqwe
touch /tmp/change_me
chown root:root /tmp/change_me
```

...to the max!

```
docker run --rm -it --security-opt seccomp:seccomp/hardcore-policy.json fedora bash
```


#### User Namespaces

https://github.com/docker/docker/blob/master/docs/reference/commandline/daemon.md#daemon-user-namespace-options

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

https://github.com/docker/docker/blob/master/docs/reference/commandline/daemon.md#daemon-configuration-file

```
--config-file=my.custom.config.json
```

You may reload with `SIGHUP`.

![config live reload](https://cloud.githubusercontent.com/assets/1050/12132395/1b06cd5a-b3d0-11e5-84ee-dfa2ab041278.gif)
