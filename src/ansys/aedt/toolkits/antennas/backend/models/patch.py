from collections import OrderedDict
import math

import pyaedt.generic.constants as constants
from pyaedt.generic.general_methods import pyaedt_function_handler

from ansys.aedt.toolkits.antennas.backend.common.logger_handler import logger
from ansys.aedt.toolkits.antennas.backend.models.common import CommonAntenna
from ansys.aedt.toolkits.antennas.backend.models.common import TransmissionLine


class CommonPatch(CommonAntenna):
    """Provides base methods common to patch antennas."""

    def __init__(self, _default_input_parameters, *args, **kwargs):
        CommonAntenna.antenna_type = "Patch"
        CommonAntenna.__init__(self, _default_input_parameters, *args, **kwargs)
        self._transmission_line_calculator = TransmissionLine(self.frequency, self.frequency_unit)

    @property
    def material(self):
        """Substrate material.

        Returns
        -------
        str
        """
        return self._input_parameters.material

    @material.setter
    def material(self, value):
        if self._app:
            if (
                value
                and value not in self._app.materials.mat_names_aedt
                and value not in self._app.materials.mat_names_aedt_lower
            ):
                logger.debug("Material not defined")
            else:
                if value != self.material and self.object_list:
                    for antenna_obj in self.object_list:
                        if (
                            self.object_list[antenna_obj].material_name == self.material.lower()
                            and "coax" not in antenna_obj
                        ):
                            self.object_list[antenna_obj].material_name = value

                self._input_parameters.material = value
                parameters = self._synthesis()
                self.update_synthesis_parameters(parameters)
                self.set_variables_in_hfss()
        else:
            self._input_parameters.material = value

    @property
    def material_properties(self):
        """Substrate material properties.

        Returns
        -------
        str
        """
        return self._input_parameters.material_properties

    @property
    def substrate_height(self):
        """Substrate height.

        Returns
        -------
        float
        """
        return self._input_parameters.substrate_height

    @substrate_height.setter
    def substrate_height(self, value):
        self._input_parameters.substrate_height = value

        if self.object_list:
            parameters = self._synthesis()
            self.update_synthesis_parameters(parameters)
            self.set_variables_in_hfss()

    @pyaedt_function_handler()
    def _synthesis(self):
        pass


