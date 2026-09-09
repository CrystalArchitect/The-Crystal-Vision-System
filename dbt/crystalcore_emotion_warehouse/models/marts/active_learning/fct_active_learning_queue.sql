-- CrystalCore.OS - Fact Table: Active Learning Queue
-- Tracks low-confidence predictions for user feedback and model retraining

with stg_queue as (
    select * from {{ ref('stg_active_learning_queue') }}
),

stg_labels as (
    select * from {{ ref('stg_emotion_labels') }}
),

labeled_queue as (
    select
        sq.queue_id,
        sq.queue_timestamp,
        sq.text_input,
        sq.predicted_emotion,
        sq.predicted_emotion_idx,
        sl_pred.emotional_valence as predicted_valence,
        sq.confidence as model_confidence,
        sq.entropy,
        sq.is_uncertain,
        sq.uncertainty_reason,
        sq.model_version,
        sq.status,
        sq.user_feedback_emotion,
        sq.user_feedback_confidence,
        case
            when sq.user_feedback_emotion = sq.predicted_emotion then true
            else false
        end as feedback_agrees_with_prediction,
        sl_feedback.emotional_valence as feedback_valence,
        sq.feedback_received_at,
        sq.used_for_retraining,
        sq.hours_in_queue,
        case
            when sq.status = 'unlabeled' and sq.hours_in_queue > 24 then 'stale'
            when sq.status = 'unlabeled' then 'pending'
            when sq.status = 'labeled' and not sq.used_for_retraining then 'ready_for_training'
            when sq.used_for_retraining then 'used_for_training'
            else sq.status
        end as queue_lifecycle_status,
        sq.dbt_loaded_at
    from stg_queue sq
    left join stg_labels sl_pred on sq.predicted_emotion_idx = sl_pred.emotion_idx
    left join stg_labels sl_feedback on sq.user_feedback_emotion = sl_feedback.emotion_label
)

select * from labeled_queue
