-- CrystalCore.OS - Dimension: Emotions
-- Emotion reference table with hierarchies and groupings

with stg_labels as (
    select * from {{ ref('stg_emotion_labels') }}
),

emotion_hierarchy as (
    select
        emotion_idx,
        emotion_label,
        description,
        ei_component,
        emotional_valence,
        case
            when emotional_valence = 'positive' then 'positive'
            when emotional_valence = 'challenging' then 'challenging'
            else 'neutral'
        end as emotional_category,
        case
            when ei_component = 'self-awareness' then 1
            when ei_component = 'self-regulation' then 2
            when ei_component = 'motivation' then 3
            when ei_component = 'empathy' then 4
            when ei_component = 'social_skills' then 5
            else 6
        end as ei_priority,
        case
            when emotion_label in ('joy', 'excitement', 'love', 'pride', 'gratitude', 'relief') then 'High Positive'
            when emotion_label in ('admiration', 'approval', 'caring', 'optimism') then 'Medium Positive'
            when emotion_label in ('amusement', 'curiosity', 'desire', 'realization', 'surprise') then 'Low Positive'
            when emotion_label in ('sadness', 'grief', 'fear', 'anger', 'disgust') then 'High Negative'
            when emotion_label in ('disappointment', 'disapproval', 'annoyance', 'nervousness') then 'Medium Negative'
            when emotion_label in ('confusion', 'embarrassment', 'remorse') then 'Low Negative'
            else 'Neutral'
        end as emotional_intensity,
        current_timestamp() as dbt_loaded_at
    from stg_labels
)

select * from emotion_hierarchy
order by emotion_idx
