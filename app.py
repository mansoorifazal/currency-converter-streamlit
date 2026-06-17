
import streamlit as st
import requests as rq
import pycountry as pyc

st.set_page_config(
    page_title="Currency Converter",
    page_icon="💱",
    layout="centered"
)

st.markdown("""
<h1 style='
text-align:center;
font-size:52px;
font-weight:800;
color:#ffffff;
letter-spacing:1px;
margin-bottom:30px;
'>
  💱  Currency Converter
</h1>
""", unsafe_allow_html=True)

st.caption(
    "Convert currencies instantly with live exchange rates"
)

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #111827 50%,
        #1e293b 100%
    );
}
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(
        135deg,
        #2563eb,
        #7c3aed
    );

    color: white;
    border: none;
    border-radius: 12px;

    font-size: 18px;
    font-weight: 600;

    height: 55px;

    transition: all 0.3s ease;
}

div[data-testid="stButton"] button[kind="primary"]:hover {
    transform: translateY(-2px);

    box-shadow:
    0px 8px 20px rgba(
        124,
        58,
        237,
        0.4
    );
}

/* Input Boxes Glass Effect */

.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    background: rgba(255, 255, 255, 0.08) !important;

    backdrop-filter: blur(12px);

    border: 1px solid rgba(255, 255, 255, 0.15) !important;

    border-radius: 12px !important;

    transition: all 0.3s ease;
}

/* Focus Effect */

.stNumberInput input:focus {
    border: 1px solid #60a5fa !important;

    box-shadow:
    0 0 15px rgba(96,165,250,0.4);
}
            
</style>
""", unsafe_allow_html=True)

# Amount Input
amount = st.number_input("ENTER AMOUNT", min_value=0.0)

# API Key
API_KEY = '47d29d6ce02e3b78375da02a'


# Sirf currencies ki list lane ke liye
url = " https://v6.exchangerate-api.com/v6/47d29d6ce02e3b78375da02a/latest/USD"
response = rq.get(url)
data = response.json()

# Currency Codes
currency_codes = list(data["conversion_rates"].keys())

custom_names = {
    "CNH": "Chinese Yuan Offshore",
    "FOK": "Faroese Króna",
    "GGP": "Guernsey Pound",
    "IMP": "Manx Pound",
    "JEP": "Jersey Pound",
    "KID": "Kiribati Dollar",
    "TVD": "Tuvalu Dollar",
    "XCG": "Caribbean Guilder",
    "ZWG": "Zimbabwe Gold",
    "XDR": "Special Drawing Right",
    "XOF": "CFA Franc BCEAO",
    "XPF": "CFP Franc"
}

currency_display = []

for code in currency_codes:
    try:
        currency = pyc.currencies.get(alpha_3=code)

        if currency:
            currency_display.append(
                f"{code} - {currency.name}"
            )

        elif code in custom_names:
            currency_display.append(
                f"{code} - {custom_names[code]}"
            )

        else:
            currency_display.append(code)

    except:
        if code in custom_names:
            currency_display.append(
                f"{code} - {custom_names[code]}"
            )
        else:
            currency_display.append(code)


# Dropdowns
from_options = ["🌍 Select Source Currency"] + currency_display
to_options =   ["🌍 Select Target Currency"] + currency_display

if "from_currency" not in st.session_state:
    st.session_state.from_currency = from_options[0]

if "to_currency" not in st.session_state:
    st.session_state.to_currency = to_options[1]

col1, col2, col3 = st.columns([2, 1, 2])

with col2:
     swap_button = st.button(
     " ⇄ Swap ",
     type="primary"
    )

if swap_button:

    temp = st.session_state.from_currency

    st.session_state.from_currency = (
        st.session_state.to_currency
    )

    st.session_state.to_currency = temp

    st.rerun()


from_currency = st.selectbox(
    "CONVERT FROM",
    from_options,
    key="from_currency"
)

to_currency = st.selectbox(
    "CONVERT TO",
    to_options,
    key="to_currency"
)

from_currency = from_currency.split(" - ")[0]
to_currency = to_currency.split(" - ")[0]

# Button
convert_button = st.button(
    "🚀 Convert Currency",
    type = "primary",
    use_container_width=True
)

# Conversion
if convert_button:

    if amount <= 0:
        st.error("⚠️ Please enter an amount greater than 0.")

    elif from_currency == "🌍 Select Source Currency":
        st.error("⚠️ Please select a source currency.")

    elif to_currency == "🌍 Select Target Currency":
        st.error("⚠️ Please select a target currency.")

    elif from_currency == to_currency:
        st.error("⚠️ Source and target currencies cannot be the same.")

    else:

        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}"

        response = rq.get(url)

        if response.status_code != 200:
            st.error("❌ Unable to connect to Exchange Rate API. Please try again later.")

        else:

            data = response.json()

            if data["result"] != "success":
                st.error("❌ API returned an invalid response.")

            else:

                rate = data["conversion_rates"][to_currency]

                converted_amount = amount * rate

                exchange_rate = rate

                st.markdown("###  Live Exchange Rate")

                st.markdown(
                    f"""
                    <div style="
                        background-color:#1f426b;
                        padding:15px;
                        border-radius:12px;
                        color:#4da3ff;
                        font-size:33px;
                    ">
                        1 {from_currency} = {exchange_rate:.5f} {to_currency}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                st.markdown("###    Conversion Result")

                st.markdown(
                    f"""
                    <div style="
                        background: rgba(34, 197, 94, 0.15);
                        backdrop-filter: blur(10px);
                        border: 1px solid rgba(74, 222, 128, 0.25);
                        border-radius: 18px;
                        padding: 25px;
                        margin-top: 15px;
                        text-align:center;
                    ">
                        <h2 style="
                            color:#4ade80;
                            margin:0;
                            font-size:30px;
                            font-weight:700;
                        ">
                            {amount:,.2f} {from_currency}
                            ➜
                            {converted_amount:,.2f} {to_currency}
                        </h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )