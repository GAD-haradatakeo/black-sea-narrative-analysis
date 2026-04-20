"""
06_civilization_analysis_labeled.py

# Description
Supplementary civilization-focused analysis responding to reviewer comments.

# Input
data/metadata/analysis_corpus_labeled.csv and data/clean/**

# Output
results/civilization_timeseries_by_country.csv
results/civilization_peak_months_russia.csv
results/civilization_top_docs_russia.csv
results/civilization_cooccurrence_russia.csv
figures/fig_value_civilization_timeseries.png
figures/fig_civilization_timeseries_comparison.png
figures/fig_civilization_timeseries_russia.png
"""
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "metadata" / "analysis_corpus_labeled.csv"
RESULTS_DIR = ROOT / "results"
FIGURES_DIR = ROOT / "figures"
RESULTS_DIR.mkdir(exist_ok=True)
FIGURES_DIR.mkdir(exist_ok=True)

CIV_PATTERNS = [
    r"\bcivilization\b",
    r"\bcivilizations\b",
    r"\bcivilizational\b",
    r"\bcivilisational\b",
]
CIV_RX = re.compile("|".join(CIV_PATTERNS), flags=re.I)
CO_TERMS = {
    "security": [r"\bsecurity\b"],
    "sovereignty": [r"\bsovereignty\b"],
    "international_law": [r"\binternational law\b"],
    "democracy": [r"\bdemocracy\b", r"\bdemocratic\b"],
    "human_rights": [r"\bhuman rights\b"],
    "rules_based": [r"\brules[- ]based\b", r"\brules based\b"],
    "multipolarity": [r"\bmultipolarity\b", r"\bmultipolar\b"],
}
CO_RX = {k: re.compile("|".join(v), flags=re.I) for k, v in CO_TERMS.items()}
TARGET_COUNTRIES = ["Russia", "Ukraine", "Georgia", "Institution"]
COLORS = {
    "Russia": "firebrick",
    "Ukraine": "royalblue",
    "Georgia": "seagreen",
    "Institution": "darkorange",
}

def resolve_text_path(value: str) -> Path:
    path = Path(str(value))
    return path if path.is_absolute() else ROOT / path

def load_text(path: str) -> str:
    try:
        return resolve_text_path(path).read_text(encoding="utf-8")
    except Exception:
        return ""

def count_words(text: str) -> int:
    return max(len(text.split()), 1)

def split_sentences(text: str):
    compact = re.sub(r"\s+", " ", text).strip()
    if not compact:
        return []
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", compact) if len(part.strip()) >= 20]

def extract_civ_sentences(text: str, max_n: int = 3):
    return [sent for sent in split_sentences(text) if CIV_RX.search(sent)][:max_n]

def build_doc_dataframe():
    df = pd.read_csv(INPUT, dtype=str)
    df = df[df["clean_path"].notna()].copy()
    df["month"] = df["month"].fillna(df["date"].fillna("")).astype(str).str.slice(0, 7)
    df["text"] = [load_text(path) for path in df["clean_path"]]
    df = df[df["text"].str.len() > 0].copy()
    df["n_words"] = df["text"].apply(count_words)
    df["civ_count"] = df["text"].apply(lambda text: len(CIV_RX.findall(text)))
    df["civ_per_1000"] = df["civ_count"] / df["n_words"] * 1000
    df["civ_doc_hit"] = (df["civ_count"] > 0).astype(int)
    df["matched_sentences"] = df["text"].apply(lambda text: " || ".join(extract_civ_sentences(text, max_n=3)))
    return df

def build_monthly_aggregate(df):
    return (
        df.groupby(["actor", "country", "month"])
        .agg(
            n_docs=("url", "count"),
            avg_civ_per_1000=("civ_per_1000", "mean"),
            total_civ_count=("civ_count", "sum"),
            doc_hit_rate=("civ_doc_hit", "mean"),
        )
        .reset_index()
        .sort_values(["country", "month"])
    )

