import xml.etree.ElementTree as ET
import re
import sqlite3
import logging
from datetime import datetime

# Logging setup
logging.basicConfig(filename='unprocessed_sms.log', level=logging.INFO, format='%(message)s')

# Define SMS categories and their regex patterns
CATEGORIES = {
    'incoming_money': r'You have received (\d+[,.]?\d*) RWF from',
    'payment_to_code_holder': r'Your payment of (\d+[,.]?\d*) RWF to [A-Za-z ]+ \d+',
    'transfer_to_mobile': r'(\d+[,.]?\d*) RWF transferred to [A-Za-z ]+ \([0-9]+\)',
    'bank_deposit': r'bank deposit of (\d+[,.]?\d*) RWF',
    'airtime_bill': r'payment of (\d+[,.]?\d*) RWF to Airtime',
    'cash_power_bill': r'payment of (\d+[,.]?\d*) RWF to Cash Power',
    'third_party': r'A transaction of (\d+[,.]?\d*) RWF by [A-Za-z ]+ on your MOMO account',
    'withdrawal_agent': r'withdrawn (\d+[,.]?\d*) RWF',
    'bank_transfer': r'External Transaction Id',
    'bundle_purchase': r'You have purchased an internet bundle',
}

DB_FILE = 'momo_sms.db'
XML_FILE = 'mom-mtn.xml'

# Database schema
SCHEMA = '''
CREATE TABLE IF NOT EXISTS sms_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    amount INTEGER,
    sender TEXT,
    receiver TEXT,
    date TEXT,
    description TEXT,
    raw_body TEXT
);
'''

def parse_amount(text):
    match = re.search(r'(\d+[,.]?\d*)\s*RWF', text)
    if match:
        return int(match.group(1).replace(',', ''))
    return None

def parse_date(text):
    # Try to find a date in the format YYYY-MM-DD HH:MM:SS
    match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', text)
    if match:
        return match.group(1)
    return None

def categorize_sms(body):
    for category, pattern in CATEGORIES.items():
        if re.search(pattern, body):
            return category
    return 'unknown'

def extract_info(body, category):
    amount = parse_amount(body)
    date = parse_date(body)
    sender = receiver = None
    # Extract sender/receiver details for certain categories
    if category == 'incoming_money':
        m = re.search(r'from ([A-Za-z ]+)', body)
        if m:
            sender = m.group(1).strip()
    elif category in ('payment_to_code_holder', 'transfer_to_mobile'):
        m = re.search(r'to ([A-Za-z ]+)', body)
        if m:
            receiver = m.group(1).strip()
    return amount, sender, receiver, date

def main():
    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(SCHEMA)

    for sms in root.findall('sms'):
        body = sms.attrib.get('body', '')
        category = categorize_sms(body)
        amount, sender, receiver, date = extract_info(body, category)
        if category == 'unknown' or amount is None:
            logging.info(body)
            continue
        c.execute('''INSERT INTO sms_transactions (category, amount, sender, receiver, date, description, raw_body) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (category, amount, sender, receiver, date, body, body))
    conn.commit()
    conn.close()
    print('Processing complete. Check unprocessed_sms.log for ignored messages.')

if __name__ == '__main__':
    main()
