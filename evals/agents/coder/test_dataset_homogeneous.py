"""
Homogeneous Difficulty Test Dataset for Coder Agent Evaluation

This dataset provides test cases with consistent medium-level difficulty
for more reliable and fair evaluation across different task types.
All test cases are designed to be challenging but achievable within
similar time constraints and complexity levels.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum


class TaskType(Enum):
    DATA_ANALYSIS = "data_analysis"
    VISUALIZATION = "visualization"
    DATA_PROCESSING = "data_processing"
    ALGORITHM = "algorithm"
    DEBUGGING = "debugging"
    STATISTICAL_TESTING = "statistical_testing"


class Difficulty(Enum):
    MEDIUM = "medium"


@dataclass
class CoderTestCase:
    """Represents a single test case for the coder agent."""
    id: str
    task_description: str
    task_type: str
    difficulty: str
    expected_deliverables: str
    sample_data: Optional[str] = None
    success_criteria: List[str] = None

    def __post_init__(self):
        if self.success_criteria is None:
            self.success_criteria = []


# Data Analysis Test Cases (Medium Difficulty)
DATA_ANALYSIS_CASES = [
    CoderTestCase(
        id="data_analysis_h001",
        task_description="""
        Analyze this customer transaction dataset to identify spending patterns and customer segments:

        ```
        customer_id,age,income,transaction_amount,category,date
        C001,28,45000,89.50,electronics,2024-01-15
        C002,34,67000,125.75,clothing,2024-01-16
        C003,22,38000,56.25,food,2024-01-17
        C004,41,82000,210.00,electronics,2024-01-18
        C005,29,52000,77.80,food,2024-01-19
        C006,55,95000,320.50,clothing,2024-01-20
        C007,31,48000,65.30,food,2024-01-21
        C008,26,41000,42.75,electronics,2024-01-22
        C009,38,71000,185.25,clothing,2024-01-23
        C010,33,59000,110.40,electronics,2024-01-24
        C011,24,36000,34.60,food,2024-01-25
        C012,47,88000,275.80,clothing,2024-01-26
        C013,30,54000,98.25,electronics,2024-01-27
        C014,39,63000,142.75,clothing,2024-01-28
        C015,27,44000,69.50,food,2024-01-29
        ```
        
        Tasks:
        1. Parse the CSV data and perform basic data validation
        2. Calculate average transaction amount by category and age group
        3. Identify the top 3 customers by total spending
        4. Analyze correlation between income and transaction amounts
        5. Create customer segments based on spending behavior
        6. Generate summary statistics report
        """,
        task_type="data_analysis",
        difficulty="medium",
        expected_deliverables="Data analysis with customer segmentation, correlations, and summary statistics",
        sample_data="""customer_id,age,income,transaction_amount,category,date
C001,28,45000,89.50,electronics,2024-01-15
C002,34,67000,125.75,clothing,2024-01-16
C003,22,38000,56.25,food,2024-01-17
C004,41,82000,210.00,electronics,2024-01-18
C005,29,52000,77.80,food,2024-01-19
C006,55,95000,320.50,clothing,2024-01-20
C007,31,48000,65.30,food,2024-01-21
C008,26,41000,42.75,electronics,2024-01-22
C009,38,71000,185.25,clothing,2024-01-23
C010,33,59000,110.40,electronics,2024-01-24
C011,24,36000,34.60,food,2024-01-25
C012,47,88000,275.80,clothing,2024-01-26
C013,30,54000,98.25,electronics,2024-01-27
C014,39,63000,142.75,clothing,2024-01-28
C015,27,44000,69.50,food,2024-01-29""",
        success_criteria=[
            "Parses CSV data correctly",
            "Calculates category and age group averages",
            "Identifies top customers accurately",
            "Analyzes income-spending correlation",
            "Creates meaningful customer segments",
            "Generates comprehensive summary"
        ]
    ),

    CoderTestCase(
        id="data_analysis_h002",
        task_description="""
        Analyze this employee performance dataset to understand productivity patterns:

        ```
        employee_id,department,years_experience,performance_score,projects_completed,hours_worked
        E001,Engineering,3,85,12,2080
        E002,Marketing,5,92,8,1920
        E003,Sales,2,78,15,2200
        E004,Engineering,7,94,18,2000
        E005,HR,4,88,6,1800
        E006,Marketing,6,91,10,1950
        E007,Sales,1,72,9,2100
        E008,Engineering,8,96,22,2050
        E009,HR,3,84,5,1850
        E010,Marketing,4,89,9,1900
        E011,Sales,5,86,18,2150
        E012,Engineering,2,81,8,2000
        E013,HR,6,93,7,1820
        E014,Marketing,3,87,7,1940
        E015,Sales,4,83,14,2120
        ```
        
        Tasks:
        1. Calculate average performance score by department
        2. Analyze relationship between experience and performance
        3. Determine productivity metrics (projects per hour)
        4. Identify high and low performers in each department
        5. Calculate department efficiency comparisons
        6. Generate performance insights and recommendations
        """,
        task_type="data_analysis",
        difficulty="medium",
        expected_deliverables="Employee performance analysis with department comparisons and productivity metrics",
        sample_data="""employee_id,department,years_experience,performance_score,projects_completed,hours_worked
E001,Engineering,3,85,12,2080
E002,Marketing,5,92,8,1920
E003,Sales,2,78,15,2200
E004,Engineering,7,94,18,2000
E005,HR,4,88,6,1800
E006,Marketing,6,91,10,1950
E007,Sales,1,72,9,2100
E008,Engineering,8,96,22,2050
E009,HR,3,84,5,1850
E010,Marketing,4,89,9,1900
E011,Sales,5,86,18,2150
E012,Engineering,2,81,8,2000
E013,HR,6,93,7,1820
E014,Marketing,3,87,7,1940
E015,Sales,4,83,14,2120""",
        success_criteria=[
            "Calculates department averages correctly",
            "Analyzes experience-performance relationship",
            "Computes productivity metrics accurately",
            "Identifies performance outliers",
            "Compares department efficiency",
            "Provides actionable insights"
        ]
    ),

    CoderTestCase(
        id="data_analysis_h003",
        task_description="""
        Analyze this website traffic dataset to understand user behavior patterns:

        ```
        date,page_views,unique_visitors,bounce_rate,avg_session_duration,conversion_rate,traffic_source
        2024-01-01,1250,890,0.45,180,0.03,organic
        2024-01-02,1380,920,0.42,195,0.035,social
        2024-01-03,1120,780,0.48,165,0.025,direct
        2024-01-04,1450,980,0.40,210,0.04,organic
        2024-01-05,1680,1100,0.38,225,0.045,paid
        2024-01-06,1890,1250,0.35,240,0.05,social
        2024-01-07,1340,920,0.43,185,0.032,direct
        2024-01-08,1520,1020,0.41,200,0.038,organic
        2024-01-09,1750,1150,0.37,230,0.047,paid
        2024-01-10,1420,950,0.44,190,0.034,social
        2024-01-11,1290,880,0.46,175,0.028,direct
        2024-01-12,1610,1080,0.39,215,0.042,organic
        2024-01-13,1830,1200,0.36,235,0.048,paid
        2024-01-14,1470,990,0.43,195,0.036,social
        2024-01-15,1350,910,0.45,180,0.031,direct
        ```
        
        Tasks:
        1. Calculate daily growth rates for key metrics
        2. Analyze performance by traffic source
        3. Identify correlation between bounce rate and conversion
        4. Calculate weekend vs weekday performance differences
        5. Determine the most effective traffic sources
        6. Generate actionable marketing insights
        """,
        task_type="data_analysis",
        difficulty="medium",
        expected_deliverables="Website analytics with traffic source analysis and performance insights",
        sample_data="""date,page_views,unique_visitors,bounce_rate,avg_session_duration,conversion_rate,traffic_source
2024-01-01,1250,890,0.45,180,0.03,organic
2024-01-02,1380,920,0.42,195,0.035,social
2024-01-03,1120,780,0.48,165,0.025,direct
2024-01-04,1450,980,0.40,210,0.04,organic
2024-01-05,1680,1100,0.38,225,0.045,paid
2024-01-06,1890,1250,0.35,240,0.05,social
2024-01-07,1340,920,0.43,185,0.032,direct
2024-01-08,1520,1020,0.41,200,0.038,organic
2024-01-09,1750,1150,0.37,230,0.047,paid
2024-01-10,1420,950,0.44,190,0.034,social
2024-01-11,1290,880,0.46,175,0.028,direct
2024-01-12,1610,1080,0.39,215,0.042,organic
2024-01-13,1830,1200,0.36,235,0.048,paid
2024-01-14,1470,990,0.43,195,0.036,social
2024-01-15,1350,910,0.45,180,0.031,direct""",
        success_criteria=[
            "Calculates growth rates accurately",
            "Analyzes traffic source performance",
            "Identifies metric correlations",
            "Compares weekday vs weekend patterns",
            "Ranks traffic source effectiveness",
            "Provides marketing recommendations"
        ]
    ),

    CoderTestCase(
        id="data_analysis_h004",
        task_description="""
        Analyze this inventory management dataset to optimize stock levels:

        ```
        product_id,category,current_stock,reorder_point,monthly_sales,unit_cost,selling_price
        P001,Electronics,45,20,38,25.50,45.99
        P002,Clothing,120,50,85,15.25,29.99
        P003,Books,78,30,42,8.75,19.95
        P004,Electronics,23,25,55,45.00,89.99
        P005,Home,67,40,33,12.50,24.99
        P006,Clothing,156,60,92,18.75,39.99
        P007,Books,89,35,48,6.25,14.95
        P008,Electronics,12,15,72,35.25,69.99
        P009,Home,134,70,56,22.00,44.99
        P010,Clothing,98,45,67,20.50,42.99
        P011,Books,145,50,38,9.50,21.95
        P012,Electronics,67,30,41,28.75,55.99
        P013,Home,89,55,29,16.25,32.99
        P014,Clothing,178,80,78,14.00,27.99
        P015,Books,112,40,52,7.50,17.95
        ```
        
        Tasks:
        1. Identify products at or below reorder points
        2. Calculate inventory turnover rates by category
        3. Analyze profit margins for each product
        4. Determine optimal stock levels based on sales velocity
        5. Identify slow-moving and fast-moving inventory
        6. Generate inventory optimization recommendations
        """,
        task_type="data_analysis",
        difficulty="medium",
        expected_deliverables="Inventory analysis with turnover rates, profit margins, and optimization recommendations",
        sample_data="""product_id,category,current_stock,reorder_point,monthly_sales,unit_cost,selling_price
P001,Electronics,45,20,38,25.50,45.99
P002,Clothing,120,50,85,15.25,29.99
P003,Books,78,30,42,8.75,19.95
P004,Electronics,23,25,55,45.00,89.99
P005,Home,67,40,33,12.50,24.99
P006,Clothing,156,60,92,18.75,39.99
P007,Books,89,35,48,6.25,14.95
P008,Electronics,12,15,72,35.25,69.99
P009,Home,134,70,56,22.00,44.99
P010,Clothing,98,45,67,20.50,42.99
P011,Books,145,50,38,9.50,21.95
P012,Electronics,67,30,41,28.75,55.99
P013,Home,89,55,29,16.25,32.99
P014,Clothing,178,80,78,14.00,27.99
P015,Books,112,40,52,7.50,17.95""",
        success_criteria=[
            "Identifies reorder alerts correctly",
            "Calculates turnover rates by category",
            "Computes profit margins accurately",
            "Determines optimal stock levels",
            "Classifies inventory movement speed",
            "Provides optimization recommendations"
        ]
    ),

    CoderTestCase(
        id="data_analysis_h005",
        task_description="""
        Analyze this educational assessment dataset to understand student performance:

        ```
        student_id,grade_level,math_score,reading_score,science_score,attendance_rate,study_hours_per_week
        S001,9,78,82,75,0.95,12
        S002,10,85,88,83,0.92,15
        S003,9,72,79,70,0.88,8
        S004,11,92,94,89,0.97,18
        S005,10,81,85,78,0.90,13
        S006,9,69,74,68,0.85,7
        S007,11,88,91,86,0.94,16
        S008,10,76,80,74,0.89,10
        S009,9,84,87,82,0.93,14
        S010,11,95,97,92,0.98,20
        S011,10,79,83,77,0.91,11
        S012,9,73,77,71,0.87,9
        S013,11,89,92,87,0.96,17
        S014,10,82,86,80,0.93,12
        S015,9,77,81,76,0.90,10
        ```
        
        Tasks:
        1. Calculate average scores by grade level and subject
        2. Analyze correlation between study hours and performance
        3. Identify the impact of attendance on academic achievement
        4. Determine top and bottom performers in each grade
        5. Calculate overall academic performance index
        6. Generate educational insights and recommendations
        """,
        task_type="data_analysis",
        difficulty="medium",
        expected_deliverables="Educational analysis with performance correlations and academic insights",
        sample_data="""student_id,grade_level,math_score,reading_score,science_score,attendance_rate,study_hours_per_week
