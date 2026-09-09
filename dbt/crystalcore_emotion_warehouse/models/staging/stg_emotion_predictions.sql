-- CrystalCore.OS - Staging: Raw Emotion Predictions
-- Transforms raw predictions from emotional intelligence detection system
-- Handles text, audio, and visual modalities

with source_predictions as (
    select
        current_timestamp() as prediction_timestamp,
        null::string as input_text,
        null::string as emotion_detected,
        null::integer as emotion_idx,
        null::float as confidence,
        null::float as entropy,
        null::float as least_confidence,
        null::float as margin_uncertainty,
        null::string as modalities,  -- 'text', 'text,audio', 'text,audio,vision'
        null::float as epistemic_uncertainty,
        null::float as aleatoric_uncertainty,
        null::integer as mc_samples,
        null::boolean as should_query_user,
        null::string as query_reason,
        'pending'::string as label_status,  -- pending, labeled, rejected
        null::string as user_label,
        null::float as label_confidence,
        null::timestamp as labeled_at
)

select
    {{ dbt_utils.generate_surrogate_key(['prediction_timestamp', 'input_text']) }} as prediction_id,
    prediction_timestamp,
    input_text,
    emotion_detected,
    emotion_idx,
    confidence,
    entropy,
    least_confidence,
    margin_uncertainty,
    modalities,
    epistemic_uncertainty,
    aleatoric_uncertainty,
    mc_samples,
    should_query_user,
    query_reason,
    label_status,
    user_label,
    label_confidence,
    labeled_at,
    current_timestamp() as dbt_loaded_at
from source_predictions
