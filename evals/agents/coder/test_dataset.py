"""
Test dataset for evaluating the Coder agent.

This module contains test cases covering various coding scenarios:
- Data analysis and statistical computation
- Data visualization and plotting
- Data manipulation and processing
- Algorithm implementation
- Error handling and debugging
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class CoderTestCase:
    """Test case for evaluating the coder agent."""
    id: str
    task_description: str
    task_type: str  # "data_analysis", "visualization", "algorithm", "data_processing", "debugging"
    difficulty: str  # "easy", "medium", "hard"
    expected_deliverables: str
    sample_data: Optional[str] = None
    reference_solution: Optional[str] = None
    success_criteria: List[str] = None
    
    def __post_init__(self):
        if self.success_criteria is None:
            self.success_criteria = []


# Data Analysis Test Cases
DATA_ANALYSIS_CASES = [
    CoderTestCase(
        id="data_analysis_001",
        task_description="""
        Create a Python script that analyzes a dataset of student grades. The dataset is provided below:

        ```
        student_id,name,math_score,science_score,english_score,history_score
        1,Alice Johnson,85,92,78,88
        2,Bob Smith,92,87,85,90
        3,Carol Brown,78,85,92,82
        4,David Wilson,88,78,87,85
        5,Eve Davis,95,93,89,91
        6,Frank Miller,82,88,84,79
        7,Grace Lee,89,91,93,87
        8,Henry Taylor,76,82,85,88
        9,Ivy Chen,93,89,91,94
        10,Jack Anderson,87,85,82,86
        11,Kate Thompson,91,94,88,92
        12,Liam Garcia,84,87,90,83
        13,Mia Rodriguez,88,83,87,89
        14,Noah Martinez,79,86,84,91
        15,Olivia Clark,92,88,93,85
        ```
        
        Please:
        1. Parse the CSV data from the text above
        2. Calculate descriptive statistics for each subject
        3. Find the top 5 students by overall average
        4. Identify which subject has the highest variance
        5. Calculate correlation matrix between subjects
        6. Create summary statistics report
        """,
        task_type="data_analysis",
        difficulty="medium",
        expected_deliverables="Python code that parses CSV data and performs statistical analysis with descriptive statistics, top students, variance analysis, and correlation matrix",
        sample_data="""student_id,name,math_score,science_score,english_score,history_score
1,Alice Johnson,85,92,78,88
2,Bob Smith,92,87,85,90
3,Carol Brown,78,85,92,82
4,David Wilson,88,78,87,85
5,Eve Davis,95,93,89,91
6,Frank Miller,82,88,84,79
7,Grace Lee,89,91,93,87
8,Henry Taylor,76,82,85,88
9,Ivy Chen,93,89,91,94
10,Jack Anderson,87,85,82,86
11,Kate Thompson,91,94,88,92
12,Liam Garcia,84,87,90,83
13,Mia Rodriguez,88,83,87,89
14,Noah Martinez,79,86,84,91
15,Olivia Clark,92,88,93,85""",
        success_criteria=[
            "Parses CSV data from text correctly",
            "Calculates mean, median, std dev for each subject",
            "Identifies top 5 students correctly",
            "Computes variance for all subjects",
            "Creates correlation matrix",
            "Outputs clear summary report"
        ]
    ),
    
    CoderTestCase(
        id="data_analysis_002",
        task_description="""
        Analyze the following sales data (passed from state memory) to identify trends and insights:

        ```
        date,product_category,units_sold,revenue,region
        2024-01-15,Electronics,120,24000,North
        2024-01-20,Clothing,85,4250,South
        2024-01-25,Home & Garden,65,3250,West
        2024-02-01,Electronics,145,29000,East
        2024-02-05,Books,95,1425,North
        2024-02-10,Clothing,110,5500,South
        2024-02-15,Sports,75,3750,West
        2024-02-20,Electronics,130,26000,North
        2024-03-01,Home & Garden,90,4500,East
        2024-03-05,Clothing,125,6250,South
        2024-03-10,Books,80,1200,West
        2024-03-15,Sports,95,4750,North
        2024-03-20,Electronics,160,32000,East
        2024-03-25,Home & Garden,105,5250,South
        2024-04-01,Clothing,140,7000,West
        ```
        
        Tasks:
        1. Parse the CSV data from the text above
        2. Calculate total revenue by product category
        3. Find monthly sales trends
        4. Identify the best performing region
        5. Calculate growth rate month-over-month
        6. Perform seasonal analysis if patterns exist
        """,
        task_type="data_analysis",
        difficulty="medium",
        expected_deliverables="Statistical analysis with data parsing, revenue summaries, trend analysis, regional performance, and growth calculations",
        sample_data="""date,product_category,units_sold,revenue,region
