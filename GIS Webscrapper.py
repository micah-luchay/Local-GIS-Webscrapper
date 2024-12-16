import urllib.request, json, arcpy

def downloadFeatures(serverLocation, output, serverLayers):

    for i in range(0, serverLayers):

        try:
            url = serverLocation + str(i)
            fields = '*'
            outputLocation = output

            urlString = url + "?f=json"
            request = urllib.request.urlopen(urlString) # request info on the feature service
            test = json.load(request) # convert the request to JSON format
            maxRetrieve = str(test["maxRecordCount"]) # grab the MaxRecordCount value from the JSON value
            layerName = str(test["name"])
            outputLocation = outputLocation + layerName
            print("Max extraction: " + maxRetrieve + " per request for " + layerName)

            urlString = url + '/query?where=1=1&returnCountOnly=true&f=json' # create the request to retrieve the number of records
            request = urllib.request.urlopen(urlString) # send the request to the server
            test = json.load(request)
            totalRecords = str(test["count"])
            print("There are " + totalRecords + " records for this feature service.")

            #test["layers"][0]["name"]

            maxRetrieve = int(maxRetrieve)
            totalRecords = int(totalRecords)
            print("Retrieving records.")
            fs = dict()


            for i in range(1, totalRecords, maxRetrieve):
                beginID = i
                endID = i + maxRetrieve

                if endID > totalRecords: # use this for the last stretch of selection
                    endID = totalRecords - 1 # simply make the upper OBJECTID one less than the total count

                print("Exporting OBJECTIDs " + str(beginID) + " - " + str(endID))
                where = "{}>={}&{}<{}".format("OBJECTID", beginID, "OBJECTID", endID)
                link = url + "/query?where={}&f=json&returnGeometry=true&outFields=*".format(where)
                #request = urllib.request.urlopen(link)
                print(link)
                fs[i] = arcpy.FeatureSet()
                fs[i].load(link)

            print ("Records successfully retrieved. Saving records for " + layerName)
            fslist = []
            for key,value in fs.items():
              fslist.append(value)
            arcpy.Merge_management(fslist, outputLocation)
            print ("Task Complete.")

        except:
            print("Error downloading layer.")


downloadFeatures(serverEndpoint, outputLocation, 59)
