# ompc-next-gen-hpccm

The CI in this repository pushes the image to:
https://hub.docker.com/r/rodrigoceccato/ompc-base


From George's receipe;

```sh
virtualenv .venv
source .venv/bin/activate
pip install hpccm
```

```sh
docker run -d -p 5000:5000 --restart=always --name registry registry:2
```

```sh
source .venv/bin/activate
hpccm --format docker --recipe ogbon_recipe.py > Dockerfile
```

```sh
docker build . --tag localhost:5000/hpccm_tmp
docker push localhost:5000/hpccm_tmp
APPTAINER_NOHTTPS=1 APPTAINER_TMPDIR=$(realpath .cache) singularity pull docker://localhost:5000/hpccm_tmp
```
