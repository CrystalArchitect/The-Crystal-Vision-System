# CrystalCore.OS Emotion Warehouse - dbt Project

Production-grade data transformation pipeline for CrystalCore.OS emotional intelligence and affective computing system.

## Overview

This dbt project manages the data warehouse for emotion detection, active learning feedback, and model retraining pipelines. It integrates with:

- **CrystalCore.OS** - Real-time emotion detection engine
- **Active Learning** - Low-confidence prediction querying and feedback collection
- **Bayesian Uncertainty** - Epistemic/aleatoric uncertainty quantification
- **Multimodal Fusion** - Text, audio, and visual emotion detection

## Project Structure

```
.
├── models/
│   ├── staging/                          # Raw data ingestion
│   │   ├── stg_emotion_predictions.sql   # Raw predictions from CrystalCore
│   │   ├── stg_emotion_labels.sql        # 28 GoEmotions reference table
│   │   └── stg_active_learning_queue.sql # Pending feedback samples
│   └── marts/
│       ├── core/                         # Core analytics
│       │   ├── fct_emotion_predictions.sql   # Fact table of predictions
│       │   ├── dim_emotions.sql             # Emotion dimension with EI mapping
│       │   └── schema.yml                   # Tests & documentation
│       └── active_learning/               # Active learning pipeline
│           ├── fct_active_learning_queue.sql    # Queue analytics
│           └── agg_daily_emotion_metrics.sql    # Daily rollups
├── tests/
│   └── test_emotion_labels_completeness.sql
├── macros/
│   └── emotion_utils.sql                # Custom transformation utilities
├── dbt_project.yml                      # Project configuration
├── profiles.yml                         # Database connection config
├── packages.yml                         # dbt package dependencies
└── README.md                            # This file
```

## Getting Started

### Installation

```bash
# Install dbt and dependencies
pip install dbt-core dbt-duckdb  # or dbt-bigquery for production

# Navigate to dbt project
cd dbt/crystalcore_emotion_warehouse

# Install dbt packages
dbt deps
```

### Configuration

Edit `profiles.yml` with your database connection:

```yaml
# Local development (DuckDB)
dev:
  type: duckdb
  path: '/tmp/crystalcore_emotion_warehouse.duckdb'

# Production (BigQuery)
prod:
  type: bigquery
  project: 'your-project'
  dataset: 'emotion_detection'
  keyfile: '~/.crystalcore/bigquery_credentials.json'
```

### Running Models

```bash
# Run all models
dbt run

# Run specific model
dbt run -s fct_emotion_predictions

# Run with specific profile (dev/prod)
dbt run --profiles-dir . --target prod

# Run tests
dbt test

# Generate documentation
dbt docs generate
dbt docs serve  # View at http://localhost:8000
```

## Data Models

### Staging Models

#### `stg_emotion_predictions`
Raw predictions from CrystalCore.OS detection:
- `prediction_id` - Unique identifier
- `emotion_detected` - Predicted emotion (28 GoEmotions labels)
- `confidence` - Model confidence (0.0-1.0)
- `entropy` - Shannon entropy of prediction
- `least_confidence`, `margin_uncertainty` - Alternative uncertainty metrics
- `epistemic_uncertainty`, `aleatoric_uncertainty` - Bayesian uncertainty estimates
- `modalities` - Which modalities contributed ('text', 'audio', 'vision')
- `should_query_user` - Active learning flag
- `label_status` - Feedback collection status

#### `stg_emotion_labels`
Reference table (28 emotions):
- Maps emotion index (0-27) to label and description
- Links to Goleman EI framework components
- Emotional valence classification

#### `stg_active_learning_queue`
Pending user feedback samples:
- Low-confidence predictions awaiting labels
- Queue lifecycle tracking (unlabeled → labeled → retrained)
- Time-in-queue metrics

### Fact Tables

#### `fct_emotion_predictions`
Clean, joined prediction facts:
- Predictions with emotion metadata
- Confidence level categorization
- Uncertainty flags and thresholds
- Labeling status tracking
- Ready for BI and ML analytics

#### `fct_active_learning_queue`
Active learning queue analytics:
- Model vs. user feedback comparison
- Queue lifecycle progression
- Stale sample identification
- Retraining readiness

### Dimension Tables

