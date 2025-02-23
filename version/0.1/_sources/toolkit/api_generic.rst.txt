Generic API
===========
This section list the available generic methods in the backend, these methods are the same for all toolkits:

.. currentmodule:: ansys.aedt.toolkits.antenna.backend.common.api_generic

.. autosummary::
   :toctree: _autosummary

   ToolkitGeneric

**ToolkitGeneric** class is accessible directly from :doc:`api` because it is inherited, then
you can create an object as in the following example to use both classes:

.. code:: python

    # Import required modules for the example
    import time

    # Import backend services
    from ansys.aedt.toolkits.template.backend.api import Toolkit

    # Backend object
    service = Toolkit()

    # Get the default properties loaded from json file
    properties = service.get_properties()

    # Set properties
    new_properties = {"aedt_version": "2022.2"}
    service.set_properties(new_properties)
    properties = service.get_properties()

    # Get AEDT sessions
    sessions = service.aedt_sessions()

    # Launch AEDT
    msg = service.launch_aedt()

    # Wait until thread is finished
    response = service.get_thread_status()
    while response[0] == 0:
        time.sleep(1)
        response = service.get_thread_status()

    # Desktop is released here
    service.release_aedt()


