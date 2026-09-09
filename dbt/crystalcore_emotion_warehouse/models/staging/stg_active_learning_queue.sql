-- CrystalCore.OS - Staging: Active Learning Queue
-- Low-confidence predictions awaiting user feedback and retraining

with queue_samples as (
    select
        current_timestamp() as queue_timestamp,
        null::string as text_input,
        null::string as predicted_emotion,
        null::integer as predicted_emotion_idx,
        null::float as confidence,
        null::float as entropy,
        null::boolean as is_uncertain,
        null::string as uncertainty_reason,
        null::string as model_version,
        'unlabeled'::string as status,  -- unlabeled, labeled, rejected, retrained
        null::string as user_feedback_emotion,
        null::float as user_feedback_confidence,
        null::timestamp as feedback_received_at,
        null::boolean as used_for_retraining
)

select
    {{ dbt_utils.generate_surrogate_key(['queue_timestamp', 'text_input']) }} as queue_id,
    queue_timestamp,
    text_input,
    predicted_emotion,
    predicted_emotion_idx,
    confidence,
    entropy,
    is_uncertain,
    uncertainty_reason,
    model_version,
    status,
    user_feedback_emotion,
    user_feedback_confidence,
    feedback_received_at,
    used_for_retraining,
    case
        when status = 'unlabeled' then datediff('hour', queue_timestamp, current_timestamp())
        else null
    end as hours_in_queue,
    current_timestamp() as dbt_loaded_at
from queue_samples
