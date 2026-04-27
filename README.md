# 🧹 Data Cleaner App (Streamlit)

A simple and interactive data cleaning web application built using **Streamlit**, **Pandas**, and **NumPy**. This tool allows users to upload datasets and perform common preprocessing tasks without writing code.

---

## 🚀 Features

### 📂 File Upload

* Supports **CSV** and **Excel (.xlsx)** files
* Automatically reads and previews uploaded data

### 👀 Data Preview

* Displays dataset in an interactive table
* Keeps state across operations using `st.session_state`

### ✏️ Column Renaming

* Rename columns interactively using a slider-based navigation
* Changes are stored and applied later

### 📊 Data Insights

Choose from:

* **Info of Data** (data types, non-null counts)
* **Statistics of Data** (summary statistics)
* **Null Values Count** (per column)

### 🔄 Data Type Management

For each column, you can:

* Keep original type
* Convert to `int`, `float`, `string`, or `datetime`
* Drop unwanted columns

### 🧼 Missing Value Handling

Options available per column:

* Keep as-is
* Drop rows with nulls
* Fill with:

  * Mean
  * Median
  * Mode
  * Forward fill
  * Backward fill
  * Custom value

### ✅ Apply All Changes

* Applies all transformations in one click:

  * Column renaming
  * Column dropping
  * Data type conversions
  * Missing value handling
* Updates dataset and refreshes UI

---

## 🛠️ Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/data-cleaner.git
cd data-cleaner
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

---

## 📦 Requirements

* streamlit
* pandas
* numpy
* matplotlib
* seaborn

---

## 🧠 How It Works

* Uses `st.session_state` to persist user selections
* All transformations are staged and applied together
* Prevents data loss by working on a copy of the original dataset

---

## ⚠️ Notes

* Invalid conversions are safely handled using `errors='coerce'`
* Dropped columns are excluded from further processing
* Null handling is applied only to existing columns after transformations

---

## 📌 Future Improvements

* Download cleaned dataset
* Data visualization dashboard
* Undo/redo functionality
* Auto data cleaning suggestions
* Column filtering and sorting

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss your ideas.

---
