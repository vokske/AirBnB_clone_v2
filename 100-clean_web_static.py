#!/usr/bin/python3
"""
This script is meant to generate a .gtz archive from the contents of the web_static folder from the Airbnb clone repo, using a function do_pack.

The script imports the task function from Fabric, the datetime module from datetime, os module, and the tarfile module.
"""
from fabric.api import env, put, run
from datetime import datetime
import os
import tarfile

env.hosts = ['18.208.106.131', '54.235.229.175']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/sandbox'

def do_pack():
    """
    A function that generates a .tgz archive from the contents of a specific folder

    Returns:
        archive_path if steps are successful, None otherwise
    """

    try:
        # Create versions folder if it doesn't exist
        if not os.path.exists('versions'):
            os.makedirs('versions')

        # Generate archive name using the timestamp
        archive_name = f'versions/web_static_{datetime.now().strftime("%Y%m%d%H%M%S")}.tgz'

        # Create a .tgz archive using tarfile

        with tarfile.open(archive_name, 'w:gz') as tar:
            tar.add("web_static", arcname=os.path.basename("web_static"))

        # Return the archive path if process successful
        return archive_name
    except Exception:
        return None

def do_deploy(archive_path):
    """
    A function that distributes an archive to web servers

    Args:
        archive_path (str): Path to the archive file.

    Returns:
        bool: True if all operations succeed, False otherwise
    """

    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp directory on the web server
        put(archive_path, '/tmp')

        # Extract the archive filename without the extension
        archive_filename = archive_path.split('/')[-1]
        release_folder = f'/data/web_static/releases/{archive_filename.split(".")[0]}'

        # Create the release folder
        run(f'mkdir -p {release_folder}')

        # Uncompress the archive to the release folder
        run(f'tar -xzf /tmp/{archive_filename} -C {release_folder}')

        # Delete the archive from the web server
        run(f'rm /tmp/{archive_filename}')

        # Move the contents of the web_static folder to the release folder
        run(f'mv {release_folder}/web_static/* {release_folder}/')

        # Remove the empty web_static folder
        run(f'rm -rf {release_folder}/web_static')

        # Delete the old symbolic link

        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the new release
        run(f'ln -s {release_folder} /data/web_static/current')
        return True
    except Exception:
        return False

def deploy():
    """
    Executes a full deployment of an archive to web servers.

    Returns:
        bool: True if all operations succeed, False otherwise.
    """
    
    # Call the do_pack function to create the archive
    archive_path = do_pack()

    # Verify that the archive was created
    if not archive_path:
        return False

    # Deploy the archive
    return do_deploy(archive_path)

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

        # Clean up archives in the versions folder on local
        local_archives = sorted(os.listdir('versions'))
        for archive in local_archives[:-number]:
            local(f'rm -rf versions/{archive}')

        # Clean up in remote web servers (/data/web_static/releases folder)
        remote_archives = run('ls -t /data/web_static/releases').split()
        for archive in remote_archives[:-number]:
            run(f'rm -rf /data/web_static/releases/{archive}')
        return True
    exception Exception:
        return False


