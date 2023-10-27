import ee

def initialize_earth_engine():
    ee.Authenticate()
    ee.Initialize()

def download_imagery(collection, area_name, drive_folder, time_range, max_cloud_percent, band_list, spatial_resolution, bbox_coords):
    AOI = ee.Geometry.Rectangle(bbox_coords)
    image_collection = ee.ImageCollection(collection).filterBounds(AOI).filterDate(time_range[0], time_range[1]).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', max_cloud_percent))
    return image_collection.first()

def export_image_to_drive(image, filename, band_list, drive_folder, AOI, spatial_resolution):
    export_job = ee.batch.Export.image.toDrive(
        image.select(band_list).divide(10000),  # scale 0.0001 GEE
        description=filename,
        folder=drive_folder,
        region=AOI.getInfo()['coordinates'],
        scale=spatial_resolution
    )
    export_job.start()
