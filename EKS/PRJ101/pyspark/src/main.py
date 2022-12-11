import sys

from pyspark.sql import *

from functions import loadWakeCountyCSV, print_df_summary


if __name__ == "__main__":

    spark = SparkSession\
        .builder\
        .appName("Rest")\
        .getOrCreate()

    if len(sys.argv) != 2:
        print("Usage: main <filename1>")
        sys.exit(-1)

    print("Starting main")
    print("###########################################################################################################")
    print("#1: Loading CSV data file having data for restaurants in Wake county")
    WakeCounty_raw_df = loadWakeCountyCSV(spark, sys.argv[1])
    print("Right after raw data load of wake county dataset")
    print(WakeCounty_raw_df.schema.simpleString())
    WakeCounty_raw_df.show(5)

    print("WakeCounty_raw_df is having ", WakeCounty_raw_df.count(), " records.")

    print_df_summary('WakeCounty_raw_df',WakeCounty_raw_df)

    spark.stop()
