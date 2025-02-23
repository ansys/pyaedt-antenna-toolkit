Helix
=====
This section list the available helix antennas:

.. currentmodule:: ansys.aedt.toolkits.antenna.backend.models.helix

.. autosummary::
   :toctree: _autosummary

   AxialMode

The API must be used using PyAEDT as in the following example:

.. code:: python

    from pyaedt import Hfss

    from ansys.aedt.toolkits.antenna.backend.models.helix import AxialMode

    aedtapp = Hfss()

    # Create antenna
    oantenna1 = AxialMode(app)
    oantenna1.model_hfss()
    oantenna1.setup_hfss()
    ...
    aedtapp.release_desktop()
