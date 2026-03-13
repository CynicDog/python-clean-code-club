# Antlr4 for Python 

## Build the official Docker image 

```bash 
git clone https://github.com/antlr/antlr4.git
cd antlr4/docker
docker build -t antlr/antlr4 --platform linux/amd64 .
```

## Compile `Hello.g4` 
```bash 
docker run --rm -u $(id -u ${USER}):$(id -g ${USER}) -v `pwd`:/work antlr/antlr4 -Dlanguage=Python3 ./hello-world/grammar/Hello.g4
```
