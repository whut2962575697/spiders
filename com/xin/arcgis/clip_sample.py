# -*- encoding:utf-8 -*-

import arcpy
import os


def clip_sample(workspace, shp_file_name, scale, step):
    scale = scale*0.6
    step = step*0.6
    arcpy.env.workspace = workspace
    if not os.path.exists(workspace+"/"+"temp"):
        os.mkdir(workspace+"/"+"temp")
    if not os.path.exists(workspace+"/"+"output"):
        os.mkdir(workspace+"/"+"output")
    desc = arcpy.Describe(shp_file_name)
    spatial_ref = desc.spatialReference
    x_min = desc.extent.XMin
    x_max = desc.extent.XMax
    y_min = desc.extent.YMin
    y_max = desc.extent.YMax
    x_steps = int((x_max - x_min)/step)
    y_steps = int((y_max - y_min)/step)
    for i in range(x_steps):
        for j in range(y_steps):

            _x_min = x_min+i*step
            _x_max = _x_min+scale
            _y_min = y_min+j*step
            _y_max = _y_min+scale

            wkt = "POLYGON(("+str(_x_min)+" "+str(_y_min)+","+str(_x_max)+" "+str(_y_min)+","\
                        +str(_x_max)+" "+str(_y_max)+","+str(_x_min)+" "+str(_y_max)+","+str(_x_min)+" "+str(_y_min)+"))"

            polygons = arcpy.FromWKT(wkt, spatial_ref)
            arcpy.CopyFeatures_management(polygons, 'temp/temp_'+str(i)+'_'+str(j)+'.shp')
            arcpy.Clip_analysis(shp_file_name, 'temp/temp_'+str(i)+'_'+str(j)+'.shp', 'output/output_'+str(i)+'_'+str(j)+'.shp')
            print ('output_'+str(i)+'_'+str(j)+'.shp is generated successfully!')










if __name__ == "__main__":
    clip_sample(r'G:\xin.data\rs_shp_big', 'hebing.shp', 200, 100)