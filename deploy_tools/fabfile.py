from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run

import random 


REPO_URL = 'https://github.com/jixinghan/tdd-dj.git'

def deploy(type):
    site_dir = f'/home/{env.user}/sites/{type}'
    source_dir = site_dir + '/source'

    _create_directory_structure_if_necessary(site_dir)
    _get_latest_source(source_dir)
    _update_app_setting_file(source_dir, env.host)
    _update_virtualenv(source_dir)
    _update_static_files(source_dir)
    _update_database(source_dir)

def _create_directory_structure_if_necessary(site_dir):
    for sub_dir in ('database', 'source', 'static', 'virtualenv'):
        run(f'mkdir -p {site_dir}/{sub_dir}')

def _get_latest_source(source_dir):
    if exists(source_dir + '/.git'):
        run(f'cd {source_dir} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_dir}')
    current_local_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'cd {source_dir} && git reset --hard {current_local_commit}')

def _update_app_setting_file(source_dir, site_name):
    setting_file_path = source_dir + '/superlists/settings.py'
    sed(setting_file_path, 'DEBUG = True', 'DEBUG = False')
    sed(setting_file_path, 'ALLOWED_HOSTS =.+$', f'ALLOWED_HOSTS = ["{site_name}"]')
    secret_key_file = source_dir + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(setting_file_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_dir):
    virtualenv_dir = source_dir + '/../virtualenv'
    if not exists(virtualenv_dir + '/bin/pip'):
        run(f'python3 -m venv {virtualenv_dir}')
    run(f'{virtualenv_dir}/bin/pip install -r {source_dir}/requirements.txt')

def _update_static_files(source_dir):
    run(
        f'cd {source_dir}'
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput'
    )

def _update_database(source_dir):
    run(
        f'cd {source_dir}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput'
    )
