from pyspark.sql.functions import lit, concat, split, col


def loadWakeCountyCSV(spark, data_file):
    return (spark.read
            .format("csv")
            .option("header", "true")
            .load(data_file)
            )


def loadDurhamCountyCSV(spark, data_file):
    return (spark.read
            .format("json")
            .load(data_file)
            )


def transformWakeCountyDF(WakeCountyDF):
    return (WakeCountyDF.withColumn("county", lit("Wake"))
            .withColumnRenamed("HSISID", "datasetId")
            .withColumnRenamed("NAME", "name")
            .withColumnRenamed("ADDRESS1", "address1")
            .withColumnRenamed("ADDRESS2", "address2")
            .withColumnRenamed("CITY", "city")
            .withColumnRenamed("STATE", "state")
            .withColumnRenamed("POSTALCODE", "zip")
            .withColumnRenamed("PHONENUMBER", "tel")
            .withColumnRenamed("RESTAURANTOPENDATE", "dateStart")
            .withColumn("dateEnd", lit(""))
            .withColumnRenamed("FACILITYTYPE", "type")
            .withColumnRenamed("X", "geoX")
            .withColumnRenamed("Y", "geoY")
            .drop("OBJECTID")
            .drop("PERMITID")
            .drop("GEOCODESTATUS")
            .withColumn("id", concat("state", lit("_"), "county", lit("_"), "datasetId"))
            )


def transformDurhamCountyDF(DurhamCountyDF):
    return (DurhamCountyDF.withColumn("county", lit("Durham"))
            .withColumn("datasetId", col("fields.id"))
            .withColumn("name", col("fields.premise_name"))
            .withColumn("address1", col("fields.premise_address1"))
            .withColumn("address2", col("fields.premise_address2"))
            .withColumn("city", col("fields.premise_city"))
            .withColumn("state", col("fields.premise_state"))
            .withColumn("zip", col("fields.premise_zip"))
            .withColumn("tel", col("fields.premise_phone"))
            .withColumn("dateStart", col("fields.opening_date"))
            .withColumn("dateEnd", col("fields.closing_date"))
            .withColumn("type", split(col("fields.type_description"), "-").getItem(1))
            .withColumn("geoX", col("fields.geolocation").getItem(0))
            .withColumn("geoY", col("fields.geolocation").getItem(1))
            .drop("fields")
            .drop("geometry")
            .drop("record_timestamp")
            .drop("recordid")
            .withColumn("id", concat("state", lit("_"), "county", lit("_"), "datasetId"))
            )

def combineDFs(df1,df2):
        return df1.unionByName(df2)
        
def print_df_summary(name, df):
    print(name, " df has ", df.count(), " rows")
    print(name, " df has ", df.rdd.getNumPartitions(), " partitions")