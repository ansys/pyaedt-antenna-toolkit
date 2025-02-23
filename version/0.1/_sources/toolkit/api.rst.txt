Toolkit API
===========
This section list the available toolkit methods in the backend at toolkit level.

Toolkit API are the calls used by the frontend. It wraps some of the methods of the **Antenna API**.

.. currentmodule:: ansys.aedt.toolkits.antenna.backend.api

.. autosummary::
   :toctree: _autosummary

   Toolkit

The API can be used as in the following example:

.. code:: python

    # Import required modules for the example
    import time

    # Import backend
    from ansys.aedt.toolkits.template.backend.api import Toolkit

    # Initialize generic service
    service = Toolkit()

    # Get the default properties loaded from json file
    properties = service.get_properties()

    # Set properties
    new_properties = {"aedt_version": "2023.1"}
    service.set_properties(new_properties)
    properties = service.get_properties()

    # Launch AEDT
    msg = service.launch_aedt()

    # Wait until thread is finished
    response = service.get_thread_status()
    while response[0] == 0:
        time.sleep(1)
        response = service.get_thread_status()

    # Create geometry
    msg = service.create_geometry()

    # Wait until thread is finished
    response = service.get_thread_status()
    while response[0] == 0:
        time.sleep(1)
        response = service.get_thread_status()

    # Desktop is released here
    service.release_aedt()
