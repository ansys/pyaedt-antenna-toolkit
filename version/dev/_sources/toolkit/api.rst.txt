Toolkit API
===========

The Toolkit API contains the ``Toolkit`` class, which provides methods for
controlling the toolkit workflow. This API provides methods
for synthesizing and creating an antenna. You use the Toolkit API at the
toolkit level.

The common methods for creating an AEDT session or connecting to an existing AEDT session are provided by the
`Common PyAEDT toolkit library <https://aedt.common.toolkit.docs.pyansys.com/>`_.

.. currentmodule:: ansys.aedt.toolkits.antenna.backend.api

.. autosummary::
   :toctree: _autosummary

   ToolkitBackend

You can use the Toolkit API as shown in this example:

.. code:: python

    # Import required modules for the example
    import time

    # Import backend
    from ansys.aedt.toolkits.template.backend.api import ToolkitBackend

    # Initialize generic service
    toolkit_api = Toolkit()

    # Load default properties from a JSON file
    properties = toolkit_api.get_properties()

    # Set properties
    new_properties = {"aedt_version": "2023.1"}
    toolkit_api.set_properties(new_properties)
    properties = toolkit_api.get_properties()

    # Launch AEDT
    thread_msg = toolkit_api.launch_thread(toolkit_api.launch_aedt)

    # Wait until thread is finished
    idle = toolkit_api.wait_to_be_idle()
    if not idle:
        print("AEDT not initialized.")
        sys.exit()

    # Create geometry
    toolkit_api.connect_design("HFSS")

    # Create setup when antenna is created
    properties.antenna.setup.create_setup = True
    properties.antenna.synthesis.outer_boundary = "Radiation"

    # Generate antenna
    antenna_parameter = toolkit_api.get_antenna("RectangularPatchProbe")

    # Release AEDT
    toolkit_api.release_aedt()
