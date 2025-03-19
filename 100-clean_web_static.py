#!/usr/bin/python3
"""
This script is meant to generate a .gtz archive from the contents of the web_static folder from the Airbnb clone repo, using a function do_pack.

The script imports the task function from Fabric, the datetime module from datetime, os module, and the tarfile module.
"""
from fabric.api import env, put, run, local
from datetime import datetime
import os
import tarfile

env.hosts = ['18.208.106.131', '54.235.229.175']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/sandbox'


def do_clean(number=0):
    """
    Function deletes out-of-date archives.

    Args:
        number (int): Number of archives, including the most recent, to keep.
            If 0 or 1, keep only the most recent archive.
            If 2, keep the most recent and the second most recent, and so on.
            Default is 0.
    """
    try:
        # Convert number to integer
        number = int(number)

        # Ensure number isn't negative
        if number < 0:
            return False

        # Keep at least one archive
        if number == 0:
            number = 1

        # Get list of archives sorted by modification time (most recent first)
        local_archives = sorted(
            os.listdir('versions'),
            key=lambda f: os.path.getmtime(os.path.join('versions', f))
        )

        # Delete all archives except the most recent `number` of archives
        for archive in local_archives[:-number]:
            local(f'rm -rf versions/{archive}')

        # Clean up in remote web servers (/data/web_static/releases folder)
        remote_archives = run('ls -t /data/web_static/releases').split()
        for archive in remote_archives[:-number]:
            run(f'rm -rf /data/web_static/releases/{archive}')
        return True
    except Exception:
        return False


