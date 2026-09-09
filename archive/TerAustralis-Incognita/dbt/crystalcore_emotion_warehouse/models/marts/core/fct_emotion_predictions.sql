-- CrystalCore.OS - Fact Table: Emotion Predictions
-- Clean, aggregated view of all emotion detection predictions
-- Dimensions: emotion, confidence, uncertainty, modalities

with stg_predictions as (
    select * from {{ ref('stg_emotion_predictions') }}
),

stg_labels as (
    select * from {{ ref('stg_emotion_labels') }}
),

joined as (
    select
        sp.prediction_id,
        sp.prediction_timestamp,
        sp.input_text,
        sl.emotion_label,
        sl.emotion_idx,
        sl.ei_component,
        sl.emotional_valence,
        sp.confidence,
        sp.entropy,
        sp.least_confidence,
        sp.margin_uncertainty,
        sp.modalities,
        sp.epistemic_uncertainty,
        sp.aleatoric_uncertainty,
        case
            when sp.confidence < var('confidence_threshold') then 'low'
            when sp.confidence < 0.85 then 'medium'
            else 'high'
        end as confidence_level,
        case
            when sp.entropy > var('entropy_threshold') then true
            else false
        end as is_high_entropy,
        case
            when sp.should_query_user then 'queried'
            when sp.label_status = 'labeled' then 'labeled'
            when sp.label_status = 'rejected' then 'rejected'
            else 'pending'
        end as labeling_status,
        sp.should_query_user,
        sp.query_reason,
        sp.user_label,
        sp.labeled_at,
        sp.dbt_loaded_at
    from stg_predictions sp
    left join stg_labels sl on sp.emotion_idx = sl.emotion_idx
)

select * from joined
