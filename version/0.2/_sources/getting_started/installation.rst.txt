.. _installation:

Installation
============

The AEDT Antenna Toolkit can be installed like any other open source package.

You can either install both the backend and user interface (UI) methods or install only the backend methods.

To install both the backend and UI methods, run this command:

.. code:: bash

    pip install pyaedt-toolkits-antenna[all]

If you only need the common API, install only the backend methods with this
command:

.. code:: bash

    pip install pyaedt-toolkits-antenna

To install the toolkit offline, you can use a wheelhouse.
On the `Releases <https://github.com/ansys/pyaedt-toolkits-antenna/releases>`_ page, you can find the wheelhouses for
specific release in its asserts and download the wheelhouse.

You can then install the toolkit with this command:

.. code:: bash

    pip install --no-cache-dir --no-index --find-links=<path_to_wheelhouse>/ansys-aedt-toolkits-antenna-v0.1.3-wheelhouse-windows-latest-3.10 ansys_aedt_toolkits_antenna

You can also install the toolkit using the toolkit manager. For more information,
see the toolkit manager (TBD).