class RectangularPatchProbe(CommonPatch):
    """Manages a rectangular patch antenna with a coaxial probe.

    This class is accessible through the ``Hfss`` object [1]_.

    Parameters
    ----------
    frequency : float, optional
        Center frequency. The default is ``10.0``.
    frequency_unit : str, optional
        Frequency units. The default is ``"GHz"``.
    material : str, optional
        Substrate material.
        If the material is not defined, a new material, ``parametrized``, is created.
        The default is ``"FR4_epoxy"``.
    outer_boundary : str, optional
        Boundary type to use. Options are ``"Radiation"``,
        ``"FEBI"``, and ``"PML"`` or None. The default is ``None``.
    huygens_box : bool, optional
        Whether to create a Huygens box. The default is ``False``.
    length_unit : str, optional
        Length units. The default is ``"cm"``.
    substrate_height : float, optional
        Substrate height. The default is ``0.1575``.
    parametrized : bool, optional
        Whether to create a parametrized antenna. The default is ``True``.

    Returns
    -------
    :class:`aedt.toolkits.antennas.RectangularPatchProbe`
        Patch antenna object.

    Notes
    -----
    .. [1] C. Balanis, "Microstrip Antennas," Antenna Theory, 2nd Ed. New York: Wiley, 1997.

    Examples
    --------
    >>> from ansys.aedt.toolkits.antennas.backend.models.patch import RectangularPatchProbe
    >>> import pyaedt
    >>> app = pyaedt.Hfss()
    >>> oantenna1 = RectangularPatchProbe(app)
    >>> oantenna1.frequency = 12.0
    >>> oantenna1.model_hfss()
    >>> oantenna1.setup_hfss()
    >>> app.release_desktop(False, False)

    """

    _default_input_parameters = {
        "antenna_name": "",
        "origin": [0, 0, 0],
        "length_unit": "cm",
        "coordinate_system": "Global",
        "frequency": 10.0,
        "frequency_unit": "GHz",
        "material": "FR4_epoxy",
        "material_properties": {"permittivity": 4.4},
        "outer_boundary": "",
        "huygens_box": False,
        "substrate_height": 0.1575,
    }

    def __init__(self, *args, **kwargs):
        CommonPatch.__init__(self, self._default_input_parameters, *args, **kwargs)
        self._parameters = self._synthesis()
        self.update_synthesis_parameters(self._parameters)
        self.antenna_type = "RectangularPatchProbe"

    @pyaedt_function_handler()
    def _synthesis(self):
        parameters = {}
        length_unit = self.length_unit
        lightSpeed = constants.SpeedOfLight  # m/s
        freq_hz = constants.unit_converter(self.frequency, "Freq", self.frequency_unit, "Hz")
        wavelength = lightSpeed / freq_hz

        if self._app and (
            self.material in self._app.materials.mat_names_aedt
            or self.material in self._app.materials.mat_names_aedt_lower
        ):
            mat_props = self._app.materials[self.material]
            permittivity = mat_props.permittivity.value
            self._input_parameters.material_properties["permittivity"] = permittivity

        elif self.material_properties:
            permittivity = self.material_properties["permittivity"]
        else:
            self._app.logger.warning("Material is not found. Create the material before assigning it.")
            return parameters

        subPermittivity = float(permittivity)

        sub_meters = constants.unit_converter(self.substrate_height, "Length", self.length_unit, "meter")

        patch_width = 3.0e8 / ((2.0 * freq_hz) * math.sqrt((subPermittivity + 1.0) / 2.0))

        eff_Permittivity = (subPermittivity + 1.0) / 2.0 + (subPermittivity - 1.0) / 2.0 * math.pow(
            1.0 + 12.0 * sub_meters / patch_width, -0.5
        )

        effective_length = 3.0e8 / (2.0 * freq_hz * math.sqrt(eff_Permittivity))

        top = (eff_Permittivity + 0.3) * (patch_width / sub_meters + 0.264)
        bottom = (eff_Permittivity - 0.258) * (patch_width / sub_meters + 0.8)

        delta_length = 0.412 * sub_meters * top / bottom

        patch_length = effective_length - 2.0 * delta_length

        # eff_WL_meters = wavelength / math.sqrt(eff_Permittivity)

        k = 2.0 * math.pi / eff_Permittivity
        G = math.pi * patch_width / (120.0 * math.pi * wavelength) * (1.0 - math.pow(k * sub_meters, 2) / 24)

        # impedance at edge of patch
        Res = 1.0 / (2.0 * G)
        offset_pin_pos = patch_length / math.pi * math.asin(math.sqrt(50.0 / Res))

        patch_x = constants.unit_converter(patch_width, "Length", "meter", length_unit)
        parameters["patch_x"] = patch_x

        patch_y = constants.unit_converter(patch_length, "Length", "meter", length_unit)
        parameters["patch_y"] = patch_y

        feed_x = 0.0
        parameters["feed_x"] = feed_x

        feed_y = round(constants.unit_converter(offset_pin_pos, "Length", "meter", length_unit), 2)
        parameters["feed_y"] = feed_y

        sub_h = self.substrate_height
        parameters["sub_h"] = sub_h

        sub_x = round(
            constants.unit_converter(1.5 * patch_width + 6.0 * sub_meters, "Length", "meter", length_unit),
            1,
        )
        parameters["sub_x"] = sub_x

        sub_y = round(
            constants.unit_converter(1.5 * patch_length + 6.0 * sub_meters, "Length", "meter", length_unit),
            1,
        )
        parameters["sub_y"] = sub_y

        coax_inner_rad = round(
            constants.unit_converter(0.025 * (1e8 / freq_hz), "Length", "meter", length_unit),
            3,
        )
        parameters["coax_inner_rad"] = coax_inner_rad

        coax_outer_rad = round(
            constants.unit_converter(0.085 * (1e8 / freq_hz), "Length", "meter", length_unit),
            3,
        )
        parameters["coax_outer_rad"] = coax_outer_rad

        feed_length = round(constants.unit_converter(wavelength / 6.0, "Length", "meter", length_unit), 2)
        parameters["feed_length"] = feed_length

        if self.huygens_box:
            gnd_x = constants.unit_converter((299792458 / freq_hz / 4), "Length", "meter", length_unit) + sub_x
            gnd_y = constants.unit_converter((299792458 / freq_hz / 4), "Length", "meter", length_unit) + sub_y
        else:
            gnd_x = sub_x
            gnd_y = sub_y

        parameters["gnd_x"] = gnd_x
        parameters["gnd_y"] = gnd_y

        parameters["pos_x"] = self.origin[0]
        parameters["pos_y"] = self.origin[1]
        parameters["pos_z"] = self.origin[2]

        myKeys = list(parameters.keys())
        myKeys.sort()
        parameters_out = OrderedDict([(i, parameters[i]) for i in myKeys])

        return parameters_out

    @pyaedt_function_handler()
    def model_hfss(self):
        """Draw rectangular patch antenna with coaxial probe.
        Once the antenna is created, this method will not be used anymore."""
        if self.object_list:
            logger.debug("This antenna already exists")
            return False

        if (
            self.material not in self._app.materials.mat_names_aedt
            and self.material not in self._app.materials.mat_names_aedt_lower
        ):
            self._app.logger.warning("Material is not found. Create the material before assigning it.")
            return False

        self.set_variables_in_hfss()

        # Map parameters
        patch_x = self.synthesis_parameters.patch_x.hfss_variable
        patch_y = self.synthesis_parameters.patch_y.hfss_variable
        feed_x = self.synthesis_parameters.feed_x.hfss_variable
        feed_y = self.synthesis_parameters.feed_y.hfss_variable
        sub_h = self.synthesis_parameters.sub_h.hfss_variable
        sub_x = self.synthesis_parameters.sub_x.hfss_variable
        sub_y = self.synthesis_parameters.sub_y.hfss_variable

        coax_inner_rad = self.synthesis_parameters.coax_inner_rad.hfss_variable
        coax_outer_rad = self.synthesis_parameters.coax_outer_rad.hfss_variable
        feed_length = self.synthesis_parameters.feed_length.hfss_variable
        gnd_x = self.synthesis_parameters.gnd_x.hfss_variable
        gnd_y = self.synthesis_parameters.gnd_y.hfss_variable
        pos_x = self.synthesis_parameters.pos_x.hfss_variable
        pos_y = self.synthesis_parameters.pos_y.hfss_variable
        pos_z = self.synthesis_parameters.pos_z.hfss_variable

        antenna_name = self.antenna_name
        coordinate_system = self.coordinate_system

        # Substrate
        sub = self._app.modeler.create_box(
            position=["-" + sub_x + "/2", "-" + sub_y + "/2", "0"],
            dimensions_list=[sub_x, sub_y, sub_h],
            name="sub_" + antenna_name,
            matname=self.material,
        )
        sub.color = (0, 128, 0)
        sub.history().props["Coordinate System"] = coordinate_system

        # Ground
        gnd = self._app.modeler.create_rectangle(
            csPlane=2,
            position=["-" + gnd_x + "/2", "-" + gnd_y + "/2", "0"],
            dimension_list=[gnd_x, gnd_y],
            name="gnd_" + antenna_name,
        )
        gnd.color = (255, 128, 65)
        gnd.history().props["Coordinate System"] = coordinate_system

        # Antenna
        ant = self._app.modeler.create_rectangle(
            csPlane=2,
            position=[
                "-" + patch_x + "/2",
                "-" + patch_y + "/2",
                sub_h,
            ],
            dimension_list=[patch_x, patch_y],
            name="ant_" + antenna_name,
        )
        ant.color = (255, 128, 65)
        ant.transparency = 0.1
        ant.history().props["Coordinate System"] = coordinate_system

        void = self._app.modeler.create_circle(
            cs_plane=2,
            position=[feed_x, feed_y, "0"],
            radius=coax_outer_rad,
            name="void_" + antenna_name,
        )

        self._app.modeler.subtract(gnd, void, False)

        feed_pin = self._app.modeler.create_cylinder(
            cs_axis=2,
            position=[feed_x, feed_y, "0"],
            radius=coax_inner_rad,
            height=sub_h,
            name="feed_pin_" + antenna_name,
            matname="pec",
        )
        feed_pin.color = (255, 128, 65)
        feed_pin.history().props["Coordinate System"] = coordinate_system

        feed_coax = self._app.modeler.create_cylinder(
            cs_axis=2,
            position=[feed_x, feed_y, "0"],
            radius=coax_inner_rad,
            height="-" + feed_length,
            name="feed_coax_" + antenna_name,
            matname="pec",
        )
        feed_coax.color = (255, 128, 65)
        feed_coax.history().props["Coordinate System"] = coordinate_system

        coax = self._app.modeler.create_cylinder(
            cs_axis=2,
            position=[feed_x, feed_y, "0"],
            radius=coax_outer_rad,
            height="-" + feed_length,
            name="coax_" + antenna_name,
            matname="Teflon (tm)",
        )
        coax.color = (128, 255, 255)
        coax.history().props["Coordinate System"] = coordinate_system

        port_cap = self._app.modeler.create_cylinder(
            cs_axis=2,
            position=[feed_x, feed_y, "-" + feed_length],
            radius=coax_outer_rad,
            height="-" + sub_h + "/" + str(10),
            name="port_cap_" + antenna_name,
            matname="pec",
        )
        port_cap.color = (132, 132, 193)
        port_cap.history().props["Coordinate System"] = coordinate_system

        p1 = self._app.modeler.create_circle(
            cs_plane=2,
            position=[feed_x, feed_y, "-" + feed_length],
            radius=coax_outer_rad,
            name="port_" + antenna_name,
        )
        p1.color = (128, 0, 0)
        p1.history().props["Coordinate System"] = coordinate_system

        self.object_list[sub.name] = sub
        self.object_list[gnd.name] = gnd
        self.object_list[ant.name] = ant
        self.object_list[feed_pin.name] = feed_pin
        self.object_list[feed_coax.name] = feed_coax
        self.object_list[coax.name] = coax
        self.object_list[port_cap.name] = port_cap
        self.object_list[p1.name] = p1

        self._app.modeler.move(list(self.object_list.keys()), [pos_x, pos_y, pos_z])

        if self.huygens_box:
            lightSpeed = constants.SpeedOfLight  # m/s
            freq_hz = constants.unit_converter(self.frequency, "Freq", self.frequency_unit, "Hz")
            huygens_dist = str(
                constants.unit_converter(lightSpeed / (10 * freq_hz), "Length", "meter", self.length_unit)
            )
            huygens = self._app.modeler.create_box(
                position=[
                    "-" + gnd_x + "/2.1" "+" + pos_x,
                    "-" + gnd_y + "/2.1" "+" + pos_y,
                    pos_z,
                ],
                dimensions_list=[
                    "abs(-" + gnd_x + "/2.1" + "-" + gnd_x + "/2.1)",
                    "abs(-" + gnd_y + "/2.1" + "-" + gnd_y + "/2.1)",
                    "abs(-" + sub_h + ")+" + huygens_dist + self.length_unit,
                ],
                name="huygens_" + antenna_name,
                matname="air",
            )
            huygens.display_wireframe = True
            huygens.color = (0, 0, 255)
            huygens.history().props["Coordinate System"] = coordinate_system
            huygens.group_name = antenna_name
            self.object_list[huygens.name] = huygens

        sub.group_name = antenna_name
        gnd.group_name = antenna_name
        ant.group_name = antenna_name
        feed_pin.group_name = antenna_name
        feed_coax.group_name = antenna_name
        coax.group_name = antenna_name
        port_cap.group_name = antenna_name
        p1.group_name = antenna_name

    @pyaedt_function_handler()
    def model_disco(self):
        """Model in PyDiscovery. To be implemenented."""
        pass

    @pyaedt_function_handler()
    def setup_disco(self):
        """Set up the model in PyDiscovery. To be implemenented."""
        pass


