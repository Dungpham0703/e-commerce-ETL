from pyspark.sql import SparkSession 
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, TimestampType

spark = SparkSession.builder.appName("E-Commerce-Data-Pipeline").getOrCreate()

s3_path = 's3://brazil-e-commerce/data/'
target_delta_path = f"{s3_path}delta/fact_sales/"
fact_table_name = "fact_sales"

df_customers = spark.read.csv(f'{s3_path}olist_customers_dataset.csv', header=True, inferSchema=True)
df_orders = spark.read.csv(f'{s3_path}olist_orders_dataset.csv', header=True, inferSchema=True)
df_order_items = spark.read.csv(f'{s3_path}olist_order_items_dataset.csv', header=True, inferSchema=True)
df_products = spark.read.csv(f'{s3_path}olist_products_dataset.csv', header=True, inferSchema=True)
df_sellers = spark.read.csv(f'{s3_path}olist_sellers_dataset.csv', header=True, inferSchema=True)
df_reviews = spark.read.csv(f'{s3_path}olist_order_reviews_dataset.csv', header=True, inferSchema=True)

print("--- Data Transform Process ---")

df_reviews_cleaned = df_reviews.select(
    F.col("review_id"),
    F.col("order_id"),
    F.col("review_comment_message"),
    F.col("review_creation_date").cast(TimestampType()).alias("review_created_at")
)

df_products_cleaned = df_products.fillna({
    'product_category_name': 'unknown',
    'product_photos_qty': 0,
    'product_weight_g': 0,
    'product_length_cm': 0,
    'product_height_cm': 0,
    'product_width_cm': 0
}).withColumn(
    "product_category_standard",
    F.lower(F.regexp_replace(F.col("product_category_name"), "[- ]", "_"))
)

df_orders_final = df_orders.filter(F.col("order_status") == "delivered") \
    .withColumn(
        "delivery_time_days",
        F.datediff(F.col("order_delivered_customer_date"), F.col("order_purchase_timestamp"))
    ).withColumn(
        "purchase_month_key", 
        F.date_format(F.col("order_purchase_timestamp"), "yyyyMM").cast(IntegerType())
    )

df_fact = df_orders_final.alias("o").join(
    df_order_items.alias("oi"), on="order_id", how="inner" 
)

# JOIN Dimension Table
df_fact = df_fact.join(df_customers.alias("c"), on="customer_id", how="left")
df_fact = df_fact.join(df_sellers.alias("s"), on="seller_id", how="left")
df_fact = df_fact.join(df_products_cleaned.alias("p"), on="product_id", how="left")
df_fact = df_fact.join(df_reviews_cleaned.alias("r"), on="order_id", how="left")

# (Final Schema Selection) ---

df_sales_fact = df_fact.select(
    F.col("o.order_id"),
    F.col("c.customer_unique_id").alias("customer_key"),
    F.col("s.seller_id").alias("seller_key"),
    F.col("p.product_id").alias("product_key"),
    
    # METRICS (Facts)
    F.col("oi.price").alias("product_price"),
    F.col("oi.freight_value").alias("shipping_cost"),
    F.col("r.review_rating"),
    F.col("o.delivery_time_days"), 
    # DIMENSION ATTRIBUTES
    F.col("o.order_status"),
    F.col("o.purchase_month_key"), 
    F.col("o.order_purchase_timestamp").alias("purchase_date"),
    F.col("c.customer_city"),
    F.col("c.customer_state"),
    F.col("p.product_category_standard").alias("product_category")
)

#  5 Save to Delta Lake 
target_delta_path = f"{s3_path}delta/fact_sales/"
df_sales_fact.write.format("delta") \
             .mode("overwrite") \
             .option("overwriteSchema", "true") \
             .partitionBy("purchase_month_key") \
             .save(target_delta_path)

spark.sql(f"""
    CREATE TABLE IF NOT EXISTS {fact_table_name}
    USING DELTA
    LOCATION '{target_delta_path}'
""")

print(f"Fact table has been created successfully: **{fact_table_name}**")
print("Schema cuối cùng:")
df_sales_fact.printSchema()
