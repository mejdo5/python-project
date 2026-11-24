import yfinance as yf
import pandas as pd

COMPANIES = {
    "Kering":    "KER.PA",
    "LVMH":      "MC.PA",
    "Hermès":    "RMS.PA",
    "Richemont": "CFR.SW",
    "Prada":     "1913.HK",
    "Moncler":   "MONC.MI",
}
YEARS = [2021, 2022, 2023, 2024, 2025]


def year_end_closes(tk):
    """Dernier cours de clôture (non ajusté) de chaque année."""
    h = tk.history(start="2021-01-01", auto_adjust=False)
    h.index = h.index.tz_localize(None)
    return {
        f"Cours fin {y}": (h.loc[h.index.year == y, "Close"].iloc[-1]
                           if (h.index.year == y).any() else None)
        for y in YEARS
    }

rows = []
for name, ticker in COMPANIES.items():
    tk = yf.Ticker(ticker)
    info = tk.info
    row = {
        "Entreprise": name,
        "Ticker": ticker,
        "Devise": info.get("currency"),
        "stock price": info.get("currentPrice") or info.get("regularMarketPrice"),
        "Capitalization": info.get("marketCap"),
        "Nb of shares": info.get("sharesOutstanding"),
        "Entreprise value (EV)": info.get("enterpriseValue"),
        "Bêta": info.get("beta"),
        "Dividende per share": info.get("dividendRate")
                                              or info.get("trailingAnnualDividendRate"),
    }
    row.update(year_end_closes(tk))
    rows.append(row)

df = pd.DataFrame(rows).set_index("Entreprise")
pd.set_option("display.width", 250, "display.max_columns", None)
print(df.T)

df.to_excel("donnees_boursieres_luxe.xlsx")
print("\nFichier créé : donnees_boursieres_luxe.xlsx")