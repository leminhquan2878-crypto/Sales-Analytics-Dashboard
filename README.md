#Sales Analytics Dashboard

A data analysis application built with **Python** and **Streamlit** to analyze sales data for an electronics store. This dashboard automates the process of merging monthly sales reports, cleaning data, and visualizing key business KPIs to support decision-making.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-red)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green)

##Overview

In the retail industry, analyzing large datasets manually is time-consuming and error-prone. This project solves that problem by:
1.  **Automating Data Processing:** Merging 12 separate CSV files (representing 12 months of sales in 2019) into a single unified dataset with over **186,000 records**.
2.  **Data Cleaning:** Handling missing values (NaN), removing invalid headers, and formatting data types.
3.  **Visualization:** Providing an interactive dashboard to explore sales trends, best-selling products, and peak shopping hours.

## Key Features

* **Automated Data Merging:** Reads and concatenates multiple CSV files from a directory automatically.
* **Data Cleaning & Preprocessing:**
    * Removes `NaN` values and duplicate headers.
    * Converts columns to correct data types (Numeric, DateTime).
    * Calculates new metrics: `Total Sales = Quantity * Price`.
* **Interactive Visualizations:**
    * **Monthly Sales:** Identify the best performing months (e.g., December).
    * **Sales by City:** Analyze which regions have the highest revenue (e.g., San Francisco).
    * **Hourly Analysis:** Discover "Golden Hours" for advertising (Peak times: 12 PM & 7 PM).
    * **Product Insights:** Top selling products and "Combo" analysis (products frequently bought together).

## Tech Stack

* **Language:** Python 3.10
* **Web Framework:** Streamlit
* **Data Processing:** Pandas, OS
* **Visualization:** Matplotlib

## Screenshots

*(Place your dashboard screenshots here. E.g., `images/dashboard_overview.png`)*

> **Sample Insight:** The data shows that **San Francisco** has the highest sales volume, and the peak shopping time is between **19:00 - 21:00**, suggesting this is the best time for targeted ads.

## Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/leminhquan2878-crypto/Sales-Analytics-Dashboard.git](https://github.com/leminhquan2878-crypto/Sales-Analytics-Dashboard.git)
    cd Sales-Analytics-Dashboard
    ```

2.  **Install dependencies:**
    ```bash
    pip install pandas matplotlib streamlit
    ```

3.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

4.  **Upload Data:**
    * On the sidebar, upload the CSV files from the `Data/` folder.
    * The dashboard will automatically process and display the insights.

## Project Structure

```text
sales-analytics-dashboard/
├── Data/                   # Contains 12 CSV files (Sales_January_2019.csv, etc.)
├── app.py                  # Main Streamlit application code
└── README.md               # Project documentation

