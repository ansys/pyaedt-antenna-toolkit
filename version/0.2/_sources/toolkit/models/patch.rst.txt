Patch
=====
This page lists the classes available for patch antennas:

.. currentmodule:: ansys.aedt.toolkits.antenna.backend.antenna_models.patch

.. autosummary::
   :toctree: _autosummary

   RectangularPatchEdge
   RectangularPatchProbe
   RectangularPatchInset

You must use these methods from PyAEDT as shown in this example:

.. code:: python

    from pyaedt import Hfss

    from ansys.aedt.toolkits.antenna.backend.antenna_models.patch import (
        RectangularPatchEdge,
    )

    aedtapp = Hfss()

    # Create antenna
    oantenna1 = RectangularPatchProbe(app)
    oantenna1.frequency = 12.0
    oantenna1.model_hfss()
    oantenna1.setup_hfss()
    ...
    aedtapp.release_desktop()
