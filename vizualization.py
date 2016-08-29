import folium
from folium import plugins


def vizualization(data, file_name):

    heatmap_map = folium.Map(data[0], zoom_start=20)

    hm = plugins.HeatMap(data)
    heatmap_map.add_children(hm)
    path = str ('maps\\' + file_name + '.html')
    heatmap_map.save(path)


