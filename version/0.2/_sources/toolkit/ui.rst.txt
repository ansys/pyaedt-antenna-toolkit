==============
Antenna wizard
==============

This section describes how to use the Antenna wizard. It assumes that you have already launched the
wizard from either the AEDT menu or AEDT console. For toolkit installation and wizard
launching information, see these topics:

- :ref:`install-toolkit-AEDT`
- :ref:`install_toolkit_console_ui`

#. On the **Settings** tab, specify settings for either creating an AEDT session or
   connecting to an existing AEDT session.

   .. note::
      If the Antenna Toolkit Wizard is launched from AEDT, the **Settings** tab does not appear
      because the toolkit is directly connected to the specific AEDT session.

   .. image:: ../_static/settings.png
      :width: 800
      :alt: Settings tab

   The wizard has a progress circle and a logger box, where you can see the status of every operation.

   .. image:: ../_static/progress.png
      :width: 800
      :alt: Progress tab

   You can choose different antennas from the **Antenna catalog** menu to load the antennas
   template.

   .. image:: ../_static/antenna_catalog.png
      :width: 800
      :alt: Antenna catalog

   .. image:: ../_static/antenna_catalog_2.png
      :width: 800
      :alt: Antenna catalog 2

   For example, if you select **Antennas > Bowtie > Bowtie Normal**,
   the central page is updated to the **Synthesis** page and it shows the antenna template:

   .. image:: ../_static/antenna_template.png
      :width: 800
      :alt: Antenna template

   You have two options: **Synthesis** and **Generate**.
   The **Generate** button is unavailable if the wizard is not connected to AEDT.

   - The **Synthesis** button is for performing the synthesis of the antenna. A connection to AEDT
   is not needed.
     You can see the parameters that control the antenna geometry. Additionally, you can do as many
     syntheses as you want and even change the antenna template.

     .. image:: ../_static/antenna_synthesis.png
        :width: 800
        :alt: Antenna synthesis

   - The **Generate** button is for creating an HFSS model. It uses the **3D Component**,
     **Create Hfss Setup**, and **Lattice pair** checkboxes along with the **Sweep Bandwidth %** option
     It also uses the length and frequency unit to perform the HFSS setup.

     Descriptions follow for how to use the checkboxes on the **Design** tab:

     - If you select the **3D Component** checkbox, the toolkit creates the antenna and replaces it
       with a 3D component.

     - If you select the **Generate** checkbox, the toolkit automatically creates the boundaries,
       excitations, and ports needed to simulate the antenna. Once you create an HFSS model, you cannot
       create another antenna. Both the **Synthesis** and **Generate** buttons become unavailable.
       If you want to create another antenna, you must restart the toolkit.

     - If you select the **Lattice pair** checkbox, the toolkit creates a unit cell assigning a
       lattice pair boundary.

Once you create an antenna, the **Synthesis** tab displays an interactive 3D model rather than
the image of the antenna template:

.. image:: ../_static/antenna_generate.png
   :width: 800
   :alt: Antenna generated

If AEDT is launched in non-graphical mode, you can still see the generated model.

In the wizard, you can modify the parameters interactively, watching both the HFSS model and the
interactive 3D plot in the wizard change.

Finally, on the wizard's **Analysis** tab, you have the **Get results** button.
This second button is unavailable until after you analyze the HFSS design.

When you click **Get results**, the project is analyzed.
You can specify the number of cores to use in the simulation.

Once the project is solved, you can click **Get results** on the **Analysis** tab to view results.

.. image:: ../_static/get_results.png
   :width: 800
   :alt: Result
