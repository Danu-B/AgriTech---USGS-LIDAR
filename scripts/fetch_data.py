import pdal
import json
from logg import Logg
from file_handler import FileHandler

class Fetch_Data:

    def __init__(self, public_data_url = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/", pipeline_json_path="./pipeline.json") -> None:
        self.logger = Logg().get_logger(__name__)
        self.public_data_url = public_data_url
        self.file_handler = File_Handler()
        self.pipeline_json = self.file_handler.read_json(pipeline_json_path)

    def get_pipeline(self, region: str, output_filename: str = "temp"):
        BOUND, polygon_input = self.get_polygon_boundaries(polygon)

        full_dataset_path = f"{self.public_data_url}{region}/ept.json"

        self.pipeline_json['pipeline'][0]['filename'] = full_dataset_path
        self.pipeline_json['pipeline'][0]['bounds'] = BOUND
        self.pipeline_json['pipeline'][1]['polygon'] = polygon_input
        self.pipeline_json['pipeline'][3]['out_srs'] = f'EPSG:{self.output_epsg}'

        pipeline = pdal.Pipeline(json.dumps(self.pipeline_json))

        return pipeline
    
    def run_pipeline(self, region: str = "IA_FullState"):
        pipeline = self.get_pipeline(region)

        try:
            pipeline.execute()
            metadata = pipeline.metadata
            log = pipeline.log
            self.logger.info(f'Pipeline executed successfully.')
            print(log)
            return pipeline
        except RuntimeError as e:
            self.logger.exception('Pipeline execution failed')
            print(e)

if(__name__ == '__main__'):
    data_fetcher = Fetch_Data()
    data_fetcher.run_pipeline()