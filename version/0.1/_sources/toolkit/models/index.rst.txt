===========
Antenna API
===========

This section describes all classes for antenna types available in the toolkit.

User has all the control to create one or more antennas. It is object oriented, the antenna can be synthesized without AEDT.

.. toctree::
   :maxdepth: 1

   bowtie
   common
   conical_spiral
   helix
   horn
   patch

Antenna synthesis:

.. code:: python

    # Import backend
    from ansys.aedt.toolkits.antenna.backend.models.horn import Conical

    # Antenna synthesis
    oantenna1 = Conical()
    oantenna1.frequency = 12.0

Antenna model generation in HFSS:

.. code:: python

    # Import pyaedt.Hfss
    from pyaedt import Hfss

    # Import backend
    from ansys.aedt.toolkits.antenna.backend.models.horn import Conical

    # Antenna synthesis
    aedtapp = Hfss()

    # Create antenna
    oantenna1 = Conical(app)
    oantenna1.model_hfss()
    oantenna1.setup_hfss()
    ...
    aedtapp.release_desktop()