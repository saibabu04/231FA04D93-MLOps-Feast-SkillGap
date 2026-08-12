# 231FA04D93-MLOps-Feast-SkillGap

## Student Details
- Name: P.Sai 
- Register Number: 231FA04D93
- Section: 9
- Repository: `231FA04D93-MLOps-Feast-SkillGap`

## Problem Statement
CSE graduates may have a mismatch between university curriculum coverage and the skills demanded by industry. This project converts a curriculum–industry skill-gap dataset into a reusable Feast feature store for consistent historical training and online prediction.

## Dataset
The supplied dataset contains **500 samples and 20 source columns**. The source columns are:

`skill_id`, `skill_name`, `curriculum_score`, `industry_score`, `practical_score`, `projects_completed`, `internships_completed`, `certifications`, `coding_score`, `communication_score`, `problem_solving_score`, `teamwork_score`, `industry_demand_score`, `curriculum_relevance_score`, `skill_gap`, `employability_score`, `gap_level`, `employability_target`.

The target is `employability_target`. The dataset contains skill-level curriculum/industry measurements, practical experience indicators, employability score and gap level.

## Feature Engineering
The 15 Feast features are:

1. curriculum_score — curriculum coverage score
2. industry_score — industry requirement score
3. practical_score — practical application score
4. projects_completed — completed projects
5. internships_completed — completed internships
6. certifications — certification count
7. coding_score — coding capability
8. communication_score — communication capability
9. problem_solving_score — problem solving capability
10. teamwork_score — teamwork capability
11. industry_demand_score — industry demand indicator
12. curriculum_relevance_score — curriculum relevance indicator
13. skill_gap — non-negative industry minus curriculum difference
14. employability_score — employability indicator
15. gap_level — Low, Medium or High

Example calculation:

```text
skill_gap = max(industry_score - curriculum_score, 0)
```

The entity is `skill_id`; the target is kept separately from the FeatureView.

## Feast Architecture
See `screenshots/01_feast_architecture.png`.

```text
Original Dataset
      ↓
Feature Engineering
      ↓
Parquet Offline Data
      ↓
Feast FeatureView
      ↓
 ┌─────────────────────────┐
 ↓                         ↓
Historical Features   Materialization
 ↓                         ↓
Model Training       SQLite Online Store
                            ↓
                     Online Retrieval
                            ↓
                        Prediction
```

## Implementation

### Entity
`skill` with join key `skill_id`.

### Data Source
`FileSource` named `cse_skillgap_source`, backed by `data/cse_skillgap_features.parquet`.

### FeatureView
`cse_skillgap_features`, containing the 15 features above.

### Feature Service
`cse_skillgap_prediction_service`.

### Historical Retrieval
Uses `get_historical_features()` to obtain point-in-time feature values for model training.

### Model
Decision Tree classifier with `max_depth=4` and `random_state=42`.

### Online Retrieval
Uses `get_online_features()` after materialization into SQLite.

## Required Analysis

### 1. What is the entity?
The entity is `skill`, using `skill_id` as the join key.

### 2. List the FeatureView features.
The FeatureView contains the 15 features listed in the Feature Engineering section.

### 3. How was one feature calculated?
`skill_gap = max(industry_score - curriculum_score, 0)`. This prevents a negative gap.

### 4. Original dataset vs feature dataset
The original dataset includes descriptive and target columns. The Feast feature dataset contains the entity, timestamps and the reusable FeatureView features. The ML target is not registered as a serving feature.

### 5. Purpose of offline store
The offline store provides historical feature data for training and point-in-time retrieval. This project uses file-based data/Parquet for local development.

### 6. Purpose of online store
The online store holds materialized feature values for fast retrieval at prediction time. SQLite is used for local development.

### 7. Purpose of `feast apply`
It registers/updates Feast entities, data sources, FeatureViews and FeatureServices in the Feast registry.

### 8. What does materialization do?
It loads feature values for a selected time range from the offline source into the online store.

### 9. Advantage of Feast retrieval
Feast provides one reusable feature definition for historical training and online prediction, reducing duplicated feature-calculation logic and helping maintain training/serving consistency.

### 10. Two limitations
1. The dataset is a constructed/sample dataset and may not fully represent real employer requirements.
2. It lacks richer longitudinal graduate outcomes such as job applications, interviews, placements and career progression.

### 11. Two improvements
1. Add continuously updated job-posting, employer-survey and graduate-outcome evidence with timestamps and source provenance.
2. Add richer entities/features for graduate, program, semester and employer-specific requirements, together with feature/model drift monitoring.

## Results

### Historical feature output
The notebook retrieves the historical features using Feast's `get_historical_features()` API. The request labels are included in `results/labels_for_historical_retrieval.csv`.

### Model accuracy
Using the supplied dataset, an 80/20 split and the Decision Tree model gives:

**99.00% test accuracy.**

### Online feature output
Demonstration entity: `SKILL_025`

- Skill: `C++`
- Curriculum score: `94`
- Industry score: `72`
- Skill gap: `0`
- Employability score: `88.80`
- Gap level: `Low`

### Final prediction
For `SKILL_025`, the model predicts:

**1**

Class 1 probability: **100.00%**

## Required Repository Structure

```text
231FA04D93-MLOps-Feast-SkillGap/
├── README.md
├── requirements.txt
├── .gitignore
├── SUBMISSION_MANIFEST.txt
├── CSE_Graduate_SkillGap_Feast_59_Cells.ipynb
├── data/
│   ├── curriculum_industry_skill_gap_500_samples.csv
│   └── cse_skillgap_features_source.csv
├── feast_repo/
│   ├── feature_store.yaml
│   ├── features.py
│   └── data/
├── results/
│   ├── labels_for_historical_retrieval.csv
│   └── model_predictions.csv
└── screenshots/
    ├── 01_feast_architecture.png
    ├── 02_dataset_shape.png
    ├── 03_feature_engineering.png
    ├── 04_parquet_output.png
    ├── 05_feast_apply.png
    ├── 06_historical_retrieval.png
    ├── 07_model_accuracy.png
    ├── 08_materialization.png
    ├── 09_online_retrieval.png
    └── 10_final_prediction.png
```

## Colab Execution Note
The included notebook is the 59-cell Feast workflow adapted from the provided Feast notebook. The package was prepared from the supplied 500-sample CSV. The local build environment did not have `pyarrow`/Feast available, so the package includes the feature-source CSV and the notebook contains the Parquet-generation step. Run the notebook in Google Colab with the requirements installed to generate the actual `cse_skillgap_features.parquet` file and live `feast apply`, materialization and online-store CLI outputs before final GitHub submission.
