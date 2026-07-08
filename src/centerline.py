def trace_skeleton(skeleton, starting_pixel, ending_pixel):
    '''
    Label pixels from tail to head
    
    PARAMETERS
        1.) skeleton: An array of coordinate pairs for every pixel in the skeleton
        2.) starting_pixel: The coordinates of the starting pixel
        3.) ending_pixel: The coordinates of the ending pixel
        
    RETURNS
        An array of skeleton coordinates, ordered from start to finish left to right
    '''
    
    #* Initialize variables
    visited = [] # Array of coordinates of visited pixels
    
    # --------------------------------------------------------------------------
    #* Main computation
    
    # Add starting point
    visited.append(tuple(starting_pixel))
    
    # Set current pixel to starting pixel
    current_pixel = tuple(starting_pixel)
    
    while current_pixel != ending_pixel:
        
        y, x = current_pixel # Get the x and y coordinates of the current pixel
        found_neighbor = False # Assume no neighbor is found yet
        
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                
                # If both dy and dx are 0 (i.e. center of the 8 pixel ring), then skip the current pixel itself. Break the entire inner loop and continue to the next iteration of the outer loop.
                if dy == 0 and dx == 0:
                    continue
                
                neighbor_pixel = (y + dy, x + dx)
                
                # Otherwise, if 4 conditions all hold, then move to the next unvisited pixel. Break the entire inner loop and continue to the next iteration of the outer loop.
                if (0 <= neighbor_pixel[0] < skeleton.shape[0] and 0 <= neighbor_pixel[1] < skeleton.shape[1] # Check if neighbor pixel is within bounds of the image
                        and skeleton[neighbor_pixel] # Check if neighbor pixel is part of the skeleton
                        and neighbor_pixel not in visited # Check if neighbor pixel has not been visited yet
                    ):
                    
                    # Move to the next unvisited pixel
                    current_pixel = neighbor_pixel
                    visited.append(current_pixel)
                    
                    found_neighbor = True # Set flag to True since a neighbor was found
                    
                    break  # Break the inner loop if a neighbor is found
                
            if found_neighbor:
                break  # Break the outer loop too if a neighbor is found
            
        #! print(visited)
            
        if not found_neighbor:
            print("No unvisited neighbors found. Stopping trace.")
            break  # Stop if no unvisited neighbors are found
        
        # ----------------------------------------------------------------------
        #* Return values
    
    return visited

