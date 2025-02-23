Conical spiral
==============
This section list the available conical spiral antennas:

.. currentmodule:: ansys.aedt.toolkits.antenna.backend.models.conical_spiral

.. autosummary::
   :toctree: _autosummary

   Archimedean

The API must be used using PyAEDT as in the following example:

.. code:: python

    from pyaedt import Hfss

    from ansys.aedt.toolkits.antenna.backend.models.conical_spiral import Archimedean

    aedtapp = Hfss()

    # Create antenna
    oantenna1 = RectangularPatchProbe(app)
    oantenna1.frequency = 12.0
    oantenna1.model_hfss()
    oantenna1.setup_hfss()
    ...
    aedtapp.release_desktop()