S001,9,78,82,75,0.95,12
S002,10,85,88,83,0.92,15
S003,9,72,79,70,0.88,8
S004,11,92,94,89,0.97,18
S005,10,81,85,78,0.90,13
S006,9,69,74,68,0.85,7
S007,11,88,91,86,0.94,16
S008,10,76,80,74,0.89,10
S009,9,84,87,82,0.93,14
S010,11,95,97,92,0.98,20
S011,10,79,83,77,0.91,11
S012,9,73,77,71,0.87,9
S013,11,89,92,87,0.96,17
S014,10,82,86,80,0.93,12
S015,9,77,81,76,0.90,10""",
        success_criteria=[
            "Calculates grade-level averages correctly",
            "Analyzes study hours correlation",
            "Evaluates attendance impact",
            "Identifies performance outliers",
            "Creates performance index",
            "Provides educational recommendations"
        ]
    )
]

# Visualization Test Cases (Medium Difficulty)
VISUALIZATION_CASES = [
    CoderTestCase(
        id="visualization_h001",
        task_description="""
        Create visualizations for this sales performance dataset:

        ```
        month,region,sales_amount,target_amount,sales_rep,product_line
        Jan,North,125000,120000,Smith,Electronics
        Jan,South,98000,100000,Johnson,Electronics
        Jan,East,142000,135000,Williams,Electronics
        Jan,West,108000,110000,Brown,Electronics
        Feb,North,135000,125000,Smith,Electronics
        Feb,South,105000,105000,Johnson,Electronics
        Feb,East,155000,140000,Williams,Electronics
        Feb,West,118000,115000,Brown,Electronics
        Mar,North,148000,130000,Smith,Electronics
        Mar,South,112000,110000,Johnson,Electronics
        Mar,East,168000,145000,Williams,Electronics
        Mar,West,125000,120000,Brown,Electronics
        ```
        
        Create these visualizations:
        1. Bar chart comparing actual vs target sales by region
        2. Line chart showing monthly sales trends by region
        3. Pie chart of total sales distribution by region
        4. Grouped bar chart of sales performance by month and region
        5. Calculate and display achievement rates (actual/target)
        
        **Save all plots to**: `/Users/samueltorres/Documents/Repos/apps/multi-agent-immuno-research/evals/outputs/coder/plots/`
        """,
        task_type="visualization",
        difficulty="medium",
        expected_deliverables="Multiple sales performance charts with clear labels and professional formatting",
        sample_data="""month,region,sales_amount,target_amount,sales_rep,product_line
Jan,North,125000,120000,Smith,Electronics
Jan,South,98000,100000,Johnson,Electronics
Jan,East,142000,135000,Williams,Electronics
Jan,West,108000,110000,Brown,Electronics
Feb,North,135000,125000,Smith,Electronics
Feb,South,105000,105000,Johnson,Electronics
Feb,East,155000,140000,Williams,Electronics
Feb,West,118000,115000,Brown,Electronics
Mar,North,148000,130000,Smith,Electronics
Mar,South,112000,110000,Johnson,Electronics
Mar,East,168000,145000,Williams,Electronics
Mar,West,125000,120000,Brown,Electronics""",
        success_criteria=[
            "Creates accurate bar charts",
            "Generates clear line charts",
            "Makes informative pie charts",
            "Shows grouped comparisons",
            "Calculates achievement rates",
            "Saves plots to specified directory"
        ]
    ),

    CoderTestCase(
        id="visualization_h002",
        task_description="""
        Create statistical visualizations for this survey response dataset:

        ```
        respondent_id,age_group,satisfaction_score,usage_frequency,recommendation_score,category
        R001,18-25,7,Daily,8,Student
        R002,26-35,8,Weekly,9,Professional
        R003,36-45,6,Monthly,6,Parent
        R004,46-55,9,Daily,10,Professional
        R005,18-25,5,Weekly,5,Student
        R006,26-35,8,Daily,8,Professional
        R007,36-45,7,Monthly,7,Parent
        R008,46-55,9,Weekly,9,Professional
        R009,18-25,6,Daily,6,Student
        R010,26-35,8,Weekly,8,Professional
        R011,36-45,7,Monthly,7,Parent
        R012,46-55,8,Daily,9,Professional
        R013,18-25,7,Weekly,7,Student
        R014,26-35,9,Daily,9,Professional
        R015,36-45,6,Monthly,6,Parent
        ```
        
        Create these visualizations:
        1. Box plots of satisfaction scores by age group
        2. Scatter plot of satisfaction vs recommendation scores
        3. Histogram of satisfaction score distribution
        4. Stacked bar chart of usage frequency by category
        5. Correlation heatmap of numerical variables
        
        **Save all plots to**: `/Users/samueltorres/Documents/Repos/apps/multi-agent-immuno-research/evals/outputs/coder/plots/`
        """,
        task_type="visualization",
        difficulty="medium",
        expected_deliverables="Statistical visualizations with proper formatting and insights",
        sample_data="""respondent_id,age_group,satisfaction_score,usage_frequency,recommendation_score,category
