# CSV Data Analyser – Python & Pandas
A command-line data analysis tool built with Python, designed to load, clean, analyse, and visualize CSV datasets — developed as a learning project to practice data handling, error management, and visualization with real-world libraries.
 
## ✨ | Features
* Load CSV files with any delimiter (`,` `;` `\t` `|`) via interactive prompts
* Preview raw data and inspect column-level metadata including data types and NaN counts
* Data cleaning pipeline: drop/fill missing values, remove duplicates, strip whitespace, fix data types
* Numerical analysis: sum, mean, median, mode, min, max, standard deviation per column
* Categorical analysis: unique values, missing values, frequency distribution, cardinality rating
* Chart generation via Matplotlib & Seaborn (histogram + boxplot for numerical, bar chart for categorical)
* Save the cleaned dataset to a new CSV file via a native file dialog
* Robust input validation and error handling throughout all menu interactions
## 🛠️ | Technologies & Libraries
* ``pandas`` - Data loading, cleaning, and analysis
* ``matplotlib`` - Chart rendering with TkAgg backend
* ``seaborn`` - Statistical plot styling and generation
* ``tkinter`` - Native file save dialog
* ``sys`` - Controlled program termination
## 📁 | Project Structure
```
csv-data-analyser/
│
├── main.py          # Entry point and all core logic
└── requirements.txt # Required packages
```
 
## 🚀 | Installation
 
1. Clone the repository
```bash
   git clone https://github.com/YOUR_USERNAME/csv-data-analyser.git
   cd csv-data-analyser
```
 
2. Install required packages
```bash
   pip install -r requirements.txt
```
 
3. Run the application
```bash
   python main.py
```
 
## 🗂️ | Usage
 
After launching, you will be prompted to enter the file path of your CSV file and its delimiter. The tool then validates the input and opens an interactive menu:
 
```
===========================================
1. View CSV file (preview of raw data)
2. Display basic information (Metadata)
3. Data cleaning options
4. Numerical analysis (if numbers detected)
5. Categorical analysis
6. Create graphic (via Matplotlib/Seaborn)
7. Save cleaned data
8. Exit
-- Press number to continue:
```
 
All inputs are validated — invalid entries (wrong type, out of range) are caught and handled gracefully without crashing the program.
 
## 🧹 | Data Cleaning Options
 
| Option | Description |
|---|---|
| Drop missing values | Removes all rows containing NaN |
| Fill missing values | Fills NaN with median (numerical) or `"Unknown"` (text) |
| Remove duplicates | Drops exact duplicate rows |
| Strip whitespaces | Trims leading/trailing spaces in string columns |
| Fix data types | Converts columns to int, float, datetime, boolean, or category |
 
## 📊 | Visualization
 
Charts open in a dedicated window using the TkAgg backend. Supported chart types:
 
* **Numerical columns** – Distribution histogram with KDE curve + boxplot side by side
* **Categorical columns** – Bar chart with frequency distribution and rotated axis labels
## 📕 | Notes
* Developed using Python 3.x and PyCharm
* The TkAgg backend is set explicitly to ensure chart windows render correctly across environments
* This is an ongoing learning project focused on real-world data workflows
## 🪲 | Bugs
* Feel free to report any bugs
