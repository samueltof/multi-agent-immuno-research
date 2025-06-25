# Test Data Files

This directory contains sample CSV files used for evaluating the Coder agent's ability to read and process various types of data files.

## File Descriptions

### Data Analysis Test Cases

- **`student_grades.csv`** (20 rows)
  - Contains student academic performance data
  - Columns: `student_id`, `name`, `math_score`, `science_score`, `english_score`, `history_score`
  - Used for: Statistical analysis, grade distribution, correlation analysis

- **`sales_data.csv`** (30 rows)  
  - Contains sales transaction data over time
  - Columns: `date`, `product_category`, `units_sold`, `revenue`, `region`
  - Used for: Trend analysis, regional performance, growth calculations

### Visualization Test Cases

- **`weather_data.csv`** (30 rows)
  - Contains daily weather measurements
  - Columns: `date`, `temperature`, `humidity`, `precipitation`, `wind_speed`
  - Used for: Time series plots, histograms, correlation heatmaps

- **`financial_data.csv`** (30 rows)
  - Contains stock market data across different sectors
  - Columns: `date`, `stock_price`, `volume`, `sector`, `market_cap`
  - Used for: Multi-plot dashboards, sector analysis, trend visualization

### Data Processing Test Cases

- **`customers.csv`** (15 rows)
  - Customer information for e-commerce analysis
  - Columns: `id`, `name`, `email`, `signup_date`
  - Used for: Data pipeline testing, joins with orders and products

- **`orders.csv`** (25 rows)
  - Order transaction records
  - Columns: `order_id`, `customer_id`, `product_id`, `quantity`, `order_date`
  - Used for: Relational data processing, customer lifetime value

- **`products.csv`** (12 rows)
  - Product catalog information
  - Columns: `product_id`, `name`, `price`, `category`
  - Used for: Product analysis, category-based insights

- **`messy_customer_data.csv`** (15 rows)
  - Intentionally messy customer data with quality issues
  - Issues: Missing values, inconsistent formats, duplicates, outliers
  - Used for: Data cleaning, quality assessment, preprocessing

### Debugging Test Cases

- **`scores.csv`** (15 rows)
  - Simple exam scores dataset
  - Columns: `student_id`, `name`, `score`
  - Used for: Testing error handling and code debugging skills

## Usage in Evaluations

The test dataset references these files via relative paths:
```python
sample_data="evals/agents/coder/test_data/filename.csv"
```

This allows the Coder agent to:
1. Practice reading actual CSV files from the filesystem
2. Handle different data types and structures
3. Work with realistic data sizes and complexity
4. Test file I/O error handling
5. Process multi-file data pipelines

## Data Characteristics

- **Realistic data patterns**: All files contain plausible data with appropriate distributions
- **Various complexities**: From simple single-table analysis to multi-file processing
- **Quality issues included**: Some files have intentional data quality problems
- **Time series data**: Several files include temporal components for trend analysis
- **Categorical data**: Multiple files include categorical variables for grouping/filtering
- **Missing values**: Strategic inclusion of missing data for robust testing 