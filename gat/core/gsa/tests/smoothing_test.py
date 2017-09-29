import pysal
import numpy as np

##age smoothing:
#different kinds availible - crude, direct, indirect. Indirect better for smaller populations, direct better for varying risks across large
#                            populations. crude- weighted average direct- compare to std population.
#                               indirect- use std population and weigh by observer pop.

##spatial smoothing
#mean and median based smoothing- objects rate replaced by average(median) rate for neighbors - disk smoothing
#can use more iterations to obtain cleaner result
w = pysal.open(pysal.examples.get_path("stl.gal")).read()
stl = pysal.open(pysal.examples.get_path("stl_hom.csv"))
e, b = np.array(stl[:,10]), np.array(stl[:,13])
if not w.id_order_set: w.id_order = range(1,len(stl) + 1)

print(e, b)

smoothMean = pysal.esda.smoothing.Disk_Smoother(e, b, w)
smoothMedian = pysal.esda.smoothing.Spatial_Median_Rate(e, b, w)
smoothMedian100 = pysal.esda.smoothing.Spatial_Median_Rate(e, b, w, iteration=100)

print("smoothMean")
print(smoothMean.r)
print("smoothMedian")
print(smoothMedian.r)
print("smoothMedian100")
print(smoothMedian100.r) #rates change

##non parametric smoothing
incomes = pysal.open(pysal.examples.get_path("us48.shp"), "r")
incomes_d = np.array([i.centroid for i in incomes])
bbox = [incomes.bbox[:2], incomes.bbox[2:]]
print(bbox)
rate = pysal.esda.smoothing.Spatial_Filtering(bbox, incomes_d, e, b, 10, 10, r=1.5)
print(rate.r)