def plot_comparison(agg):
    plt.figure(figsize=(12, 6))
    for country in TARGET_COUNTRIES:
        sub = agg[agg["country"] == country].sort_values("month")
        if sub.empty:
            continue
        plt.plot(sub["month"], sub["avg_civ_per_1000"], label=country, color=COLORS.get(country, "gray"), linewidth=1.8)
    plt.xticks(rotation=60, ha="right", fontsize=8)
    plt.ylabel("Average occurrences per 1000 words")
    plt.title("Civilization Narrative Dynamics by Country")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig_civilization_timeseries_comparison.png", dpi=220)
    plt.close()

def plot_russia(ru, peak_months):
    if ru.empty:
        return
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.plot(ru["month"], ru["avg_civ_per_1000"], color=COLORS["Russia"], linewidth=2.0, label="Russia")
    ymax = max(float(ru["avg_civ_per_1000"].max()), 0.05)
    ax.set_ylim(0, ymax * 1.18)
    for peak in peak_months.itertuples(index=False):
        ax.axvline(peak.month, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)
        ax.text(peak.month, 0.965, peak.month, rotation=90, va="top", ha="center", fontsize=7, transform=ax.get_xaxis_transform(), bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.85, "pad": 0.8}, clip_on=False)
    ax.tick_params(axis="x", rotation=60, labelsize=8)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right")
    ax.set_ylabel("Average occurrences per 1000 words")
    ax.set_title("Civilization Narrative Dynamics: Russia")
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig_civilization_timeseries_russia.png", dpi=220)
    plt.close(fig)

def plot_value_timeseries(agg):
    sub = agg[agg["country"].isin(TARGET_COUNTRIES)].copy()
    plt.figure(figsize=(12, 6))
    for country in TARGET_COUNTRIES:
        row = sub[sub["country"] == country].sort_values("month")
        if row.empty:
            continue
        plt.plot(row["month"], row["avg_civ_per_1000"], label=country, color=COLORS[country], linewidth=1.8)
    plt.xticks(rotation=60, ha="right", fontsize=8)
    plt.ylabel("Average occurrences per 1000 words")
    plt.title("Civilization Value Narrative Timeseries")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig_value_civilization_timeseries.png", dpi=220)
    plt.close()

def build_peak_months(agg):
    ru = agg[agg["country"] == "Russia"].sort_values("month").copy()
    peak_months = ru.sort_values(["avg_civ_per_1000", "total_civ_count", "month"], ascending=[False, False, True]).head(5).copy()
    return ru, peak_months

def build_top_docs(df, peak_months):
    ru_docs = df[(df["country"] == "Russia") & (df["civ_count"] > 0)].copy()
    top_rows = []
    for month in peak_months["month"].tolist():
        subset = ru_docs[ru_docs["month"] == month].sort_values(["civ_count", "civ_per_1000", "date"], ascending=[False, False, True]).head(3)
        top_rows.append(subset[["month", "date", "title", "url", "civ_count", "civ_per_1000", "matched_sentences"]])
    if not top_rows:
        return pd.DataFrame(columns=["month", "date", "title", "url", "civ_count", "civ_per_1000", "matched_sentences"])
    return pd.concat(top_rows, ignore_index=True)

def build_cooccurrence(df):
    ru_docs = df[(df["country"] == "Russia") & (df["civ_count"] > 0)].copy()
    rows = []
    for rec in ru_docs.itertuples(index=False):
        for sent in split_sentences(rec.text):
            if not CIV_RX.search(sent):
                continue
            for label, rx in CO_RX.items():
                if rx.search(sent):
                    rows.append({
                        "month": rec.month,
                        "date": rec.date,
                        "title": rec.title,
                        "url": rec.url,
                        "co_term": label,
                        "sentence": sent,
                    })
    return pd.DataFrame(rows)

def main():
    df = build_doc_dataframe()
    agg = build_monthly_aggregate(df)
    agg.to_csv(RESULTS_DIR / "civilization_timeseries_by_country.csv", index=False)
    ru, peak_months = build_peak_months(agg)
    peak_months.to_csv(RESULTS_DIR / "civilization_peak_months_russia.csv", index=False)
    build_top_docs(df, peak_months).to_csv(RESULTS_DIR / "civilization_top_docs_russia.csv", index=False)
    build_cooccurrence(df).to_csv(RESULTS_DIR / "civilization_cooccurrence_russia.csv", index=False)
    plot_comparison(agg)
    plot_russia(ru, peak_months)
    plot_value_timeseries(agg)

if __name__ == "__main__":
    main()
