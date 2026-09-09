# CrystalCore.OS × dbt Data Warehouse Integration

Complete data transformation and analytics pipeline for emotion detection and active learning.

---

## Overview

The dbt Emotion Warehouse integrates CrystalCore.OS emotional intelligence system with a production-grade data pipeline:

**Data Pipeline:**
```
CrystalCore.OS (Predictions)
        ↓
DbtDataExporter (JSONL Export)
        ↓
Staging Models (Raw ingestion)
        ↓
Fact/Dimension Tables (Transformed)
        ↓
Aggregate Models (Analytics)
        ↓
BI Dashboard, ML Retraining, Insights
```

**Key Benefits:**
- 📊 Centralized analytics on all predictions and active learning
- 🔍 Data quality testing and validation
- 📈 Daily aggregation metrics and trends
- 🤖 Feed refined data back to model retraining
- 📋 Complete data lineage and documentation
- 🏗️ Scalable to BigQuery, Snowflake, or local DuckDB

---

## Architecture

### 1. Staging Models (Raw Data)

**`stg_emotion_predictions`**
- Raw emotion predictions from CrystalCore.OS
- Includes all uncertainty metrics and modality information
- No transformations (load as-is)

**`stg_emotion_labels`**
- Reference table of 28 GoEmotions labels
- Maps to Goleman EI framework components
- Classifies emotional valence

**`stg_active_learning_queue`**
- Incoming predictions with low confidence
- Pending user feedback
- Queue lifecycle tracking

### 2. Fact Tables (Cleaned & Enriched)

**`fct_emotion_predictions`**
- Predictions joined with label metadata
- Confidence/entropy/uncertainty classifications
- Active learning decision flags
- Analysis-ready structure

**`fct_active_learning_queue`**
- Queue analytics (model vs. user feedback)
- Stale sample identification
- Retraining readiness tracking

### 3. Dimension Tables (Reference Data)

**`dim_emotions`**
- Emotion hierarchy with EI mappings
- Emotional valence and intensity classifications
- For joins and groupings in analytics

### 4. Aggregate Models (Analytics)

**`agg_daily_emotion_metrics`**
- Daily rollup of predictions per emotion
- Average confidence, entropy, uncertainty
- Active learning query counts
- Multimodal contribution percentages

---

## Installation & Setup

### 1. Install dbt

```bash
# Local development (DuckDB)
pip install dbt-core dbt-duckdb

# Or for BigQuery
pip install dbt-core dbt-bigquery
```

### 2. Install Dependencies

```bash
cd dbt/crystalcore_emotion_warehouse
dbt deps
```

### 3. Configure Database

Edit `profiles.yml`:

```yaml
crystalcore:
  outputs:
    dev:
      type: duckdb
      path: '/tmp/crystalcore_emotion_warehouse.duckdb'
      threads: 4

    prod:
      type: bigquery
      project: 'your-project-id'
      dataset: 'emotion_detection'
      keyfile: '~/.crystalcore/bigquery_credentials.json'

  target: dev
```

### 4. Run Models

```bash
# Transform all data
dbt run

# Run specific target
dbt run --target prod

# Run tests
dbt test

# Generate docs
dbt docs generate
dbt docs serve
```

---

## Python Integration

### Exporting Data

```python
from src.crystalcore_os.dbt_integration import DbtDataExporter

exporter = DbtDataExporter(export_dir="~/.crystalcore/dbt_exports")

# Export a prediction
exporter.export_prediction(
    text="I'm really happy today!",
    emotion="joy",
    emotion_idx=17,
    confidence=0.92,
    entropy=0.18,
    least_confidence=0.08,
    margin_uncertainty=0.05,
    modalities=["text"],
    epistemic_uncertainty=0.04,
    aleatoric_uncertainty=0.02,
    mc_samples=8,
    should_query=False,
)

# Export low-confidence prediction for active learning
exporter.export_active_learning_sample(
    text="I'm not sure how I feel...",
    predicted_emotion="confusion",
    predicted_emotion_idx=6,
    confidence=0.58,
    entropy=0.72,
    is_uncertain=True,
    uncertainty_reason="Confidence < 0.65",
    model_version="v1.2.0",
)

# Update with user feedback
exporter.update_label(
    queue_timestamp="2026-07-23T15:30:45.123456",
    user_emotion="curiosity",
    user_confidence=0.85,
)

# Daily metrics
exporter.export_daily_metrics(
    date="2026-07-23",
    emotion="joy",
    prediction_count=142,
    avg_confidence=0.78,
    avg_entropy=0.31,
    queries_triggered=12,
    labeled_count=8,
)
```

### Monitoring Exports

