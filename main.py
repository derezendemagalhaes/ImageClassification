import earth_engine_operations as ee_ops

if __name__ == '__main__':
    ee_ops.initialize_earth_engine()

    # Define variables to download the imagery
    collection = 'COPERNICUS/S2'
    area_name = 'varginha'  # Varginha, Minas Gerais - Brazil
    drive_folder = 'varginha_sentinel2_level1C'

    # Define time range for the 3 images
    time_range_1 = ['2020-05-01', '2020-06-01']
    time_range_2 = ['2019-05-01', '2019-06-01']
    time_range_3 = ['2018-05-01', '2018-06-01']

    # Defined very low cloud percentage to garantee an image cloud-free:
    max_cloud_percent = 1

    # Selected bands for output raster
    band_list = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B11', 'B12']
    spatial_resolution = 10
  
    # Coordinates of bounding box for selected region of Varginha, Brazil.
    bbox_coords = [-45.476406, -21.565619, -45.443921, -21.538263]

    image_1 = ee_ops.download_imagery(collection, area_name, drive_folder, time_range_1, max_cloud_percent, band_list, spatial_resolution, bbox_coords)
    image_2 = ee_ops.download_imagery(collection, area_name, drive_folder, time_range_2, max_cloud_percent, band_list, spatial_resolution, bbox_coords)
    image_3 = ee_ops.download_imagery(collection, area_name, drive_folder, time_range_3, max_cloud_percent, band_list, spatial_resolution, bbox_coords)

    filename_1 = '01_' + image_1.getInfo()['properties']['PRODUCT_ID'] + '_' + area_name + '_stacked_rescaled'
    filename_2 = '02_' + image_2.getInfo()['properties']['PRODUCT_ID'] + '_' + area_name + '_stacked_rescaled'
    filename_3 = '03_' + image_3.getInfo()['properties']['PRODUCT_ID'] + '_' + area_name + '_stacked_rescaled'

    ee_ops.export_image_to_drive(image_1, filename_1, band_list, drive_folder, ee.Geometry.Rectangle(bbox_coords), spatial_resolution)
    ee_ops.export_image_to_drive(image_2, filename_2, band_list, drive_folder, ee.Geometry.Rectangle(bbox_coords), spatial_resolution)
    ee_ops.export_image_to_drive(image_3, filename_3, band_list, drive_folder, ee.Geometry.Rectangle(bbox_coords), spatial_resolution)
