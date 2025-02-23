Common
======
This pages lists common methods available in the Antenna API:

.. currentmodule:: ansys.aedt.toolkits.antenna.backend.antenna_models.common

.. autosummary::
   :toctree: _autosummary

   TransmissionLine
   StandardWaveguide

You must use these methods from PyAEDT as shown in this example:

.. code:: python

    from ansys.aedt.toolkits.antenna.backend.antenna_models.common import TransmissionLine

    # Transmission line calculation
    tl_calc = TransmissionLine(frequency=2)
    tl_calc.stripline_calculator(substrate_height=10, permittivity=2.2, impedance=60)