R001,18-25,7,Daily,8,Student
R002,26-35,8,Weekly,9,Professional
R003,36-45,6,Monthly,6,Parent
R004,46-55,9,Daily,10,Professional
R005,18-25,5,Weekly,5,Student
R006,26-35,8,Daily,8,Professional
R007,36-45,7,Monthly,7,Parent
R008,46-55,9,Weekly,9,Professional
R009,18-25,6,Daily,6,Student
R010,26-35,8,Weekly,8,Professional
R011,36-45,7,Monthly,7,Parent
R012,46-55,8,Daily,9,Professional
R013,18-25,7,Weekly,7,Student
R014,26-35,9,Daily,9,Professional
R015,36-45,6,Monthly,6,Parent""",
        success_criteria=[
            "Creates informative box plots",
            "Generates meaningful scatter plots",
            "Shows distribution histograms",
            "Makes stacked bar charts",
            "Creates correlation heatmaps",
            "Saves plots to specified directory"
        ]
    ),

    CoderTestCase(
        id="visualization_h003",
        task_description="""
        Create financial analysis visualizations for this portfolio dataset:

        ```
        date,asset_type,symbol,price,volume,market_cap,sector
        2024-01-01,Stock,AAPL,185.50,45000000,2850000000000,Technology
        2024-01-01,Stock,MSFT,375.25,28000000,2780000000000,Technology
        2024-01-01,Stock,GOOGL,142.75,32000000,1800000000000,Technology
        2024-01-01,Stock,AMZN,155.80,41000000,1650000000000,Consumer
        2024-01-01,Stock,TSLA,248.90,85000000,780000000000,Automotive
        2024-01-02,Stock,AAPL,187.20,42000000,2875000000000,Technology
        2024-01-02,Stock,MSFT,378.50,26000000,2800000000000,Technology
        2024-01-02,Stock,GOOGL,144.25,30000000,1820000000000,Technology
        2024-01-02,Stock,AMZN,158.30,39000000,1680000000000,Consumer
        2024-01-02,Stock,TSLA,251.40,82000000,795000000000,Automotive
        2024-01-03,Stock,AAPL,189.75,38000000,2920000000000,Technology
        2024-01-03,Stock,MSFT,382.10,24000000,2830000000000,Technology
        2024-01-03,Stock,GOOGL,146.80,28000000,1850000000000,Technology
        2024-01-03,Stock,AMZN,161.25,37000000,1710000000000,Consumer
        2024-01-03,Stock,TSLA,254.20,79000000,810000000000,Automotive
        ```
        
        Create these visualizations:
        1. Candlestick chart showing price movements
        2. Volume analysis by sector
        3. Market cap comparison chart
        4. Daily price change percentage chart
        5. Sector performance comparison
        
        **Save all plots to**: `/Users/samueltorres/Documents/Repos/apps/multi-agent-immuno-research/evals/outputs/coder/plots/`
        """,
        task_type="visualization",
        difficulty="medium",
        expected_deliverables="Financial charts with technical analysis and sector comparisons",
        sample_data="""date,asset_type,symbol,price,volume,market_cap,sector
2024-01-01,Stock,AAPL,185.50,45000000,2850000000000,Technology
2024-01-01,Stock,MSFT,375.25,28000000,2780000000000,Technology
2024-01-01,Stock,GOOGL,142.75,32000000,1800000000000,Technology
2024-01-01,Stock,AMZN,155.80,41000000,1650000000000,Consumer
2024-01-01,Stock,TSLA,248.90,85000000,780000000000,Automotive
2024-01-02,Stock,AAPL,187.20,42000000,2875000000000,Technology
2024-01-02,Stock,MSFT,378.50,26000000,2800000000000,Technology
2024-01-02,Stock,GOOGL,144.25,30000000,1820000000000,Technology
2024-01-02,Stock,AMZN,158.30,39000000,1680000000000,Consumer
2024-01-02,Stock,TSLA,251.40,82000000,795000000000,Automotive
2024-01-03,Stock,AAPL,189.75,38000000,2920000000000,Technology
2024-01-03,Stock,MSFT,382.10,24000000,2830000000000,Technology
2024-01-03,Stock,GOOGL,146.80,28000000,1850000000000,Technology
2024-01-03,Stock,AMZN,161.25,37000000,1710000000000,Consumer
2024-01-03,Stock,TSLA,254.20,79000000,810000000000,Automotive""",
        success_criteria=[
            "Creates price movement charts",
            "Analyzes volume by sector",
            "Compares market capitalizations",
            "Shows price change percentages",
            "Compares sector performance",
            "Saves plots to specified directory"
        ]
    )
]

# Data Processing Test Cases (Medium Difficulty)
DATA_PROCESSING_CASES = [
    CoderTestCase(
        id="data_processing_h001",
        task_description="""
        Clean and process this messy customer dataset:

        ```
        customer_name,email,phone,registration_date,status,purchase_amount
        John Smith,john.smith@email.com,555-123-4567,2024-01-15,active,125.50
        jane doe,JANE.DOE@EMAIL.COM,5551234568,2024/01/16,Active,89.75
        Bob Johnson,bob@email,555.123.4569,01-17-2024,inactive,0
        Alice Brown,alice.brown@email.com,555-123-4570,2024-01-18,ACTIVE,245.25
        charlie wilson,,555 123 4571,2024-01-19,active,67.80
        Diana Davis,diana.davis@email.com,555-123-4572,2024-01-20,suspended,156.90
        Eve Miller,eve.miller@email.com,555-123-4573,2024-01-21,active,
        Frank Moore,frank.moore@email.com,555-123-4574,2024-01-22,Active,198.45
        Grace Taylor,grace.taylor@email.com,555-123-4575,2024-01-23,inactive,78.30
        Henry Wilson,henry.wilson@email.com,555-123-4576,2024-01-24,active,234.70
        ```
        
        Tasks:
        1. Standardize name formatting (proper case)
        2. Clean and validate email addresses
        3. Standardize phone number format
        4. Parse and standardize date formats
        5. Normalize status values
        6. Handle missing values appropriately
        7. Validate and clean purchase amounts
        8. Generate data quality report
        """,
        task_type="data_processing",
        difficulty="medium",
        expected_deliverables="Cleaned dataset with standardized formats and quality report",
        sample_data="""customer_name,email,phone,registration_date,status,purchase_amount
