def run_PIV_on_frames(frame_a, frame_b, settings):
    '''
    Runs PIV on a single pair of frames, one pass then subsequent passes using windef.multipass_img_deform
    
    PARAMETERS
        1.) frame_a: One slice from reference .tif stack
        2.) frame_b: One slice from deformed .tif stack
        3.) settings: OpenPIV settings 
    
    RETURNS
        1.) x (array): x coordinates of each displacement vector
        2.) y (array): y coordinates of each displacement vector
        3.) u (array): magnitude of x-components of displacement vectors
        4.) v (array): magnitude of y-components of displacement vectors
        5.) sig2noise: IDK
        6.) flags (array): Boolean array marking which vectors to replace
    '''
    
    # Run first pass of PIV
    x, y, u, v, sig2noise = windef.first_pass(frame_a, frame_b, settings)
    
    # Clear any NaNs from the first pass
    u, v = filters.replace_outliers(
        u, v, flags,
        method='localmean',     # Choose from 'localmean', 'disk', or 'distance'
        max_iter=10,            # Max number of replacement iterations
        kernel_size=2           # Size of neighborhood used for replacement
    )
    
    # Run multipass FFT deformation algorithm for subsequent passes
    for iteration in range(1, settings.num_iterations):
        
        # Call the function from OpenPIV
        x, y, u, v, grid_mask, flags = windef.multipass_img_deform(
            frame_a, frame_b, iteration, x, y, u, v, settings
        )
    
    return x, y, u, v, sig2noise, flags