from fabric import Connection, task


@task
def restart_django(ctx):
    c = Connection('lagagogn.is')
    result = c.run('sudo service gunicorn restart')
    print(result)