```python
# Check export status
status = exporter.get_export_status()
print(f"Total predictions exported: {status['total_predictions']}")
print(f"Active learning queue: {status['total_queued']}")
print(f"Labels collected: {status['total_labeled']}")
```

---

## Data Models Details

### Staging: `stg_emotion_predictions`

| Column | Type | Description |
|--------|------|-------------|
| `prediction_id` | string | Unique identifier |
| `prediction_timestamp` | timestamp | When prediction made |
| `input_text` | string | Input text being analyzed |
| `emotion_detected` | string | Predicted emotion (28 labels) |
| `emotion_idx` | integer | Emotion index (0-27) |
| `confidence` | float | Model confidence (0.0-1.0) |
| `entropy` | float | Shannon entropy ≥ 0 |
| `least_confidence` | float | 1 - max(p) (0.0-1.0) |
| `margin_uncertainty` | float | 1 - (p₁ - p₂) (0.0-1.0) |
| `modalities` | string | "text", "text,audio", "text,audio,vision" |
| `epistemic_uncertainty` | float | Model parameter uncertainty |
| `aleatoric_uncertainty` | float | Data noise uncertainty |
| `mc_samples` | integer | Number of MC dropout samples |
| `should_query_user` | boolean | Trigger active learning? |
| `query_reason` | string | Why active learning triggered |
| `label_status` | string | pending, labeled, rejected |
| `user_label` | string | User's feedback emotion |
| `label_confidence` | float | User's confidence in label |
| `labeled_at` | timestamp | When user labeled |

### Staging: `stg_emotion_labels`

| Column | Type | Description |
|--------|------|-------------|
| `emotion_idx` | integer | 0-27 |
| `emotion_label` | string | Emotion name |
| `description` | string | Meaning |
| `ei_component` | string | Goleman component |
| `emotional_valence` | string | positive, neutral, challenging |

### Fact: `fct_emotion_predictions`

All staging columns, plus:

| Column | Type | Description |
|--------|------|-------------|
| `confidence_level` | string | low (< 0.65), medium, high (≥ 0.85) |
| `is_high_entropy` | boolean | entropy > 0.55? |
| `labeling_status` | string | queried, labeled, rejected, pending |

### Aggregate: `agg_daily_emotion_metrics`

| Column | Type | Description |
|--------|------|-------------|
| `prediction_date` | date | YYYY-MM-DD |
| `emotion_label` | string | Emotion |
| `prediction_count` | integer | Predictions that day |
| `avg_confidence` | float | Average confidence |
| `avg_entropy` | float | Average entropy |
| `queries_triggered` | integer | Active learning queries |
| `labeled_count` | integer | Labels collected |
| `audio_predictions` | integer | Multimodal (audio) |
| `visual_predictions` | integer | Multimodal (visual) |

---

## Integration Flow

### Real-time Prediction Export

```
CrystalCore.OS.detect_emotion(text)
    ↓
Returns: {emotion, confidence, entropy, ...}
    ↓
exporter.export_prediction(...)
    ↓
→ stg_emotion_predictions.jsonl
    ↓
dbt run (transform)
    ↓
→ fct_emotion_predictions (fact table)
    ↓
Ready for analytics, BI dashboard
```

### Active Learning Loop

```
Prediction confidence < 0.65
    ↓
exporter.export_active_learning_sample(...)
    ↓
→ stg_active_learning_queue.jsonl
    ↓
User sees clarification query
    ↓
User provides feedback
    ↓
exporter.update_label(timestamp, emotion, confidence)
    ↓
→ stg_active_learning_queue.jsonl (updated)
    ↓
dbt run (transform)
    ↓
→ fct_active_learning_queue (labeled status)
    ↓
Batch: Collect 50+ labels → Retrain model
```

### Daily Metrics Export

```
End of day (UTC midnight)
    ↓
Compute daily aggregates per emotion
    ↓
exporter.export_daily_metrics(date, emotion, counts, ...)
    ↓
→ agg_daily_emotion_metrics.jsonl
    ↓
dbt run (aggregate already exists)
    ↓
→ agg_daily_emotion_metrics (table)
    ↓
Trend analysis, performance tracking
```

---

## Thresholds & Configuration

All configurable in `dbt_project.yml`:

```yaml
vars:
  confidence_threshold: 0.65      # Query if < 65%
  entropy_threshold: 0.55         # Query if > 0.55
  margin_threshold: 0.15          # Query if > 0.15
  emotion_labels: [...]           # 28 GoEmotions
```

### Threshold Meanings

| Metric | Threshold | Meaning |
|--------|-----------|---------|
| **Confidence** | 0.65 | Model < 65% sure → Query user |
| **Entropy** | 0.55 | Multiple emotions likely → Query user |
| **Margin** | 0.15 | Top-2 predictions close → Query user |

---

## dbt Commands

