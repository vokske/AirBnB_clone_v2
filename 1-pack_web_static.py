#!/usr/bin/python3
"""
This script is meant to generate a .gtz archive from the contents of the web_static folder from the Airbnb clone repo, using a function do_pack.

The script imports the task function from Fabric, the datetime module from datetime, os module, and the tarfile module.
"""
from fabric.api import task
from datetime import datetime
import os
import tarfile

def do_pack():
    """
    A function that generates a .tgz archive from the contents of a specific folder.
    Returns:
        archive_name if process is successful, None otherwise.

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
