import sys

from pyspark.sql import *

from functions import loadWakeCountyCSV, transformWakeCountyDF, loadDurhamCountyCSV, transformDurhamCountyDF, combineDFs, print_df_summary


if __name__ == "__main__":

    spark = SparkSession\
        .builder\
        .appName("Rest")\
        .getOrCreate()

    if len(sys.argv) != 3:
        print("Usage: main <filename1> <filename2>")
        sys.exit(-1)

    print("Starting main")
    print("###########################################################################################################")
    print("#1: Loading CSV data file having data for restaurants in Wake county")
    WakeCounty_raw_df = loadWakeCountyCSV(spark, sys.argv[1])
    print("Right after raw data load of wake county dataset")
    print(WakeCounty_raw_df.schema.simpleString())
    WakeCounty_raw_df.show(5)

    print("WakeCounty_raw_df is having ", WakeCounty_raw_df.count(), " records.")

    WakeCounty_transformed_df = transformWakeCountyDF(WakeCounty_raw_df)
    print("Right after wake county raw dataframe is transformed")
    #WakeCounty_transformed_df.printSchema()
    print(WakeCounty_transformed_df.schema.simpleString())

    WakeCounty_transformed_df.show(5)
    #print("WakeCounty_transformed_df has ", WakeCounty_transformed_df.rdd.getNumPartitions(), " Partitions")

    #print(WakeCounty_transformed_df.schema)
    #print(WakeCounty_transformed_df.schema.simpleString())
    #print(WakeCounty_transformed_df.schema.json())

    print(" ")
    print("###########################################################################################################")
    print("#2: Loading Json data file having data for restaurants in Durham county")
    DurhamCounty_raw_df = loadDurhamCountyCSV(spark, sys.argv[2])
    print("Right after raw data load of wake county dataset")
    #DurhamCounty_raw_df.printSchema()
    print(DurhamCounty_raw_df.schema.simpleString())
    DurhamCounty_raw_df.show(5, truncate=False)

    # The Json has nested data & arrays, which is bit difficult to handle
    #to access the fields in a nested structure use dot(.) symbol in path.
    #To access an element in an array, use the getItem() method
    DurhamCounty_transformed_df = transformDurhamCountyDF(DurhamCounty_raw_df)

    #DurhamCounty_transformed_df.printSchema()
    print(DurhamCounty_transformed_df.schema.simpleString())
    DurhamCounty_transformed_df.show(5, truncate=True)

    print(" ")
    print("###########################################################################################################")
    print("#3: union the two dataframes")
    union_df = combineDFs(WakeCounty_transformed_df,DurhamCounty_transformed_df)
    union_df.show(5)
    union_df.printSchema()

    print_df_summary('WakeCounty_raw_df', WakeCounty_raw_df)
    print_df_summary('WakeCounty_transformed_df', WakeCounty_transformed_df)

    print_df_summary('DurhamCounty_raw_df', WakeCounty_raw_df)
    print_df_summary('DurhamCounty_transformed_df', WakeCounty_transformed_df)

    print_df_summary('union_df',union_df)

    spark.stop()