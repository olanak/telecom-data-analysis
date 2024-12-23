Telecom Data Analysis Project
=========================================
A data-driven analysis of telecom user engagement, experience, and satisfaction using PostgreSQL, MySQL, and Python visualization tools.

-----------------------------------------
🚀 Project Overview
-----------------------------------------
This project focuses on analyzing telecom data to extract valuable insights into user behavior, network experience, and overall satisfaction. The analysis spans across multiple tasks, with the final output visualized in an interactive Streamlit dashboard.

-----------------------------------------
🔧 Technologies Used
-----------------------------------------
- Python 3.12
- PostgreSQL – Primary data source
- MySQL – User satisfaction data storage
- Streamlit – Interactive dashboard for data visualization
- Pandas, Seaborn, Matplotlib – Data processing and plotting
- SQLAlchemy – Database connectivity and querying
- scikit-learn – Clustering and machine learning models

-----------------------------------------
📂 Project Structure
-----------------------------------------
telecom-data-analysis/
│
├── data/                    # Raw and processed datasets
│   ├── raw/                 # Original CSV and SQL files
│   └── processed/           # Cleaned data for modeling
│
├── notebooks/               # Jupyter notebooks for data exploration
│
├── src/                     # Source code for analysis and dashboard
│   ├── db_connection.py     # PostgreSQL connection handler
│   ├── mysql_connection.py  # MySQL connection handler
│   ├── user_overview.py     # Task 1 - User Overview Analysis
│   ├── user_engagement.py   # Task 2 - Engagement Analysis
│   ├── experience_analysis.py  # Task 3 - Experience Analysis
│   ├── satisfaction_analysis.py  # Task 4 - Satisfaction Analysis
│   └── dashboard.py         # Task 5 - Streamlit dashboard
│
└── README.txt

-----------------------------------------
📈 Tasks Breakdown
-----------------------------------------
Task 1: User Overview Analysis
- Analyze handset types and manufacturers.
- Identify the top 10 handsets and top 3 manufacturers.
- Visualize results through bar plots.

Task 2: User Engagement Analysis
- Aggregate user session frequency and duration.
- Use clustering (K-means) to segment users by engagement levels.
- Visualize engagement distribution.

Task 3: Experience Analysis
- Calculate network experience metrics (RTT, throughput).
- Cluster users based on experience.
- Highlight outliers and frequent users.

Task 4: Satisfaction Analysis
- Assign engagement and experience scores to users.
- Derive satisfaction scores using regression models.
- Export results to MySQL.

Task 5: Dashboard Development
- Develop a multi-page Streamlit dashboard.
- Visualize insights across user engagement, experience, and satisfaction.

-----------------------------------------
🖥️ How to Run the Project
-----------------------------------------
1. Clone the Repository
    git clone https://github.com/olanak/telecom-data-analysis.git
    cd telecom-data-analysis

2. Set Up Virtual Environment
    python3.12 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

3. Configure PostgreSQL and MySQL
- Ensure PostgreSQL and MySQL databases are running.
- Update db_connection.py and mysql_connection.py with your credentials.

4. Run Analysis Scripts
    python src/user_overview.py
    python src/user_engagement.py
    python src/experience_analysis.py
    python src/satisfaction_analysis.py

5. Launch Streamlit Dashboard
    streamlit run src/dashboard.py

-----------------------------------------
⚙️ Environment Variables
-----------------------------------------
- POSTGRES_USER
- POSTGRES_PASSWORD
- MYSQL_USER
- MYSQL_PASSWORD

Store these in a .env file or export them directly in your shell.

-----------------------------------------
📊 Dashboard Preview
-----------------------------------------
Access the interactive dashboard to visualize all analysis results:
    http://localhost:8501

-----------------------------------------
📄 License
-----------------------------------------
This project is licensed under the MIT License.

