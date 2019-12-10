from pyspark.sql import SparkSession, SQLContext, DataFrame
from pyspark import SparkContext, SparkConf
from pyspark.sql.types import *
from operator import add
import sys

if __name__ == "__main__":
    # Config
    SparkC = SparkContext()
    sc = SQLContext(SparkC)

    spark = SparkSession \
        .builder \
        .appName("sparkProcessing") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    DFschema = StructType([\
        StructField("geo", BooleanType(), True), \
        StructField("id", LongType(), True), \
        StructField("lat", FloatType(), True), \
        StructField("long", FloatType(), True), \
        StructField("reply", BooleanType(), True), \
        StructField("replyText", StringType(), True), \
        StructField("restaurant", StringType(), True), \
        StructField("text", StringType(), True), \
        StructField("timestamp", StringType(), True), \
        StructField("url", StringType(), True), \
        StructField("user", StringType(), True), \
        StructField("userLocation", StringType(), True), \
        StructField("sentiment", FloatType(), True), \
        StructField("sarcasm", FloatType(), True), \
        StructField("stateName", StringType(), True), \
        StructField("stateCode", StringType(), True), \
        StructField("countryName", StringType(), True), \
        StructField("countryCode", StringType(), True)])

    df = sc.read.option("delimiter", ",").csv("./data/processedLocation/*.csv", header="false", schema=DFschema)
    df.createOrReplaceTempView("data")
    
    #
    mapQuery = "SELECT restaurant, stateCode AS location " 
    mapQuery += "FROM data WHERE countryCode=\'US\' AND stateCode != \'\' "
    mapQuery += "GROUP BY restaurant, location "
    mapQuery += "ORDER BY restaurant, location "
    
    d = {} # Initialize map with unique (restaurant, location)
    # Initialize values for numPosSent, numNegSent, numPosSarc, numNegSarc to 0
    dictMap = spark.sql(mapQuery).collect()
    for row in dictMap:
        key = (row[0], row[1])
        d[key] = ([0, 0, 0, 0])

    # Count all occurences of unique (restaurant, location, sentiment, sarcasm)
    query = "SELECT restaurant, stateCode, sentiment, sarcasm, COUNT(*) AS numTweets FROM data "
    query += "WHERE countryCode=\'US\' AND stateCode != \'\' "
    query += "GROUP BY restaurant, stateCode, sentiment, sarcasm "
    query += "ORDER BY restaurant, stateCode"
    countEntries = spark.sql(query).collect()
    result = open('./data/finalData/completedProcessing.csv', 'w')

    # Convert these counts into desired data format
    for row in countEntries:
        pair = (row[0], row[1])
        sent = row[2]
        sarc = row[3]
        count = row[4]
        # Populate dictionary with values
        if(sent == 0.0 and sarc == 0.0):
            d[pair][0] = count
        elif(sent == 1.0 and sarc == 0.0):
            d[pair][1] = count
        elif(sent == 0.0 and sarc == 1.0):
            d[pair][2] = count
        else:
            d[pair][3] = count

    # Sort dictionary and output to file in csv format
    for k in sorted(d.keys()):
        result.write(str(k[0]) + ", " + str(k[1]))
        for i in d[k]:
            result.write(", " + str(i))
        result.write("\n")
    result.close()