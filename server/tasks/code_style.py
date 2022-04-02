from invoke import task


@task()
def isort_check(ctx):
    ctx.run("isort --check-only")


@task()
def isort(ctx):
    ctx.run("isort . --apply")


@task()
def pylama(ctx):
    ctx.run("pylama apps")


@task()
def black_check(ctx):
    ctx.run("black --check .")


@task()
def black(ctx):
    ctx.run("black .")
