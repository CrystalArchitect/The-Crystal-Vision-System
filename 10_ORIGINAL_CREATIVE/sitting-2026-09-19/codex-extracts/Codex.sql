-- CrystalCore.OS - Staging: Emotion Labels Reference
-- 28 GoEmotions labels with descriptions and Goleman EI framework mapping

with emotion_labels as (
    select 0 as emotion_idx, 'admiration' as emotion_label, 'Positive sense of approval' as description, 'empathy' as ei_component union all
    select 1, 'amusement', 'Finding something funny', 'self-awareness' union all
    select 2, 'anger', 'Strong displeasure', 'self-regulation' union all
    select 3, 'annoyance', 'Mild irritation', 'self-regulation' union all
    select 4, 'approval', 'Acceptance or agreement', 'empathy' union all
    select 5, 'caring', 'Compassion and concern', 'empathy' union all
    select 6, 'confusion', 'Lack of clarity', 'self-awareness' union all
    select 7, 'curiosity', 'Desire to know', 'motivation' union all
    select 8, 'desire', 'Strong wish or want', 'motivation' union all
    select 9, 'disappointment', 'Unmet expectations', 'self-regulation' union all
    select 10, 'disapproval', 'Expression of rejection', 'social_skills' union all
    select 11, 'disgust', 'Strong aversion', 'self-regulation' union all
    select 12, 'embarrassment', 'Self-consciousness', 'self-awareness' union all
    select 13, 'excitement', 'Intense enthusiasm', 'motivation' union all
    select 14, 'fear', 'Anxiety about threat', 'self-regulation' union all
    select 15, 'gratitude', 'Appreciation', 'empathy' union all
    select 16, 'grief', 'Deep sorrow', 'self-regulation' union all
    select 17, 'joy', 'Happiness', 'motivation' union all
    select 18, 'love', 'Deep affection', 'empathy' union all
    select 19, 'nervousness', 'Anxious state', 'self-regulation' union all
    select 20, 'optimism', 'Positive outlook', 'motivation' union all
    select 21, 'pride', 'Satisfaction with achievement', 'self-awareness' union all
    select 22, 'realization', 'Sudden understanding', 'self-awareness' union all
    select 23, 'relief', 'Release from tension', 'self-regulation' union all
    select 24, 'remorse', 'Regret for action', 'self-awareness' union all
    select 25, 'sadness', 'Sorrow', 'self-regulation' union all
    select 26, 'surprise', 'Unexpected reaction', 'self-awareness' union all
    select 27, 'neutral', 'No strong emotion', 'neutral' union all
)

select
    emotion_idx,
    emotion_label,
    description,
    ei_component,
    case
        when ei_component in ('empathy', 'motivation', 'social_skills') then 'positive'
        when ei_component = 'neutral' then 'neutral'
        else 'challenging'
    end as emotional_valence,
    current_timestamp() as dbt_loaded_at
from emotion_labels
