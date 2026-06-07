# Monobank ETL: End-to-End Data Pipeline & Advanced Analytics

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15.0+-336791.svg?logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811.svg?logo=powerbi&logoColor=black)
![Machine Learning](https://img.shields.io/badge/Machine_Learning-Scikit_Learn-F7931E.svg?logo=scikit-learn&logoColor=white)

## Project Overview
**Monobank ETL** is a comprehensive, automated Data Engineering and Analytics pipeline. It extracts raw personal financial data via the Monobank API, transforms it using Python, securely stores it in a PostgreSQL database, and leverages Machine Learning (K-Means, Isolation Forest) alongside an interactive Power BI dashboard to generate deep behavioral insights.

The goal of this project was to build a production-ready system to track spending pacing, detect financial anomalies, and calculate dynamic financial runways without relying on third-party budgeting apps.

---

## Architecture & Technical Decisions

I designed the system using a modular architecture to ensure scalability, reliability, and clear separation of concerns (adhering to SOLID principles).

* **Extraction:** A robust API client handles HTTP 429 Rate Limits and fetches raw JSON data.
* **Transformation:** Pandas cleans the data, converts UNIX timestamps, and maps MCC codes to 70+ business categories.
* **Loading:** SQLAlchemy manages PostgreSQL sessions using `session.merge()` for safe upserts, preventing data duplication during daily automated runs.
* **Automation:** A Windows Batch script integrated with Task Scheduler runs the ETL process daily at 23:00, logging outputs to `etl_sync.log`.

**Why offline-first?** By storing transactions in a local PostgreSQL database, the Machine Learning models and Power BI dashboard can perform heavy calculations instantly, completely bypassing the Monobank API rate limits and potential network outages.

---

## Key Results & Analytics

### 1. Interactive BI Dashboard (Power BI)
I built a dynamic BI interface to replace standard banking apps. 
* **Dynamic Budgeting:** Built complex DAX measures using `DATESINPERIOD` to calculate a 3-month moving average, creating a dynamic pacing budget.
* **Spending Heatmap:** A day-and-time cohort matrix highlights routine spending clusters.
* **Custom Tooltips:** Hovering over the heatmap triggers a hidden Donut chart detailing exact categories for that specific hour.

![PowerBi Dashboard](images/PoweBiDashboard.png)

### 2. Behavioral Segmentation (K-Means Clustering)
To move beyond basic categories, I applied **K-Means Clustering** to identify latent spending "personas".
* Features used: Normalized Amount, Hour of Day, Day of Week.
* Using the Elbow Method, the model identified **4 optimal clusters** (e.g., "Weekday Morning Coffee," "Weekend Grocery Runs," "Rare Large Transfers").

![Elbow Method Plot](images/Elbow.png)

![3D Cluster Plot](images/3d_cluster.png)

### 3. Anti-Fraud & Irregular Spending (Isolation Forest)
Instead of hardcoding thresholds, I deployed an **Isolation Forest** unsupervised algorithm (0.03 contamination) to automatically flag the top 3% of anomalous transactions. 
* The model successfully isolated rare events based on a multi-dimensional context (e.g., an unusually large purchase for a specific merchant at 3:00 AM).

![Anomaly Detection Results](images/Anomalies.png)

### 4. Predictive Financial Runway (Burn Rate)
Calculated the actual 30-day average daily burn rate to project the exact "Zero Cash Date". The model pulls the absolute latest balance directly from the raw database snapshot, ensuring predictions are perfectly synchronized with the transaction history.

![Runway Projection](images/Runway.png)

### 5. Habit Volatility & Routine Detection (Time Series)
Conducted a Time Series analysis on transaction intervals to distinguish between rigid lifestyle habits and spontaneous purchases using the **Coefficient of Variation (CV)**.
* **Findings:** The mathematical analysis revealed a high interval volatility across most frequent merchants (high CV scores). This data-driven insight confirmed that the spending behavior is predominantly dynamic and spontaneous rather than strictly scheduled or routine-based, preventing false assumptions about predictable spending habits.

![Routine Analysis](images/Routines.png)
---

## Project Structure

```text
Monobank_ETL_Pipeline/
│
├── dashboards/
│   └── finance_xray_dashboard.pbix         # The final BI interface connected to PostgreSQL
│
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb  # EDA, statistical summaries, time-series analysis
│   └── 02_machine_learning.ipynb           # K-Means, Isolation Forest, Burn Rate models
│
├── src/                                    # ETL Backend Layer (Modular Architecture)
│   ├── api_client.py                       # Monobank API connection & HTTP error handling
│   ├── config.py                           # MCC to Category mapping dictionary
│   ├── database.py                         # SQLAlchemy Engine, Session, and ORM Models
│   ├── processor.py                        # Pandas data cleaning and transformation
│   └── sync_data.py                        # Orchestrator script executing the ETL flow
│
├── .gitignore                              # Blocks sensitive tokens and large virtual environments
├── README.md                               # Project documentation (You are here)
├── requirements.txt                        # Python dependencies for easy replication
├── run_sync.bat                            # Windows execution script for cron/Task Scheduler - Ignored by Git
├── etl_sync.log                            # Auto-generated execution log for the Task Scheduler - Ignored by Git
└── .env                                    # Environment variables (API tokens, DB credentials) - Ignored by Git
```

---

## Setup & Installation

**1. Clone the repository:**
```bash
git clone https://github.com/yourusername/Monobank_ETL_Pipeline.git
cd monobank_finance_xray
```

**2. Set up the virtual environment:**
```bash
python -m venv .venv
# Activate on Windows
.venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Environment Variables:**
Create a `.env` file in the root directory:
```env
MONOBANK_API_TOKEN=your_token_here
MONOBANK_ACCOUNT_ID=your_account_id
POSTGRES_URL=postgresql+psycopg2://user:password@localhost:5432/db_name
```

**5. Initialize Database & Run Pipeline:**
```bash
# Create tables
python -m src.database

# Execute the ETL pipeline
python -m src.sync_data
```

---

## Author
**Artem Shcherbinin**
* 2nd-year Computer Science Student at KNEU (IITE)
* Aspiring Data Analyst / Data Scientist
* Stack: Python (Pandas, Scikit-Learn, NumPy, MatPlotLib, Seaborn, Plotly), SQL (PostgreSQL, MySQL, Microsoft SQL Server), Power BI, Tableau