2024-01-15,Electronics,120,24000,North
2024-01-20,Clothing,85,4250,South
2024-01-25,Home & Garden,65,3250,West
2024-02-01,Electronics,145,29000,East
2024-02-05,Books,95,1425,North
2024-02-10,Clothing,110,5500,South
2024-02-15,Sports,75,3750,West
2024-02-20,Electronics,130,26000,North
2024-03-01,Home & Garden,90,4500,East
2024-03-05,Clothing,125,6250,South
2024-03-10,Books,80,1200,West
2024-03-15,Sports,95,4750,North
2024-03-20,Electronics,160,32000,East
2024-03-25,Home & Garden,105,5250,South
2024-04-01,Clothing,140,7000,West""",
        success_criteria=[
            "Parses CSV data from text correctly",
            "Aggregates revenue by category correctly",
            "Identifies monthly trends",
            "Ranks regions by performance",
            "Calculates growth rates",
            "Provides insights on seasonal patterns"
        ]
    )
]

# Visualization Test Cases
VISUALIZATION_CASES = [
    CoderTestCase(
        id="visualization_001",
        task_description="""
        Create visualizations for the following weather dataset (provided from state memory):

        ```
        date,temperature,humidity,precipitation,wind_speed
        2024-01-01,32.5,65,0.0,8.2
        2024-01-02,28.1,72,0.1,12.5
        2024-01-03,35.0,58,0.0,6.8
        2024-01-04,29.3,68,0.3,15.2
        2024-01-05,31.7,61,0.0,9.1
        2024-01-06,26.8,75,0.8,18.3
        2024-01-07,33.2,55,0.0,7.6
        2024-01-08,30.5,70,0.2,11.4
        2024-01-09,27.9,73,1.2,22.1
        2024-01-10,34.1,59,0.0,8.9
        ```
        
        Create the following plots:
        1. Parse the CSV data from the text above
        2. Line plot showing temperature trends over time
        3. Histogram of precipitation values
        4. Scatter plot of temperature vs humidity
        5. Box plot comparing wind speeds by month (if enough data)
        6. Heatmap showing correlation between all numeric variables
        
        Ensure all plots have proper titles, labels, and legends.
        
        **Save all plots to**: `/Users/samueltorres/Documents/Repos/apps/multi-agent-immuno-research/evals/outputs/coder/plots/`
        """,
        task_type="visualization",
        difficulty="medium",
        expected_deliverables="Multiple well-formatted plots with data parsing and appropriate titles, labels, and styling",
        sample_data="""date,temperature,humidity,precipitation,wind_speed
