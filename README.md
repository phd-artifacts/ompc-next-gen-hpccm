# ompc-next-gen-hpccm

From George's receipe;

```sh
virtualenv .venv
source .venv/bin/activate
pip install hpccm
```

```sh
source .venv/bin/activate
hpccm --format docker --recipe ogbon_recipe.py > Dockerfile
```
