# Black Sea Narrative Analysis

## Paper

**Strategic Signaling through Value Narratives:
Discursive Alignment and Narrative Interaction in the Black Sea Region after 2022**

## Authors

- Takeo Harada
- Yoko Hirose

## Data Sources

Official English-language documents from:

- President of Russia (Kremlin)
- President of Ukraine
- Ministry of Foreign Affairs of Georgia
- United Nations (Security Council verbatim records)
- OSCE
- European Union Council

Time window: February 2022 – December 2024

## Methods

- Dictionary-based value analysis
- BERTopic topic modeling
- Sentence-transformer embeddings
- Cosine similarity alignment analysis
- Disruption narrative detection

## Repository Structure

```
black-sea-narrative-analysis/
├── data/
│   ├── clean/
│   │   ├── russia/         # Kremlin + MFA Russia clean text
│   │   ├── ukraine/        # President of Ukraine clean text
│   │   ├── georgia/        # MFA Georgia clean text
│   │   └── institutions/   # UN / OSCE / EU Council clean text
│   └── metadata/
│       ├── metadata_all.csv
│       ├── analysis_corpus.csv
│       └── analysis_corpus_labeled.csv
├── analysis/
│   ├── 01_preprocessing.ipynb
│   ├── 02_value_dictionary_analysis.ipynb
│   ├── 03_topic_modeling.ipynb
│   ├── 04_alignment_analysis.ipynb
│   └── 05_layer3_disruption_analysis.ipynb
├── figures/                # All figures used in the paper
├── results/                # Summary CSV tables
└── paper/                  # Manuscript (forthcoming)
```

## Reproduction

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run preprocessing (or skip if using the provided corpus):
   ```bash
   jupyter notebook analysis/01_preprocessing.ipynb
   ```

3. Run value dictionary analysis:
   ```bash
   jupyter notebook analysis/02_value_dictionary_analysis.ipynb
   ```

4. Run topic modeling:
   ```bash
   jupyter notebook analysis/03_topic_modeling.ipynb
   ```

5. Run alignment analysis:
   ```bash
   jupyter notebook analysis/04_alignment_analysis.ipynb
   ```

6. Run disruption narrative analysis:
   ```bash
   jupyter notebook analysis/05_layer3_disruption_analysis.ipynb
   ```

> **Note on raw HTML**: Raw HTML files are not included in this repository to avoid
> copyright issues. The clean text corpus and metadata (including source URLs) are
> provided, enabling full reproducibility of all analyses.