### Development

```bash
cd dbt/crystalcore_emotion_warehouse

# Parse models
dbt parse

# Compile SQL
dbt compile

# Run models (dev target)
dbt run

# Run specific model
dbt run -s fct_emotion_predictions

# Run tests
dbt test

# Debug connections
dbt debug
```

### Documentation

```bash
# Generate docs
dbt docs generate

# Serve docs locally
dbt docs serve
# → http://localhost:8000
```

### Production Deployment

```bash
# Run with prod target
dbt run --target prod

# Validate all tests pass
dbt test --target prod

# Full refresh (replace tables)
dbt run --full-refresh --target prod
```

### Scheduling (Cloud Scheduler)

```bash
# Deploy to BigQuery + Cloud Scheduler
dbt run --target prod

# Schedule daily at 1 AM UTC:
# Cloud Scheduler → Cloud Functions → gcloud dbt run
```

---

## Data Quality Tests

Automatic validation includes:

✅ **Uniqueness**: No duplicate predictions  
✅ **Not Null**: Required fields populated  
✅ **Value Ranges**: Confidence in [0.0, 1.0]  
✅ **Accepted Values**: Emotions in 28-label set  
✅ **Expression Tests**: Custom validations  
✅ **Referential Integrity**: emotion_idx → dim_emotions  

Run tests:
```bash
dbt test
dbt test -s fct_emotion_predictions
dbt test --select tag:core
```

---

## Goleman EI Framework Mapping

All 28 emotions mapped to EI components:

| Component | Count | Examples |
|-----------|-------|----------|
| **Self-Awareness** | 7 | amusement, pride, realization, surprise |
| **Self-Regulation** | 9 | anger, fear, sadness, relief |
| **Motivation** | 6 | excitement, joy, optimism, curiosity |
| **Empathy** | 6 | admiration, caring, love, gratitude |
| **Social Skills** | 1 | disapproval |
| **Neutral** | 1 | neutral |

Models use `dim_emotions` for joins and filtering by EI component.

---

## Performance & Scaling

### DuckDB (Local Development)
- ✅ Fast (in-memory)
- ✅ Zero setup
- ❌ Single-threaded
- ❌ Limited to local disk

### BigQuery (Production)
- ✅ Scalable to billions of rows
- ✅ Cost-optimized for analytics
- ✅ Real-time dashboards
- ✅ Integration with Looker
- ❌ Requires GCP credentials

### Data Refresh Frequency

| Model | Frequency | Reason |
|-------|-----------|--------|
| Staging | Real-time | Immediate export |
| Fact tables | Hourly | Join latency |
| Aggregates | Daily (midnight UTC) | Cost optimization |

---

## Troubleshooting

### Problem: `ModuleNotFoundError: dbt_utils`

**Solution:**
```bash
dbt deps
```

### Problem: No data in tables

**Verify exports:**
```python
status = exporter.get_export_status()
print(status['files'])  # Check file paths
```

**Check JSONL format:**
```bash
cat ~/.crystalcore/dbt_exports/stg_emotion_predictions.jsonl | head -1
```

### Problem: BigQuery authentication fails

**Setup credentials:**
```bash
gcloud auth application-default login
# OR
export GOOGLE_APPLICATION_CREDENTIALS=~/.crystalcore/bigquery_credentials.json
```

### Problem: Tests fail

**Debug test:**
```bash
dbt test -s model_name --debug
```

---

## Best Practices

### 1. Export Data Immediately After Prediction

```python
# Good: Export inline
result = ei.detect_emotion(text)
exporter.export_prediction(
    text=text,
    emotion=result['emotion'],
    confidence=result['confidence'],
    ...
)

# Avoid: Buffering locally then exporting later
# Risk: Data loss if process crashes
```

### 2. Batch Label Updates

```python
# Good: Update in bulk
for queue_id, label, confidence in feedback_batch:
    exporter.update_label(queue_id, label, confidence)

# Avoid: One at a time (I/O overhead)
```

### 3. Run dbt Once Daily

```bash
# Schedule: 1 AM UTC (after log rotation)
dbt run --target prod
dbt test --target prod
```

### 4. Monitor Data Freshness

```python
status = exporter.get_export_status()
if status['total_predictions'] < expected_count:
    alert("Low prediction volume")
```

---

## References

- **dbt Documentation**: https://docs.getdbt.com/
- **CrystalCore.OS EI**: `docs/EMOTIONAL_INTELLIGENCE_BLUEPRINT.md`
- **Uncertainty Methods**: `docs/ADVANCED_UNCERTAINTY_METHODS.md`
- **dbt Project**: `dbt/crystalcore_emotion_warehouse/`

---

*CrystalCore.OS Data Warehouse – Production Analytics Pipeline*
