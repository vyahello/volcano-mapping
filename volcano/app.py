from pathlib import Path
from typing import List

import folium
import pandas
import pandas.core.frame

CUR_PATH = Path(__file__).parent


def set_volcano_color(elevation: int) -> str:
    if elevation < 1000:
        return 'green'
    if 1000 <= elevation < 3000:
        return 'orange'
    return 'red'


class Volcanoes:
    def __init__(self, path: Path) -> None:
        self._path: Path = path

    def mapped_coordinates(self) -> zip:
        return zip(self.latitudes, self.longitudes, self.elevation)

    @property
    def latitudes(self) -> List[float]:
        return self._list_coordinate('lat')

    @property
    def longitudes(self) -> List[float]:
        return self._list_coordinate('lon')

    @property
    def elevation(self) -> List[float]:
        return self._list_coordinate('elev')

    def _list_coordinate(self, name: str) -> List[float]:
        return list(self.__dataframe[name.upper()])

    @property
    def __dataframe(self) -> pandas.core.frame.DataFrame:
        return pandas.read_csv(self._path)


class VolcanoMap:
    def __init__(
        self,
        location: List[float],
        zoom_start: int,
        titles: str,
        volcano_group: folium.FeatureGroup,
        population_group: folium.FeatureGroup,
    ) -> None:
        self._map = folium.Map(
            location=location, zoom_start=zoom_start, titles=titles
        )
        self._volcanoes = Volcanoes(CUR_PATH / 'volcanoes.txt')
        self._volcanoes_group = volcano_group
        self._population_group = population_group

    def build(self) -> None:
        for lat, lon, elev in self._volcanoes.mapped_coordinates():
            self._volcanoes_group.add_child(
                folium.CircleMarker(
                    location=(lat, lon),
                    radius=6,
                    popup=f"{elev}m",
                    fill_color=set_volcano_color(elev),
                    color="grey",
                    fill_opacity=0.7,
                )
            )
        self._population_group.add_child(
            folium.GeoJson(
                data=(CUR_PATH / 'world.json')
                .open("r", encoding="utf-8-sig")
                .read(),
                style_function=lambda x: {
                    "fillColor": "green"
                    if x["properties"]["POP2005"] < 10_000_000
                    else "orange"
                    if 10_000_000 <= x["properties"]["POP2005"] < 20_000_000
                    else "red"
                },
            )
        )
        for group in self._volcanoes_group, self._population_group:
            self._map.add_child(group)
        self._map.add_child(folium.LayerControl())

    def save(self, as_file: Path) -> None:
        return self._map.save(as_file.as_posix())


def main():
    volcano_map = VolcanoMap(
        location=[38.58, -99.09],
        zoom_start=6,
        titles="Stamen Terrain",
        volcano_group=folium.FeatureGroup(name='Volcanoes'),
        population_group=folium.FeatureGroup(name='Population'),
    )
    volcano_map.build()
    volcano_map.save(as_file=CUR_PATH.parent / 'volcanoes.html')


if __name__ == '__main__':
    main()
