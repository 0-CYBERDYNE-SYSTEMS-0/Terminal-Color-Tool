---
name: ai-data-analyst
description: Perform comprehensive data analysis, statistical modeling, and create publication-quality visualizations using Python and the full data science ecosystem. Use when you need deep data insights, statistical analysis, or visual storytelling from datasets.
---
# Skill: AI Data Analyst

## Purpose

Perform comprehensive data analysis, statistical modeling, and create publication-quality visualizations using Python and the full data science ecosystem. This skill handles everything from data cleaning and exploratory analysis to advanced modeling and visual storytelling.

## When to use this skill

- You need **deep data insights** and statistical analysis from datasets.
- You want to create **publication-quality visualizations** and reports.
- The analysis requires **statistical modeling**, hypothesis testing, or machine learning.
- You need to handle complex data transformation and cleaning workflows.
- You want to generate reproducible analysis notebooks and reports.

## Key capabilities

- **Data exploration**: Identify patterns, outliers, and relationships in data
- **Statistical analysis**: Hypothesis testing, correlation analysis, regression models
- **Machine learning**: Classification, clustering, and predictive modeling
- **Visualization**: Publication-quality charts, graphs, and interactive dashboards
- **Data cleaning**: Handle missing values, outliers, and data type issues
- **Report generation**: Create comprehensive analysis reports with code and insights

## Inputs

- **Dataset(s)**: File paths or database connections to the data sources
- **Analysis objectives**: What questions you want to answer or hypotheses to test
- **Data format/type**: CSV, JSON, database tables, or other data formats
- **Output requirements**: Preferred visualization types, report format, or delivery method
- **Constraints**: Time limits, computational resources, or specific statistical requirements

## Out of scope

- Real-time streaming analysis or production monitoring dashboards.
- Large-scale distributed data processing that requires spark clusters.
- Operational database modifications or data engineering pipeline creation.
- Handling PHI or other regulated data without proper anonymization.

## Tool ecosystem and conventions

### Primary tools (Python-based)
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing and array operations  
- **matplotlib/seaborn**: Statistical visualization and plotting
- **plotly**: Interactive visualizations and dashboards
- **scikit-learn**: Machine learning and statistical modeling
- **scipy**: Scientific computing and statistical tests
- **jupyter**: Interactive notebooks and analysis workflows

### Statistical methods
- **Descriptive statistics**: Summarize data distributions and central tendencies
- **Inferential statistics**: Hypothesis testing and confidence intervals
- **Regression analysis**: Linear, logistic, and other regression models
- **Time series analysis**: Trend analysis, seasonality, and forecasting
- **Clustering**: Unsupervised learning for pattern discovery
- **Classification**: Supervised learning for prediction tasks

## Required behavior

1. **Data validation**: Assess data quality, identify issues, and propose solutions
2. **Exploratory analysis**: Generate initial insights and guide further analysis
3. **Statistical rigor**: Apply appropriate methods with proper assumptions and tests
4. **Visualization best practices**: Choose appropriate chart types and design principles
5. **Reproducible workflows**: Create well-documented Jupyter notebooks or scripts
6. **Clear communication**: Translate technical findings into actionable insights

## Required artifacts

- **Jupyter notebook(s)** with reproducible analysis workflow
- **Data cleaning scripts** for data preparation and validation
- **Statistical analysis code** with proper methodology documentation
- **Visualization files** (PNG/SVG for static, HTML for interactive)
- **Analysis report** summarizing findings, limitations, and recommendations
- **requirements.txt** with all Python dependencies for reproducibility

## Implementation checklist

### 1. Data assessment and preparation
- [ ] Load and inspect dataset structure and metadata
- [ ] Identify data quality issues (missing values, outliers, inconsistencies)
- [ ] Document data schema and variable descriptions
- [ ] Perform data cleaning and validation procedures

### 2. Exploratory data analysis
- [ ] Generate descriptive statistics and summary tables
- [ ] Create appropriate univariate visualizations (histograms, box plots)
- [ ] Examine relationships between variables (correlations, scatter plots)
- [ ] Identify patterns, trends, and potential anomalies

### 3. Statistical modeling and analysis
- [ ] Formulate hypotheses and research questions
- [ ] Select appropriate statistical methods and models
- [ ] Perform statistical tests with proper assumptions checking
- [ ] Validate model performance and assess uncertainty

