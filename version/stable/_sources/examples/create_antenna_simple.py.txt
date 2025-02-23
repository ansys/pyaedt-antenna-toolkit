# # Bowtie antenna synthesis
#
# This example demonstrates how to synthesize a bowtie antenna using the ``BowTieRounded`` class.
# It initiates AEDT through PyAEDT, sets up an empty HFSS design, and proceeds to create the antenna.


# ## Perform required imports
#
# Import the antenna toolkit class and PyAEDT.

import tempfile

import ansys.aedt.core

from ansys.aedt.toolkits.antenna.backend.antenna_models.bowtie import BowTieRounded

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
project_name = ansys.aedt.core.generate_unique_project_name(root_name=temp_dir.name, project_name="bowtie_example")

# ## Create antenna object only for synthesis
#
# Create antenna object.

oantenna1 = BowTieRounded(None)
print(
    "Arm length: {}{} at {}{}".format(
        str(oantenna1.synthesis_parameters.arm_length.value),
        oantenna1.length_unit,
        oantenna1.frequency,
        oantenna1.frequency_unit,
    )
)

# ## Change synthesis frequency
#
# Modify resonance frequency and modify parameters.

oantenna1.frequency = 12.0
print(
    "Arm length: {}{} at {}{}".format(
        str(oantenna1.synthesis_parameters.arm_length.value),
        oantenna1.length_unit,
        oantenna1.frequency,
        oantenna1.frequency_unit,
    )
)

# ## Create an empty HFSS design
#
# Create an empty HFSS design.

app = ansys.aedt.core.Hfss(project=project_name, version=aedt_version, non_graphical=non_graphical)

# ## Create antenna in HFSS
#
# Create antenna object, change frequency synthesis, create antenna, and set up in HFSS.

oantenna1 = BowTieRounded(app)

# Create antenna in HFSS.
oantenna1.model_hfss()

# Create antenna setup.

oantenna1.setup_hfss()

# Change default name.

oantenna1.name = "MyAmazingAntenna"

# ## Create antenna in HFSS
#
# Create antenna object, change origin parameter in the antenna definition, create antenna, and set up in HFSS.

oantenna2 = BowTieRounded(app, origin=[2, 5, 0], name="MyAntenna")
oantenna2.model_hfss()
oantenna2.setup_hfss()

# ## Plot HFSS model
#
# Plot geometry with PyVista.

app.plot()

# ## Release AEDT
#
# Release AEDT.

app.release_desktop(True, True)

# ## Clean temporary directory

temp_dir.cleanup()
