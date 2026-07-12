from openpiv import windef
from openpiv import tools, scaling, validation, filters, preprocess
import openpiv.pyprocess as process
from openpiv import pyprocess
import numpy as np
import pathlib
from time import time
import warnings
import tifffile as tif


import matplotlib.pyplot as plt

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


#* INITIALIZE

# Data 
reference_stack = tif.imread(data_path + reference_stack_path)
deformed_stack = tif.imread(data_path + deformed_stack_path)

# Results
results_u = []
results_v = []
results_x = None 
results_y = None 

# n_frames = reference_stack.shape[0]
n_frames = 10

# ------------------------------------------------------------------------------

#* COMPUTATION

for current_frame in range(n_frames):
    # Set current slices
    frame_a = reference_stack[current_frame].astype(np.int32)
    frame_b = deformed_stack[current_frame].astype(np.int32)
    
    # Run the first pass
    x, y, u, v, sig2noise = windef.first_pass(frame_a, frame_b, settings)
    
    # Wrap as masked arrays (required by multipass_img_deform)
    u = np.ma.masked_array(u, mask=np.ma.nomask)
    v = np.ma.masked_array(v, mask=np.ma.nomask)
    
    # Run subsequent passes
    for iteration in range(1, settings.num_iterations):
        x, y, u, v, grid_mask, flags = windef.multipass_img_deform(
            frame_a, frame_b, iteration, x, y, u, v, settings
        )
        
    # Append results
    results_u.append(np.array(u))
    results_v.append(np.array(v))
    
    # x and y
    if results_x is None:
        results_x , results_y = x, y
    
    # Check progress every 50 frames
    if current_frame % 50 == 0:
        print(f"frame {current_frame}/{n_frames} done - u range {np.nanmin(u):.2f} to {np.nanmax(u):.2f}")
        
results_u = np.array(results_u)  # shape: (571, ny, nx)
results_v = np.array(results_v)

print("Done. results_u shape:", results_u.shape)