John Smith,john.smith@email.com,555-123-4567,2024-01-15,active,125.50
jane doe,JANE.DOE@EMAIL.COM,5551234568,2024/01/16,Active,89.75
Bob Johnson,bob@email,555.123.4569,01-17-2024,inactive,0
Alice Brown,alice.brown@email.com,555-123-4570,2024-01-18,ACTIVE,245.25
charlie wilson,,555 123 4571,2024-01-19,active,67.80
Diana Davis,diana.davis@email.com,555-123-4572,2024-01-20,suspended,156.90
Eve Miller,eve.miller@email.com,555-123-4573,2024-01-21,active,
Frank Moore,frank.moore@email.com,555-123-4574,2024-01-22,Active,198.45
Grace Taylor,grace.taylor@email.com,555-123-4575,2024-01-23,inactive,78.30
Henry Wilson,henry.wilson@email.com,555-123-4576,2024-01-24,active,234.70""",
        success_criteria=[
            "Standardizes name formatting",
            "Validates email addresses",
            "Formats phone numbers consistently",
            "Normalizes date formats",
            "Standardizes status values",
            "Handles missing data appropriately",
            "Validates purchase amounts",
            "Generates quality report"
        ]
    ),

    CoderTestCase(
        id="data_processing_h002",
        task_description="""
        Process and merge these product inventory datasets:

        ```
        # Dataset 1: Product Information
        product_id,name,category,brand,unit_price
        P001,Laptop Computer,Electronics,TechBrand,899.99
        P002,Office Chair,Furniture,ComfortCorp,249.50
        P003,Coffee Maker,Appliances,BrewMaster,89.99
        P004,Smartphone,Electronics,TechBrand,599.99
        P005,Desk Lamp,Furniture,LightCorp,45.75

        # Dataset 2: Inventory Levels
        product_code,warehouse_location,quantity_on_hand,last_updated
        P001,Warehouse A,25,2024-01-20
        P002,Warehouse B,45,2024-01-21
        P003,Warehouse A,67,2024-01-22
        P004,Warehouse C,12,2024-01-23
        P005,Warehouse B,89,2024-01-24

        # Dataset 3: Sales Data
        item_id,units_sold,sale_date,revenue
        P001,5,2024-01-25,4499.95
        P002,3,2024-01-26,748.50
        P003,8,2024-01-27,719.92
        P004,2,2024-01-28,1199.98
        P005,12,2024-01-29,549.00
        ```
        
        Tasks:
        1. Parse and validate all three datasets
        2. Standardize product identifiers across datasets
        3. Merge datasets on product ID
        4. Calculate inventory turnover rates
        5. Identify products with low stock levels
        6. Generate consolidated inventory report
        7. Flag data inconsistencies
        """,
        task_type="data_processing",
        difficulty="medium",
        expected_deliverables="Merged and processed inventory dataset with analysis",
        success_criteria=[
            "Parses all datasets correctly",
            "Standardizes product identifiers",
            "Merges datasets successfully",
            "Calculates turnover rates",
            "Identifies low stock items",
            "Generates consolidated report",
            "Flags data inconsistencies"
        ]
    ),

    CoderTestCase(
        id="data_processing_h003",
        task_description="""
        Process and analyze this time series sensor data:

        ```
        timestamp,sensor_id,temperature,humidity,pressure,status
        2024-01-01 00:00:00,S001,22.5,45.2,1013.25,normal
        2024-01-01 01:00:00,S001,22.8,44.8,1013.10,normal
        2024-01-01 02:00:00,S001,23.1,44.5,1012.95,normal
        2024-01-01 03:00:00,S001,999.9,44.2,1012.80,error
        2024-01-01 04:00:00,S001,23.7,43.9,1012.65,normal
        2024-01-01 05:00:00,S001,24.0,43.6,1012.50,normal
        2024-01-01 06:00:00,S001,24.3,43.3,1012.35,normal
        2024-01-01 07:00:00,S001,24.6,43.0,1012.20,normal
        2024-01-01 08:00:00,S001,24.9,42.7,-999.9,error
        2024-01-01 09:00:00,S001,25.2,42.4,1011.90,normal
        2024-01-01 10:00:00,S001,25.5,42.1,1011.75,normal
        2024-01-01 11:00:00,S001,25.8,41.8,1011.60,normal
        2024-01-01 12:00:00,S001,26.1,41.5,1011.45,normal
        2024-01-01 13:00:00,S001,26.4,41.2,1011.30,normal
        2024-01-01 14:00:00,S001,26.7,41.0,1011.15,normal
        ```
        
        Tasks:
        1. Parse timestamp data correctly
        2. Identify and handle sensor errors/outliers
        3. Interpolate missing or invalid readings
        4. Calculate rolling averages for each metric
        5. Detect anomalies in the data
        6. Generate data quality metrics
        7. Create processed time series dataset
        """,
        task_type="data_processing",
        difficulty="medium",
        expected_deliverables="Cleaned time series data with anomaly detection and quality metrics",
        sample_data="""timestamp,sensor_id,temperature,humidity,pressure,status
2024-01-01 00:00:00,S001,22.5,45.2,1013.25,normal
2024-01-01 01:00:00,S001,22.8,44.8,1013.10,normal
2024-01-01 02:00:00,S001,23.1,44.5,1012.95,normal
2024-01-01 03:00:00,S001,999.9,44.2,1012.80,error
2024-01-01 04:00:00,S001,23.7,43.9,1012.65,normal
2024-01-01 05:00:00,S001,24.0,43.6,1012.50,normal
2024-01-01 06:00:00,S001,24.3,43.3,1012.35,normal
2024-01-01 07:00:00,S001,24.6,43.0,1012.20,normal
2024-01-01 08:00:00,S001,24.9,42.7,-999.9,error
2024-01-01 09:00:00,S001,25.2,42.4,1011.90,normal
2024-01-01 10:00:00,S001,25.5,42.1,1011.75,normal
2024-01-01 11:00:00,S001,25.8,41.8,1011.60,normal
2024-01-01 12:00:00,S001,26.1,41.5,1011.45,normal
2024-01-01 13:00:00,S001,26.4,41.2,1011.30,normal
2024-01-01 14:00:00,S001,26.7,41.0,1011.15,normal""",
        success_criteria=[
            "Parses timestamps correctly",
            "Identifies sensor errors",
            "Interpolates invalid readings",
            "Calculates rolling averages",
            "Detects anomalies",
            "Generates quality metrics",
            "Creates clean dataset"
        ]
    )
]

# Algorithm Test Cases (Medium Difficulty)
ALGORITHM_CASES = [
    CoderTestCase(
        id="algorithm_h001",
        task_description="""
        Implement a recommendation system for this user-item rating dataset:

        ```
        user_id,item_id,rating,category,timestamp
        U001,I001,4.5,books,2024-01-01
        U001,I002,3.0,electronics,2024-01-02
        U001,I003,5.0,books,2024-01-03
        U002,I001,4.0,books,2024-01-04
        U002,I004,2.5,clothing,2024-01-05
        U003,I002,4.5,electronics,2024-01-06
        U003,I003,4.0,books,2024-01-07
        U003,I005,3.5,electronics,2024-01-08
        U004,I001,5.0,books,2024-01-09
        U004,I004,3.0,clothing,2024-01-10
        U004,I005,4.5,electronics,2024-01-11
        U005,I002,3.5,electronics,2024-01-12
        U005,I003,4.5,books,2024-01-13
        U005,I006,2.0,clothing,2024-01-14
        ```
        
        Tasks:
        1. Implement collaborative filtering algorithm
        2. Calculate user-user similarity matrix
        3. Calculate item-item similarity matrix
        4. Generate recommendations for each user
        5. Implement content-based filtering using categories
        6. Combine collaborative and content-based approaches
        7. Evaluate recommendation quality metrics
        """,
        task_type="algorithm",
        difficulty="medium",
        expected_deliverables="Recommendation system with multiple algorithms and evaluation metrics",
        sample_data="""user_id,item_id,rating,category,timestamp
