# Project README: AWS S3 Data Transformation Pipeline

This project implements a robust and scalable **ETL (Extract, Transform, Load)** pipeline designed for data stored in **Amazon S3**. It utilizes **Databricks** and **PySpark** to efficiently process large volumes of data, handling ingestion, complex transformations, and the generation of analytical reports.

---

## Getting Started

This section outlines how to set up the environment and execute the data pipeline, which reads data from S3, transforms it, and writes the results back to S3.

### Prerequisites

* **AWS Credentials:** IAM role/user with necessary permissions for the S3 buckets.
* Databricks Workspace (with proper AWS integration setup).
* Python 3.x, Git for version control.

### Data Flow
```bash
                 
     ┌───────────▼────────────┐
     │  ├── Bronze (Raw)      │  ← Amazon S3
     │  ├── Silver (Cleansed) │  ← Databricks cleaning
     │  └── Gold (Star Schema)│  ← Load Fact table to Amazon S3
     └───────────┬────────────┘
                 │
                 │
           ┌─────▼─────┐
           │ Metabase   │
           │ Dashboards │
           └────────────┘
```
### Visualization with Metabase 
#### 1. Sale Performace
<img width="1857" height="926" alt="image" src="https://github.com/Dungpham0703/e-commerce-ETL/blob/main/reports/Sale_Performace_Dashboard.jpg" />
**Key Metrics Addressed**

Key Performance Indicators (KPIs)

    Total Revenue: What is the total sales revenue to date?
    
    Total Orders: What is the total number of orders to date?
    
    Total Products Sold: What is the total quantity of products sold to date?
    
    AVG Value per Order: What is the average monetary value of each order?

Detailed Visualizations

    Monthly Revenue & Orders: How have Total Orders and Total Revenue trended month-over-month over time?
    
    Orders by Payment Method: What is the distribution of orders across different payment methods (redit, boleto, voucher)?
    
    Revenue per State: How is the Total Revenue geographically distributed across different states in the country?
    
    Key Metrics by Category (Top 5): What are the top 5 product categories based on total revenue, average order value, and total orders?
    
    Daily Revenue & Orders by Dayname: How do Total Orders and Total Revenue fluctuate across the days of the week?
#### 2. Customer Insights
<img width="1857" height="926" alt="image" src="https://github.com/Dungpham0703/e-commerce-ETL/blob/main/reports/Customer%20Insights.jpg" />
**Key Metrics Addressed**

Key Performance Indicators (KPIs)

    Total Customers: What is the total number of unique customers to date?
    
    Repeat Customers: What is the total number of customers who have placed more than one order?
    
    Customer Lifetime Value (LCL...): What is the average predicted monetary value a customer will bring over their relationship with the company?
    
    Average Purchase Frequency: On average, how often does a customer place an order?

Detailed Visualizations

    Total Reviews based on Review Category: What is the distribution of customer reviews across different star ratings (1-star through 5-star)?
    
    Key Metrics by State: Which states have the highest total number of customers, repeat customers, and the highest repeat rate?
    
    Customer per State: How are total customers geographically distributed across different states?
    
    Top 10 Customer by number of Orders: Who are the top 10 customers (by unique ID) based on the number of orders they have placed?


### Running the Pipeline

The core transformation logic resides in the `databricks/` directory and is executed as a Databricks Job configured to run on a Spark cluster.

1.  **Configure AWS Access:** Ensure your Databricks cluster is configured to access S3 (using Instance Profiles or Secret Scopes).
2.  **Deployment:** Clone the repository to your Databricks Repos.

    ```bash
    git clone <your-repo-url>
    ```

3.  **Execution:** Run the main transformation script, `databricks/transform_data.py`. This script reads data from the source S3 path and writes the processed output to the target S3 path, typically defined via widget parameters or configuration files within Databricks.

---

## Repository Structure

The project is organized into clear directories to separate data, code, and output reports.

| Directory | Description | Key Files/Technologies |
| :--- | :--- | :--- |
| `data/` | Placeholder for **local data testing** or configuration files defining **S3 source paths**. In production, data is accessed directly from S3. | AWS S3 Source Data |
| `databricks/` | Contains the PySpark ETL scripts, optimized for execution on Databricks clusters. | `transform_data.py`, PySpark, Spark SQL |
| `reports/` | Placeholder for **local reports/schemas** or configuration defining **S3 target paths** for processed data. | AWS S3 Target Data, Final Tables |
| `.gitattributes` | Configuration for Git management. | Git Configuration |

---

## Technology Stack

* **PySpark:** For distributed, in-memory data processing and scalable transformations.
* **Databricks:** The cloud-based platform used for development, orchestration, and execution of ETL jobs.
* **AWS S3:** Primary storage layer for both raw (source) and processed (target) data.
* **Spark SQL:** Utilized for declarative data manipulation and joins.

---
