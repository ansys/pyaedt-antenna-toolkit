# # Antenna toolkit example
#
# This example demonstrates how to use the ``ToolkitBackend`` class.
# It initiates AEDT through PyAEDT, sets up an empty HFSS design, and proceeds to create the antenna.


# ## Perform required imports

import sys
import tempfile

from ansys.aedt.core import generate_unique_project_name
from ansys.aedt.core.generic.farfield_visualization import FfdSolutionData

from ansys.aedt.toolkits.antenna.backend.api import ToolkitBackend
from ansys.aedt.toolkits.antenna.backend.models import properties

# ##  Set AEDT version
#
# Set AEDT version.

aedt_version = "2024.2"

# ## Set non-graphical mode
#
# Set non-graphical mode.

non_graphical = True

# ## Create temporary directory

temp_dir = tempfile.TemporaryDirectory(suffix="_ansys")
project_name = generate_unique_project_name(root_name=temp_dir.name, project_name="antenna_toolkit")

# ## Set default properties

properties.aedt_version = aedt_version
properties.non_graphical = non_graphical
properties.active_project = project_name

# ## Initialize toolkit
#
# Initialize the toolkit.

toolkit_api = ToolkitBackend()

# ## Get available_antennas

print(toolkit_api.available_antennas)

# ## Get default properties

backend_properties = toolkit_api.get_properties()
frequency = backend_properties["antenna"]["synthesis"]["frequency"]
frequency_units = backend_properties["antenna"]["synthesis"]["frequency_unit"]
length_unit = backend_properties["antenna"]["synthesis"]["length_unit"]

# ## Modify default length units

properties.antenna.synthesis.length_unit = "cm"

# ## Create antenna object only for synthesis
#
# Create antenna object.

antenna_parameters_1 = toolkit_api.get_antenna("RectangularPatchProbe", synth_only=True)

print(
    "Patch X length: {}{} at {}{}".format(
        str(antenna_parameters_1["patch_x"]),
        length_unit,
        frequency,
        frequency_units,
    )
)

# ## Change synthesis frequency
#
# Modify resonance frequency and modify parameters with the ``set_properties()`` method.

new_frequency1 = 12.0
new_properties = {"frequency": new_frequency1}
toolkit_api.set_properties(new_properties)

antenna_parameters_2 = toolkit_api.get_antenna("RectangularPatchProbe", synth_only=True)

print(
    "Patch X length: {}{} at {}{}".format(
        str(antenna_parameters_2["patch_x"]),
        length_unit,
        new_frequency1,
        frequency_units,
    )
)

# ## Change synthesis frequency
#
# Modify resonance frequency with properties directly.

new_frequency2 = 15.0
properties.antenna.synthesis.frequency = new_frequency2

antenna_parameters_3 = toolkit_api.get_antenna("RectangularPatchProbe", synth_only=True)

print(
    "Patch X length: {}{} at {}{}".format(
        str(antenna_parameters_3["patch_x"]),
        length_unit,
        new_frequency2,
        frequency_units,
    )
)

# ## Initialize AEDT
#
# Launch a new AEDT session in a thread.

thread_msg = toolkit_api.launch_thread(toolkit_api.launch_aedt)

# ## Wait for the toolkit thread to be idle
#
# Wait for the toolkit thread to be idle and ready to accept a new task.

idle = toolkit_api.wait_to_be_idle()
if not idle:
    print("AEDT not initialized.")
    sys.exit()

# ## Connect to HFSS design
#
# Create an HFSS design.

toolkit_api.connect_design("HFSS")

# ## Create setup when antenna is created
#
# Set ``create_setup`` property.

properties.antenna.setup.create_setup = True
properties.antenna.synthesis.outer_boundary = "Radiation"

# ## Create antenna in HFSS
#
# Create antenna and set up in HFSS.

antenna_parameter = toolkit_api.get_antenna("RectangularPatchProbe")

# ## Try. to create antenna
#
# The AEDT Antenna Toolkit API does not allow the creation of more than one antenna. However, you can use the antenna
# model's API to create more than one antenna.

new_antenna = toolkit_api.get_antenna("BowTie")

print(new_antenna)

# ## Set properties
#
# Move antenna X position

toolkit_api.update_hfss_parameters("pos_x", "20")

# ## Fit all

toolkit_api.connect_design()

toolkit_api.aedtapp.modeler.fit_all()

toolkit_api.release_aedt(False, False)

# ## Set properties
#
# Move antenna X position to origin

toolkit_api.update_hfss_parameters("pos_x", "0")

# ## Analyze design in batch mode

toolkit_api.analyze()

# ## Get scattering results

scattering_data = toolkit_api.scattering_results()

# ## Get farfield results

frequency_str = str(properties.antenna.synthesis.frequency) + properties.antenna.synthesis.frequency_unit
farfield_metadata, farfield_frequency = toolkit_api.export_farfield(
    frequencies=frequency_str, sphere="3D", encode=False
)

# ## Get antenna model

files = toolkit_api.export_aedt_model(encode=False)

# ## Release AEDT
#
# Release AEDT.

toolkit_api.release_aedt(True, True)

# ## Plot results

# Plot exported files

from ansys.aedt.core.generic.plot import ModelPlotter

model = ModelPlotter()
for file in files:
    model.add_object(file[0], file[1], file[2])

model.plot(show=False)

# ## Load far field

farfield_data = FfdSolutionData(farfield_metadata)

# ## Plot far field

data = farfield_data.plot_3d(show=False)

# ## Clean temporary directory

temp_dir.cleanup()
