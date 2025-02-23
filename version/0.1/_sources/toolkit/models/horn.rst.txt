Horn
====
This section lists the available horns:

.. currentmodule:: ansys.aedt.toolkits.antenna.backend.models.horn

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

The API must be used using PyAEDT as in the following example:

.. code:: python

    import pyaedt.Hfss

    from ansys.aedt.toolkits.antenna.backend.models.horn import Conical

    aedtapp = Hfss()

    # Create antenna
    oantenna1 = Conical(app)
    oantenna1.frequency = 12.0
    oantenna1.model_hfss()
    oantenna1.setup_hfss()
    ...
    aedtapp.release_desktop()