#### `dim_emotions`
Emotion reference with hierarchies:
- Emotion index → label mapping
- Goleman EI component (self-awareness, self-regulation, motivation, empathy, social_skills)
- Emotional category (positive, neutral, challenging)
- Emotional intensity (High/Medium/Low Positive/Negative, Neutral)

### Aggregate Models

#### `agg_daily_emotion_metrics`
Daily rollup of predictions and active learning:
- Predictions per emotion per day
- Active learning query counts
- Average confidence, entropy, uncertainty
- Multimodal contribution (% audio, % visual)

## Variables & Thresholds

Configure in `dbt_project.yml`:

```yaml
vars:
  confidence_threshold: 0.65      # Query if confidence < 65%
  entropy_threshold: 0.55         # Query if entropy > 0.55
  margin_threshold: 0.15          # Query if margin > 0.15
  emotion_labels: [...]           # 28 GoEmotions labels
```

## Tests & Data Quality

Run tests to validate data integrity:

```bash
dbt test
```

Tests include:
- ✅ Unique emotion indices (0-27)
- ✅ No duplicate emotion labels
- ✅ Confidence values in [0.0, 1.0]
- ✅ Entropy non-negative
- ✅ Valid emotion labels (28 GoEmotions)
- ✅ Valid EI components
- ✅ Status lifecycle validation

## Integration with CrystalCore.OS

### Data Flow

```
CrystalCore.OS
    ↓
Emotion Predictions (logits, confidence, text)
    ↓
stg_emotion_predictions (raw ingestion)
    ↓
fct_emotion_predictions (joined with labels)
    ↓
BI Dashboard, ML Retraining, Analytics
```

### Active Learning Pipeline

```
Low-confidence prediction
    ↓
should_query_user = true
    ↓
Add to stg_active_learning_queue
    ↓
User provides feedback
    ↓
fct_active_learning_queue (update with label)
    ↓
Aggregate to agg_daily_emotion_metrics
    ↓
Batch retrain model on collected labels
```

### Uncertainty Quantification

Models track multiple uncertainty types:

| Metric | Range | Use Case |
|--------|-------|----------|
| **Confidence** | 0.0-1.0 | Overall model certainty |
| **Entropy** | 0.0-log(28) | Prediction ambiguity |
| **Least Confidence** | 0.0-1.0 | Complement of max probability |
| **Margin** | 0.0-1.0 | Gap between top-2 predictions |
| **Epistemic Uncertainty** | 0.0-1.0 | Model parameter uncertainty (MC Dropout) |
| **Aleatoric Uncertainty** | 0.0-1.0 | Data noise/ambiguity |

## Goleman EI Framework Mapping

All 28 emotions mapped to Goleman's 5 EI components:

1. **Self-Awareness** (7 emotions)
   - amusement, confusion, embarrassment, pride, realization, remorse, surprise

2. **Self-Regulation** (9 emotions)
   - anger, annoyance, disappointment, disapproval, disgust, fear, grief, nervousness, sadness, relief

3. **Motivation** (6 emotions)
   - curiosity, desire, excitement, joy, optimism, relief

4. **Empathy** (6 emotions)
   - admiration, approval, caring, gratitude, joy, love

5. **Social Skills** (1 emotion)
   - disapproval

## Production Deployment

### BigQuery Setup

```bash
# Create dataset
bq mk --dataset emotion_detection

# Deploy models to BigQuery
dbt run --profiles-dir . --target prod

# Schedule daily dbt run
# Configure Cloud Scheduler → Cloud Functions → dbt run
```

### Data Freshness

- **Staging models** - Updated in real-time from CrystalCore predictions
- **Fact tables** - Updated every 1 hour (configurable)
- **Aggregate models** - Updated daily (post-midnight UTC)

## Documentation

Auto-generated documentation available via:

```bash
dbt docs generate
dbt docs serve
```

Then open http://localhost:8000

## Troubleshooting

### Model not compiling?
```bash
dbt parse
dbt compile -s model_name
```

### Tests failing?
```bash
dbt test -s model_name --debug
```

### Database connection issues?
```bash
dbt debug
# Check profiles.yml path and credentials
```

## References

- [dbt Documentation](https://docs.getdbt.com/)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)
- [CrystalCore.OS Emotional Intelligence](../../docs/EMOTIONAL_INTELLIGENCE_BLUEPRINT.md)
- [Uncertainty Quantification Methods](../../docs/ADVANCED_UNCERTAINTY_METHODS.md)

---

*CrystalCore.OS Emotion Warehouse - Production Data Pipeline*
