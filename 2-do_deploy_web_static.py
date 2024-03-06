#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric import task, Connection
from os.path import exists
from os import remove
from datetime import datetime

env.hosts = ['<IP web-01>', 'IP web-02']


@task
def do_deploy(c, archive_path):
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        archive_name = archive_path.split('/')[-1]
        tmp_path = '/tmp/{}'.format(archive_name)
        c.put(archive_path, tmp_path)

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension> on the web server
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        release_path = '/data/web_static/releases/{}/'.format(timestamp)
        c.run('mkdir -p {}'.format(release_path))
        c.run('tar -xzf {} -C {}'.format(tmp_path, release_path))
        c.run('rm {}'.format(tmp_path))

        # Move contents of web_static/ to release_path
        c.run('mv {}web_static/* {}'.format(release_path, release_path))
        c.run('rm -rf {}web_static'.format(release_path))

        # Delete the symbolic link /data/web_static/current from the web server
        current_path = '/data/web_static/current'
        if exists(current_path):
            c.run('rm {}'.format(current_path))

        # Create a new the symbolic link /data/web_static/current on the web server
        c.run('ln -s {} {}'.format(release_path, current_path))

        return True
    except Exception as e:
        print('Error:', e)
        return False
