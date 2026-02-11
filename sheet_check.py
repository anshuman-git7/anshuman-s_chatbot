# import pandas as pd
# import requests
# from io import StringIO
# from datetime import datetime

# SHEET_URL = "https://docs.google.com/spreadsheets/d/1D6SAxXLiwyaYd5vMY7Li30MUpqA3-vQpiWqw5Nnm4Ls/export?format=csv"

# # Download CSV
# response = requests.get(SHEET_URL)
# response.raise_for_status()

# # Load into DataFrame
# df = pd.read_csv(StringIO(response.text))

# # Clean column names
# df.columns = df.columns.str.strip()

# # 🔑 Convert Date column to datetime
# df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# # Get today's date (date object, not string)
# today = datetime.today().date()

# # Compare properly
# today_row = df[df["Date"].dt.date == today]

# if today_row.empty:
#     print("No word scheduled for today.")
# else:
#     print("Today's word:")
#     print(today_row[["Word", "Meaning"]])

import pandas as pd
import requests
from datetime import datetime
import pytz

# =========================
# TELEGRAM CONFIG
# =========================
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")




# =========================
# GOOGLE SHEET CSV URL
# =========================
CSV_URL = "https://docs.google.com/spreadsheets/d/1D6SAxXLiwyaYd5vMY7Li30MUpqA3-vQpiWqw5Nnm4Ls/export?format=csv"


def get_todays_word():
    df = pd.read_csv(CSV_URL)

    # normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # convert date column
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    ist = pytz.timezone("Asia/Kolkata")
    today = datetime.now(ist).date()


    today_row = df[df["date"].dt.date == today]

    if today_row.empty:
        return None

    word = today_row.iloc[0]["word"]
    meaning = today_row.iloc[0]["meaning"]

    return word, meaning


def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()


# =========================
# MAIN EXECUTION
# =========================
if __name__ == "__main__":
    result = get_todays_word()

    if result is None:
        message = "❌ No word scheduled for today."
    else:
        word, meaning = result
        message = (
            "📘 *Word of the Day*\n\n"
            f"🔤 *Word:* {word}\n"
            f"📖 *Meaning:* {meaning}"
        )

    print(message)
    send_telegram_message(message)
