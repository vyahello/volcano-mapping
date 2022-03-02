import folium
import pandas

data = pandas.read_csv("volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])


def color_prod(el: int) -> str:
    if el < 1000:
        return "green"
    elif 1000 <= el < 3000:
        return "orange"
    return "red"


mp = folium.Map(location=[38.58, -99.09], zoom_start=6, titles="Stamen Terrain")
fgv = folium.FeatureGroup(name="Volcanoes")
for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(
        folium.CircleMarker(
            location=(lt, ln),
            radius=6,
            popup=f"{el}m",
            fill_color=color_prod(el),
            color="grey",
            fill_opacity=0.7,
        )
    )


fgp = folium.FeatureGroup(name="Population")
fgp.add_child(
    folium.GeoJson(
        data=open("world.json", "r", encoding="utf-8-sig").read(),
        style_function=lambda x: {
            "fillColor": "green"
            if x["properties"]["POP2005"] < 10_000_000
            else "orange"
            if 10_000_000 <= x["properties"]["POP2005"] < 20_000_000
            else "red"
        },
    )
)
mp.add_child(fgv)
mp.add_child(fgp)
mp.add_child(folium.LayerControl())
mp.save("volcano.html")