2024-01-01,32.5,65,0.0,8.2
2024-01-02,28.1,72,0.1,12.5
2024-01-03,35.0,58,0.0,6.8
2024-01-04,29.3,68,0.3,15.2
2024-01-05,31.7,61,0.0,9.1
2024-01-06,26.8,75,0.8,18.3
2024-01-07,33.2,55,0.0,7.6
2024-01-08,30.5,70,0.2,11.4
2024-01-09,27.9,73,1.2,22.1
2024-01-10,34.1,59,0.0,8.9""",
        success_criteria=[
            "Parses CSV data from text correctly",
            "Creates line plot with time series data",
            "Generates histogram with proper binning",
            "Makes scatter plot with clear axes",
            "Produces box plot with categorical grouping",
            "Creates correlation heatmap",
            "All plots have titles and labels",
            "Saves all plots to specified directory path"
        ]
    ),
    
    CoderTestCase(
        id="visualization_002",
        task_description="""
        Create an interactive dashboard-style visualization for the following financial data:

        ```
        date,stock_price,volume,sector,market_cap
        2024-01-01,150.25,2500000,Technology,50000000000
        2024-01-02,152.80,2100000,Technology,50500000000
        2024-01-03,148.90,2800000,Technology,49200000000
        2024-01-04,155.40,1900000,Technology,51400000000
        2024-01-05,153.20,2200000,Technology,50600000000
        2024-01-08,157.75,2400000,Technology,52100000000
        2024-01-09,160.30,2000000,Technology,53000000000
        2024-01-10,158.65,2300000,Technology,52400000000
        2024-01-11,162.10,1800000,Technology,53600000000
        2024-01-12,159.85,2100000,Technology,52800000000
        2024-01-15,45.20,1500000,Healthcare,15000000000
        2024-01-16,46.80,1200000,Healthcare,15500000000
        2024-01-17,44.10,1800000,Healthcare,14600000000
        2024-01-18,47.50,1100000,Healthcare,15700000000
        2024-01-19,46.25,1400000,Healthcare,15300000000
        2024-01-22,48.90,1600000,Healthcare,16200000000
        2024-01-23,50.15,1000000,Healthcare,16600000000
        2024-01-24,49.30,1300000,Healthcare,16300000000
        2024-01-25,51.75,1700000,Healthcare,17100000000
        2024-01-26,50.90,1200000,Healthcare,16800000000
        ```
        
        Requirements:
        1. Parse the CSV data from the text above
        2. Multi-subplot figure with stock price and volume over time
        3. Bar chart showing average market cap by sector
        4. Scatter plot of price vs volume colored by sector
        5. Use consistent color scheme across all plots
        6. Add trend lines where appropriate
        
        **Save all plots to**: `/Users/samueltorres/Documents/Repos/apps/multi-agent-immuno-research/evals/outputs/coder/plots/`
        """,
        task_type="visualization",
        difficulty="hard",
        expected_deliverables="Complex multi-plot visualization with consistent styling and trend analysis",
        sample_data="""date,stock_price,volume,sector,market_cap