U001,I001,4.5,books,2024-01-01
U001,I002,3.0,electronics,2024-01-02
U001,I003,5.0,books,2024-01-03
U002,I001,4.0,books,2024-01-04
U002,I004,2.5,clothing,2024-01-05
U003,I002,4.5,electronics,2024-01-06
U003,I003,4.0,books,2024-01-07
U003,I005,3.5,electronics,2024-01-08
U004,I001,5.0,books,2024-01-09
U004,I004,3.0,clothing,2024-01-10
U004,I005,4.5,electronics,2024-01-11
U005,I002,3.5,electronics,2024-01-12
U005,I003,4.5,books,2024-01-13
U005,I006,2.0,clothing,2024-01-14""",
        success_criteria=[
            "Implements collaborative filtering",
            "Calculates similarity matrices",
            "Generates user recommendations",
            "Implements content-based filtering",
            "Combines multiple approaches",
            "Evaluates recommendation quality"
        ]
    ),

    CoderTestCase(
        id="algorithm_h002",
        task_description="""
        Implement clustering algorithm for this customer segmentation dataset:

        ```
        customer_id,age,income,spending_score,frequency,recency_days
        C001,25,35000,65,12,5
        C002,32,50000,78,18,3
        C003,28,42000,45,8,15
        C004,45,75000,82,22,2
        C005,38,58000,55,10,12
        C006,29,48000,70,15,4
        C007,52,85000,88,25,1
        C008,26,38000,42,7,18
        C009,41,68000,75,20,3
        C010,33,52000,68,14,6
        C011,47,78000,85,24,2
        C012,30,45000,52,9,14
        C013,39,62000,72,17,5
        C014,27,40000,48,8,16
        C015,44,72000,80,21,3
        ```
        
        Tasks:
        1. Implement K-means clustering algorithm
        2. Determine optimal number of clusters using elbow method
        3. Implement hierarchical clustering
        4. Compare clustering results
        5. Create customer segment profiles
        6. Validate cluster quality using silhouette analysis
        7. Generate actionable business insights
        """,
        task_type="algorithm",
        difficulty="medium",
        expected_deliverables="Customer segmentation with multiple clustering algorithms and validation",
        sample_data="""customer_id,age,income,spending_score,frequency,recency_days