class RectangularPatchInset(CommonPatch):
    """Manages a rectangular patch antenna inset fed.

    This class is accessible through the ``Hfss`` object [1]_.

    Parameters
    ----------
    frequency : float, optional
        Center frequency. The default is ``10.0``.
    frequency_unit : str, optional
        Frequency units. The default is ``"GHz"``.
    material : str, optional
        Substrate material. If the material is not defined, a new
        material, ``parametrized``, is created. The default is ``"FR4_epoxy"``.
    outer_boundary : str, optional
        Boundary type to use. Options are ``"Radiation"``,
        ``"FEBI"``, ``"PML"``, and ``None``. The default is ``None``.
    huygens_box : bool, optional
        Whether to create a Huygens box. The default is ``False``.
    length_unit : str, optional
        Length units. The default is ``"cm"``.
    substrate_height : float, optional
        Substrate height. The default is ``0.1575``.
    parametrized : bool, optional
        Whether to create a parametrized antenna. The default is ``True``.

    Returns
    -------
    :class:`aedt.toolkits.antennas.RectangularPatchInset`
        Patch antenna object.

    Notes
    -----
    .. [1] C. Balanis, "Microstrip Antennas," Antenna Theory, 2nd Ed. New York: Wiley, 1997.

    Examples
    --------
    >>> from ansys.aedt.toolkits.antennas.backend.models.patch import RectangularPatchInset
    >>> import pyaedt
    >>> app = pyaedt.Hfss()
    >>> oantenna1 = RectangularPatchInset(app)
    >>> oantenna1.frequency = 12.0
    >>> oantenna1.model_hfss()
    >>> oantenna1.setup_hfss()
    >>> app.release_desktop(False, False)

    """

    _default_input_parameters = {
        "antenna_name": "",
        "origin": [0, 0, 0],
        "length_unit": "cm",
        "coordinate_system": "Global",
        "frequency": 10.0,
        "frequency_unit": "GHz",
        "material": "FR4_epoxy",
        "material_properties": {"permittivity": 4.4},
        "outer_boundary": "",
        "huygens_box": False,
        "substrate_height": 0.1575,
    }

    def __init__(self, *args, **kwargs):
        CommonPatch.__init__(self, self._default_input_parameters, *args, **kwargs)

        self._parameters = self._synthesis()
        self.update_synthesis_parameters(self._parameters)
        self.antenna_type = "RectangularPatchInset"

    @pyaedt_function_handler()
    def _synthesis(self):
        parameters = {}
        length_unit = self.length_unit
        lightSpeed = constants.SpeedOfLight  # m/s
        freq_hz = constants.unit_converter(self.frequency, "Freq", self.frequency_unit, "Hz")
        wavelength = lightSpeed / freq_hz

        if self._app and (
            self.material in self._app.materials.mat_names_aedt
            or self.material in self._app.materials.mat_names_aedt_lower
        ):
            mat_props = self._app.materials[self.material]
            permittivity = mat_props.permittivity.value
            self._input_parameters.material_properties["permittivity"] = permittivity

        elif self.material_properties:
            permittivity = self.material_properties["permittivity"]
        else:
            self._app.logger.warning("Material is not found. Create the material before assigning it.")
            return parameters

        subPermittivity = float(permittivity)

        patch_width = 3.0e8 / ((2.0 * freq_hz) * math.sqrt((subPermittivity + 1.0) / 2.0))

        sub_meters = constants.unit_converter(self.substrate_height, "Length", self.length_unit, "meter")

        eff_Permittivity = (subPermittivity + 1.0) / 2.0 + (subPermittivity - 1.0) / 2.0 * math.pow(
            1.0 + 12.0 * sub_meters / patch_width, -0.5
        )

        effective_length = 3.0e8 / (2.0 * freq_hz * math.sqrt(eff_Permittivity))

        top = (eff_Permittivity + 0.3) * (patch_width / sub_meters + 0.264)
        bottom = (eff_Permittivity - 0.258) * (patch_width / sub_meters + 0.8)

        delta_length = 0.412 * sub_meters * top / bottom

        patch_length = effective_length - 2.0 * delta_length

        # eff_WL_meters = wavelength / math.sqrt(eff_Permittivity)

        k = 2.0 * math.pi / eff_Permittivity
        G = math.pi * patch_width / (120.0 * math.pi * wavelength) * (1.0 - math.pow(k * sub_meters, 2) / 24)

        # impedance at edge of patch
        Res = 1.0 / (2.0 * G)
        inset_distance_meter = patch_length / math.pi * math.asin(math.sqrt(50.0 / Res))

        # quarterwave_imped = math.sqrt(50.0 * Res)

        uStrip = self._transmission_line_calculator.microstrip_calculator(sub_meters, subPermittivity, 50.0, 150.0)

        microstrip_width = uStrip[0]
        microstrip_length = uStrip[1]

        patch_x = round(constants.unit_converter(patch_width, "Length", "meter", length_unit), 2)
        parameters["patch_x"] = patch_x

        patch_y = round(constants.unit_converter(patch_length, "Length", "meter", length_unit), 2)
        parameters["patch_y"] = patch_y

        sub_h = self.substrate_height
        parameters["sub_h"] = sub_h

        sub_x = round(
            constants.unit_converter(1.5 * patch_width + 6.0 * sub_meters, "Length", "meter", length_unit),
            1,
        )
        parameters["sub_x"] = sub_x

        sub_y = round(
            constants.unit_converter(2.1 * (microstrip_length + patch_length / 2), "Length", "meter", length_unit),
            2,
        )
        parameters["sub_y"] = sub_y

        inset_distance = round(
            constants.unit_converter(patch_length / 2 - inset_distance_meter, "Length", "meter", length_unit),
            4,
        )
        parameters["inset_distance"] = inset_distance

        microstrip_length = constants.unit_converter(microstrip_length, "Length", "meter", length_unit)
        microstrip_width = constants.unit_converter(microstrip_width, "Length", "meter", length_unit)

        inset_gap = round(microstrip_width / 2, 3)
        parameters["inset_gap"] = inset_gap

        feed_width = round(microstrip_width, 3)
        parameters["feed_width"] = feed_width

        feed_length = round(microstrip_length, 3)
        parameters["feed_length"] = feed_length

        parameters["pos_x"] = self.origin[0]
        parameters["pos_y"] = self.origin[1]
        parameters["pos_z"] = self.origin[2]

        myKeys = list(parameters.keys())
        myKeys.sort()
        parameters_out = OrderedDict([(i, parameters[i]) for i in myKeys])

        return parameters_out

    @pyaedt_function_handler()
    def model_hfss(self):
        """Draw a rectangular patch antenna inset fed.

        Once the antenna is created, this method is not used anymore."""
        if self.object_list:
            self._app.logger.warning("This antenna already exists.")
            return False

        if (
            self.material not in self._app.materials.mat_names_aedt
            and self.material not in self._app.materials.mat_names_aedt_lower
        ):
            self._app.logger.warning("Material is not found. Create the material before assigning it.")
            return False

        self.set_variables_in_hfss()

        # Map parameters
        patch_x = self.synthesis_parameters.patch_x.hfss_variable
        patch_y = self.synthesis_parameters.patch_y.hfss_variable
        sub_h = self.synthesis_parameters.sub_h.hfss_variable
        sub_x = self.synthesis_parameters.sub_x.hfss_variable
        sub_y = self.synthesis_parameters.sub_y.hfss_variable

        inset_distance = self.synthesis_parameters.inset_distance.hfss_variable
        inset_gap = self.synthesis_parameters.inset_gap.hfss_variable
        feed_width = self.synthesis_parameters.feed_width.hfss_variable
        feed_length = self.synthesis_parameters.feed_length.hfss_variable
        pos_x = self.synthesis_parameters.pos_x.hfss_variable
        pos_y = self.synthesis_parameters.pos_y.hfss_variable
        pos_z = self.synthesis_parameters.pos_z.hfss_variable

        antenna_name = self.antenna_name
        coordinate_system = self.coordinate_system

        # Substrate
        sub = self._app.modeler.create_box(
            position=["-" + sub_x + "/2", "-" + sub_y + "/2", "0"],
            dimensions_list=[sub_x, sub_y, sub_h],
            name="sub_" + antenna_name,
            matname=self.material,
        )
        sub.color = (0, 128, 0)
        sub.history().props["Coordinate System"] = coordinate_system

        # Ground
        gnd = self._app.modeler.create_rectangle(
            csPlane=2,
            position=["-" + sub_x + "/2", "-" + sub_y + "/2", "0"],
            dimension_list=[sub_x, sub_y],
            name="gnd_" + antenna_name,
        )
        gnd.color = (255, 128, 65)
        gnd.transparency = 0.1
        gnd.history().props["Coordinate System"] = coordinate_system

        # Antenna
        ant = self._app.modeler.create_rectangle(
            csPlane=2,
            position=[
                "-" + patch_x + "/2",
                "-" + patch_y + "/2",
                sub_h,
            ],
            dimension_list=[patch_x, patch_y],
            name="ant_" + antenna_name,
        )
        ant.color = (255, 128, 65)
        ant.transparency = 0.1
        ant.history().props["Coordinate System"] = coordinate_system

        cutout = self._app.modeler.create_rectangle(
            csPlane=2,
            position=[
                "-" + feed_width + "/2" + "-" + inset_gap,
                patch_y + "/2" + "-" + inset_distance,
                sub_h,
            ],
            dimension_list=[feed_width + "+2*" + inset_gap, feed_length],
            name="cutout_" + antenna_name,
        )
        cutout.color = (255, 128, 65)
        cutout.history().props["Coordinate System"] = coordinate_system

        self._app.modeler.subtract(ant, cutout, False)

        feed = self._app.modeler.create_rectangle(
            csPlane=2,
            position=[
                "-" + feed_width + "/2",
                patch_y + "/2" "-" + inset_distance,
                sub_h,
            ],
            dimension_list=[feed_width, feed_length + "+" + inset_distance],
            name="feed_" + antenna_name,
        )
        feed.color = (255, 128, 65)
        feed.history().props["Coordinate System"] = coordinate_system

        self._app.modeler.unite([ant, feed])

        p1 = self._app.modeler.create_rectangle(
            csPlane=1,
            position=[
                "-" + feed_width + "/2",
                patch_y + "/2" + "+" + feed_length,
                "0",
            ],
            dimension_list=[sub_h, feed_width],
            name="port_lump_" + antenna_name,
        )
        p1.color = (255, 128, 65)
        p1.history().props["Coordinate System"] = coordinate_system

        self.object_list[sub.name] = sub
        self.object_list[gnd.name] = gnd
        self.object_list[ant.name] = ant
        self.object_list[p1.name] = p1

        self._app.modeler.move(list(self.object_list.keys()), [pos_x, pos_y, pos_z])
        if self.huygens_box:
            lightSpeed = constants.SpeedOfLight  # m/s
            freq_hz = constants.unit_converter(self.frequency, "Freq", self.frequency_unit, "Hz")
            huygens_dist = str(
                constants.unit_converter(lightSpeed / (10 * freq_hz), "Length", "meter", self.length_unit)
            )
            huygens = self._app.modeler.create_box(
                position=[
                    "-" + sub_x + "/2" "+" + pos_x + "-" + "+" + huygens_dist + self.length_unit + "/2",
                    "-" + sub_y + "/2" "+" + pos_y + "-" + "+" + huygens_dist + self.length_unit + "/2",
                    pos_z,
                ],
                dimensions_list=[
                    "abs(-" + sub_x + "/2" + "-" + sub_x + "/2)" + "+" + huygens_dist + self.length_unit,
                    "abs(-" + sub_y + "/2" + "-" + sub_y + "/2)" + "+" + huygens_dist + self.length_unit,
                    "abs(-" + sub_h + ")+" + huygens_dist + self.length_unit,
                ],
                name="huygens_" + antenna_name,
                matname="air",
            )
            huygens.display_wireframe = True
            huygens.color = (0, 0, 255)
            huygens.history().props["Coordinate System"] = coordinate_system
            huygens.group_name = self.antenna_name
            self.object_list[huygens.name] = huygens

        sub.group_name = antenna_name
        gnd.group_name = antenna_name
        ant.group_name = antenna_name
        p1.group_name = antenna_name

    @pyaedt_function_handler()
    def model_disco(self):
        """Model in PyDiscovery. To be implemenented."""
        pass

    @pyaedt_function_handler()
    def setup_disco(self):
        """Set up the model in PyDiscovery. To be implemenented."""
        pass


