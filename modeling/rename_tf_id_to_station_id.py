# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 13:23:57 2024

@author: jpeacock

Relable the transfer function id as the station name.

"""

# =============================================================================
# Imports
# =============================================================================
from pathlib import Path
from mtpy import MTCollection

# =============================================================================

with MTCollection() as mc:
    mc.open_collection(Path().cwd().joinpath("NIC_phx_edi.h5"))
    for row in mc.dataframe.itertuples():
        sg = mc.mth5_collection.from_reference(row.station_hdf5_reference)
        tg = sg.transfer_functions_group.get_transfer_function(sg.metadata.id)
        tg.metadata.id = sg.metadata.id
        tg.write_metadata()

    mc.mth5_collection.tf_summary.summarize()
