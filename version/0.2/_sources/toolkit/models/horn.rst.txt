Horn
====
This page lists the classes available for horns:

.. currentmodule:: ansys.aedt.toolkits.antenna.backend.antenna_models.horn

.. autosummary::
   :toctree: _autosummary

   Conical
   Corrugated
   Elliptical
   EPlane
   HPlane
   Pyramidal
   PyramidalRidged
   QuadRidged

You must use these methods from PyAEDT as shown in this example:

.. code:: python

    import pyaedt.Hfss

    from ansys.aedt.toolkits.antenna.backend.antenna_models.horn import Conical

    aedtapp = Hfss()

    # Create antenna
    oantenna1 = Conical(app)
    oantenna1.frequency = 12.0
    oantenna1.model_hfss()
    oantenna1.setup_hfss()
    ...
    aedtapp.release_desktop()


