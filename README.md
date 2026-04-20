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

Time window: February 2022 - December 2024

## Methods

- Dictionary-based value analysis
- BERTopic topic modeling
- Sentence-transformer embeddings
- Cosine similarity alignment analysis
- Disruption narrative detection
- Supplementary civilization narrative analysis

## Repository Structure

```text
black-sea-narrative-analysis/
├── data/
│   ├── clean/
│   │   ├── russia/
│   │   ├── ukraine/
│   │   ├── georgia/
│   │   └── institutions/
│   └── metadata/
│       ├── metadata_all.csv
│       ├── analysis_corpus.csv
│       └── analysis_corpus_labeled.csv
├── analysis/
│   ├── 01_preprocessing.ipynb
│   ├── 02_value_dictionary_analysis.ipynb
│   ├── 03_topic_modeling.ipynb
│   ├── 04_alignment_analysis.ipynb
│   ├── 05_layer3_disruption_analysis.ipynb
│   └── 06_civilization_analysis_labeled.py
├── figures/
├── results/
└── paper/
```

## Reproduction

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run preprocessing if you need to rebuild corpus tables:
   ```bash
   jupyter notebook analysis/01_preprocessing.ipynb
   ```

3. Run the core paper analyses:
   ```bash
   jupyter notebook analysis/02_value_dictionary_analysis.ipynb
   jupyter notebook analysis/03_topic_modeling.ipynb
   jupyter notebook analysis/04_alignment_analysis.ipynb
   jupyter notebook analysis/05_layer3_disruption_analysis.ipynb
   ```

4. Run the supplementary civilization analysis:
   ```bash
   python analysis/06_civilization_analysis_labeled.py
   ```

## Included Outputs

Core paper outputs are stored in `figures/` and `results/`.
Supplementary civilization outputs are included as additional CSV and PNG files, but explanatory Markdown notes are intentionally omitted from the public package.

> **Note on raw HTML**: Raw HTML files are not included in this repository to avoid copyright issues. The clean text corpus and metadata (including source URLs) are provided, enabling reproducibility of the public analyses.