C001,25,35000,65,12,5
C002,32,50000,78,18,3
C003,28,42000,45,8,15
C004,45,75000,82,22,2
C005,38,58000,55,10,12
C006,29,48000,70,15,4
C007,52,85000,88,25,1
C008,26,38000,42,7,18
C009,41,68000,75,20,3
C010,33,52000,68,14,6
C011,47,78000,85,24,2
C012,30,45000,52,9,14
C013,39,62000,72,17,5
C014,27,40000,48,8,16
C015,44,72000,80,21,3""",
        success_criteria=[
            "Implements K-means clustering",
            "Determines optimal cluster count",
            "Implements hierarchical clustering",
            "Compares clustering results",
            "Creates segment profiles",
            "Validates cluster quality",
            "Provides business insights"
        ]
    ),

    CoderTestCase(
        id="algorithm_h003",
        task_description="""
        Implement optimization algorithm for this resource allocation problem:

        ```
        project_id,resource_requirement,expected_return,priority,duration_weeks
        P001,50000,75000,high,8
        P002,30000,45000,medium,6
        P003,80000,120000,high,12
        P004,25000,35000,low,4
        P005,60000,85000,high,10
        P006,40000,55000,medium,7
        P007,35000,50000,medium,5
        P008,70000,95000,high,9
        P009,20000,28000,low,3
        P010,45000,65000,medium,6
        
        # Constraints:
        total_budget = 300000
        max_projects = 6
        min_high_priority = 2
        max_duration = 8
        ```
        
        Tasks:
        1. Implement greedy algorithm for project selection
        2. Implement dynamic programming solution
        3. Implement genetic algorithm approach
        4. Compare algorithm performance
        5. Handle multiple constraints simultaneously
        6. Optimize for maximum ROI within constraints
        7. Generate allocation recommendations
        """,
        task_type="algorithm",
        difficulty="medium",
        expected_deliverables="Resource allocation optimization with multiple algorithms and constraint handling",
        success_criteria=[
            "Implements greedy algorithm",
            "Implements dynamic programming",
            "Implements genetic algorithm",
            "Compares algorithm performance",
            "Handles multiple constraints",
            "Optimizes ROI effectively",
            "Provides allocation recommendations"
        ]
    )
]

# Debugging Test Cases (Medium Difficulty)
DEBUGGING_CASES = [
    CoderTestCase(
        id="debugging_h001",
        task_description="""
        Debug this data analysis script that has multiple issues:

        ```python
        import pandas as pd
        import numpy as np
        
        def analyze_sales_data(data_string):
            # Parse CSV data
            lines = data_string.strip().split('\\n')
            headers = lines[0].split(',')
            data = []
            
            for line in lines[1:]:
                row = line.split(',')
                data.append(row)
            
            df = pd.DataFrame(data, columns=headers)
            
            # Convert numeric columns
            df['sales_amount'] = df['sales_amount'].astype(float)
            df['quantity'] = df['quantity'].astype(int)
            
            # Calculate total sales by region
            regional_sales = df.groupby('region')['sales_amount'].sum()
            
            # Calculate average sales per unit
            df['price_per_unit'] = df['sales_amount'] / df['quantity']
            
            # Find top performing products
            top_products = df.groupby('product')['sales_amount'].sum().sort_values(ascending=False).head(3)
            
            # Calculate monthly growth rate
            df['month'] = pd.to_datetime(df['date']).dt.month
            monthly_sales = df.groupby('month')['sales_amount'].sum()
            growth_rate = monthly_sales.pct_change() * 100
            
            return regional_sales, top_products, growth_rate
        
        # Test data
        sales_data = '''date,region,product,sales_amount,quantity
        2024-01-15,North,Widget A,1250.50,25
        2024-01-16,South,Widget B,980.75,0
        2024-02-17,East,Widget A,1450.25,30
        2024-02-18,West,Widget C,750.00,15
        2024-03-19,North,Widget B,1100.80,22'''
        
        result = analyze_sales_data(sales_data)
        print(result)
        ```
        
        Tasks:
        1. Identify all bugs in the code
        2. Fix data type conversion errors
        3. Handle division by zero errors
        4. Fix date parsing issues
        5. Correct grouping and aggregation logic
        6. Add proper error handling
        7. Improve code robustness and efficiency
        """,
        task_type="debugging",
        difficulty="medium",
        expected_deliverables="Debugged and improved data analysis script with proper error handling",
        success_criteria=[
            "Identifies all bugs correctly",
            "Fixes data type conversions",
            "Handles division by zero",
            "Fixes date parsing",
            "Corrects aggregation logic",
            "Adds error handling",
            "Improves code quality"
        ]
    ),

    CoderTestCase(
        id="debugging_h002",
        task_description="""
        Debug this machine learning pipeline with performance and accuracy issues:

        ```python
        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score, classification_report
        from sklearn.preprocessing import StandardScaler
        
        def train_model(data_string):
            # Load data
            df = pd.read_csv(data_string)
            
            # Prepare features and target
            X = df.drop('target', axis=1)
            y = df['target']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            model = LogisticRegression()
            model.fit(X_train_scaled, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test_scaled)
            
            # Evaluate
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred)
            
            return model, accuracy, report
        
        # Test with this data format issue
        test_data = '''feature1,feature2,feature3,target
        1.5,2.3,0.8,1
        2.1,1.9,1.2,0
        1.8,2.5,0.9,1
        2.3,1.7,1.4,0
        missing,2.1,1.0,1
        1.9,null,1.1,0
        2.0,2.2,0.7,1'''
        
        model, acc, report = train_model(test_data)
        print(f"Accuracy: {acc}")
        ```
        
        Tasks:
        1. Fix data loading issues
        2. Handle missing values properly
        3. Fix data type conversion problems
        4. Improve model performance
        5. Add cross-validation
        6. Fix evaluation metrics calculation
        7. Add proper preprocessing pipeline
        """,
        task_type="debugging",
        difficulty="medium",
        expected_deliverables="Fixed ML pipeline with proper data handling and improved performance",
        success_criteria=[
            "Fixes data loading",
            "Handles missing values",
            "Fixes data types",
            "Improves model performance",
            "Adds cross-validation",
            "Fixes evaluation metrics",
            "Improves preprocessing"
        ]
    )
]

# Statistical Testing Test Cases (Medium Difficulty)
STATISTICAL_TESTING_CASES = [
    CoderTestCase(
        id="statistical_testing_h001",
        task_description="""
        Perform comprehensive statistical analysis on this A/B testing dataset:

        ```
        user_id,group,conversion,revenue,session_duration,page_views
        U001,A,1,25.50,180,5
        U002,A,0,0.00,120,3
        U003,A,1,42.75,240,7
        U004,B,1,38.25,200,6
        U005,B,0,0.00,90,2
        U006,A,1,31.80,210,4
        U007,B,1,45.60,260,8
        U008,A,0,0.00,110,3
        U009,B,1,52.30,280,9
        U010,A,1,28.90,190,5
        U011,B,0,0.00,100,2
        U012,A,1,36.40,220,6
        U013,B,1,41.70,250,7
        U014,A,0,0.00,130,4
        U015,B,1,48.20,270,8
        ```
        
        Tasks:
        1. Perform two-sample t-test for conversion rates
        2. Test for significance in revenue differences
        3. Analyze session duration between groups
        4. Perform chi-square test for independence
        5. Calculate effect sizes and confidence intervals
        6. Test for normality assumptions
        7. Generate comprehensive statistical report
        """,
        task_type="statistical_testing",
        difficulty="medium",
        expected_deliverables="Complete A/B test analysis with statistical tests and interpretation",
        sample_data="""user_id,group,conversion,revenue,session_duration,page_views
