Patch
=====
This section list the available patch antennas:

.. currentmodule:: ansys.aedt.toolkits.antenna.backend.models.patch

.. autosummary::
   :toctree: _autosummary

   RectangularPatchEdge
   RectangularPatchProbe
   RectangularPatchInset

The API must be used using PyAEDT as in the following example:

.. code:: python

    from pyaedt import Hfss

    from ansys.aedt.toolkits.antenna.backend.models.patch import RectangularPatchEdge

    aedtapp = Hfss()

    # Create antenna
    oantenna1 = RectangularPatchProbe(app)
    oantenna1.frequency = 12.0
    oantenna1.model_hfss()
    oantenna1.setup_hfss()
    ...
    aedtapp.release_desktop()
