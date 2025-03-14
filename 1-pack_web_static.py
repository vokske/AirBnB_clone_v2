#!/usr/bin/python3
# Generates a .tgz archive from the contents of a folder

from fabric.api import task
from datetime import datetime
import os
import tarfile

@task
def do_pack():
    """Generates a .tgz archive from the contents of a specific directory."""
    try:
        # Create versions folder if it doesn't exist
        if not os.path.exists('versions'):
            os.makedirs('versions')

        # Generate archive name using the timestamp
        archive_name = f"versions/web_static_{datetime.now().strftime("%Y%m%d%H%M%S")}.tgz"

        # Create a .tgz archive using tarfile

        with tarfile.open(archive_name, 'w:gz') as tar:
            tar.add("web_static", arcname=os.path.basename("web_static"))

        # Return the archive path if process successful
        return archive_name
    except Exception:
        return None