2024-01-01,150.25,2500000,Technology,50000000000
2024-01-02,152.80,2100000,Technology,50500000000
2024-01-03,148.90,2800000,Technology,49200000000
2024-01-04,155.40,1900000,Technology,51400000000
2024-01-05,153.20,2200000,Technology,50600000000
2024-01-08,157.75,2400000,Technology,52100000000
2024-01-09,160.30,2000000,Technology,53000000000
2024-01-10,158.65,2300000,Technology,52400000000
2024-01-11,162.10,1800000,Technology,53600000000
2024-01-12,159.85,2100000,Technology,52800000000
2024-01-15,45.20,1500000,Healthcare,15000000000
2024-01-16,46.80,1200000,Healthcare,15500000000
2024-01-17,44.10,1800000,Healthcare,14600000000
2024-01-18,47.50,1100000,Healthcare,15700000000
2024-01-19,46.25,1400000,Healthcare,15300000000
2024-01-22,48.90,1600000,Healthcare,16200000000
2024-01-23,50.15,1000000,Healthcare,16600000000
2024-01-24,49.30,1300000,Healthcare,16300000000
2024-01-25,51.75,1700000,Healthcare,17100000000
2024-01-26,50.90,1200000,Healthcare,16800000000""",
        success_criteria=[
            "Parses CSV data from text correctly",
            "Creates multi-subplot layout",
            "Shows time series with dual y-axes",
            "Makes grouped bar chart",
            "Uses consistent color coding",
            "Adds trend lines or regression",
            "Saves all plots to specified directory path"
        ]
    )
]

# Data Processing Test Cases
DATA_PROCESSING_CASES = [
    CoderTestCase(
        id="data_processing_001",
        task_description="""
        Clean and process the following messy customer dataset. The data has issues like missing values, 
        inconsistent date formats, duplicate entries, outliers, and inconsistent text formatting:

        ```
        customer_id,name,email,phone,signup_date,age,annual_income,city
        1,alice johnson,alice@email.com,555-1234,2023-01-15,25,45000,New York
        2,BOB SMITH,bob.smith@gmail.com,555.5678,01/20/2023,35,75000,Los Angeles
        3,Carol Brown,carol@email.com,(555) 9012,2023-02-10,28,55000,Chicago
        4,alice johnson,alice@email.com,555-1234,2023-01-15,25,45000,New York
        5,David Wilson,david.w@yahoo.com,555-3456,2023/03/05,42,95000,Houston
        6,Eve Davis,,555-7890,2023-03-20,,62000,Phoenix
        7,Frank Miller,frank@email.com,555-2345,2023-04-12,31,48000,Philadelphia
        8,Grace Lee,grace.lee@hotmail.com,555-6789,04/25/2023,29,71000,San Antonio
        9,,ivy.chen@email.com,555-0123,2023-05-10,26,53000,San Diego
        10,Jack Anderson,jack@email.com,555-4567,2023-05-22,33,67000,Dallas
        11,Kate Thompson,kate.t@gmail.com,555-8901,2023-06-08,27,59000,San Jose
        12,Liam Garcia,liam@email.com,555-2345,2023-06-15,38,83000,Austin
        13,Mia Rodriguez,mia.r@yahoo.com,555-5678,2023-07-03,24,41000,Jacksonville
        14,Noah Martinez,noah@email.com,555-9012,2023-07-18,36,72000,San Francisco
        15,Olivia Clark,olivia@email.com,555-3456,2023-08-05,30,58000,Columbus
        16,alice johnson,alice@email.com,555-1234,2023-01-15,25,450000,New York
        17,Paul White,paul.white@gmail.com,555-7890,2023-08-20,45,89000,Fort Worth
        18,Quinn Taylor,quinn@email.com,,2023-09-10,32,64000,Charlotte
        19,Rachel Green,rachel.g@email.com,555-1234,2023-09-25,28,56000,Seattle
        20,Sam Johnson,sam@email.com,555-5678,2023-10-12,34,76000,Denver
        ```
        
        Tasks:
        1. Parse the CSV data from the text above
        2. Handle missing values appropriately
        3. Standardize date formats
        4. Remove duplicates
        5. Detect and handle outliers
        6. Standardize text fields (proper case, trimming)
        7. Create a data quality report
        """,
        task_type="data_processing",
        difficulty="medium",
        expected_deliverables="Clean dataset with documented preprocessing steps and data quality report",
        sample_data="""customer_id,name,email,phone,signup_date,age,annual_income,city
