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
    ),

    CoderTestCase(
        id="data_analysis_003",
        task_description="""
        Perform exploratory data analysis on this clinical trial dataset with proper statistical validation:

        ```
        patient_id,age,gender,treatment_group,baseline_score,week_4_score,week_8_score,week_12_score,adverse_events
        P001,34,F,Treatment,45,52,58,65,0
        P002,28,M,Control,42,44,46,48,1
        P003,41,F,Treatment,38,48,55,62,0
        P004,35,M,Placebo,40,41,43,44,0
        P005,29,F,Control,47,49,51,53,1
        P006,52,M,Treatment,35,45,54,63,1
        P007,31,F,Placebo,44,45,46,47,0
        P008,38,M,Control,41,43,45,47,0
        P009,45,F,Treatment,39,50,57,64,0
        P010,33,M,Placebo,43,44,45,46,1
        P011,27,F,Control,46,48,50,52,0
        P012,39,M,Treatment,37,47,56,65,1
        P013,42,F,Placebo,41,42,43,44,0
        P014,36,M,Control,44,46,48,50,1
        P015,30,F,Treatment,40,51,59,66,0
        ```
        
        Requirements:
        1. Parse the CSV data and validate data integrity
        2. Calculate change from baseline for each time point
        3. Perform descriptive statistics by treatment group
        4. Analyze adverse event rates by group
        5. Test for baseline differences between groups
        6. Calculate effect sizes for treatment differences
        7. Create comprehensive summary with clinical interpretation
        """,
        task_type="data_analysis",
        difficulty="hard",
        expected_deliverables="Clinical data analysis with baseline comparisons, effect sizes, and statistical validation",
        sample_data="""patient_id,age,gender,treatment_group,baseline_score,week_4_score,week_8_score,week_12_score,adverse_events
P001,34,F,Treatment,45,52,58,65,0
P002,28,M,Control,42,44,46,48,1
P003,41,F,Treatment,38,48,55,62,0
P004,35,M,Placebo,40,41,43,44,0
P005,29,F,Control,47,49,51,53,1
P006,52,M,Treatment,35,45,54,63,1
P007,31,F,Placebo,44,45,46,47,0
P008,38,M,Control,41,43,45,47,0
P009,45,F,Treatment,39,50,57,64,0
P010,33,M,Placebo,43,44,45,46,1
P011,27,F,Control,46,48,50,52,0
P012,39,M,Treatment,37,47,56,65,1
P013,42,F,Placebo,41,42,43,44,0
P014,36,M,Control,44,46,48,50,1
P015,30,F,Treatment,40,51,59,66,0""",
        success_criteria=[
            "Validates data integrity and handles missing values",
            "Calculates change from baseline correctly",
            "Provides descriptive statistics by group",
            "Analyzes adverse event rates",
            "Tests baseline group differences",
            "Calculates meaningful effect sizes",
            "Provides clinical interpretation"
        ]
    ),

    CoderTestCase(
        id="data_analysis_004",
        task_description="""
        Perform comprehensive time series analysis on this environmental monitoring data:

        ```
        datetime,temperature,humidity,air_quality_index,rainfall,wind_speed,pressure
        2024-01-01 00:00,15.2,68,45,0.0,8.5,1013.2
        2024-01-01 06:00,14.8,72,48,0.2,7.2,1012.8
        2024-01-01 12:00,18.5,65,52,0.0,9.1,1013.5
        2024-01-01 18:00,16.3,69,49,0.1,8.8,1013.1
        2024-01-02 00:00,13.9,74,46,0.5,6.8,1012.5
        2024-01-02 06:00,13.2,76,44,0.8,6.2,1012.2
        2024-01-02 12:00,17.1,67,51,0.0,8.9,1013.8
        2024-01-02 18:00,15.8,70,48,0.3,8.1,1013.3
        2024-01-03 00:00,14.5,73,47,0.1,7.5,1012.9
        2024-01-03 06:00,14.0,75,45,0.4,7.0,1012.6
        2024-01-03 12:00,19.2,63,53,0.0,9.5,1014.1
        2024-01-03 18:00,17.4,66,50,0.0,9.2,1013.7
        2024-01-04 00:00,15.8,71,48,0.2,8.3,1013.0
        2024-01-04 06:00,15.1,73,46,0.6,7.8,1012.7
        2024-01-04 12:00,20.1,61,55,0.0,10.2,1014.4
        ```
        
        Analysis requirements:
        1. Parse datetime and validate temporal consistency
        2. Calculate daily aggregations (mean, min, max)
        3. Identify diurnal patterns for each variable
        4. Detect outliers using statistical methods
        5. Calculate cross-correlations between variables
        6. Perform trend analysis and seasonality detection
        7. Generate environmental quality assessment
        """,
        task_type="data_analysis",
        difficulty="hard",
        expected_deliverables="Time series analysis with trend detection, correlation analysis, and environmental assessment",
        sample_data="""datetime,temperature,humidity,air_quality_index,rainfall,wind_speed,pressure
2024-01-01 00:00,15.2,68,45,0.0,8.5,1013.2
2024-01-01 06:00,14.8,72,48,0.2,7.2,1012.8
2024-01-01 12:00,18.5,65,52,0.0,9.1,1013.5
2024-01-01 18:00,16.3,69,49,0.1,8.8,1013.1
2024-01-02 00:00,13.9,74,46,0.5,6.8,1012.5
2024-01-02 06:00,13.2,76,44,0.8,6.2,1012.2
2024-01-02 12:00,17.1,67,51,0.0,8.9,1013.8
2024-01-02 18:00,15.8,70,48,0.3,8.1,1013.3
2024-01-03 00:00,14.5,73,47,0.1,7.5,1012.9
2024-01-03 06:00,14.0,75,45,0.4,7.0,1012.6
2024-01-03 12:00,19.2,63,53,0.0,9.5,1014.1
2024-01-03 18:00,17.4,66,50,0.0,9.2,1013.7
2024-01-04 00:00,15.8,71,48,0.2,8.3,1013.0
2024-01-04 06:00,15.1,73,46,0.6,7.8,1012.7
2024-01-04 12:00,20.1,61,55,0.0,10.2,1014.4""",
        success_criteria=[
            "Correctly parses datetime and validates data",
            "Calculates daily aggregations accurately",
            "Identifies diurnal patterns",
            "Detects outliers using appropriate methods",
            "Calculates cross-correlations",
            "Performs trend and seasonality analysis",
            "Provides environmental quality assessment"
        ]
    ),

    CoderTestCase(
        id="data_analysis_005",
        task_description="""
        Analyze this A/B testing dataset with proper statistical rigor for business decision making:

        ```
        user_id,variant,conversion,revenue,session_duration,page_views,device_type
        U001,A,1,29.99,245,8,desktop
        U002,B,0,0.00,156,4,mobile
        U003,A,0,0.00,89,2,tablet
        U004,B,1,49.99,312,12,desktop
        U005,A,1,19.99,198,6,mobile
        U006,B,0,0.00,67,3,mobile
        U007,A,1,39.99,278,9,desktop
        U008,B,1,29.99,203,7,tablet
        U009,A,0,0.00,134,5,mobile
        U010,B,1,59.99,345,15,desktop
        U011,A,1,24.99,221,8,tablet
        U012,B,0,0.00,98,4,mobile
        U013,A,0,0.00,112,3,desktop
        U014,B,1,44.99,289,11,desktop
        U015,A,1,34.99,256,10,tablet
        U016,B,0,0.00,87,2,mobile
        U017,A,1,19.99,167,5,mobile
        U018,B,1,39.99,234,8,desktop
        U019,A,0,0.00,143,4,tablet
        U020,B,1,54.99,301,13,desktop
        ```
        
        Statistical analysis requirements:
        1. Calculate conversion rates with confidence intervals
        2. Perform statistical significance tests (z-test, chi-square)
        3. Calculate effect sizes and practical significance
        4. Analyze revenue per user and statistical significance
        5. Segment analysis by device type
        6. Power analysis for sample size adequacy
        7. Provide business recommendations with statistical backing
        """,
        task_type="data_analysis",
        difficulty="hard",
        expected_deliverables="A/B test analysis with statistical significance, effect sizes, and business recommendations",
        sample_data="""user_id,variant,conversion,revenue,session_duration,page_views,device_type
U001,A,1,29.99,245,8,desktop
U002,B,0,0.00,156,4,mobile
U003,A,0,0.00,89,2,tablet
U004,B,1,49.99,312,12,desktop
U005,A,1,19.99,198,6,mobile
U006,B,0,0.00,67,3,mobile
U007,A,1,39.99,278,9,desktop
U008,B,1,29.99,203,7,tablet
U009,A,0,0.00,134,5,mobile
U010,B,1,59.99,345,15,desktop
U011,A,1,24.99,221,8,tablet
U012,B,0,0.00,98,4,mobile
U013,A,0,0.00,112,3,desktop
U014,B,1,44.99,289,11,desktop
U015,A,1,34.99,256,10,tablet
U016,B,0,0.00,87,2,mobile
U017,A,1,19.99,167,5,mobile
U018,B,1,39.99,234,8,desktop
U019,A,0,0.00,143,4,tablet
U020,B,1,54.99,301,13,desktop""",
        success_criteria=[
            "Calculates conversion rates with confidence intervals",
            "Performs appropriate statistical tests",
            "Calculates effect sizes correctly",
            "Analyzes revenue differences statistically",
            "Provides device-type segmentation",
            "Conducts power analysis",
            "Gives actionable business recommendations"
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
    ),

    CoderTestCase(
        id="visualization_003",
        task_description="""
        Create advanced statistical visualizations for the following experimental data:

        ```
        treatment_group,measurement_1,measurement_2,measurement_3,subject_id,age,gender
        Control,23.5,45.2,67.8,1,25,M
        Control,24.1,44.8,66.9,2,28,F
        Control,22.9,46.1,68.2,3,31,M
        Control,23.8,45.5,67.5,4,26,F
        Control,24.2,44.9,67.1,5,29,M
        Treatment_A,26.7,48.3,72.1,6,27,F
        Treatment_A,27.2,49.1,73.4,7,30,M
        Treatment_A,26.1,47.8,71.8,8,24,F
        Treatment_A,27.8,49.5,74.2,9,32,M
        Treatment_A,26.4,48.7,72.6,10,28,F
        Treatment_B,29.3,52.1,78.9,11,29,M
        Treatment_B,30.1,53.4,80.2,12,26,F
        Treatment_B,28.8,51.7,78.1,13,33,M
        Treatment_B,29.7,52.8,79.5,14,27,F
        Treatment_B,30.4,53.1,80.8,15,31,M
        ```
        
        Create the following statistical visualizations:
        1. Parse the CSV data from the text above
        2. Box plots comparing measurements across treatment groups
        3. Violin plots showing distribution shapes for each treatment
        4. Pair plot matrix showing relationships between all measurements
        5. Strip plot with jitter showing individual data points by group
        6. Q-Q plots to test normality of measurements
        7. Distribution plots (histograms with KDE) for each measurement
        
        **Save all plots to**: `/Users/samueltorres/Documents/Repos/apps/multi-agent-immuno-research/evals/outputs/coder/plots/`
        """,
        task_type="visualization",
        difficulty="hard",
        expected_deliverables="Advanced statistical plots with proper distribution analysis and group comparisons",
        sample_data="""treatment_group,measurement_1,measurement_2,measurement_3,subject_id,age,gender
Control,23.5,45.2,67.8,1,25,M
Control,24.1,44.8,66.9,2,28,F
Control,22.9,46.1,68.2,3,31,M
Control,23.8,45.5,67.5,4,26,F
Control,24.2,44.9,67.1,5,29,M
Treatment_A,26.7,48.3,72.1,6,27,F
Treatment_A,27.2,49.1,73.4,7,30,M
Treatment_A,26.1,47.8,71.8,8,24,F
Treatment_A,27.8,49.5,74.2,9,32,M
Treatment_A,26.4,48.7,72.6,10,28,F
Treatment_B,29.3,52.1,78.9,11,29,M
Treatment_B,30.1,53.4,80.2,12,26,F
Treatment_B,28.8,51.7,78.1,13,33,M
Treatment_B,29.7,52.8,79.5,14,27,F
Treatment_B,30.4,53.1,80.8,15,31,M""",
        success_criteria=[
            "Parses CSV data from text correctly",
            "Creates box plots for group comparisons",
            "Generates violin plots showing distributions",
            "Makes pair plot matrix with correlations",
            "Creates strip plots with proper jittering",
            "Generates Q-Q plots for normality testing",
            "Creates distribution plots with KDE",
            "All plots have proper statistical interpretation",
            "Saves all plots to specified directory path"
        ]
    ),

    CoderTestCase(
        id="visualization_004",
        task_description="""
        Create time series visualizations with trend analysis for the following sales data:

        ```
        date,sales,marketing_spend,temperature,day_of_week,is_holiday
        2024-01-01,1250,500,32.1,1,1
        2024-01-02,1100,450,28.5,2,0
        2024-01-03,1350,600,35.2,3,0
        2024-01-04,1400,650,33.8,4,0
        2024-01-05,1200,480,29.7,5,0
        2024-01-06,1600,750,31.4,6,0
        2024-01-07,1800,800,34.6,7,0
        2024-01-08,1150,420,27.9,1,0
        2024-01-09,1250,550,30.2,2,0
        2024-01-10,1300,580,32.8,3,0
        2024-01-11,1450,680,35.1,4,0
        2024-01-12,1350,620,33.4,5,0
        2024-01-13,1700,780,31.8,6,0
        2024-01-14,1900,850,34.9,7,0
        2024-01-15,2200,950,36.2,1,1
        ```
        
        Create the following time series visualizations:
        1. Parse the CSV data from the text above
        2. Time series plot with sales trend line and confidence intervals
        3. Dual-axis plot showing sales vs marketing spend over time
        4. Seasonal decomposition plot (if patterns exist)
        5. Rolling average plot with different window sizes
        6. Autocorrelation and partial autocorrelation plots
        7. Residuals plot after trend removal
        
        **Note**: Create only static plots, no interactive visualizations.
        **Save all plots to**: `/Users/samueltorres/Documents/Repos/apps/multi-agent-immuno-research/evals/outputs/coder/plots/`
        """,
        task_type="visualization",
        difficulty="hard",
        expected_deliverables="Time series analysis plots with trend decomposition and statistical analysis",
        sample_data="""date,sales,marketing_spend,temperature,day_of_week,is_holiday
2024-01-01,1250,500,32.1,1,1
2024-01-02,1100,450,28.5,2,0
2024-01-03,1350,600,35.2,3,0
2024-01-04,1400,650,33.8,4,0
2024-01-05,1200,480,29.7,5,0
2024-01-06,1600,750,31.4,6,0
2024-01-07,1800,800,34.6,7,0
2024-01-08,1150,420,27.9,1,0
2024-01-09,1250,550,30.2,2,0
2024-01-10,1300,580,32.8,3,0
2024-01-11,1450,680,35.1,4,0
2024-01-12,1350,620,33.4,5,0
2024-01-13,1700,780,31.8,6,0
2024-01-14,1900,850,34.9,7,0
2024-01-15,2200,950,36.2,1,1""",
        success_criteria=[
            "Parses CSV data from text correctly",
            "Creates time series plot with trend analysis",
            "Generates dual-axis plots",
            "Shows rolling averages with multiple windows",
            "Creates autocorrelation plots",
            "Generates residuals analysis",
            "Uses proper time series formatting",
            "Creates only static plots (no interactive)",
            "Saves all plots to specified directory path"
        ]
    ),

    CoderTestCase(
        id="visualization_005",
        task_description="""
        Create scientific publication-quality plots for this gene expression analysis dataset:

        ```
        gene_id,control_expression,treatment_expression,log2_fold_change,p_value,gene_name,pathway
        GENE001,125.4,89.2,-0.49,0.023,APOE,Lipid metabolism
        GENE002,78.9,156.3,0.98,0.001,BRCA1,DNA repair
        GENE003,203.7,198.1,-0.04,0.856,TP53,Cell cycle
        GENE004,45.2,89.7,0.99,0.002,VEGFA,Angiogenesis
        GENE005,167.8,84.3,-0.99,0.001,MYC,Cell proliferation
        GENE006,92.1,91.8,-0.01,0.945,GAPDH,Glycolysis
        GENE007,134.5,268.9,1.00,0.000,EGFR,Signal transduction
        GENE008,56.7,28.4,-1.00,0.003,CDKN1A,Cell cycle
        GENE009,189.3,378.6,1.00,0.000,STAT3,Transcription
        GENE010,98.4,49.2,-1.00,0.001,PTEN,Tumor suppression
        GENE011,145.7,292.1,1.00,0.000,AKT1,Cell survival
        GENE012,67.8,33.9,-1.00,0.002,RB1,Cell cycle
        GENE013,156.2,312.4,1.00,0.000,PI3K,Signal transduction
        GENE014,89.6,44.8,-1.00,0.001,BAX,Apoptosis
        GENE015,178.9,357.8,1.00,0.000,MAPK,Signal transduction
        ```
        
        Create these publication-quality visualizations:
        1. Volcano plot (log2 fold change vs -log10 p-value)
        2. MA plot (mean expression vs log2 fold change)
        3. Heatmap of expression values with hierarchical clustering
        4. Pathway enrichment bar plot
        5. Scatter plot with regression line for control vs treatment
        6. Box plots comparing expression by pathway
        
        **Requirements**: All plots must be publication-ready with proper statistical annotations.
        **Save all plots to**: `/Users/samueltorres/Documents/Repos/apps/multi-agent-immuno-research/evals/outputs/coder/plots/`
        """,
        task_type="visualization",
        difficulty="hard",
        expected_deliverables="Publication-quality scientific plots with proper statistical annotations and formatting",
        sample_data="""gene_id,control_expression,treatment_expression,log2_fold_change,p_value,gene_name,pathway
GENE001,125.4,89.2,-0.49,0.023,APOE,Lipid metabolism
GENE002,78.9,156.3,0.98,0.001,BRCA1,DNA repair
GENE003,203.7,198.1,-0.04,0.856,TP53,Cell cycle
GENE004,45.2,89.7,0.99,0.002,VEGFA,Angiogenesis
GENE005,167.8,84.3,-0.99,0.001,MYC,Cell proliferation
GENE006,92.1,91.8,-0.01,0.945,GAPDH,Glycolysis
GENE007,134.5,268.9,1.00,0.000,EGFR,Signal transduction
GENE008,56.7,28.4,-1.00,0.003,CDKN1A,Cell cycle
GENE009,189.3,378.6,1.00,0.000,STAT3,Transcription
GENE010,98.4,49.2,-1.00,0.001,PTEN,Tumor suppression
GENE011,145.7,292.1,1.00,0.000,AKT1,Cell survival
GENE012,67.8,33.9,-1.00,0.002,RB1,Cell cycle
GENE013,156.2,312.4,1.00,0.000,PI3K,Signal transduction
GENE014,89.6,44.8,-1.00,0.001,BAX,Apoptosis
GENE015,178.9,357.8,1.00,0.000,MAPK,Signal transduction""",
        success_criteria=[
            "Creates volcano plot with proper thresholds",
            "Generates MA plot with statistical annotations",
            "Makes clustered heatmap with dendrograms",
            "Creates pathway enrichment visualization",
            "Shows regression analysis with confidence intervals",
            "Compares pathways with statistical tests",
            "Uses publication-quality formatting",
            "Saves all plots to specified directory path"
        ]
    ),

    CoderTestCase(
        id="visualization_006",
        task_description="""
        Create comprehensive diagnostic plots for this medical diagnostic dataset:

        ```
        patient_id,age,biomarker_1,biomarker_2,biomarker_3,diagnosis,severity_score
        P001,45,12.5,78.2,145.6,Positive,7.2
        P002,38,8.9,65.1,98.4,Negative,2.1
        P003,52,15.7,89.3,178.9,Positive,8.9
        P004,29,7.2,52.8,87.5,Negative,1.8
        P005,41,11.8,72.4,132.7,Positive,6.8
        P006,35,9.1,58.9,95.2,Negative,2.3
        P007,48,14.2,85.7,165.3,Positive,8.1
        P008,33,8.4,61.5,92.1,Negative,2.0
        P009,56,16.9,92.8,189.4,Positive,9.3
        P010,27,6.8,49.2,82.7,Negative,1.5
        P011,44,13.1,79.6,152.3,Positive,7.6
        P012,39,8.7,63.4,96.8,Negative,2.2
        P013,51,15.1,87.2,171.5,Positive,8.4
        P014,31,7.9,56.7,89.3,Negative,1.9
        P015,47,12.9,76.8,148.2,Positive,7.4
        ```
        
        Create diagnostic visualization suite:
        1. ROC curves for each biomarker with AUC calculations
        2. Box plots comparing biomarkers by diagnosis
        3. Correlation matrix heatmap with significance stars
        4. 3D scatter plot of biomarkers colored by diagnosis
        5. Distribution plots (histograms + KDE) for each biomarker by group
        6. Biomarker performance comparison radar chart
        
        **Requirements**: Include statistical annotations and diagnostic performance metrics.
        **Save all plots to**: `/Users/samueltorres/Documents/Repos/apps/multi-agent-immuno-research/evals/outputs/coder/plots/`
        """,
        task_type="visualization",
        difficulty="hard",
        expected_deliverables="Medical diagnostic plots with ROC analysis, performance metrics, and statistical annotations",
        sample_data="""patient_id,age,biomarker_1,biomarker_2,biomarker_3,diagnosis,severity_score
P001,45,12.5,78.2,145.6,Positive,7.2
P002,38,8.9,65.1,98.4,Negative,2.1
P003,52,15.7,89.3,178.9,Positive,8.9
P004,29,7.2,52.8,87.5,Negative,1.8
P005,41,11.8,72.4,132.7,Positive,6.8
P006,35,9.1,58.9,95.2,Negative,2.3
P007,48,14.2,85.7,165.3,Positive,8.1
P008,33,8.4,61.5,92.1,Negative,2.0
P009,56,16.9,92.8,189.4,Positive,9.3
P010,27,6.8,49.2,82.7,Negative,1.5
P011,44,13.1,79.6,152.3,Positive,7.6
P012,39,8.7,63.4,96.8,Negative,2.2
P013,51,15.1,87.2,171.5,Positive,8.4
P014,31,7.9,56.7,89.3,Negative,1.9
P015,47,12.9,76.8,148.2,Positive,7.4""",
        success_criteria=[
            "Creates ROC curves with AUC calculations",
            "Generates diagnostic box plots with p-values",
            "Makes correlation heatmap with significance",
            "Creates 3D visualization with clear separation",
            "Shows distribution comparisons by group",
            "Includes performance metrics and statistics",
            "Uses appropriate medical visualization standards",
            "Saves all plots to specified directory path"
        ]
    ),

    CoderTestCase(
        id="visualization_007",
        task_description="""
        Create advanced statistical plots for this multi-factorial experimental design:

        ```
        subject_id,factor_a,factor_b,response,block,replicate
        S001,Low,Control,23.4,1,1
        S002,High,Control,45.7,1,1
        S003,Low,Treatment,34.2,1,1
        S004,High,Treatment,67.8,1,1
        S005,Low,Control,25.1,1,2
        S006,High,Control,47.3,1,2
        S007,Low,Treatment,36.8,1,2
        S008,High,Treatment,69.2,1,2
        S009,Low,Control,22.9,2,1
        S010,High,Control,44.1,2,1
        S011,Low,Treatment,33.7,2,1
        S012,High,Treatment,66.4,2,1
        S013,Low,Control,24.6,2,2
        S014,High,Control,46.8,2,2
        S015,Low,Treatment,35.5,2,2
        S016,High,Treatment,68.1,2,2
        ```
        
        Create advanced experimental design visualizations:
        1. Interaction plot showing factor A × factor B effects
        2. Box plots with individual data points (strip plot overlay)
        3. Factorial design mean plot with error bars
        4. Residuals analysis plots (residuals vs fitted, Q-Q plot)
        5. Effect size visualization with confidence intervals
        6. Multi-panel plot showing block effects
        
        **Requirements**: Include proper statistical annotations and ANOVA assumptions checking.
        **Save all plots to**: `/Users/samueltorres/Documents/Repos/apps/multi-agent-immuno-research/evals/outputs/coder/plots/`
        """,
        task_type="visualization",
        difficulty="hard",
        expected_deliverables="Advanced experimental design plots with interaction effects and residuals analysis",
        sample_data="""subject_id,factor_a,factor_b,response,block,replicate
S001,Low,Control,23.4,1,1
S002,High,Control,45.7,1,1
S003,Low,Treatment,34.2,1,1
S004,High,Treatment,67.8,1,1
S005,Low,Control,25.1,1,2
S006,High,Control,47.3,1,2
S007,Low,Treatment,36.8,1,2
S008,High,Treatment,69.2,1,2
S009,Low,Control,22.9,2,1
S010,High,Control,44.1,2,1
S011,Low,Treatment,33.7,2,1
S012,High,Treatment,66.4,2,1
S013,Low,Control,24.6,2,2
S014,High,Control,46.8,2,2
S015,Low,Treatment,35.5,2,2
S016,High,Treatment,68.1,2,2""",
        success_criteria=[
            "Creates interaction plot with proper interpretation",
            "Generates box plots with data point overlay",
            "Shows factorial means with error bars",
            "Creates comprehensive residuals analysis",
            "Visualizes effect sizes with confidence intervals",
            "Shows block effects appropriately",
            "Includes proper statistical annotations",
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
    ),

    CoderTestCase(
        id="data_processing_003",
        task_description="""
        Process and clean this complex multi-source scientific dataset with various data quality issues:

        ```
        experiment_id,lab_code,measurement_date,temperature,ph_level,concentration,operator,notes,quality_flag
        EXP001,LAB_A,2024-01-15,25.2,7.4,12.5,Smith,Normal conditions,PASS
        EXP002,LAB_B,2024/01/16,23.8,7.1,15.3,Jones,Equipment calibrated,PASS
        EXP003,LAB_A,2024-01-17,NULL,7.2,11.8,Smith,Temperature sensor failed,FAIL
        EXP004,LAB_C,15-Jan-2024,26.1,7.6,14.2,Brown,Late start due to power outage,PASS
        EXP005,LAB_B,2024-01-18,24.5,NULL,13.7,Jones,pH probe replaced,FAIL
        EXP006,LAB_A,2024-01-19,25.0,7.3,-5.2,Smith,Negative concentration error,FAIL
        EXP007,LAB_C,2024-01-20,999.9,7.5,12.9,Brown,Temperature spike from heater malfunction,FAIL
        EXP008,LAB_B,2024-01-21,24.8,14.2,13.1,Jones,pH reading abnormally high,FAIL
        EXP009,LAB_A,01/22/2024,25.3,7.4,12.8,SMITH,Operator name inconsistent,PASS
        EXP010,LAB_D,2024-01-23,24.9,7.2,13.5,Davis,New lab added,PASS
        EXP011,LAB_A,,25.1,7.3,12.6,Smith,Missing date,FAIL
        EXP012,LAB_B,2024-01-24,24.7,7.0,INVALID,Jones,Concentration measurement error,FAIL
        EXP013,LAB_C,2024-01-25,25.4,7.8,13.9,brown,Case inconsistency,PASS
        EXP014,LAB_A,2024-01-26,24.2,6.9,12.3,Smith,pH slightly low but acceptable,PASS
        EXP015,LAB_B,2024-01-27,25.6,7.5,,Jones,Missing concentration,FAIL
        ```

        Data cleaning and processing tasks:
        1. Standardize date formats to ISO format
        2. Handle missing values with appropriate strategies
        3. Detect and flag outliers using statistical methods
        4. Standardize categorical variables (operator names, lab codes)
        5. Validate measurement ranges (temp: 15-35°C, pH: 6.0-8.0, conc: 0-20)
        6. Create data quality scores
        7. Generate summary statistics by lab and operator
        8. Export cleaned dataset with quality flags
        """,
        task_type="data_processing",
        difficulty="hard",
        expected_deliverables="Cleaned scientific dataset with quality assessment and standardized formats",
        sample_data="""experiment_id,lab_code,measurement_date,temperature,ph_level,concentration,operator,notes,quality_flag
EXP001,LAB_A,2024-01-15,25.2,7.4,12.5,Smith,Normal conditions,PASS
EXP002,LAB_B,2024/01/16,23.8,7.1,15.3,Jones,Equipment calibrated,PASS
EXP003,LAB_A,2024-01-17,NULL,7.2,11.8,Smith,Temperature sensor failed,FAIL
EXP004,LAB_C,15-Jan-2024,26.1,7.6,14.2,Brown,Late start due to power outage,PASS
EXP005,LAB_B,2024-01-18,24.5,NULL,13.7,Jones,pH probe replaced,FAIL
EXP006,LAB_A,2024-01-19,25.0,7.3,-5.2,Smith,Negative concentration error,FAIL
EXP007,LAB_C,2024-01-20,999.9,7.5,12.9,Brown,Temperature spike from heater malfunction,FAIL
EXP008,LAB_B,2024-01-21,24.8,14.2,13.1,Jones,pH reading abnormally high,FAIL
EXP009,LAB_A,01/22/2024,25.3,7.4,12.8,SMITH,Operator name inconsistent,PASS
EXP010,LAB_D,2024-01-23,24.9,7.2,13.5,Davis,New lab added,PASS
EXP011,LAB_A,,25.1,7.3,12.6,Smith,Missing date,FAIL
EXP012,LAB_B,2024-01-24,24.7,7.0,INVALID,Jones,Concentration measurement error,FAIL
EXP013,LAB_C,2024-01-25,25.4,7.8,13.9,brown,Case inconsistency,PASS
EXP014,LAB_A,2024-01-26,24.2,6.9,12.3,Smith,pH slightly low but acceptable,PASS
EXP015,LAB_B,2024-01-27,25.6,7.5,,Jones,Missing concentration,FAIL""",
        success_criteria=[
            "Standardizes all date formats correctly",
            "Handles missing values appropriately",
            "Detects outliers using statistical methods",
            "Implements proper data preprocessing",
            "Performs stratified train-test split",
            "Implements multiple ML algorithms",
            "Conducts cross-validation properly",
            "Performs hyperparameter tuning",
            "Analyzes feature importance",
            "Compares models systematically",
            "Evaluates final model comprehensively"
        ]
    ),

    CoderTestCase(
        id="data_processing_004",
        task_description="""
        Implement advanced data transformation and feature engineering pipeline:

        ```
        customer_id,signup_date,last_login,age,income,transactions_count,total_spent,days_since_last_purchase,product_categories,device_type
        C001,2023-01-15,2024-01-20,28,45000,12,890.50,5,electronics;books,mobile
        C002,2023-03-22,2024-01-18,34,67000,8,1250.75,12,clothing;home,desktop
        C003,2023-05-10,2024-01-22,22,38000,15,567.25,3,books;electronics;games,mobile
        C004,2023-07-08,2024-01-15,41,82000,6,2100.00,20,luxury;clothing,tablet
        C005,2023-02-14,2024-01-19,29,52000,10,775.80,8,electronics;sports,mobile
        C006,2023-09-03,2024-01-21,55,95000,4,3200.50,15,luxury;home;electronics,desktop
        C007,2023-04-17,2024-01-16,31,48000,18,654.30,7,books;clothing;sports,mobile
        C008,2023-11-25,2024-01-23,26,41000,9,423.75,2,games;electronics,tablet
        C009,2023-06-12,2024-01-17,38,71000,7,1850.25,18,luxury;clothing,desktop
        C010,2023-08-30,2024-01-24,33,59000,13,1100.40,6,electronics;home;books,mobile
        C011,2023-12-05,2024-01-14,24,36000,20,342.60,25,books;games,mobile
        C012,2023-10-18,2024-01-22,47,88000,5,2750.80,10,luxury;home,tablet
        C013,2023-01-28,2024-01-20,30,54000,11,980.25,4,electronics;clothing;sports,desktop
        C014,2023-03-15,2024-01-18,39,63000,14,1420.75,9,clothing;home;books,mobile
        C015,2023-07-22,2024-01-25,27,44000,16,695.50,1,electronics;games;sports,tablet
        ```

        Feature engineering tasks:
        1. Create temporal features (days since signup, recency, frequency)
        2. Engineer customer lifetime value and transaction metrics
        3. Parse and encode categorical features (product categories, device types)
        4. Create customer segmentation features
        5. Generate interaction features between numerical variables
        6. Implement binning for continuous variables
        7. Calculate rolling statistics and trend features
        8. Scale features appropriately for machine learning
        """,
        task_type="data_processing",
        difficulty="hard",
        expected_deliverables="Advanced feature engineering pipeline with customer segmentation and ML-ready features",
        sample_data="""customer_id,signup_date,last_login,age,income,transactions_count,total_spent,days_since_last_purchase,product_categories,device_type
C001,2023-01-15,2024-01-20,28,45000,12,890.50,5,electronics;books,mobile
C002,2023-03-22,2024-01-18,34,67000,8,1250.75,12,clothing;home,desktop
C003,2023-05-10,2024-01-22,22,38000,15,567.25,3,books;electronics;games,mobile
C004,2023-07-08,2024-01-15,41,82000,6,2100.00,20,luxury;clothing,tablet
C005,2023-02-14,2024-01-19,29,52000,10,775.80,8,electronics;sports,mobile
C006,2023-09-03,2024-01-21,55,95000,4,3200.50,15,luxury;home;electronics,desktop
C007,2023-04-17,2024-01-16,31,48000,18,654.30,7,books;clothing;sports,mobile
C008,2023-11-25,2024-01-23,26,41000,9,423.75,2,games;electronics,tablet
C009,2023-06-12,2024-01-17,38,71000,7,1850.25,18,luxury;clothing,desktop
C010,2023-08-30,2024-01-24,33,59000,13,1100.40,6,electronics;home;books,mobile
C011,2023-12-05,2024-01-14,24,36000,20,342.60,25,books;games,mobile
C012,2023-10-18,2024-01-22,47,88000,5,2750.80,10,luxury;home,tablet
C013,2023-01-28,2024-01-20,30,54000,11,980.25,4,electronics;clothing;sports,desktop
C014,2023-03-15,2024-01-18,39,63000,14,1420.75,9,clothing;home;books,mobile
C015,2023-07-22,2024-01-25,27,44000,16,695.50,1,electronics;games;sports,tablet""",
        success_criteria=[
            "Creates meaningful temporal features",
            "Engineers customer value metrics",
            "Properly encodes categorical features",
            "Implements customer segmentation",
            "Generates interaction features",
            "Applies appropriate binning strategies",
            "Calculates rolling statistics",
            "Scales features for ML applications"
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
    ),

    CoderTestCase(
        id="algorithm_004",
        task_description="""
        Implement a complete machine learning pipeline for binary classification:

        ```
        feature_1,feature_2,feature_3,feature_4,feature_5,target
        2.1,3.4,1.2,0.8,2.5,0
        1.8,2.9,1.1,0.7,2.1,0
        3.2,4.1,1.8,1.2,3.4,1
        2.9,3.8,1.6,1.1,3.1,1
        1.9,3.1,1.0,0.6,2.2,0
        3.1,4.2,1.7,1.3,3.3,1
        2.2,3.3,1.3,0.9,2.6,0
        3.4,4.5,1.9,1.4,3.6,1
        1.7,2.8,0.9,0.5,2.0,0
        3.3,4.3,1.8,1.3,3.5,1
        2.0,3.2,1.1,0.8,2.3,0
        3.0,4.0,1.6,1.2,3.2,1
        1.8,3.0,1.0,0.6,2.1,0
        3.2,4.4,1.7,1.3,3.4,1
        2.1,3.3,1.2,0.9,2.4,0
        3.5,4.6,2.0,1.5,3.7,1
        1.6,2.7,0.8,0.4,1.9,0
        3.1,4.1,1.6,1.2,3.3,1
        2.3,3.4,1.3,0.9,2.7,0
        3.3,4.4,1.8,1.4,3.5,1
        ```

        Implement complete ML pipeline:
        1. Data preprocessing and feature scaling
        2. Train-test split with stratification
        3. Implement multiple algorithms (Logistic Regression, Random Forest, SVM)
        4. Cross-validation with performance metrics
        5. Hyperparameter tuning using grid search
        6. Feature importance analysis
        7. Model comparison and selection
        8. Final model evaluation with confusion matrix and ROC curve
        """,
        task_type="algorithm",
        difficulty="hard",
        expected_deliverables="Complete ML pipeline with model comparison, hyperparameter tuning, and performance evaluation",
        sample_data="""feature_1,feature_2,feature_3,feature_4,feature_5,target
2.1,3.4,1.2,0.8,2.5,0
1.8,2.9,1.1,0.7,2.1,0
3.2,4.1,1.8,1.2,3.4,1
2.9,3.8,1.6,1.1,3.1,1
1.9,3.1,1.0,0.6,2.2,0
3.1,4.2,1.7,1.3,3.3,1
2.2,3.3,1.3,0.9,2.6,0
3.4,4.5,1.9,1.4,3.6,1
1.7,2.8,0.9,0.5,2.0,0
3.3,4.3,1.8,1.3,3.5,1
2.0,3.2,1.1,0.8,2.3,0
3.0,4.0,1.6,1.2,3.2,1
1.8,3.0,1.0,0.6,2.1,0
3.2,4.4,1.7,1.3,3.4,1
2.1,3.3,1.2,0.9,2.4,0
3.5,4.6,2.0,1.5,3.7,1
1.6,2.7,0.8,0.4,1.9,0
3.1,4.1,1.6,1.2,3.3,1
2.3,3.4,1.3,0.9,2.7,0
3.3,4.4,1.8,1.4,3.5,1""",
        success_criteria=[
            "Implements proper data preprocessing",
            "Performs stratified train-test split",
            "Implements multiple ML algorithms",
            "Conducts cross-validation properly",
            "Performs hyperparameter tuning",
            "Analyzes feature importance",
            "Compares models systematically",
            "Evaluates final model comprehensively"
        ]
    ),

    CoderTestCase(
        id="algorithm_005",
        task_description="""
        Implement a dimensionality reduction and visualization algorithm suite:

        ```
        sample_id,gene_1,gene_2,gene_3,gene_4,gene_5,gene_6,gene_7,gene_8,condition
        S001,12.5,8.9,15.2,6.7,11.3,9.8,14.1,7.2,Control
        S002,11.8,9.2,14.8,6.9,10.9,9.5,13.7,7.5,Control
        S003,18.9,12.3,19.5,10.1,16.2,13.7,18.8,11.4,Treatment
        S004,19.2,11.8,20.1,9.8,15.9,13.2,19.3,10.9,Treatment
        S005,12.1,8.7,15.0,6.5,11.1,9.6,14.3,7.1,Control
        S006,11.9,9.0,14.7,6.8,10.8,9.7,13.9,7.3,Control
        S007,18.7,12.1,19.3,10.3,16.0,13.5,18.6,11.2,Treatment
        S008,19.0,11.9,19.8,9.9,15.8,13.3,19.1,11.0,Treatment
        S009,12.3,8.8,15.1,6.6,11.2,9.9,14.2,7.4,Control
        S010,19.1,12.0,19.7,10.0,16.1,13.4,18.9,11.1,Treatment
        S011,12.0,9.1,14.9,6.7,11.0,9.4,14.0,7.0,Control
        S012,18.8,12.2,19.4,10.2,15.7,13.6,18.7,11.3,Treatment
        S013,11.7,8.6,14.6,6.4,10.7,9.3,13.8,6.9,Control
        S014,19.3,11.7,20.0,9.7,16.3,13.1,19.2,10.8,Treatment
        S015,12.2,8.9,15.3,6.8,11.4,9.8,14.4,7.2,Control
        ```

        Implement dimensionality reduction suite:
        1. Principal Component Analysis (PCA) from scratch
        2. t-SNE implementation or usage for non-linear reduction
        3. Linear Discriminant Analysis (LDA) for supervised reduction
        4. Variance explained analysis and scree plots
        5. Biplot creation with loading vectors
        6. Cluster validation using silhouette analysis
        7. Compare all methods with visualization
        8. Assess optimal number of components
        """,
        task_type="algorithm",
        difficulty="hard",
        expected_deliverables="Comprehensive dimensionality reduction analysis with multiple methods and validation",
        sample_data="""sample_id,gene_1,gene_2,gene_3,gene_4,gene_5,gene_6,gene_7,gene_8,condition
S001,12.5,8.9,15.2,6.7,11.3,9.8,14.1,7.2,Control
S002,11.8,9.2,14.8,6.9,10.9,9.5,13.7,7.5,Control
S003,18.9,12.3,19.5,10.1,16.2,13.7,18.8,11.4,Treatment
S004,19.2,11.8,20.1,9.8,15.9,13.2,19.3,10.9,Treatment
S005,12.1,8.7,15.0,6.5,11.1,9.6,14.3,7.1,Control
S006,11.9,9.0,14.7,6.8,10.8,9.7,13.9,7.3,Control
S007,18.7,12.1,19.3,10.3,16.0,13.5,18.6,11.2,Treatment
S008,19.0,11.9,19.8,9.9,15.8,13.3,19.1,11.0,Treatment
S009,12.3,8.8,15.1,6.6,11.2,9.9,14.2,7.4,Control
S010,19.1,12.0,19.7,10.0,16.1,13.4,18.9,11.1,Treatment
S011,12.0,9.1,14.9,6.7,11.0,9.4,14.0,7.0,Control
S012,18.8,12.2,19.4,10.2,15.7,13.6,18.7,11.3,Treatment
S013,11.7,8.6,14.6,6.4,10.7,9.3,13.8,6.9,Control
S014,19.3,11.7,20.0,9.7,16.3,13.1,19.2,10.8,Treatment
S015,12.2,8.9,15.3,6.8,11.4,9.8,14.4,7.2,Control""",
        success_criteria=[
            "Implements PCA from scratch correctly",
            "Applies t-SNE or other non-linear methods",
            "Conducts LDA for supervised reduction",
            "Creates variance explained analysis",
            "Generates biplots with loadings",
            "Performs silhouette analysis",
            "Compares methods systematically",
            "Determines optimal components"
        ]
    ),

    CoderTestCase(
        id="algorithm_006",
        task_description="""
        Implement optimization algorithms for parameter estimation:

        ```
        x_data,y_observed,weight
        0.1,2.12,1.0
        0.3,2.45,1.0
        0.5,3.08,1.2
        0.7,3.91,1.1
        0.9,4.87,0.9
        1.1,5.95,1.0
        1.3,7.21,1.1
        1.5,8.58,1.0
        1.7,10.12,0.8
        1.9,11.89,1.0
        2.1,13.95,1.2
        2.3,16.24,1.1
        2.5,18.82,0.9
        2.7,21.73,1.0
        2.9,25.01,1.1
        ```

        Implement optimization algorithms:
        1. Gradient descent for non-linear curve fitting (y = a*exp(b*x) + c)
        2. Implement Newton-Raphson method
        3. Gauss-Newton algorithm for least squares
        4. Levenberg-Marquardt algorithm
        5. Compare convergence rates and final parameters
        6. Bootstrap parameter uncertainty estimation
        7. Weighted least squares implementation
        8. Residuals analysis and goodness of fit
        """,
        task_type="algorithm",
        difficulty="hard",
        expected_deliverables="Optimization algorithm suite with parameter estimation and uncertainty analysis",
        sample_data="""x_data,y_observed,weight
0.1,2.12,1.0
0.3,2.45,1.0
0.5,3.08,1.2
0.7,3.91,1.1
0.9,4.87,0.9
1.1,5.95,1.0
1.3,7.21,1.1
1.5,8.58,1.0
1.7,10.12,0.8
1.9,11.89,1.0
2.1,13.95,1.2
2.3,16.24,1.1
2.5,18.82,0.9
2.7,21.73,1.0
2.9,25.01,1.1""",
        success_criteria=[
            "Implements gradient descent correctly",
            "Applies Newton-Raphson method",
            "Implements Gauss-Newton algorithm",
            "Applies Levenberg-Marquardt method",
            "Compares convergence characteristics",
            "Estimates parameter uncertainties",
            "Implements weighted least squares",
            "Analyzes residuals and goodness of fit"
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
    ),

    CoderTestCase(
        id="debugging_002",
        task_description="""
        Debug and fix this code that has performance bottlenecks:

        ```
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
        1. Identify and fix the performance bottlenecks
        2. Optimize the code structure
        3. Test the corrected function with the provided data
        """,
        task_type="debugging",
        difficulty="medium",
        expected_deliverables="Debugged and optimized code with improved performance",
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
            "Identifies performance bottlenecks correctly",
            "Optimizes parsing with pandas",
            "Removes unnecessary loops",
            "Implements vectorized operations",
            "Adds comprehensive error handling",
            "Benchmarks performance improvements",
            "Creates memory-efficient solution"
        ]
    ),

    CoderTestCase(
        id="debugging_003",
        task_description="""
        Debug and fix this statistical analysis code that has multiple methodological and implementation errors:

        ```
        participant_id,group,pre_score,post_score,age,gender
        P001,Treatment,45.2,52.8,28,M
        P002,Control,43.7,45.1,31,F
        P003,Treatment,41.9,49.3,26,M
        P004,Control,44.8,46.2,33,F
        P005,Treatment,42.5,50.7,29,M
        P006,Control,43.1,44.9,30,F
        P007,Treatment,40.8,48.6,27,M
        P008,Control,45.3,47.1,32,F
        P009,Treatment,43.6,51.2,25,M
        P010,Control,42.9,44.5,34,F
        ```

        Problematic statistical code to debug:
        ```python
        import pandas as pd
        import scipy.stats as stats
        import numpy as np
        
        def flawed_statistical_analysis(data_text):
            # Parsing issues
            data = pd.read_csv(data_text)  # Wrong - should use StringIO
            
            # Calculate difference scores incorrectly
            data['improvement'] = data['pre_score'] - data['post_score']  # Wrong direction
            
            # Wrong statistical test selection
            treatment_improvement = data[data['group'] == 'Treatment']['improvement']
            control_improvement = data[data['group'] == 'Control']['improvement']
            
            # Using wrong test for paired data
            t_stat, p_value = stats.ttest_ind(treatment_improvement, control_improvement)
            
            # Effect size calculation error
            pooled_std = np.sqrt((treatment_improvement.var() + control_improvement.var()) / 2)
            cohens_d = (treatment_improvement.mean() - control_improvement.mean()) / pooled_std
            
            # Multiple testing without correction
            age_ttest = stats.ttest_ind(
                data[data['group'] == 'Treatment']['age'],
                data[data['group'] == 'Control']['age']
            )
            
            gender_chi2 = stats.chi2_contingency(pd.crosstab(data['group'], data['gender']))
            
            # Wrong confidence interval calculation
            ci_lower = treatment_improvement.mean() - 1.96 * treatment_improvement.std()
            ci_upper = treatment_improvement.mean() + 1.96 * treatment_improvement.std()
            
            return {
                'p_value': p_value,
                'effect_size': cohens_d,
                'confidence_interval': (ci_lower, ci_upper)
            }
        ```

        Tasks:
        1. Fix CSV parsing using StringIO
        2. Correct the improvement calculation direction
        3. Use appropriate statistical tests for the data structure
        4. Fix effect size calculation methodology
        5. Apply multiple testing corrections
        6. Correct confidence interval calculations
        7. Add proper assumption checking
        """,
        task_type="debugging",
        difficulty="hard",
        expected_deliverables="Corrected statistical analysis code with proper methodology and implementation",
        sample_data="""participant_id,group,pre_score,post_score,age,gender
P001,Treatment,45.2,52.8,28,M
P002,Control,43.7,45.1,31,F
P003,Treatment,41.9,49.3,26,M
P004,Control,44.8,46.2,33,F
P005,Treatment,42.5,50.7,29,M
P006,Control,43.1,44.9,30,F
P007,Treatment,40.8,48.6,27,M
P008,Control,45.3,47.1,32,F
P009,Treatment,43.6,51.2,25,M
P010,Control,42.9,44.5,34,F""",
        success_criteria=[
            "Fixes CSV parsing with StringIO",
            "Corrects improvement calculation direction", 
            "Selects appropriate statistical tests",
            "Fixes effect size calculation",
            "Applies multiple testing corrections",
            "Corrects confidence interval calculations",
            "Adds statistical assumption checking"
        ]
    ),

    CoderTestCase(
        id="debugging_004",
        task_description="""
        Debug this machine learning pipeline that has data leakage and validation issues:

        ```
        feature_1,feature_2,feature_3,feature_4,target
        1.2,3.4,0.8,2.1,0
        2.3,4.1,1.2,3.2,1
        1.8,3.7,0.9,2.5,0
        2.7,4.5,1.4,3.6,1
        1.5,3.2,0.7,2.0,0
        2.1,3.9,1.1,3.1,1
        1.9,3.5,1.0,2.4,0
        2.5,4.3,1.3,3.4,1
        1.7,3.3,0.8,2.2,0
        2.4,4.2,1.2,3.3,1
        1.6,3.6,0.9,2.3,0
        2.6,4.4,1.4,3.5,1
        1.4,3.1,0.6,1.9,0
        2.8,4.6,1.5,3.7,1
        1.3,2.9,0.5,1.8,0
        ```

        Problematic ML code to debug:
        ```python
        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import accuracy_score
        import numpy as np
        
        def flawed_ml_pipeline(data_text):
            # Data loading
            data = pd.read_csv(data_text)  # Missing StringIO
            
            # Data leakage: scaling before split
            scaler = StandardScaler()
            scaled_features = scaler.fit_transform(data.drop('target', axis=1))
            
            X = scaled_features
            y = data['target']
            
            # Poor train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42  # No stratification
            )
            
            # Model training with poor hyperparameters
            model = RandomForestClassifier(n_estimators=10, random_state=42)  # Too few trees
            model.fit(X_train, y_train)
            
            # Evaluation issues
            train_pred = model.predict(X_train)
            test_pred = model.predict(X_test)
            
            # Only reporting accuracy
            train_acc = accuracy_score(y_train, train_pred)
            test_acc = accuracy_score(y_test, test_pred)
            
            # No cross-validation
            # No feature importance analysis
            # No confidence intervals
            
            return {
                'train_accuracy': train_acc,
                'test_accuracy': test_acc,
                'model': model
            }
        ```

        Tasks:
        1. Fix data loading with proper CSV parsing
        2. Prevent data leakage by scaling after train-test split
        3. Add stratification to train-test split
        4. Implement proper cross-validation
        5. Add comprehensive evaluation metrics
        6. Include feature importance analysis
        7. Add confidence intervals for performance estimates
        """,
        task_type="debugging",
        difficulty="hard",
        expected_deliverables="Corrected ML pipeline without data leakage and with proper validation",
        sample_data="""feature_1,feature_2,feature_3,feature_4,target
1.2,3.4,0.8,2.1,0
2.3,4.1,1.2,3.2,1
1.8,3.7,0.9,2.5,0
2.7,4.5,1.4,3.6,1
1.5,3.2,0.7,2.0,0
2.1,3.9,1.1,3.1,1
1.9,3.5,1.0,2.4,0
2.5,4.3,1.3,3.4,1
1.7,3.3,0.8,2.2,0
2.4,4.2,1.2,3.3,1
1.6,3.6,0.9,2.3,0
2.6,4.4,1.4,3.5,1
1.4,3.1,0.6,1.9,0
2.8,4.6,1.5,3.7,1
1.3,2.9,0.5,1.8,0""",
        success_criteria=[
            "Fixes CSV parsing with StringIO",
            "Prevents data leakage in preprocessing",
            "Adds stratification to train-test split",
            "Implements cross-validation properly",
            "Includes comprehensive evaluation metrics",
            "Analyzes feature importance",
            "Provides confidence intervals for performance"
        ]
    )
]

# Statistical Testing Cases
STATISTICAL_TESTING_CASES = [
    CoderTestCase(
        id="statistical_001",
        task_description="""
        Perform comprehensive statistical testing on the following experimental data:

        ```
        group,score,age,gender,pre_score,post_score
        Control,85.2,25,M,78.1,85.2
        Control,82.7,28,F,76.8,82.7
        Control,87.1,31,M,81.2,87.1
        Control,84.5,26,F,79.5,84.5
        Control,86.3,29,M,80.7,86.3
        Treatment,92.4,27,F,85.1,92.4
        Treatment,94.8,30,M,87.3,94.8
        Treatment,91.2,24,F,84.6,91.2
        Treatment,95.1,32,M,88.2,95.1
        Treatment,93.7,28,F,86.9,93.7
        Placebo,88.9,29,M,82.4,88.9
        Placebo,87.3,26,F,81.1,87.3
        Placebo,89.6,33,M,83.7,89.6
        Placebo,86.8,27,F,80.3,86.8
        Placebo,90.2,31,M,84.5,90.2
        ```
        
        Perform the following statistical analyses:
        1. Parse the CSV data from the text above
        2. Descriptive statistics for each group
        3. Test for normality (Shapiro-Wilk test)
        4. One-way ANOVA comparing groups
        5. Post-hoc pairwise comparisons (Tukey HSD)
        6. Paired t-test for pre vs post scores
        7. Effect size calculations (Cohen's d)
        8. Power analysis for sample size adequacy
        
        State your hypotheses clearly and interpret all results with statistical significance levels.
        """,
        task_type="statistical_testing",
        difficulty="hard",
        expected_deliverables="Complete statistical analysis with hypothesis testing, effect sizes, and interpretation",
        sample_data="""group,score,age,gender,pre_score,post_score
Control,85.2,25,M,78.1,85.2
Control,82.7,28,F,76.8,82.7
Control,87.1,31,M,81.2,87.1
Control,84.5,26,F,79.5,84.5
Control,86.3,29,M,80.7,86.3
Treatment,92.4,27,F,85.1,92.4
Treatment,94.8,30,M,87.3,94.8
Treatment,91.2,24,F,84.6,91.2
Treatment,95.1,32,M,88.2,95.1
Treatment,93.7,28,F,86.9,93.7
Placebo,88.9,29,M,82.4,88.9
Placebo,87.3,26,F,81.1,87.3
Placebo,89.6,33,M,83.7,89.6
Placebo,86.8,27,F,80.3,86.8
Placebo,90.2,31,M,84.5,90.2""",
        success_criteria=[
            "Parses CSV data from text correctly",
            "Calculates descriptive statistics",
            "Performs normality testing",
            "Conducts ANOVA with proper interpretation",
            "Performs post-hoc comparisons",
            "Conducts paired t-tests",
            "Calculates effect sizes",
            "States hypotheses clearly",
            "Interprets results with significance levels"
        ]
    ),

    CoderTestCase(
        id="statistical_002",
        task_description="""
        Perform correlation and regression analysis on the following dataset:

        ```
        house_price,square_feet,bedrooms,bathrooms,age,neighborhood_score,distance_to_center
        425000,2100,3,2,15,8.2,12.5
        380000,1850,3,2,22,7.5,18.3
        520000,2450,4,3,8,9.1,8.7
        310000,1600,2,1,35,6.8,25.2
        680000,3200,5,4,3,9.8,5.1
        445000,2200,3,2,12,8.5,11.9
        390000,1950,3,2,28,7.2,19.6
        750000,3500,5,4,2,9.9,3.2
        325000,1700,2,1,40,6.5,28.1
        580000,2800,4,3,6,9.3,7.4
        ```
        
        Perform the following analyses:
        1. Parse the CSV data from the text above
        2. Calculate correlation matrix with significance tests
        3. Create scatter plots with regression lines
        4. Multiple linear regression analysis
        5. Check regression assumptions (residuals, normality, homoscedasticity)
        6. Calculate R-squared, adjusted R-squared, and model fit statistics
        7. Identify and handle outliers
        8. Feature importance analysis
        
        Provide detailed interpretation of regression coefficients and model performance.
        """,
        task_type="statistical_testing",
        difficulty="hard",
        expected_deliverables="Complete regression analysis with assumption checking and model interpretation",
        sample_data="""house_price,square_feet,bedrooms,bathrooms,age,neighborhood_score,distance_to_center
425000,2100,3,2,15,8.2,12.5
380000,1850,3,2,22,7.5,18.3
520000,2450,4,3,8,9.1,8.7
310000,1600,2,1,35,6.8,25.2
680000,3200,5,4,3,9.8,5.1
445000,2200,3,2,12,8.5,11.9
390000,1950,3,2,28,7.2,19.6
750000,3500,5,4,2,9.9,3.2
325000,1700,2,1,40,6.5,28.1
580000,2800,4,3,6,9.3,7.4""",
        success_criteria=[
            "Parses CSV data from text correctly",
            "Calculates correlation matrix with p-values",
            "Creates regression scatter plots",
            "Performs multiple linear regression",
            "Checks regression assumptions",
            "Calculates model fit statistics",
            "Identifies outliers appropriately",
            "Provides clear coefficient interpretation"
        ]
    ),

    CoderTestCase(
        id="statistical_003",
        task_description="""
        Perform comprehensive survival analysis on this clinical outcomes dataset:

        ```
        patient_id,treatment_group,survival_time,event_observed,age,stage,biomarker_level
        P001,Treatment,24.5,1,65,III,8.2
        P002,Control,18.2,1,58,II,5.1
        P003,Treatment,36.8,0,42,I,12.4
        P004,Control,12.1,1,71,IV,3.8
        P005,Treatment,42.3,0,55,II,9.7
        P006,Control,15.7,1,63,III,4.2
        P007,Treatment,28.9,1,49,II,7.9
        P008,Control,8.4,1,67,IV,2.9
        P009,Treatment,39.1,0,38,I,11.8
        P010,Control,22.6,1,59,III,5.6
        P011,Treatment,31.4,1,52,II,8.5
        P012,Control,19.8,1,64,III,4.7
        P013,Treatment,45.2,0,44,I,13.1
        P014,Control,11.3,1,69,IV,3.4
        P015,Treatment,33.7,0,47,II,10.2
        ```
        
        Perform these survival analyses:
        1. Kaplan-Meier survival curves by treatment group
        2. Log-rank test for survival differences
        3. Cox proportional hazards regression
        4. Hazard ratios with confidence intervals
        5. Survival probability tables at key time points
        6. Univariate and multivariate analysis
        7. Proportional hazards assumption testing
        
        State all hypotheses clearly and interpret clinical significance.
        """,
        task_type="statistical_testing",
        difficulty="hard",
        expected_deliverables="Comprehensive survival analysis with hazard ratios, survival curves, and clinical interpretation",
        sample_data="""patient_id,treatment_group,survival_time,event_observed,age,stage,biomarker_level
P001,Treatment,24.5,1,65,III,8.2
P002,Control,18.2,1,58,II,5.1
P003,Treatment,36.8,0,42,I,12.4
P004,Control,12.1,1,71,IV,3.8
P005,Treatment,42.3,0,55,II,9.7
P006,Control,15.7,1,63,III,4.2
P007,Treatment,28.9,1,49,II,7.9
P008,Control,8.4,1,67,IV,2.9
P009,Treatment,39.1,0,38,I,11.8
P010,Control,22.6,1,59,III,5.6
P011,Treatment,31.4,1,52,II,8.5
P012,Control,19.8,1,64,III,4.7
P013,Treatment,45.2,0,44,I,13.1
P014,Control,11.3,1,69,IV,3.4
P015,Treatment,33.7,0,47,II,10.2""",
        success_criteria=[
            "Creates Kaplan-Meier survival curves",
            "Performs log-rank test correctly",
            "Conducts Cox regression analysis",
            "Calculates hazard ratios with CI",
            "Provides survival probability tables",
            "Performs univariate and multivariate analysis",
            "Tests proportional hazards assumptions",
            "Interprets results with clinical significance"
        ]
    ),

    CoderTestCase(
        id="statistical_004",
        task_description="""
        Perform repeated measures ANOVA and mixed-effects modeling on this longitudinal dataset:

        ```
        subject_id,time_point,treatment,response,baseline_covariate,age_group
        S01,0,A,45.2,42.1,Young
        S01,1,A,48.7,42.1,Young
        S01,2,A,52.3,42.1,Young
        S01,3,A,55.8,42.1,Young
        S02,0,B,43.8,41.5,Young
        S02,1,B,44.2,41.5,Young
        S02,2,B,45.1,41.5,Young
        S02,3,B,46.3,41.5,Young
        S03,0,A,38.9,39.2,Old
        S03,1,A,42.1,39.2,Old
        S03,2,A,45.8,39.2,Old
        S03,3,A,49.2,39.2,Old
        S04,0,B,37.5,38.8,Old
        S04,1,B,38.1,38.8,Old
        S04,2,B,38.9,38.8,Old
        S04,3,B,39.7,38.8,Old
        S05,0,A,44.1,41.8,Young
        S05,1,A,47.2,41.8,Young
        S05,2,A,50.9,41.8,Young
        S05,3,A,54.1,41.8,Young
        ```
        
        Perform comprehensive longitudinal analysis:
        1. Repeated measures ANOVA with sphericity testing
        2. Mixed-effects model with random intercepts and slopes
        3. Growth curve analysis
        4. Between-subjects and within-subjects effects
        5. Post-hoc comparisons with multiple testing correction
        6. Model diagnostics and assumption checking
        7. Effect size calculations for time and treatment effects
        """,
        task_type="statistical_testing",
        difficulty="hard",
        expected_deliverables="Longitudinal data analysis with mixed-effects modeling and growth curve analysis",
        sample_data="""subject_id,time_point,treatment,response,baseline_covariate,age_group
S01,0,A,45.2,42.1,Young
S01,1,A,48.7,42.1,Young
S01,2,A,52.3,42.1,Young
S01,3,A,55.8,42.1,Young
S02,0,B,43.8,41.5,Young
S02,1,B,44.2,41.5,Young
S02,2,B,45.1,41.5,Young
S02,3,B,46.3,41.5,Young
S03,0,A,38.9,39.2,Old
S03,1,A,42.1,39.2,Old
S03,2,A,45.8,39.2,Old
S03,3,A,49.2,39.2,Old
S04,0,B,37.5,38.8,Old
S04,1,B,38.1,38.8,Old
S04,2,B,38.9,38.8,Old
S04,3,B,39.7,38.8,Old
S05,0,A,44.1,41.8,Young
S05,1,A,47.2,41.8,Young
S05,2,A,50.9,41.8,Young
S05,3,A,54.1,41.8,Young""",
        success_criteria=[
            "Performs repeated measures ANOVA correctly",
            "Tests sphericity assumptions",
            "Conducts mixed-effects modeling",
            "Analyzes growth curves appropriately",
            "Tests between and within-subjects effects",
            "Applies multiple testing corrections",
            "Checks model assumptions thoroughly",
            "Calculates meaningful effect sizes"
        ]
    ),

    CoderTestCase(
        id="statistical_005",
        task_description="""
        Perform non-parametric statistical analysis on this ordinal and skewed data:

        ```
        participant_id,group,ordinal_rating,skewed_measure,rank_score,satisfaction_level
        P01,Control,3,12.4,8,Moderate
        P02,Treatment,5,45.7,15,High
        P03,Control,2,8.9,5,Low
        P04,Treatment,4,38.2,12,Moderate
        P05,Control,3,15.1,9,Moderate
        P06,Treatment,5,52.3,18,High
        P07,Control,1,6.2,3,Low
        P08,Treatment,4,41.8,14,High
        P09,Control,2,11.7,7,Low
        P10,Treatment,5,48.9,16,High
        P11,Control,3,13.8,10,Moderate
        P12,Treatment,4,39.5,13,Moderate
        P13,Control,2,9.4,6,Low
        P14,Treatment,5,46.1,17,High
        P15,Control,1,7.8,4,Low
        ```
        
        Perform non-parametric statistical tests:
        1. Mann-Whitney U test for group differences
        2. Kruskal-Wallis test for multiple group comparisons
        3. Spearman rank correlations
        4. Wilcoxon signed-rank test (if applicable)
        5. Chi-square test for categorical associations
        6. Effect size calculations (rank-biserial correlation)
        7. Bootstrap confidence intervals for medians
        8. Ordinal regression analysis
        """,
        task_type="statistical_testing",
        difficulty="medium",
        expected_deliverables="Non-parametric statistical analysis with rank-based tests and ordinal data modeling",
        sample_data="""participant_id,group,ordinal_rating,skewed_measure,rank_score,satisfaction_level
P01,Control,3,12.4,8,Moderate
P02,Treatment,5,45.7,15,High
P03,Control,2,8.9,5,Low
P04,Treatment,4,38.2,12,Moderate
P05,Control,3,15.1,9,Moderate
P06,Treatment,5,52.3,18,High
P07,Control,1,6.2,3,Low
P08,Treatment,4,41.8,14,High
P09,Control,2,11.7,7,Low
P10,Treatment,5,48.9,16,High
P11,Control,3,13.8,10,Moderate
P12,Treatment,4,39.5,13,Moderate
P13,Control,2,9.4,6,Low
P14,Treatment,5,46.1,17,High
P15,Control,1,7.8,4,Low""",
        success_criteria=[
            "Performs Mann-Whitney U test correctly",
            "Conducts Kruskal-Wallis analysis",
            "Calculates Spearman correlations",
            "Applies appropriate signed-rank tests",
            "Performs chi-square tests for associations",
            "Calculates non-parametric effect sizes",
            "Generates bootstrap confidence intervals",
            "Conducts ordinal regression appropriately"
        ]
    )
]



# Combine all test cases
ALL_CODER_TEST_CASES = (
    DATA_ANALYSIS_CASES + 
    VISUALIZATION_CASES + 
    DATA_PROCESSING_CASES + 
    ALGORITHM_CASES + 
    DEBUGGING_CASES +
    STATISTICAL_TESTING_CASES
)

# Test case counts for verification
def get_test_case_summary():
    """Return summary of test cases by category."""
    return {
        "Data Analysis": len(DATA_ANALYSIS_CASES),
        "Visualization": len(VISUALIZATION_CASES), 
        "Data Processing": len(DATA_PROCESSING_CASES),
        "Algorithm": len(ALGORITHM_CASES),
        "Debugging": len(DEBUGGING_CASES),
        "Statistical Testing": len(STATISTICAL_TESTING_CASES),
        "Total": len(ALL_CODER_TEST_CASES)
    }

# Quick access functions
def get_test_case_by_id(test_id: str) -> CoderTestCase:
    """Get a specific test case by its ID."""
    for test_case in ALL_CODER_TEST_CASES:
        if test_case.id == test_id:
            return test_case
    raise ValueError(f"Test case with ID '{test_id}' not found")

def get_test_cases_by_difficulty(difficulty: str) -> list[CoderTestCase]:
    """Get all test cases of a specific difficulty level."""
    return [tc for tc in ALL_CODER_TEST_CASES if tc.difficulty == difficulty]

def get_test_cases_by_type(task_type: str) -> list[CoderTestCase]:
    """Get all test cases of a specific task type."""
    return [tc for tc in ALL_CODER_TEST_CASES if tc.task_type == task_type]

def get_dataset_summary() -> dict[str, any]:
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