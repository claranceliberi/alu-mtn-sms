# MoMo Data Analysis Dashboard

A fullstack application for analyzing and visualizing MTN MoMo SMS transaction data. This project demonstrates backend data processing, database management, and interactive frontend dashboard development.

---

## Project Structure

```
mtn/
├── backend/
│   ├── api.py                # FastAPI backend for serving data
│   ├── process_momo_sms.py   # Script to parse and process the XML file
│   ├── momo_sms.db           # SQLite database with processed transactions
│   ├── mom-mtn.xml           # Source XML file with SMS data
│   └── unprocessed_sms.log   # Log of unprocessed/uncategorized messages
├── frontend/
│   ├── index.html            # Dashboard UI
│   ├── style.css             # Dashboard styling
│   ├── main.js               # Dashboard logic and data fetching
│   └── sample_data.json      # Demo data (optional)
├── pyproject.toml            # Poetry dependency management
├── poetry.lock               # Poetry lock file
└── README.md                 # Project documentation
```

---

## Setup Instructions

### 1. Install Dependencies

This project uses [Poetry](https://python-poetry.org/) for Python dependency management. If Poetry is not installed:

```sh
pip install poetry
```

Then, from the project root:

```sh
poetry install
```

### 2. Process the XML Data

Parse and load the SMS data into the SQLite database:

```sh
poetry run python backend/process_momo_sms.py
```

### 3. Run the Backend API

Start the FastAPI server to serve transaction data:

```sh
poetry run uvicorn backend.api:app --reload
```

The API will be available at [http://localhost:8000/api/transactions](http://localhost:8000/api/transactions).

### 4. Run the Frontend Dashboard

**Recommended:** Serve the frontend using a local HTTP server for full functionality.

```sh
cd frontend
python3 -m http.server 8080
```

Then open [http://localhost:8080](http://localhost:8080) in your browser.

### 5. Usage
- Use the dashboard to filter, search, and visualize your MoMo transaction data.
- Click on any row to see transaction details.

---

## Features
- **Data Cleaning & Categorization:** Parses and cleans raw SMS messages, categorizing them by transaction type.
- **Database Storage:** Stores structured data in SQLite for easy querying.
- **API Backend:** FastAPI serves data to the frontend with filtering support.
- **Interactive Dashboard:** HTML/JS dashboard with filters, search, and visualizations (Chart.js).
- **Logging:** Unprocessed/uncategorized messages are logged for review.

---

## Authors
- Your Name (edit this section)

---

## License
MIT License (or your preferred license)