1,alice johnson,alice@email.com,555-1234,2023-01-15,25,45000,New York
2,BOB SMITH,bob.smith@gmail.com,555.5678,01/20/2023,35,75000,Los Angeles
3,Carol Brown,carol@email.com,(555) 9012,2023-02-10,28,55000,Chicago
4,alice johnson,alice@email.com,555-1234,2023-01-15,25,45000,New York
5,David Wilson,david.w@yahoo.com,555-3456,2023/03/05,42,95000,Houston
6,Eve Davis,,555-7890,2023-03-20,,62000,Phoenix
7,Frank Miller,frank@email.com,555-2345,2023-04-12,31,48000,Philadelphia
8,Grace Lee,grace.lee@hotmail.com,555-6789,04/25/2023,29,71000,San Antonio
9,,ivy.chen@email.com,555-0123,2023-05-10,26,53000,San Diego
10,Jack Anderson,jack@email.com,555-4567,2023-05-22,33,67000,Dallas
11,Kate Thompson,kate.t@gmail.com,555-8901,2023-06-08,27,59000,San Jose
12,Liam Garcia,liam@email.com,555-2345,2023-06-15,38,83000,Austin
13,Mia Rodriguez,mia.r@yahoo.com,555-5678,2023-07-03,24,41000,Jacksonville
14,Noah Martinez,noah@email.com,555-9012,2023-07-18,36,72000,San Francisco
15,Olivia Clark,olivia@email.com,555-3456,2023-08-05,30,58000,Columbus
16,alice johnson,alice@email.com,555-1234,2023-01-15,25,450000,New York
17,Paul White,paul.white@gmail.com,555-7890,2023-08-20,45,89000,Fort Worth
18,Quinn Taylor,quinn@email.com,,2023-09-10,32,64000,Charlotte
19,Rachel Green,rachel.g@email.com,555-1234,2023-09-25,28,56000,Seattle
20,Sam Johnson,sam@email.com,555-5678,2023-10-12,34,76000,Denver""",
        success_criteria=[
            "Parses CSV data from text correctly",
            "Handles missing values with appropriate strategy",
            "Converts dates to consistent format",
            "Removes duplicate records",
            "Identifies and treats outliers",
            "Standardizes text formatting",
            "Generates data quality report"
        ]
    ),
    
    CoderTestCase(
        id="data_processing_002",
        task_description="""
        Create a data pipeline that merges multiple CSV datasets and performs transformations:
        
        Customers dataset:
        ```
        customer_id,name,email,signup_date
        1,Alice Johnson,alice@email.com,2023-01-15
        2,Bob Smith,bob.smith@gmail.com,2023-01-20
        3,Carol Brown,carol@email.com,2023-02-10
        4,David Wilson,david.w@yahoo.com,2023-03-05
        5,Eve Davis,eve@email.com,2023-03-20
        ```
        
        Orders dataset:
        ```
        order_id,customer_id,product_id,quantity,order_date
        101,1,201,2,2023-02-01
        102,2,202,1,2023-02-15
        103,1,203,3,2023-03-01
        104,3,201,1,2023-03-10
        105,4,204,2,2023-03-15
        106,1,202,1,2023-04-01
        107,5,203,2,2023-04-10
        108,2,201,3,2023-04-20
        109,3,204,1,2023-05-01
        110,4,202,2,2023-05-15
        ```
        
        Products dataset:
        ```
        product_id,name,price,category
        201,Laptop,999.99,Electronics
        202,Book,19.99,Education
        203,Coffee Maker,79.99,Home
        204,Headphones,129.99,Electronics
        ```
        
        Tasks:
        1. Parse all three CSV datasets from the text above
        2. Merge them into a comprehensive sales dataset
        3. Calculate total order value for each order
        4. Add customer lifetime value calculations
        5. Create monthly aggregations
        6. Export processed data with proper indexing
        """,
        task_type="data_processing",
        difficulty="hard",
        expected_deliverables="Merged and transformed dataset with calculated metrics and proper data structure",
        sample_data="""customers:
customer_id,name,email,signup_date
1,Alice Johnson,alice@email.com,2023-01-15
2,Bob Smith,bob.smith@gmail.com,2023-01-20
3,Carol Brown,carol@email.com,2023-02-10
4,David Wilson,david.w@yahoo.com,2023-03-05
5,Eve Davis,eve@email.com,2023-03-20

orders:
order_id,customer_id,product_id,quantity,order_date
101,1,201,2,2023-02-01
102,2,202,1,2023-02-15
103,1,203,3,2023-03-01
104,3,201,1,2023-03-10
105,4,204,2,2023-03-15
106,1,202,1,2023-04-01
107,5,203,2,2023-04-10
108,2,201,3,2023-04-20
109,3,204,1,2023-05-01
110,4,202,2,2023-05-15

