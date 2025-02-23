Bowtie
======
This page list the classes available for bowtie antennas:

.. currentmodule:: ansys.aedt.toolkits.antenna.backend.antenna_models.bowtie

.. autosummary::
   :toctree: _autosummary

   BowTieNormal
   BowTieRounded
   BowTieSlot

You must use these methods from PyAEDT as shown in this example:

.. code:: python

    from ansys.aedt.core import Hfss

    from ansys.aedt.toolkits.antenna.backend.antenna_models.bowtie import BowTieNormal

    aedtapp = Hfss()

    # Create antenna
    oantenna1 = BowTieNormal(app)
    oantenna1.frequency = 12.0
    oantenna1.model_hfss()
    oantenna1.setup_hfss()
    ...
    aedtapp.release_desktop()
