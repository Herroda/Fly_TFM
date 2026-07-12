import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

from openpiv import windef
from openpiv import tools, scaling, validation, filters, preprocess
import openpiv.pyprocess as process
from openpiv import pyprocess
import numpy as np
import pathlib
from time import time
import warnings
import tifffile as tif

#* SETTINGS

settings = windef.PIVSettings()

data_path = '/mnt/crunch/Clark/Larva/Larva 4.0 (7-5-26)/'
reference_stack_path = 'Rolling_Balled.tif'
deformed_stack_path = 'reference-rolling_Stack.tif'

# Change image settings to your own data
settings.filepath_images = pathlib.Path(data_path)
settings.save_path = pathlib.Path(data_path)
settings.save_folder_suffix = 'my_run'
settings.frame_pattern_a = 'frame_a.tif'   # Adjust to your naming
settings.frame_pattern_b = 'frame_b.tif'   # Adjust to your naming

settings.roi = 'full'
settings.dynamic_masking_method = 'None'

settings.deformation_method = 'symmetric'
settings.correlation_method = 'circular'
settings.normalized_correlation = False

# Multipass FFT settings
settings.num_iterations = 2
settings.windowsizes = (64, 32, 16)   # Coarse -> fine
settings.overlap = (32, 16, 8)        # 50% overlap at each pass
settings.subpixel_method = 'gaussian'
settings.interpolation_order = 3
settings.scaling_factor = 1
settings.dt = 1

settings.sig2noise_method = 'peak2peak'
settings.sig2noise_mask = 2

settings.validation_first_pass = True
settings.min_max_u_disp = (-60, 60)
settings.min_max_v_disp = (-60, 60)
settings.std_threshold = 8
settings.median_threshold = 4
settings.median_size = 1
settings.sig2noise_threshold = 1.0

settings.replace_vectors = True
settings.smoothn = True
settings.smoothn_p = 0.5
settings.filter_method = 'localmean'
settings.max_filter_iteration = 4
settings.filter_kernel_size = 2

settings.save_plot = False
settings.show_plot = False
settings.scale_plot = 200

# ------------------------------------------------------------------------------

reference_stack = tif.imread('/mnt/crunch/Clark/Larva/Larva 4.0 (7-5-26)/reference-rolling_Stack.tif')
deformed_stack = tif.imread('/mnt/crunch/Clark/Larva/Larva 4.0 (7-5-26)/Rolling_Balled.tif')

frame_a = reference_stack[0].astype(np.int32)
frame_b = deformed_stack[0].astype(np.int32)

print("running first_pass on frame 0...")
x, y, u, v, s2n = windef.first_pass(frame_a, frame_b, settings)
print("frame 0 first_pass done")

frame_a2 = reference_stack[1].astype(np.int32)
frame_b2 = deformed_stack[1].astype(np.int32)

print("running first_pass on frame 1...")
x2, y2, u2, v2, s2n2 = windef.first_pass(frame_a2, frame_b2, settings)
print("frame 1 first_pass done")