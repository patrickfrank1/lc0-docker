# lc0-docker

Run [Leela Chess Zero](https://github.com/LeelaChessZero/lc0) anywhere in a docker container on CPU

## Requirements

This repository requires a working docker installation on your host system. If you don't have docker installed, please follow the [official installation guide](https://docs.docker.com/engine/install/ubuntu/). Afterwards you can perform the following steps to get lc0 running.

## Build an image and run a container

First you need to clone the git repository:

```bash
git clone https://github.com/patrickfrank1/lc0-docker.git
```

Next you select a git branch, each branch lets you build a different image. The images are described in detail in the subsections below. To build the image and run a container, simply execute the ./build.sh script. Scripts to stop and remove the container are also available.

### lc0 base image

This image is implemented on the `master` branch. It installs lc0 and preconfigures it with the Leelenstein 15 network. Build the image and run the container with default settings:

``` bash
./build.sh
```

The engine should now be accessible via command line.

![image](https://user-images.githubusercontent.com/25801668/130368968-eabf85fe-549d-4fea-8a50-6dcb666c4311.png)

Communicate via [UCI Protocol](http://wbec-ridderkerk.nl/html/UCIProtocol.html), for example to analyse a position to depth 10 first set up the position, then strat the analysis.

```
position fen rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR
go depth 10
```

The console output should look something like this:

![image](https://user-images.githubusercontent.com/25801668/130369155-39819e86-7506-4256-8bf5-8a0410683e36.png)

Exit the engine by sending the `quit` command, then exit the container by sending the `exit` command. Logs are by default saved to `./settings/log.txt` in your local directory.

### lc0 and stockfish base image

This image is somewhat similar to the lc0 base image, with the exception that here two UCI compliant chess engines are available: lc0 and stockfish 14. To build the image check out the git branch `lc0-and-stockfish-command-line`.

``` bash
git checkout lc0-and-stockfish-command-line
```

After building the image with the build script

``` bash
./build.sh
```

the container provides the standard shell. To start lc0 execute the command

``` bash
lc0 --config=/lc0/settings/lc0.config 
```

this will set the correct path to the configuration and network files. To analyze with stockfish execute the command

``` bash
stockfish_14_x64_popcnt
```

### lc0 analysis with fie input and output

This image implements a service that analyses a set of positions and prints the analysis results to file. The container runs silently in the background. Check out the git branch `lc0-file-io`

``` bash
git checkout lc0-file-io
```

and build the image

``` bash
./build.sh
```

now navigate to `./analysis/queue.txt` in your workspace and follow the instructions therein. For example the following input, which runs an analysis for exactly one position

![image](https://user-images.githubusercontent.com/25801668/130369628-1af28025-fbcd-4cbf-bb97-ed000ea2f261.png)

results in the following output file (truncated)

![image](https://user-images.githubusercontent.com/25801668/130369674-54c51bd8-fd3f-4b03-84a2-9b8c4415ea8c.png)