### 4. Visualization and reporting
- [ ] Create publication-quality visualizations with proper labeling
- [ ] Generate interactive dashboards for data exploration
- [ ] Produce comprehensive analysis report with methodology
- [ ] Document limitations and suggest further analysis

### 5. Quality assurance and reproducibility
- [ ] Review code quality and add documentation
- [ ] Test analysis on holdout data or validation sets
- [ ] Verify statistical assumptions and model diagnostics
- [ ] Create requirements.txt and setup instructions

## Verification

Run the following validation steps:

```bash
# Install dependencies
pip install -r requirements.txt

# Execute analysis (adjust command based on workflow)
jupyter nbconvert --to html --execute analysis.ipynb
# OR
python analysis_script.py

# Validate data pipeline
python -c "import pandas as pd; df = pd.read_csv('data.csv'); print(df.shape, df.columns.tolist())"

# Check visualizations
ls -la figures/ output/
```

The skill is complete when:

- All analysis code runs without errors or warnings.
- Statistical methods are applied correctly with proper assumptions.
- Visualizations are clear, accurate, and publication-ready.
- Findings are well-documented with methodology and limitations.
- The workflow is reproducible from the provided artifacts.

## Statistical best practices

### Experimental design
- Define clear hypotheses and success criteria before analysis
- Consider sample size requirements and statistical power
- Control for confounding variables and biases
- Use appropriate experimental designs for the research question

### Data analysis methodology
- Document all data transformations and cleaning steps
- Perform sensitivity analysis for robustness checking
- Address missing data appropriately rather than deleting
- Validate assumptions of statistical tests and models

### Visualization principles
- Choose chart types that accurately represent the data relationships
- Use appropriate scales and axis ranges
- Include clear labels, legends, and annotations
- Avoid chart junk and misleading visual elements

## Communication and reporting

### Analysis structure
1. **Executive summary**: Key findings and business implications
2. **Methodology**: Data sources, cleaning, and analytical approaches
3. **Results**: Detailed findings with supporting visualizations
4. **Limitations**: Data constraints and methodological caveats
5. **Recommendations**: Actionable insights and next steps

### Technical documentation
- Code comments explaining analytical decisions
- Data dictionaries and variable definitions
- Statistical test results with p-values and confidence intervals
- Model performance metrics and validation procedures

## Safety and ethical considerations

- **Data privacy**: Never include personally identifiable information in results
- **Statistical integrity**: Avoid p-hacking or data dredging
- **Transparency**: Document all assumptions and methodological choices
- **Limitations**: Clearly communicate uncertainty and caveats
- **Bias awareness**: Consider potential sources of bias in data and analysis

## Integration with other skills

This skill can be combined with:

- **Data querying**: For fetching data from databases and APIs
- **Internal tools**: When building data analysis dashboards for internal teams
- **Product management**: For feature analysis and user behavior insights
- **Service integration**: When analysis needs to process live data from services

## Example workflows

### Customer behavior analysis
```
User: "Analyze customer purchase patterns to identify high-value segments"

AI Data Analyst will:
1. Load customer transaction data and validate structure
2. Calculate RFM metrics (recency, frequency, monetary)
3. Perform clustering analysis to identify customer segments
4. Create visualizations of segment characteristics and behavior
5. Generate recommendations for targeted marketing strategies
6. Produce comprehensive report with methodology and limitations
```

### A/B test analysis
```
User: "Analyze the results of our recent feature A/B test"

AI Data Analyst will:
1. Load experiment data and validate experimental design
2. Perform statistical significance testing for key metrics
3. Calculate confidence intervals and effect sizes
4. Create visualizations of treatment vs control performance
5. Assess statistical power and minimum detectable effect
6. Provide recommendations based on experimental outcomes
```

### Time series forecasting
```
User: "Forecast monthly revenue for the next 6 months"

AI Data Analyst will:
1. Load historical revenue data and check for seasonality
2. Decompose time series into trend, seasonal, and residual components
3. Fit appropriate forecasting models (ARIMA, exponential smoothing)
4. Validate model using cross-validation and backtesting
5. Generate forecasts with confidence intervals
6. Create interactive dashboard for scenario analysis
```
