import numpy as np
import rasterio
from rasterio.mask import mask
import geopandas as gpd
from shapely.geometry import mapping

def pre_processing(sentinel_fp: str, label_fp: str):
 
 ''' 
 Inputs:
 sentinel_fp = the imagery filepath in which the model will be trained on.
 label_fp = the labels for the same planet imagery in order to train the classification.
 date = date of the planet image
 AOI = area of interest of the image
 
 This function will load the labels, check the projection and put the data in the same projection as the labels,
 generate a list of shapely geometries, transform the GeoJSON format using rasterio and pull out the pixel values
 using a mask in order to finally loop over the geometries and get the raster pixel values within the geometries.
 
 Outputs:
 X_reshape and y. Which consist of the pixel values and the associated class 
 of each pixel, respectively.
 
 '''
 # Load the scene and print the metadata:
 full_dataset = rasterio.open(sentinel_fp)
 meta = (full_dataset.meta)
 
 # Assign the number of bands to a variable:
 n_bands = full_dataset.count
 
 # Check the projection of the data:
 project_to = full_dataset.crs.to_dict()['init']
  
 # Now load the shapefile using geopandas and check it's projection:
 shapefile = gpd.read_file(label_fp)
  
 # Use geopandas to put the data in the same projection:
 shapefile = shapefile.to_crs(project_to)
 
 # This generates a list of shapely geometries:
 geoms = shapefile.geometry.values
 geometry = geoms[2]
 classname = shapefile['classname'][2]
 
 # Transform to GeoJSON format using rasterio 'mapping' function:
 feature = [mapping(geometry)]
  
 # Pull out the the pixel values with mask:
 out_image = mask(full_dataset, feature, crop=True, filled=True)[0]
 
 # Loop over all polygons in the training labels to form our samples from the raster:
 X = np.array([], dtype=np.float32).reshape(n_bands, -1)
  
 # Labels for training:
 y = np.array([], dtype=np.string_)
 
 # Loop over geometries:
 for index, geom in enumerate(geoms):
   # Get current polygon
   feature = [mapping(geom)]
   # Get the classname for the polygon:
   classname = shapefile['classname'][index]
   # The mask function returns an array of the raster pixels within this polygon:
   out_image = mask(full_dataset, feature, nodata=0, crop=True)[0]
   # Eliminate all the pixels with 0 values for all bands - AKA not actually part of the shapefile:
   out_image = out_image[:, ~np.all(out_image == 0, axis=0)]
   # Append the labels to the y array:
   y = np.append(y, [classname] * out_image.shape[1])
   # Stack the pixels onto the pixel array:
   X = np.hstack((X, out_image))
 
 # Define classification labels:
 labels = np.unique(shapefile['classname'])
 
 # Now we save out the X (pixel bands) and y (pixel classes) 
 # Reshape the X array for passing to classifiers
 X_reshape = X.T
 
 return X_reshape, y, labels

# Load labels and sentinel images
label_01 = '01_varginha_labels.shp'
label_02 = '02_varginha_labels.shp'
label_03 = '03_varginha_labels.shp'
sentinel_01 = '01_S2B_MSIL1C_20200501T131239_N0209_R138_T23KMS_20200501T144404_varginha_stacked_rescaled.tif'
sentinel_02 = '02_S2B_MSIL1C_20190527T131249_N0207_R138_T23KMS_20190527T135301_varginha_stacked_rescaled.tif'
sentinel_03 = '03_S2B_MSIL1C_20180502T131239_N0206_R138_T23KMS_20180502T135204_varginha_stacked_rescaled.tif'

# Rescale the range 0-0.275 in our first three bands to 8-bit 1-255 using gdal
# Your gdal_translate commands

# Apply pre_processing function in sentinel images for 2020, 2019, and 2018, respectively.
X_01, y_01, labels_01 = pre_processing(sentinel_01, label_01)
X_02, y_02, labels_02 = pre_processing(sentinel_02, label_02)
X_03, y_03, labels_03 = pre_processing(sentinel_03, label_03)

# Check labels for the 3 images, they should be the same
print(labels_01)
print(labels_02)
print(labels_03)

# Now save the pixel values for each Sentinel image and the associated class of each pixel
with open('01_pixel_bands_2020.npy', 'wb') as f:
    np.save(f, X_01)

with open('02_pixel_bands_2019.npy', 'wb') as f:
    np.save(f, X_02)

with open('03_pixel_bands_2018.npy', 'wb') as f:
    np.save(f, X_03)

with open('01_pixel_band_classes_2020.npy', 'wb') as f:
    np.save(f, y_01)

with open('02_pixel_band_classes_2019.npy', 'wb') as f:
    np.save(f, y_02)

with open('03_pixel_band_classes_2018.npy', 'wb') as f:
    np.save(f, y_03)
