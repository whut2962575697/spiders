import string
import sys
import arcpy
import os
reload(sys)
def DirPath(SampleID, minID1, maxID, setdirinterval):
    startdirmin=(minID/ Interval)* Interval;
    startDirindex = ((SampleID - startdirmin) / Interval) * Interval + (minID1/ Interval)* Interval;
    endDirindex = startDirindex+setdirinterval;
    return str(startDirindex)+"_"+ str(endDirindex-1);
sys.setdefaultencoding("utf-8")



try:

    raster = arcpy.GetParameterAsText(0)  # clip raster

    clip_feat = arcpy.GetParameterAsText(1)  # clip featureclass

    field1 = arcpy.GetParameterAsText(2)  # name field

    field2 = arcpy.GetParameterAsText(3)  # output ws

    outworkspace = arcpy.GetParameterAsText(4)  # output ws

    outworkspace1 = arcpy.GetParameterAsText(5)  # output ws

    outtype = arcpy.GetParameterAsText(6)  # output ws
##    raster ="E:\\data\\2009100test.tif"
##    clip_feat = "E:\\data\\gg2009_patch.shp";
##    field1="ID";
##    field2 ="True_class"
##    outworkspace="E:\\gg2009data"
##    outtype = ".tif"
##    total = int(arcpy.GetCount_management(clip_feat).getOutput(0))

    total = int(arcpy.GetCount_management(clip_feat).getOutput(0))

    minID=0;
    maxID=13000;
    Interval=40000;
    startdir=(minID/ Interval)* Interval;
    arcpy.env.overwriteOutput = True
    count=0;
    while  startdir <= maxID :
        enddir=startdir+Interval-1;
       
        fileoutworkspace=outworkspace +"\\"+str(startdir)+"_"+str(enddir);#8bits
        fileoutworkspace1=outworkspace1 +"\\"+str(startdir)+"_"+str(enddir);#16bits
        if (os.path.exists(fileoutworkspace)) & (os.path.exists(fileoutworkspace1)) :
            arcpy.AddMessage(fileoutworkspace1);
        else:
            os.makedirs(fileoutworkspace);
            os.makedirs(fileoutworkspace1);
        
        startdir=enddir+1;




    arcpy.env.XYResolution = "0.6 Meters";
    arcpy.env.cellSize = "0.6"
    for row in arcpy.SearchCursor(clip_feat):
        mask = row.getValue("Shape")
        inaa=100
        arcpy.env.extent=mask.extent        
        ID= str(row.getValue(field1));
        Class_Name = str(row.getValue(field2));

        patchindex=Class_Name[len(Class_Name)-1];

        patchclass =Class_Name[0:(len(Class_Name)-2)]

        outPath = outworkspace+"\\" +DirPath(int(ID),minID,maxID,Interval)+ "\\"+ ID+outtype;#8bits
        outPath1 = outworkspace1+"\\" +DirPath(int(ID),minID,maxID,Interval)+ "\\"+ ID+outtype;#16bits
        arcpy.AddMessage(outPath1);
        arcpy.AddMessage("chipping: " + str(row.getValue(field1)) + "...count:" + str(total) + "\\" + str(count))

        arcpy.gp.ExtractByMask_sa(raster, mask, outPath1)
        arcpy.CopyRaster_management(outPath1,
                           outPath,"DEFAULTS","0","9",
                          "","","8_BIT_UNSIGNED")

        count = count + 1

except arcpy.ExecuteError:

    print arcpy.GetMessages()



