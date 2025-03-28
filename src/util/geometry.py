import meep as mp
import numpy as np

# Function to extract vertices from geometry for plotting
def extract_vertices(geometry):
    vertices = []
    for obj in geometry:
        if isinstance(obj, mp.Block):
            # Get block vertices
            center = obj.center
            size = obj.size
            block_vertices = [
                [center.x - size.x / 2, center.y - size.y / 2],
                [center.x + size.x / 2, center.y - size.y / 2],
                [center.x + size.x / 2, center.y + size.y / 2],
                [center.x - size.x / 2, center.y + size.y / 2]
            ]
            vertices.extend(block_vertices)

        elif isinstance(obj, mp.Cylinder):
            # For cylinder, we can plot a circle
            param = np.linspace(0, 2 * np.pi, 50)
            circle = [obj.center + obj.radius * np.cos(param), obj.center + obj.radius * np.cos(param)]
            vertices.append(circle)

        elif isinstance(obj, mp.Prism):
            # Get prism vertices
            prism_vertices = [(v.x, v.y) for v in obj.vertices]
            vertices.extend(prism_vertices)

    return vertices