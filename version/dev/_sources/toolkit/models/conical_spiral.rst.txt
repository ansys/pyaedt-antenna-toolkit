Conical spiral
==============
This page lists the classes available for conical spiral antennas:

.. currentmodule:: ansys.aedt.toolkits.antenna.backend.antenna_models.conical_spiral

.. autosummary::
   :toctree: _autosummary

   Archimedean

You must use these methods from PyAEDT as shown in this example:

.. code:: python

    from ansys.aedt.core import Hfss

    from ansys.aedt.toolkits.antenna.backend.antenna_models.conical_spiral import (
        Archimedean,
    )

    aedtapp = Hfss()

    # Create antenna
    oantenna1 = RectangularPatchProbe(app)
    oantenna1.frequency = 12.0
    oantenna1.model_hfss()
    oantenna1.setup_hfss()
    ...
    aedtapp.release_desktop()
