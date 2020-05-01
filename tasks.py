import warnings

from invoke import task


@task
def test(ctx):
    ctx.run("pytest tests/ --cov")
    ctx.run("black --check .")
    ctx.run("pycodestyle")


@task
def prepare_data(ctx, force=False):
    if force:
        ctx.run("rm ./data/tmp/* -rfv")
        for dir in ["br", "world"]:
            ctx.run(f"cd data/{dir} && python prepare.py")

    ctx.run("python -m mundi_demography.prepare")