products:
product_id,name,price,category
201,Laptop,999.99,Electronics
202,Book,19.99,Education
203,Coffee Maker,79.99,Home
204,Headphones,129.99,Electronics""",
        success_criteria=[
            "Parses all CSV datasets from text correctly",
            "Performs correct joins between tables",
            "Calculates order values accurately",
            "Computes customer lifetime value",
            "Creates time-based aggregations",
            "Exports well-structured final dataset"
        ]
    )
]

# Algorithm Implementation Test Cases
ALGORITHM_CASES = [
    CoderTestCase(
        id="algorithm_001",
        task_description="""
        Implement a recommendation system for products based on user purchase history.
        
        Given user-item interaction data, implement:
        1. Collaborative filtering algorithm (user-based or item-based)
        2. Content-based filtering using product features
        3. Hybrid approach combining both methods
        4. Evaluation metrics (precision, recall, RMSE)
        5. Function to generate top-N recommendations for a user
        
        Test the system with sample data and show performance metrics.
        """,
        task_type="algorithm",
        difficulty="hard",
        expected_deliverables="Complete recommendation system with multiple algorithms and evaluation framework",
        success_criteria=[
            "Implements collaborative filtering",
            "Implements content-based filtering", 
            "Creates hybrid recommendation approach",
            "Calculates evaluation metrics",
            "Generates ranked recommendations",
            "Tests system with sample data"
        ]
    ),
    
    CoderTestCase(
        id="algorithm_002",
        task_description="""
        Create a time series forecasting system for sales prediction.
        
        Requirements:
        1. Implement moving average forecasting
        2. Implement exponential smoothing
        3. Implement simple linear regression for trends
        4. Create ensemble method combining all three
        5. Add seasonality detection and adjustment
        6. Evaluate forecast accuracy with MAE, RMSE, MAPE
        7. Generate forecast plots with confidence intervals
        """,
        task_type="algorithm",
        difficulty="hard",
        expected_deliverables="Time series forecasting system with multiple methods and comprehensive evaluation",
        success_criteria=[
            "Implements multiple forecasting methods",
            "Detects and handles seasonality",
            "Creates ensemble predictions",
            "Calculates multiple accuracy metrics",
            "Generates forecast visualizations",
            "Shows confidence intervals"
        ]
    ),
    
    CoderTestCase(
        id="algorithm_003",
        task_description="""
        Implement a simple data clustering algorithm using the following dataset provided from state memory:

        ```
        x,y,category
        2.1,3.4,A
        2.5,3.1,A
        1.8,3.7,A
        8.2,7.9,B
        8.5,8.1,B
        7.9,7.6,B
        5.1,5.2,C
        5.3,4.9,C
        4.8,5.4,C
        1.2,8.9,D
        1.5,9.1,D
        1.1,8.7,D
        ```
        
        Tasks:
        1. Parse the CSV data from the text above
        2. Implement K-means clustering algorithm (k=4)
        3. Compare your clustering results with the actual categories
        4. Calculate clustering accuracy/purity
        5. Visualize the original data points and cluster assignments
        6. Create a simple evaluation report
        
        **Save all plots to**: `/Users/samueltorres/Documents/Repos/apps/multi-agent-immuno-research/evals/outputs/coder/plots/`
        """,
        task_type="algorithm",
        difficulty="medium",
        expected_deliverables="K-means clustering implementation with data parsing, accuracy evaluation, and visualization",
        sample_data="""x,y,category
