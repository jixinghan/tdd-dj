from fabric.api import env

def deploy(type):
    print(type)
    print(env.user, env.host)
