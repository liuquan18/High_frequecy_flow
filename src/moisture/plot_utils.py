import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def draw_box(ax, base_point):
    lon_window = 33 # index wise
    lat_window = 5 # index wise
    lon_width = lon_window * 1.875 # resolution of lon
    lat_width = lat_window * 1.86525287 # resolution of lat

    ex_box = [
    (base_point[0] - lon_width / 2, base_point[1] - lat_width / 2),
    (base_point[0] + lon_width / 2, base_point[1] - lat_width / 2),
    (base_point[0] + lon_width / 2, base_point[1] + lat_width / 2),
    (base_point[0] - lon_width / 2, base_point[1] + lat_width / 2),
    (base_point[0] - lon_width / 2, base_point[1] - lat_width / 2)
]

    # add box to the plot
    ex_box = np.array(ex_box)
    ax.plot(ex_box[:,0], ex_box[:,1], color="red")

    # add the base point
    ax.plot(base_point[0], base_point[1], marker="o", color="red")
