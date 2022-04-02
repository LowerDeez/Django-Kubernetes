from invoke import Collection

from .code_style import black, black_check, isort, isort_check, pylama
from .docker import deploy, login

ns = Collection()

# test and code style
ns.add_task(isort)
ns.add_task(isort_check)
ns.add_task(pylama)
ns.add_task(black)
ns.add_task(black_check)

# Docker feature
docker = Collection("docker")
docker.add_task(deploy, "deploy")
docker.add_task(login, "login")
ns.add_collection(docker)
