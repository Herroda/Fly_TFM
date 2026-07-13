# %%

# ==============================================================================
# SECTION 1. IMPORTS
# ==============================================================================

# OpenPIV
from openpiv import windef
from openpiv import tools, scaling, validation, filters, preprocess
import openpiv.pyprocess as process
from openpiv import pyprocess

# General
import numpy as np
import tifffile as tif
import matplotlib.pyplot as plt

import pathlib
from time import time
import warnings

# Custom functions
from PIV import run_PIV_on_frames

# !SECTION

#%%

# ==============================================================================
# SECTION 2. SETTINGS
# ==============================================================================

settings = windef.PIVSettings()

data_path = '/mnt/crunch/Clark/Larva/Larva 4.0 (7-5-26)/'
reference_stack_path = 'Rolling_Balled.tif'
deformed_stack_path = 'reference-rolling_Stack.tif'

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

# !SECTION

#%%

# ==============================================================================
# SECTION 3. ACTUAL PIV
# ==============================================================================

# ANCHOR Load data

data_path = '/mnt/crunch/Clark/Larva/Larva 4.0 (7-5-26)/'
reference_stack_name = 'reference-rolling_Stack.tif'
deformed_stack_name = 'Rolling_Balled.tif'  # Has shape (num_slices, height, width)

reference_stack = tif.imread(data_path + reference_stack_name)
deformed_stack = tif.imread(data_path + deformed_stack_name)

# ------------------------------------------------------------------------------

# ANCHOR Main computation loop

# Initialize variables
num_frames = deformed_stack.shape[0]
results_u = []
results_v = []

# Run main computational loop
for current_frame in range(1, num_frames):
    
    # Set current slices of the stacks
    current_reference_slice = reference_stack[current_frame]
    current_deformed_slice = deformed_stack[current_frame]
    
    # Run PIV on these slices
    x, y, u, v, sig2noise, flags = run_PIV_on_frames(current_reference_slice, current_deformed_slice, settings)
    
    # Append results to lists
    results_u.append(np.array(u))
    results_v.append(np.array(v))
    
    # Print progress every 10 frames
    if current_frame % 10 == 0:
        print(f'Processed frame {current_frame}/{num_frames}')
        
results_u = np.array(results_u)
results_v = np.array(results_v)

# !SECTION
