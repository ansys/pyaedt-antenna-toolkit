Helix
=====
This pages lists the classes available for helix antennas:

.. currentmodule:: ansys.aedt.toolkits.antenna.backend.antenna_models.helix

.. autosummary::
   :toctree: _autosummary

   AxialMode

You must use these methods from PyAEDT as shown in this example:

.. code:: python

    from pyaedt import Hfss

    from ansys.aedt.toolkits.antenna.backend.antenna_models.helix import AxialMode

    aedtapp = Hfss()

    # Create antenna
    oantenna1 = AxialMode(app)
    oantenna1.model_hfss()
    oantenna1.setup_hfss()
    ...
    aedtapp.release_desktop()
