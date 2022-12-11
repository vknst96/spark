from pyspark.sql.functions import lit, concat, split, col


def loadWakeCountyCSV(spark, data_file):
    return (spark.read
            .format("csv")
            .option("header", "true")
            .load(data_file)
            )
        
def print_df_summary(name, df):
    print(name, " df has ", df.count(), " rows")
    print(name, " df has ", df.rdd.getNumPartitions(), " partitions")