class RectangularPatchEdge(CommonPatch):
    """Manages a rectangular patch edge antenna.

    This class is accessible through the ``Hfss`` object [1]_.

    Parameters
    ----------
    frequency : float, optional
        Center frequency. The default is ``10.0``.
    frequency_unit : str, optional
        Frequency units. The default is ``"GHz"``.
    material : str, optional
        Substrate material. If the material is not defined,
        a new material, ``parametrized``, is created.
        The default is ``"FR4_epoxy"``.
    outer_boundary : str, optional
        Boundary type to use. Options are ``"Radiation"``,
        ``"FEBI"``, ``"PML"``, and ``None``. The default is ``None``.
    huygens_box : bool, optional
        Whether to create a Huygens box. The default is ``False``.
    length_unit : str, optional
        Length units. The default is ``"cm"``.
    substrate_height : float, optional
        Substrate height. The default is ``0.1575``.
    parametrized : bool, optional
        Whether to create a parametrized antenna. The default is ``True``.

    Returns
    -------
    :class:`aedt.toolkits.antennas.RectangularPatchEdge`
        Patch antenna object.

    Notes
    -----
    .. [1] C. Balanis, "Microstrip Antennas," Antenna Theory, 2nd Ed. New York: Wiley, 1997.

    Examples
    --------
    >>> from ansys.aedt.toolkits.antennas.backend.models.patch import RectangularPatchEdge
    >>> import pyaedt
    >>> app = pyaedt.Hfss()
    >>> oantenna1 = RectangularPatchEdge(app)
    >>> oantenna1.frequency = 12.0
    >>> oantenna1.model_hfss()
    >>> oantenna1.setup_hfss()
    >>> app.release_desktop(False, False)

    """

    _default_input_parameters = {
        "antenna_name": "",
        "origin": [0, 0, 0],
        "length_unit": "cm",
        "coordinate_system": "Global",
        "frequency": 10.0,
        "frequency_unit": "GHz",
        "material": "FR4_epoxy",
        "material_properties": {"permittivity": 4.4},
        "outer_boundary": "",
        "huygens_box": False,
        "substrate_height": 0.1575,
    }

    def __init__(self, *args, **kwargs):
        CommonPatch.__init__(self, self._default_input_parameters, *args, **kwargs)
        self._parameters = self._synthesis()
        self.update_synthesis_parameters(self._parameters)
        self.antenna_type = "RectangularPatchEdge"

    @pyaedt_function_handler()
    def _synthesis(self):
        parameters = {}
        length_unit = self.length_unit
        lightSpeed = constants.SpeedOfLight  # m/s
        freq_hz = constants.unit_converter(self.frequency, "Freq", self.frequency_unit, "Hz")
        wavelength = lightSpeed / freq_hz

        if self._app and (
            self.material in self._app.materials.mat_names_aedt
            or self.material in self._app.materials.mat_names_aedt_lower
        ):
            mat_props = self._app.materials[self.material]
            permittivity = mat_props.permittivity.value
            self._input_parameters.material_properties["permittivity"] = permittivity

        elif self.material_properties:
            permittivity = self.material_properties["permittivity"]
        else:
            self._app.logger.warning("Material is not found. Create the material before assigning it.")
            return parameters

        subPermittivity = float(permittivity)

        patch_width = 3.0e8 / ((2.0 * freq_hz) * math.sqrt((subPermittivity + 1.0) / 2.0))

        sub_meters = constants.unit_converter(self.substrate_height, "Length", self.length_unit, "meter")

        eff_Permittivity = (subPermittivity + 1.0) / 2.0 + (subPermittivity - 1.0) / 2.0 * math.pow(
            1.0 + 12.0 * sub_meters / patch_width, -0.5
        )

        effective_length = 3.0e8 / (2.0 * freq_hz * math.sqrt(eff_Permittivity))

        top = (eff_Permittivity + 0.3) * (patch_width / sub_meters + 0.264)
        bottom = (eff_Permittivity - 0.258) * (patch_width / sub_meters + 0.8)

        delta_length = 0.412 * sub_meters * top / bottom

        patch_length = effective_length - 2.0 * delta_length

        # eff_WL_meters = wavelength / math.sqrt(eff_Permittivity)

        k = 2.0 * math.pi / eff_Permittivity
        G = math.pi * patch_width / (120.0 * math.pi * wavelength) * (1.0 - math.pow(k * sub_meters, 2) / 24)

        # impedance at edge of patch
        Res = 1.0 / (2.0 * G)
        # offset_pin_pos = patch_length / math.pi * math.asin(math.sqrt(50.0 / Res))

        quarterwave_imped = math.sqrt(50.0 * Res)

        uStrip1 = self._transmission_line_calculator.microstrip_calculator(
            sub_meters, subPermittivity, quarterwave_imped, 90.0
        )

        microstrip_edge_width = uStrip1[0]
        microstrip_edge_length = uStrip1[1]

        uStrip2 = self._transmission_line_calculator.microstrip_calculator(sub_meters, subPermittivity, 50.0, 150.0)

        microstrip_width = uStrip2[0]
        microstrip_length = uStrip2[1]

        patch_x = round(constants.unit_converter(patch_width, "Length", "meter", length_unit), 2)
        parameters["patch_x"] = patch_x

        patch_y = round(constants.unit_converter(patch_length, "Length", "meter", length_unit), 2)
        parameters["patch_y"] = patch_y

        sub_h = self.substrate_height
        parameters["sub_h"] = sub_h

        sub_x = round(
            constants.unit_converter(1.5 * patch_width + 6.0 * sub_meters, "Length", "meter", length_unit),
            1,
        )
        parameters["sub_x"] = sub_x

        sub_y = round(
            constants.unit_converter(
                2.1 * (microstrip_length + microstrip_edge_length + patch_length / 2),
                "Length",
                "meter",
                length_unit,
            ),
            2,
        )
        parameters["sub_y"] = sub_y

        edge_feed_width = round(
            constants.unit_converter(microstrip_edge_width, "Length", "meter", length_unit),
            3,
        )
        parameters["edge_feed_width"] = edge_feed_width

        edge_feed_length = round(
            constants.unit_converter(microstrip_edge_length, "Length", "meter", length_unit),
            3,
        )
        parameters["edge_feed_length"] = edge_feed_length

        feed_width = round(
            constants.unit_converter(microstrip_width, "Length", "meter", length_unit),
            3,
        )
        parameters["feed_width"] = feed_width

        feed_length = round(
            constants.unit_converter(microstrip_length, "Length", "meter", length_unit),
            3,
        )
        parameters["feed_length"] = feed_length

        parameters["pos_x"] = self.origin[0]
        parameters["pos_y"] = self.origin[1]
        parameters["pos_z"] = self.origin[2]

        myKeys = list(parameters.keys())
        myKeys.sort()
        parameters_out = OrderedDict([(i, parameters[i]) for i in myKeys])

        return parameters_out

    @pyaedt_function_handler()
    def model_hfss(self):
        """Draw a rectangular patch edge antenna inset fed.

        Once the antenna is created, this method is not used anymore."""
        if self.object_list:
            self._app.logger.warning("This antenna already exists.")
            return False

        if (
            self.material not in self._app.materials.mat_names_aedt
            and self.material not in self._app.materials.mat_names_aedt_lower
        ):
            self._app.logger.warning("Material is not found. Create the material before assigning it.")
            return False

        self.set_variables_in_hfss()

        # Map parameters
        patch_x = self.synthesis_parameters.patch_x.hfss_variable
        patch_y = self.synthesis_parameters.patch_y.hfss_variable
        sub_h = self.synthesis_parameters.sub_h.hfss_variable
        sub_x = self.synthesis_parameters.sub_x.hfss_variable
        sub_y = self.synthesis_parameters.sub_y.hfss_variable

        edge_feed_width = self.synthesis_parameters.edge_feed_width.hfss_variable
        edge_feed_length = self.synthesis_parameters.edge_feed_length.hfss_variable
        feed_width = self.synthesis_parameters.feed_width.hfss_variable
        feed_length = self.synthesis_parameters.feed_length.hfss_variable
        pos_x = self.synthesis_parameters.pos_x.hfss_variable
        pos_y = self.synthesis_parameters.pos_y.hfss_variable
        pos_z = self.synthesis_parameters.pos_z.hfss_variable

        antenna_name = self.antenna_name
        coordinate_system = self.coordinate_system

        # Substrate
        sub = self._app.modeler.create_box(
            position=["-" + sub_x + "/2", "-" + sub_y + "/2", "0"],
            dimensions_list=[sub_x, sub_y, sub_h],
            name="sub_" + antenna_name,
            matname=self.material,
        )
        sub.color = (0, 128, 0)
        sub.history().props["Coordinate System"] = coordinate_system

        # Ground
        gnd = self._app.modeler.create_rectangle(
            csPlane=2,
            position=["-" + sub_x + "/2", "-" + sub_y + "/2", "0"],
            dimension_list=[sub_x, sub_y],
            name="gnd_" + antenna_name,
        )
        gnd.color = (255, 128, 65)
        gnd.transparency = 0.1
        gnd.history().props["Coordinate System"] = coordinate_system

        # Antenna
        ant = self._app.modeler.create_rectangle(
            csPlane=2,
            position=[
                "-" + patch_x + "/2",
                "-" + patch_y + "/2",
                sub_h,
            ],
            dimension_list=[patch_x, patch_y],
            name="ant_" + antenna_name,
        )
        ant.color = (255, 128, 65)
        ant.transparency = 0.1
        ant.history().props["Coordinate System"] = coordinate_system

        edge_feed = self._app.modeler.create_rectangle(
            csPlane=2,
            position=[
                "-" + edge_feed_width + "/2",
                "0",
                sub_h,
            ],
            dimension_list=[edge_feed_width, patch_y + "/2" + "+" + edge_feed_length],
            name="cutout_" + antenna_name,
        )
        edge_feed.color = (255, 128, 65)
        edge_feed.history().props["Coordinate System"] = coordinate_system

        feed = self._app.modeler.create_rectangle(
            csPlane=2,
            position=[
                "-" + feed_width + "/2",
                patch_y + "/2" + "+" + edge_feed_length,
                sub_h,
            ],
            dimension_list=[feed_width, feed_length],
            name="feed_" + antenna_name,
        )
        feed.color = (255, 128, 65)
        feed.history().props["Coordinate System"] = coordinate_system

        self._app.modeler.unite([ant, edge_feed, feed])

        p1 = self._app.modeler.create_rectangle(
            csPlane=1,
            position=[
                "-" + feed_width + "/2",
                patch_y + "/2" + "+" + edge_feed_length + "+" + feed_length,
                "0",
            ],
            dimension_list=[sub_h, feed_width],
            name="port_lump_" + antenna_name,
        )
        p1.color = (255, 128, 65)
        p1.history().props["Coordinate System"] = coordinate_system

        self.object_list[sub.name] = sub
        self.object_list[gnd.name] = gnd
        self.object_list[ant.name] = ant
        self.object_list[p1.name] = p1

        self._app.modeler.move(list(self.object_list.keys()), [pos_x, pos_y, pos_z])

        if self.huygens_box:
            lightSpeed = constants.SpeedOfLight  # m/s
            freq_hz = constants.unit_converter(self.frequency, "Freq", self.frequency_unit, "Hz")
            huygens_dist = str(
                constants.unit_converter(lightSpeed / (10 * freq_hz), "Length", "meter", self.length_unit)
            )
            huygens = self._app.modeler.create_box(
                position=[
                    "-" + sub_x + "/2" "-" + "+" + huygens_dist + self.length_unit + "/2",
                    "-" + sub_y + "/2" "-" + "+" + huygens_dist + self.length_unit + "/2",
                    "0",
                ],
                dimensions_list=[
                    "abs(-" + sub_x + "/2" + "-" + sub_x + "/2)" + "+" + huygens_dist + self.length_unit,
                    "abs(-" + sub_y + "/2" + "-" + sub_y + "/2)" + "+" + huygens_dist + self.length_unit,
                    "abs(-" + sub_h + ")+" + huygens_dist + self.length_unit,
                ],
                name="huygens_" + antenna_name,
                matname="air",
            )
            huygens.display_wireframe = True
            huygens.color = (0, 0, 255)
            huygens.history().props["Coordinate System"] = coordinate_system
            huygens.group_name = antenna_name
            self.object_list[huygens.name] = huygens

        sub.group_name = antenna_name
        gnd.group_name = antenna_name
        ant.group_name = antenna_name
        p1.group_name = antenna_name

    @pyaedt_function_handler()
    def model_disco(self):
        """Model in PyDisco. To be implemenented."""
        pass

    @pyaedt_function_handler()
    def setup_disco(self):
        """Set up the model in PyDisco. To be implemenented."""
        pass
