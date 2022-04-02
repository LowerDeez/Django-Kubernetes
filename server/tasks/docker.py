import os

from invoke import task

# Defaults
DC = "\033[0m"  # Escape to default terminal font colour
DI = "\033[1;32m"  # Start using green colour for terminal font

DEFAULT_USER = os.environ["DEFAULT_USER"]
EC2_PUBLIC_IP_ADDRESS = os.environ["EC2_PUBLIC_IP_ADDRESS"]
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_ACCOUNT_ID = os.environ["AWS_ACCOUNT_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_ECR_ACCOUNT_URL = os.environ["AWS_ECR_ACCOUNT_URL"]
AWS_DEFAULT_REGION = os.environ["AWS_DEFAULT_REGION"]
CIRCLECI_ROOT_FOLDER = "/home/circleci/project"
PROJECT_ROOT_FOLDER = "/home/ubuntu/devops_try"


def message(ctx, text, color=DI) -> None:
    ctx.run(f"echo '{color}{text}{DC}'")


def command(ctx, text) -> None:
    message(ctx, text)
    ctx.run(f"ssh -o StrictHostKeyChecking=no {DEFAULT_USER}@{EC2_PUBLIC_IP_ADDRESS} '{text}'", pty=True)


@task()
def login(ctx):
    """
    Login to AWS ECR
    """
    aws_login_command = (
        f"aws ecr get-login-password --region {AWS_DEFAULT_REGION} "
        f"| docker login --username AWS --password-stdin {AWS_ECR_ACCOUNT_URL}"
    )
    message(ctx, "Login to ECR")
    command(ctx, f"export AWS_ACCESS_KEY_ID={AWS_ACCESS_KEY_ID}")
    command(ctx, f"export AWS_ACCOUNT_ID={AWS_ACCOUNT_ID} ")
    command(ctx, f"export AWS_SECRET_ACCESS_KEY={AWS_SECRET_ACCESS_KEY}")
    command(ctx, f"{aws_login_command}")


@task(iterable=["molo_envs"], pre=[login])
def deploy(ctx, molo_envs):
    ctx.run("cd /home/circleci/project/.envs/.production/ && cat .django")
    command(ctx, f"mkdir -p {PROJECT_ROOT_FOLDER}/.envs/.production/")
    ctx.run(
        f"scp {CIRCLECI_ROOT_FOLDER}/.envs/.production/.django "
        f"{DEFAULT_USER}@{EC2_PUBLIC_IP_ADDRESS}:{PROJECT_ROOT_FOLDER}/.envs/.production/.django"
    )
    ctx.run(f"scp {CIRCLECI_ROOT_FOLDER}/production.yml {DEFAULT_USER}@{EC2_PUBLIC_IP_ADDRESS}:{PROJECT_ROOT_FOLDER}")
    command(ctx, f"cd {PROJECT_ROOT_FOLDER} && ls -la")
    # command(ctx, "export $(cat ./.envs/.production/.django | xargs)")
    command(ctx, f"cd {PROJECT_ROOT_FOLDER} && docker pull {AWS_ECR_ACCOUNT_URL}:django")
    command(ctx, f"cd {PROJECT_ROOT_FOLDER} && docker pull {AWS_ECR_ACCOUNT_URL}:nginx")
    command(ctx, f"cd {PROJECT_ROOT_FOLDER} && docker pull {AWS_ECR_ACCOUNT_URL}:celeryworker")
    command(ctx, f"cd {PROJECT_ROOT_FOLDER} && docker-compose -f production.yml up -d")
