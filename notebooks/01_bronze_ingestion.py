# Databricks notebook source
# MAGIC %md
# MAGIC ## Step 1: Read files from Volume

# COMMAND ----------

volume_path = "/Volumes/nyc_taxi/raw/taxi_files"
display(dbutils.fs.ls(volume_path))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2: Read all parquet files

# COMMAND ----------

df_raw = spark.read.parquet("/Volumes/nyc_taxi/raw/taxi_files")

display(df_raw.limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 3: Check Schema

# COMMAND ----------

df_raw.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 4: Record Count

# COMMAND ----------

print(f"Total Records = {df_raw.count():,}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 5: Create Bronze Delta Table

# COMMAND ----------

(
    df_raw.write
        .format("delta")
        .mode("overwrite")
        .saveAsTable("nyc_taxi.bronze.taxi_trip_bronze")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 6: Validate

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from nyc_taxi.bronze.taxi_trip_bronze

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 7: Explore table

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from nyc_taxi.bronze.taxi_trip_bronze limit 10

# COMMAND ----------

df_raw = (
    spark.read
    .parquet("/Volumes/nyc_taxi/raw/taxi_files/*.parquet")
    .select("*", "_metadata")
)
display(df_raw.select("_metadata").limit(5))

# COMMAND ----------

from pyspark.sql.functions import current_timestamp,col

df_bronze = (
    df_raw
    .withColumn("ingestion_timestamp", current_timestamp())
    .withColumn("source_file_path", df_raw["_metadata.file_path"])
    .withColumn("source_file_name",df_raw["_metadata.file_name"])
)
display(df_bronze.limit(10))

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS nyc_taxi.bronze.taxi_trip_bronze;

# COMMAND ----------

(
    df_bronze
    .drop("_metadata")
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("nyc_taxi.bronze.taxi_trip_bronze")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from nyc_taxi.bronze.taxi_trip_bronze

# COMMAND ----------

# MAGIC %sql
# MAGIC select source_file_name, count(*) from nyc_taxi.bronze.taxi_trip_bronze
# MAGIC group by source_file_name

# COMMAND ----------

# MAGIC
# MAGIC %sql
# MAGIC DESCRIBE nyc_taxi.bronze.taxi_trip_bronze;

# COMMAND ----------

# MAGIC %md
# MAGIC ## NULL ANALYSIS

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC COUNT(*) total_records,
# MAGIC SUM(CASE WHEN passenger_count IS NULL THEN 1 ELSE 0 END) passenger_nulls,
# MAGIC SUM(CASE WHEN fare_amount IS NULL THEN 1 ELSE 0 END) fare_nulls,
# MAGIC SUM(CASE WHEN trip_distance IS NULL THEN 1 ELSE 0 END) distance_nulls
# MAGIC FROM nyc_taxi.bronze.taxi_trip_bronze;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Check Duplicate records

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) total_rows,
# MAGIC COUNT(DISTINCT CONCAT(
# MAGIC VendorID,
# MAGIC tpep_pickup_datetime,
# MAGIC tpep_dropoff_datetime,
# MAGIC PULocationID,
# MAGIC DOLocationID
# MAGIC )) distinct_rows
# MAGIC FROM nyc_taxi.bronze.taxi_trip_bronze;