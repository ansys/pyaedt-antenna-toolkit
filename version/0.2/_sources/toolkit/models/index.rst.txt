===========
Antenna API
===========

The Antenna API contains classes for all antenna types available in the toolkit:

.. toctree::
   :maxdepth: 1

   bowtie
   common
   conical_spiral
   helix
   horn
   patch

You use the Antenna API at the model level from PyAEDT.

You can create one or more antennas. An antenna is object-oriented. You can synthesis an
antenna without AEDT.

This code shows how to synthesis an antenna:

.. code:: python

    # Import backend
    from ansys.aedt.toolkits.antenna.backend.models.horn import Conical

    # Synthesize antenna
    oantenna1 = Conical()
    oantenna1.frequency = 12.0

This code shows how to synthesize and create a model of an antenna in HFSS:

.. code:: python

    # Import HFSS
    from pyaedt import Hfss

    # Import backend
    from ansys.aedt.toolkits.antenna.backend.models.horn import Conical

    # Synthesize antenna
    aedtapp = Hfss()

    # Create antenna
    oantenna1 = Conical(app)
    oantenna1.model_hfss()
    oantenna1.setup_hfss()
    ...
    aedtapp.release_desktop()
