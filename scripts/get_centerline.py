import tifffile as tif
import napari
import numpy as np
import skimage
import scipy as sp
from src.centerline import trace_skeleton

larva_mask = tif.imread("larva_mask.tif")  # Load the larva mask from a TIFF file

# Set kernel
kernel = np.ones((3, 3))
kernel[1, 1] = 0  # Make center 0

skeleton_stack = np.zeros_like(larva_mask, dtype=bool)
labeled_paths = []  # will hold one [frame, y, x] array per frame for napari Shapes

for current_frame in range(larva_mask.shape[0]):
    # Skeletonize the larva mask to extract the centerline
    skeleton = skimage.morphology.skeletonize(larva_mask[current_frame] > 0)
    skeleton_stack[current_frame] = skeleton

    # Convolve kernel with skeleton to find neighbors
    convolved_mask = sp.ndimage.convolve(skeleton.astype(int), kernel)

    # Choose head and tail pixels based on neighbor count
    endpoints = np.argwhere(skeleton & (convolved_mask == 1))
    endpoints = [tuple(point) for point in endpoints]

    if len(endpoints) != 2:
        print(f"Frame {current_frame}: expected 2 endpoints, got {len(endpoints)} -- skipping")
        continue

    starting_pixel, ending_pixel = endpoints[0], endpoints[1]
    labeled_skeleton = trace_skeleton(skeleton, starting_pixel, ending_pixel)

    # Prepend frame index to each point so napari's Shapes layer can slice by frame
    path = np.array([[current_frame, y, x] for (y, x) in labeled_skeleton])
    labeled_paths.append(path)

# --- Visualize in napari ---
viewer = napari.Viewer()
viewer.add_image(larva_mask, name="Larva Mask", colormap="gray")
viewer.add_image(skeleton_stack, name="Skeleton", colormap="red", opacity=0.5)
viewer.add_shapes(
    labeled_paths,
    shape_type="path",
    name="Labeled Skeleton",
    edge_color="cyan",
    edge_width=1,
)

napari.run()