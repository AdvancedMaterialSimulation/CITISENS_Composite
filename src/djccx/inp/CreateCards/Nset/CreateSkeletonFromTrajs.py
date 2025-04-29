import numpy as np  # Import numpy for numerical operations
from scipy.spatial.distance import cdist  # Import cdist to compute pairwise distances between points

def CreateSkeletonFromTrajs(inp_files, element, trajs, radius: float = 0.2, name: str = "skeleton") -> None:
    """
    Creates a skeleton (set of nodes) based on the closest nodes to the given trajectory.

    Parameters:
    - inp_files: The object containing the nodes and elements of the .inp file.
    - element: The element object from which unique nodes are extracted.
    - trajs (np.ndarray): An array of trajectory points. It is expected to be a 2D array with shape (n_points, 3) representing the trajectory in 3D space.
    - radius (float, optional): The radius used to filter nodes that are within a certain distance from the trajectory. Defaults to 0.2.
    - name (str, optional): The name to assign to the node set (nset). Defaults to "skeleton".

    Returns:
    - None: This function modifies the .inp file object by creating a new node set if nodes are found, or prints a warning if no nodes are close enough.

    Example:
    ----------
    ```python
    # Assuming `inp_files` is a loaded .inp file object and `element` is an element object
    trajs = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])  # Example trajectory in 3D space
    radius = 0.3
    CreateSkeletonFromTrajs(inp_files, element, trajs, radius, name="example_skeleton")
    ```
    """
    
    # ===============================================================
    # Extract unique nodes from the provided element and get their IDs and coordinates
    nodes = element.GetUniqueNodes(inp_files.nodes)
    id_nodes = nodes.index.values  # Node IDs
    values = nodes.values  # Node coordinates (x, y, z)

    # Refine the trajectory by interpolating between points to create a finer trajectory
    old_span = np.arange(0, trajs.shape[0])  # Original indices of trajectory points
    new_span = np.linspace(0, trajs.shape[0], 500)  # Create 500 equally spaced points
    trajs = np.array([np.interp(new_span, old_span, trajs[:, i]) for i in range(trajs.shape[1])]).T  # Interpolate the trajectory

    # Find the nodes that are closest to the trajectory using a distance threshold
    # Calculate distances between trajectory points and the element's nodes
    distances = cdist(trajs, values)
    # Find the minimum distance for each trajectory point and the corresponding node
    dista_value = np.min(distances, axis=1)
    arg_value = np.argmin(distances, axis=1)
    # Filter nodes that are within a certain distance (radius * 0.5) from the trajectory
    arg_value = arg_value[dista_value < (radius * 0.5)]
    id_nodes = id_nodes[arg_value]
    id_nodes = np.unique(id_nodes)  # Ensure node IDs are unique

    # Select the nodes based on the filtered IDs
    nodes_selected = nodes.loc[id_nodes]
    
    # Sort the selected nodes by their z-coordinate (vertical axis)
    index_sort = np.argsort(nodes_selected["z"])
    id_nodes = nodes_selected.index[index_sort]

    # Remove nodes that are at the "bot" (bottom) and "top" (top) positions to avoid edge issues
    id_nodes = id_nodes[1:-1]

    # If no nodes are left after filtering, print a warning and return without creating the skeleton
    if len(id_nodes) == 0:
        print(f"WARNING: id_nodes is empty. The skeleton named '{name}' was not created.")
        return

    # Create a node set (nset) using the filtered node IDs and assign it the provided name
    inp_files.CreateNsetFromIds(id_nodes, name)
