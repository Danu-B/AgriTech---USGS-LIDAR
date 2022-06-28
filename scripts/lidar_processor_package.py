import json
import geopandas as gpd
import numpy as np
import pdal
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point

from logg import Logg
from file_handler import File_Handler

class LidarProcessor:
    """
    This class is a functons useful for fetching, manipulating, and visualizing LIDAR point cloud data.
    """
    def __init__(self, public_data_url = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/", pipeline_json_path="./ept.json") -> None:
        self.logger = Logg().get_logger(__name__)
        self.public_data_url = public_data_url
        self.file_handler = File_Handler()
        self.pipeline_json = self.file_handler.read_json(pipeline_json_path)   
    
    def get_polygon_boundaries(self, polygon: Polygon):
       
        polygon_df = gpd.GeoDataFrame([polygon], columns=['geometry'])

        polygon_df.set_crs(epsg=self.output_epsg, inplace=True)
        polygon_df['geometry'] = polygon_df['geometry'].to_crs(epsg=self.input_epsg)
        minx, miny, maxx, maxy = polygon_df['geometry'][0].bounds

        polygon_input = 'POLYGON(('
        xcords, ycords = polygon_df['geometry'][0].exterior.coords.xy
        for x, y in zip(list(xcords), list(ycords)):
            polygon_input += f'{x} {y}, '
        polygon_input = polygon_input[:-2]
        polygon_input += '))'

        return f"({[minx, maxx]},{[miny,maxy]})", polygon_input

    def get_pipeline(self, region: str, polygon: Polygon):
        BOUND, polygon_input = self.get_polygon_boundaries(polygon)

        full_dataset_path = f"{self.public_data_url}{region}/ept.json"

        self.pipeline_json['pipeline'][0]['filename'] = full_dataset_path
        self.pipeline_json['pipeline'][0]['bounds'] = BOUND
        self.pipeline_json['pipeline'][1]['polygon'] = polygon_input
        self.pipeline_json['pipeline'][3]['out_srs'] = f'EPSG:{self.output_epsg}'

        pipeline = pdal.Pipeline(json.dumps(self.pipeline_json))

        return pipeline
       

    def run_pipeline(self, polygon: Polygon, epsg, region: str = "IA_FullState"):
        
        self.output_epsg = epsg
        pipeline = self.get_pipeline(region, polygon)

        try:
            pipeline.execute()
            self.logger.info(f'Executed successfully.')
            return pipeline
        except RuntimeError as e:
            self.logger.exception('Execution failed')
            print(e)

    def subsample(self, gdf: gpd.GeoDataFrame, res: int = 3):
        """
        This subsamples the points in a point cloud data using some resolution.
        """

        points = np.vstack((gdf.geometry.x, gdf.geometry.y, gdf.elevation)).transpose()

        voxel_size=res

        non_empty_voxel_keys, inverse, nb_pts_per_voxel = np.unique(((points - np.min(points, axis=0)) // voxel_size).astype(int), axis=0, return_inverse=True, return_counts=True)
        idx_pts_vox_sorted=np.argsort(inverse)

        voxel_grid={}
        grid_barycenter=[]
        last_seen=0

        for idx,vox in enumerate(non_empty_voxel_keys):
            voxel_grid[tuple(vox)]= points[idx_pts_vox_sorted[
            last_seen:last_seen+nb_pts_per_voxel[idx]]]
            grid_barycenter.append(np.mean(voxel_grid[tuple(vox)],axis=0))
            last_seen+=nb_pts_per_voxel[idx]

        sub_sampled =  np.array(grid_barycenter)
        df_subsampled = gpd.GeoDataFrame(columns=["elevation", "geometry"])

        geometry = [Point(x, y) for x, y in zip( sub_sampled[:, 0],  sub_sampled[:, 1])]

        df_subsampled['elevation'] = sub_sampled[:, 2]
        df_subsampled['geometry'] = geometry

        return df_subsampled

    def plot_terrain_3d(self, gdf: gpd.GeoDataFrame, fig_size: tuple=(12, 10), size: float=0.01):
        """
        This displays points in a geodataframe as a 3d scatter plot.
       """
        fig, ax = plt.subplots(1, 1, figsize=fig_size)
        ax = plt.axes(projection='3d')
        ax.scatter(gdf.geometry.x, gdf.geometry.y, gdf.elevation, s=size)
        plt.show()