U001,A,1,25.50,180,5
U002,A,0,0.00,120,3
U003,A,1,42.75,240,7
U004,B,1,38.25,200,6
U005,B,0,0.00,90,2
U006,A,1,31.80,210,4
U007,B,1,45.60,260,8
U008,A,0,0.00,110,3
U009,B,1,52.30,280,9
U010,A,1,28.90,190,5
U011,B,0,0.00,100,2
U012,A,1,36.40,220,6
U013,B,1,41.70,250,7
U014,A,0,0.00,130,4
U015,B,1,48.20,270,8""",
        success_criteria=[
            "Performs t-tests correctly",
            "Tests revenue differences",
            "Analyzes session duration",
            "Performs chi-square tests",
            "Calculates effect sizes",
            "Tests normality assumptions",
            "Generates comprehensive report"
        ]
    ),

    CoderTestCase(
        id="statistical_testing_h002",
        task_description="""
        Analyze this medical treatment effectiveness dataset:

        ```
        patient_id,treatment,age,baseline_score,followup_score,gender,comorbidities
        P001,Drug A,45,85,78,M,1
        P002,Drug A,52,82,75,F,0
        P003,Drug A,38,88,80,M,1
        P004,Drug B,41,84,72,F,1
        P005,Drug B,55,86,70,M,2
        P006,Placebo,48,83,82,F,0
        P007,Drug A,33,87,79,M,0
        P008,Drug B,46,85,68,F,1
        P009,Placebo,51,84,83,M,1
        P010,Drug A,39,86,77,F,0
        P011,Drug B,44,88,71,M,2
        P012,Placebo,42,85,84,F,0
        P013,Drug A,37,89,81,M,1
        P014,Drug B,49,87,69,F,1
        P015,Placebo,43,86,85,M,0
        ```
        
        Tasks:
        1. Perform ANOVA to compare treatment groups
        2. Conduct post-hoc pairwise comparisons
        3. Analyze treatment effect controlling for covariates (ANCOVA)
        4. Test for interaction effects (age, gender, comorbidities)
        5. Calculate treatment effect sizes
        6. Perform non-parametric alternatives if needed
        7. Generate clinical interpretation report
        """,
        task_type="statistical_testing",
        difficulty="medium",
        expected_deliverables="Medical treatment analysis with ANOVA, ANCOVA, and clinical interpretation",
        sample_data="""patient_id,treatment,age,baseline_score,followup_score,gender,comorbidities
P001,Drug A,45,85,78,M,1
P002,Drug A,52,82,75,F,0
P003,Drug A,38,88,80,M,1
P004,Drug B,41,84,72,F,1
P005,Drug B,55,86,70,M,2
P006,Placebo,48,83,82,F,0
P007,Drug A,33,87,79,M,0
P008,Drug B,46,85,68,F,1
P009,Placebo,51,84,83,M,1
P010,Drug A,39,86,77,F,0
P011,Drug B,44,88,71,M,2
P012,Placebo,42,85,84,F,0
P013,Drug A,37,89,81,M,1
P014,Drug B,49,87,69,F,1
P015,Placebo,43,86,85,M,0""",
        success_criteria=[
            "Performs ANOVA correctly",
            "Conducts post-hoc tests",
            "Analyzes with ANCOVA",
            "Tests interaction effects",
            "Calculates effect sizes",
            "Uses non-parametric tests when appropriate",
            "Provides clinical interpretation"
        ]
    ),

    CoderTestCase(
        id="statistical_testing_h003",
        task_description="""
        Perform quality control analysis on this manufacturing dataset:

        ```
        batch_id,machine,operator,measurement,specification_limit,temperature,humidity
        B001,M1,Op1,10.2,10.0,22.5,45
        B002,M1,Op2,9.8,10.0,22.8,46
        B003,M2,Op1,10.5,10.0,23.1,44
        B004,M2,Op3,9.9,10.0,22.7,45
        B005,M3,Op2,10.1,10.0,22.9,47
        B006,M1,Op1,10.3,10.0,23.0,45
        B007,M2,Op3,9.7,10.0,22.6,46
        B008,M3,Op1,10.4,10.0,23.2,44
        B009,M1,Op2,9.9,10.0,22.8,45
        B010,M2,Op1,10.0,10.0,22.9,46
        B011,M3,Op3,10.2,10.0,23.1,47
        B012,M1,Op1,9.8,10.0,22.7,45
        B013,M2,Op2,10.1,10.0,22.8,46
        B014,M3,Op1,10.3,10.0,23.0,44
        B015,M1,Op3,9.9,10.0,22.9,45
        ```
        
        Tasks:
        1. Test process capability (Cp, Cpk indices)
        2. Perform control chart analysis (X-bar, R charts)
        3. Test for differences between machines (ANOVA)
        4. Analyze operator effects
        5. Test correlation with environmental factors
        6. Identify out-of-control points
        7. Generate quality control recommendations
        """,
        task_type="statistical_testing",
        difficulty="medium",
        expected_deliverables="Quality control analysis with capability studies and control charts",
        sample_data="""batch_id,machine,operator,measurement,specification_limit,temperature,humidity
B001,M1,Op1,10.2,10.0,22.5,45
B002,M1,Op2,9.8,10.0,22.8,46
B003,M2,Op1,10.5,10.0,23.1,44
B004,M2,Op3,9.9,10.0,22.7,45
B005,M3,Op2,10.1,10.0,22.9,47
B006,M1,Op1,10.3,10.0,23.0,45
B007,M2,Op3,9.7,10.0,22.6,46
B008,M3,Op1,10.4,10.0,23.2,44
B009,M1,Op2,9.9,10.0,22.8,45
B010,M2,Op1,10.0,10.0,22.9,46
B011,M3,Op3,10.2,10.0,23.1,47
B012,M1,Op1,9.8,10.0,22.7,45
B013,M2,Op2,10.1,10.0,22.8,46
B014,M3,Op1,10.3,10.0,23.0,44
B015,M1,Op3,9.9,10.0,22.9,45""",
        success_criteria=[
            "Calculates capability indices",
            "Creates control charts",
            "Performs machine comparisons",
            "Analyzes operator effects",
            "Tests environmental correlations",
            "Identifies control violations",
            "Provides QC recommendations"
        ]
    )
]

# Combine all test cases
ALL_HOMOGENEOUS_TEST_CASES = (
    DATA_ANALYSIS_CASES + 
    VISUALIZATION_CASES +
    DATA_PROCESSING_CASES +
    ALGORITHM_CASES +
    DEBUGGING_CASES +
    STATISTICAL_TESTING_CASES
)

def get_homogeneous_summary():
    """Return summary of homogeneous test cases."""
    return {
        "Data Analysis": len(DATA_ANALYSIS_CASES),
        "Visualization": len(VISUALIZATION_CASES),
        "Data Processing": len(DATA_PROCESSING_CASES),
        "Algorithm": len(ALGORITHM_CASES),
        "Debugging": len(DEBUGGING_CASES),
        "Statistical Testing": len(STATISTICAL_TESTING_CASES),
        "Total": len(ALL_HOMOGENEOUS_TEST_CASES),
        "Difficulty": "All Medium",
        "Consistency": "Homogeneous complexity levels"
    } 