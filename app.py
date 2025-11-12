import streamlit as st
import sqlite3

# --- Function to initialize DB if missing ---
def setup_database():
    conn = sqlite3.connect("currency.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exchange_rates (
            currency_code TEXT PRIMARY KEY,
            rate_to_inr REAL
        )
    """)

    # Add some example data if the table is empty
    cursor.execute("SELECT COUNT(*) FROM exchange_rates")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO exchange_rates (currency_code, rate_to_inr)
            VALUES (?, ?)
        """, [
            ("USD", 83.2),
            ("EUR", 90.5),
            ("GBP", 105.3),
            ("JPY", 0.56),
            ("INR", 1.0)
        ])
        conn.commit()
    conn.close()

# --- Function to fetch rates from the database ---
def get_exchange_rates():
    conn = sqlite3.connect("currency.db")
    cursor = conn.cursor()
    cursor.execute("SELECT currency_code, rate_to_inr FROM exchange_rates")
    data = cursor.fetchall()
    conn.close()
    return {code: rate for code, rate in data}

# --- Currency conversion function ---
def convert_currency(amount, from_currency, to_currency, rates):
    if from_currency not in rates or to_currency not in rates:
        return None
    # Convert to INR then to target currency
    amount_in_inr = amount * rates[from_currency]
    converted = amount_in_inr / rates[to_currency]
    return converted

# --- Streamlit UI ---
st.set_page_config(page_title="Currency Converter", page_icon="💱", layout="centered")

st.title("💱 Currency Converter")
st.write("Easily convert between different world currencies using live stored rates!")

# Setup database (creates table & inserts sample data if missing)
setup_database()

# Load currency data
rates = get_exchange_rates()
currencies = list(rates.keys())

# --- Input fields ---
col1, col2 = st.columns(2)
with col1:
    from_currency = st.selectbox("Convert from:", currencies)
with col2:
    to_currency = st.selectbox("Convert to:", currencies)

amount = st.number_input("Enter amount:", min_value=0.0, step=0.1)

# --- Conversion ---
if st.button("Convert"):
    result = convert_currency(amount, from_currency, to_currency, rates)
    if result is not None:
        st.success(f"💰 {amount:.2f} {from_currency} = {result:.2f} {to_currency}")
    else:
        st.error("Invalid currency selection!")

# --- Footer ---
st.markdown("---")
st.caption("🌍 Made with Streamlit & SQLite | Example project by Narasimha")