2.1,3.4,A
2.5,3.1,A
1.8,3.7,A
8.2,7.9,B
8.5,8.1,B
7.9,7.6,B
5.1,5.2,C
5.3,4.9,C
4.8,5.4,C
1.2,8.9,D
1.5,9.1,D
1.1,8.7,D""",
        success_criteria=[
            "Parses CSV data from text correctly",
            "Implements K-means algorithm from scratch",
            "Compares clustering with actual categories",
            "Calculates clustering accuracy metrics",
            "Creates visualization of clusters",
            "Generates evaluation report",
            "Saves plots to specified directory path"
        ]
    )
]

# Debugging and Error Handling Cases
DEBUGGING_CASES = [
    CoderTestCase(
        id="debugging_001",
        task_description="""
        Debug and fix the following problematic Python code that's supposed to analyze exam scores 
        from the dataset provided below:

        Dataset:
        ```
        student_id,name,score
        1,Alice,85
        2,Bob,92
        3,Carol,78
        4,David,88
        5,Eve,95
        6,Frank,82
        7,Grace,89
        8,Henry,76
        9,Ivy,93
        10,Jack,87
        ```
        
        Problematic code to debug:
        ```python
        import pandas as pd
        
        def analyze_scores(data_text):
            data = pd.read_csv(data_text)
            average = data['score'].mean()
            max_score = data['score'].max()
            min_score = data['score'].min()
            
            # Calculate grade distribution
            grades = []
            for score in data['score']:
                if score >= 90:
                    grades.append('A')
                elif score >= 80:
                    grades.append('B')
                elif score >= 70:
                    grades.append('C')
                elif score >= 60:
                    grades.append('D')
                else:
                    grades.append('F')
            
            data['grade'] = grades
            
            # Group by grade
            grade_counts = data.groupby('grade').size()
            
            return {
                'average': average,
                'max': max_score,
                'min': min_score,
                'grade_distribution': grade_counts
            }
        
        # Test the function
        scores_data = '''student_id,name,score
        1,Alice,85
        2,Bob,92
        3,Carol,78
        4,David,88
        5,Eve,95
        6,Frank,82
        7,Grace,89
        8,Henry,76
        9,Ivy,93
        10,Jack,87'''
        
        result = analyze_scores(scores_data)
        print(result)
        ```
        
        Tasks:
        1. Identify and fix all issues in the code
        2. Add proper error handling
        3. Improve the code structure
        4. Test the corrected function with the provided data
        """,
        task_type="debugging",
        difficulty="easy",
        expected_deliverables="Debugged and improved code with error handling and best practices",
        sample_data="""student_id,name,score
1,Alice,85
2,Bob,92
3,Carol,78
4,David,88
5,Eve,95
6,Frank,82
7,Grace,89
8,Henry,76
9,Ivy,93
10,Jack,87""",
        success_criteria=[
            "Identifies syntax/logic errors",
            "Fixes CSV parsing from text",
            "Handles missing/invalid data",
            "Improves code structure",
            "Adds comprehensive error handling",
            "Tests the corrected function"
        ]
    )
]

# Combine all test cases
ALL_CODER_TEST_CASES = (
    DATA_ANALYSIS_CASES + 
    VISUALIZATION_CASES + 
    DATA_PROCESSING_CASES + 
    ALGORITHM_CASES + 
    DEBUGGING_CASES
)


def get_test_cases_by_type(task_type: str) -> List[CoderTestCase]:
    """Get test cases filtered by task type."""
    return [case for case in ALL_CODER_TEST_CASES if case.task_type == task_type]


def get_test_cases_by_difficulty(difficulty: str) -> List[CoderTestCase]:
    """Get test cases filtered by difficulty level."""
    return [case for case in ALL_CODER_TEST_CASES if case.difficulty == difficulty]


def get_test_case_by_id(test_id: str) -> Optional[CoderTestCase]:
    """Get a specific test case by ID."""
    for case in ALL_CODER_TEST_CASES:
        if case.id == test_id:
            return case
    return None


def get_dataset_summary() -> Dict[str, Any]:
    """Get summary statistics about the test dataset."""
    total_cases = len(ALL_CODER_TEST_CASES)
    
    # Count by type
    type_counts = {}
    for case in ALL_CODER_TEST_CASES:
        type_counts[case.task_type] = type_counts.get(case.task_type, 0) + 1
    
    # Count by difficulty
    difficulty_counts = {}
    for case in ALL_CODER_TEST_CASES:
        difficulty_counts[case.difficulty] = difficulty_counts.get(case.difficulty, 0) + 1
    
    return {
        "total_test_cases": total_cases,
        "by_task_type": type_counts,
        "by_difficulty": difficulty_counts,
        "test_case_ids": [case.id for case in ALL_CODER_TEST_CASES]
    }


if __name__ == "__main__":
    # Print dataset summary
    summary = get_dataset_summary()
    print("Coder Agent Test Dataset Summary:")
    print(f"Total test cases: {summary['total_test_cases']}")
    print(f"By task type: {summary['by_task_type']}")
    print(f"By difficulty: {summary['by_difficulty']}")
    print(f"Test case IDs: {summary['test_case_ids']}") 