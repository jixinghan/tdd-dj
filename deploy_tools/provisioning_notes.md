Provisioning a site
===================

## Required packages
* python3.6
* virtualenv + pip
* git
* nginx

Assume you have a bare VPS server with root privilege running Debian Linux operetion system.
Generally, there won't be latest python available on Debian's package repository, so you need to compile it from source yourself, here is how:
    * First, you need to install some necessary packages to get a full-fledged python compiling environment
        sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus \
                             libncursesw5-dev libgdbm-dev libc6-dev zlib1g-dev libsqlite3-dev tk-dev libssl-dev libffi-dev libreadline-dev
    * Next, get the python3.6.5 source, and compile it with some settings
        curl -OL https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz
        tar -xvzf Python-3.6.5.tgz
        cd Python-3.6.5.tgz
        ./configure --enable-optimization --enable-shared
        make
        sudo make install (default, it will be installed in /usr/local/bin, if you want to change installed directory, add '--prefix= ' when run ./configure)
    * Next, because we used '--enable-shared' when run ./configure, this means python itself's libraries are dynamicly linked.
      Our newly compiled python doesn't know where to find its own libraries, so we must explicitly tell it.
        Add /usr/local/lib to /etc/ld.so.conf and run ldconfig

After we'v installed python, the remaining is easy
    sudo apt-get install git nginx

## Nginx site configuration
* See nginx.template.conf
* Substitute USERNAME and SITENAME for your own appropriate ones, (e.g. tom staging.my-domain.com) and rename it to 'mysite' (you can use any name you prefer)
* Place the modified file into /etc/nginx/sites-available/mysite
* Make a symbolic link by
    sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/mysite
* Because we'v created a new nginx configuration, we need to reload the configuration file
    sudo nginx -t  (Check correctness of the new cofiguration)
    sudo systemctl reload nginx.service

## Customized System service configuraion for gunicorn
* See gunicorn-systemd.template.service
* Substitute USERNAME and SITENAME for your own appropriate ones, and rename it to 'gunicorn.service'
* Place the modified file into /etc/systemd/system/gunicorn.service
* Beacuse we modify systemd, we need to run
    sudo systemctl daemon-reload
  to reload the systemd configuration
* Enable the service
    sudo systemctl enable gunicorn.service

## Folder structure
Assume we have a user accont at /home/username, our site structure may looks like below

/home/username
|----sites
     |----SITENAME
          |----database
          |----source
          |----static
          |----virtualenv
