"""
Market Share.

A python-based FastAPI web API for calculating the market share for retails in an area.
"""

import pandas as pd
import geopandas as gpd
from shapely.ops import unary_union

from fastapi import HTTPException, UploadFile


class MarketShare:
    """
    Class to calculate share percentage for each retail location.

    Attributes
    ----------
    boundary: UploadFile
        City boundary .geojson file.
    locations: UploadFile
        Retails location .csv file.
    distance: float
        Used to calculate the market share by adding a buffer around each location.
    skip_merge: bool
        If False, the common areas covered by more than one location is ignored.
    """

    def __init__(
            self,
            boundary: UploadFile,
            locations: UploadFile,
            distance: float,
            skip_merge: bool):
        """Initiate class."""
        try:
            self.boundary = boundary.file
            self.locations = locations.file
            self.buffer_size = distance
            self.skip_merge = skip_merge

        except Exception as e:
            status_code = e.status_code if \
                isinstance(e, HTTPException) else 500
            message = e.detail if \
                isinstance(e, HTTPException) else f"Internal Server Error => {str(e)}"

            raise HTTPException(
                status_code=status_code,
                detail=message)

    def csv2gdf(self) -> gpd.GeoDataFrame:
        """Return geopandas GeoDataFrame from csv file in EPSG:4326."""
        try:
            df = pd.read_csv(self.locations)

            if 'geometry' in df:
                df = df.rename(columns={'geometry': 'geometry2'})

            gdf = gpd.GeoDataFrame(
                df,
                geometry=gpd.points_from_xy(
                    x=df['longitude'],
                    y=df['latitude'],
                    crs='EPSG:4326'))

            return gdf

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to convert csv to geopandas DataFrame => {str(e)}")

    def validate_boundary(self) -> bool:
        """Validate boundary .geojson file."""
        try:
            return True

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Invalid boundary file => {str(e)}")

    def validate_locations(self) -> bool:
        """Validate retails location .csv file."""
        try:
            return True

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Invalid location file => {str(e)}")

    def calculate(self, epsg='esri:54009') -> float:
        """Calculate the market share of the retails location in percent."""
        try:
            self.validate_boundary()
            self.validate_locations()

            city_boundary_gdf = gpd.read_file(self.boundary)
            city_boundary_gdf_planner = city_boundary_gdf.to_crs(epsg)

            city_boundary_area = city_boundary_gdf_planner['geometry'].area[0]
            city_boundary_geom = None
            for poly in city_boundary_gdf_planner.itertuples():
                city_boundary_geom = poly.geometry

            location_gdf = self.csv2gdf()
            location_gdf_planner = location_gdf.to_crs(epsg)

            total_retails_coverage_area = 0
            buffer_polygon_intersect_list = []

            for loc in location_gdf_planner.itertuples():
                if city_boundary_geom.contains(loc.geometry):
                    buffer_polygon = loc.geometry.buffer(self.buffer_size)

                    buffer_polygon_intersect = \
                        city_boundary_geom.intersection(buffer_polygon)

                    total_retails_coverage_area += buffer_polygon_intersect.area

                    buffer_polygon_intersect_list.\
                        append(buffer_polygon_intersect)

            if self.skip_merge:
                merged_buffers = unary_union(buffer_polygon_intersect_list)
                return merged_buffers.area / city_boundary_area

            return total_retails_coverage_area / city_boundary_area

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to calculate market share => {str(e)}")
