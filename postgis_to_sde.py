import arcpy
import os
import yaml

yaml.safe_load(open("config.yaml"))

arcpy.env.overwriteOutput = True

# set version where updates will be made
version = "FPDCC.FPD_test"
new_fl = None
pg_fl = None
#fcList = [f.name for f in arcpy.ListFields(sde_ws)]
#print fcList

postgis_table_list = ["picnicgroves", "trails"]
featureclass_list = ["Grove", "LeaderLine"]

for (postgis_table, featureclass) in zip(postgis_table_list, featureclass_list):

        try:
                #######################
                # new postgis workspace
                #######################

                postgis_connection = "C:\Users\jeremyhall\AppData\Roaming\ESRI\Desktop10.4\ArcCatalog\postgis.sde"
                arcpy.env.workspace = POSTGIS_CONNECTION
                pg_ws = POSTGIS_CONNECTION + POSTGIS_SCHEMA + '.' + postgis_table 
                pg_layer = postgis_table + '_layer'

        except:
                print ("##################")
                print ("could not connect to postgis")
                print (arcpy.GetMessages())

                
        try:
                ###################
                # new SDE workspace
                ###################

                fc_layer = featureclass + '_layer'
                arcpy.env.workspace = SDE_CONNECTION
                sde_ws = PATH_TO_FC + SDE_SCHEMA + featureclass
                new_fl = arcpy.MakeFeatureLayer_management(sde_ws, fc_layer)
                print ("sde feature layer {}".format(new_fl))

                # change sde version
                arcpy.ChangeVersion_management(fc_layer,"TRANSACTIONAL",version)

                # delete sde contents
                arcpy.DeleteFeatures_management(fc_layer)

        except:
                print ("##################")
                print ("could not connect to SDE")
                print (arcpy.GetMessages())


        try:
                pg_fl = arcpy.MakeFeatureLayer_management(pg_ws, pg_layer)
                print ("postgis table {}".format(pg_fl))

                print("appending new contents")
                arcpy.Append_management(pg_fl, fc_layer, "NO_TEST")    

        except:
                print ("##################")
                print ("No contents appended")
                print (arcpy.GetMessages())
                
        finally:
                if arcpy.Exists(new_fl):
                        arcpy.Delete_management(new_fl)
                if arcpy.Exists(pg_fl):
                        arcpy.Delete_management(pg_fl)
                        arcpy.ClearEnvironment("workspace")


# If you do not specify a connection, 
# all enterprise geodatabase workspaces will be removed from the Cache
# arcpy.ClearWorkspaceCache_management() 
# print(arcpy.GetMessages()) 
    
    
