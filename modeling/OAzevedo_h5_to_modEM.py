from pathlib import Path
import numpy as np
from mtpy import MTCollection
from mtpy.modeling import StructuredGrid3D
from mtpy.modeling.modem import Covariance, ControlInv, ControlFwd

with MTCollection() as mc:
    mc.open_collection(Path().cwd().joinpath("NIC_phx_edi.h5"))
    mt_data = mc.to_mt_data()
    # this epsg number should be for a UTM grid. Not a global datum
    # mt_data.utm_epsg = 4326
    mt_data.utm_epsg = 32616

plot_stations = mt_data.plot_stations()  # fig_num=1)

inv_period_list = np.logspace(-np.log10(10), np.log10(10000), num=24)
interp_mt_data = mt_data.interpolate(inv_period_list, inplace=False)

# There currently isn't support for error types like this because its a bit of
# a diservice to using 3D inversion.  You can use row errors or like you did a
# percent.

# z_err_floor = np.array([[0.10, 0.05], [0.05, 0.10]])
# interp_mt_data.compute_model_errors(z_error_value=z_err_floor,
#                                     z_error_type="percent")
"""PRODUCES ERROR: 
Traceback (most recent call last):
    File "/Users/oazevedo3/Desktop/mtpy_read_edi/h5_to_modEM.py", line 20, in <module>
        interp_mt_data.compute_model_errors(z_error_value=z_err_floor,#0.10, 
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/Users/oazevedo3/miniconda3/envs/auroraenv/lib/python3.11/site-packages/mtpy/core/mt_data.py", line 657, in compute_model_errors
        self.z_model_error.error_value = z_error_value
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/Users/oazevedo3/miniconda3/envs/auroraenv/lib/python3.11/site-packages/mtpy/modeling/errors.py", line 127, in error_value
        self._error_value = self.validate_percent(value)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/Users/oazevedo3/miniconda3/envs/auroraenv/lib/python3.11/site-packages/mtpy/modeling/errors.py", line 88, in validate_percent
        if value >= 1:
        ^^^^^^^^^^
ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
"""

interp_mt_data.compute_model_errors(z_error_value=0.05, z_error_type="percent")
"""PRODUCES WARNINGS:
24:04:12T14:39:26 | WARNING | line:706 |mtpy.core.mt | compute_model_t_errors | MT object for NIC01_R_NIC14 contains no Tipper, cannot compute model errors
24:04:12T14:39:26 | WARNING | line:843 |mtpy.core.mt_data | to_modem_data | 'to_modem_data' will be deprecated in future versions, use 'to_modem'
24:04:12T14:39:26 | WARNING | line:684 |mtpy.modeling.modem.data | _check_for_errors_of_zero | Found errors with values of 0 in tzx 21 times. Setting error as tzx x 0.02.
24:04:12T14:39:26 | WARNING | line:684 |mtpy.modeling.modem.data | _check_for_errors_of_zero | Found errors with values of 0 in tzy 21 times. Setting error as tzy x 0.02.
24:04:12T14:39:26 | WARNING | line:758 |mtpy.modeling.modem.data | _check_for_too_small_values | Found values in tzx smaller than 1e-10 23 times. Setting to nan
24:04:12T14:39:26 | WARNING | line:758 |mtpy.modeling.modem.data | _check_for_too_small_values | Found values in tzy smaller than 1e-10 23 times. Setting to nan
"""


interp_mt_data.compute_relative_locations()
interp_mt_data.station_locations.plot.scatter(x="model_east", y="model_north")

modem_data = interp_mt_data.to_modem(
    Path().cwd().joinpath("test_write.dat"), topography=False
)

# mc.average_stations()
