-- CrystalCore.OS - Aggregate: Daily Emotion Metrics
-- Daily rollup of emotion predictions and active learning metrics

with fct_predictions as (
    select * from {{ ref('fct_emotion_predictions') }}
),

daily_metrics as (
    select
        cast(fct_predictions.prediction_timestamp as date) as prediction_date,
        fct_predictions.emotion_label,
        fct_predictions.ei_component,
        fct_predictions.emotional_valence,
        fct_predictions.confidence_level,
        count(distinct fct_predictions.prediction_id) as prediction_count,
        sum(case when fct_predictions.should_query_user then 1 else 0 end) as queries_triggered,
        sum(case when fct_predictions.labeling_status = 'labeled' then 1 else 0 end) as labeled_count,
        avg(fct_predictions.confidence) as avg_confidence,
        min(fct_predictions.confidence) as min_confidence,
        max(fct_predictions.confidence) as max_confidence,
        avg(fct_predictions.entropy) as avg_entropy,
        avg(fct_predictions.epistemic_uncertainty) as avg_epistemic_uncertainty,
        avg(fct_predictions.aleatoric_uncertainty) as avg_aleatoric_uncertainty,
        count(distinct case when fct_predictions.modalities like '%audio%' then fct_predictions.prediction_id end) as audio_predictions,
        count(distinct case when fct_predictions.modalities like '%vision%' then fct_predictions.prediction_id end) as visual_predictions,
        current_timestamp() as dbt_loaded_at
    from fct_predictions
    group by
        cast(fct_predictions.prediction_timestamp as date),
        fct_predictions.emotion_label,
        fct_predictions.ei_component,
        fct_predictions.emotional_valence,
        fct_predictions.confidence_level
)

select * from daily_metrics
