{% macro get_emotion_name(emotion_idx) %}
    case {{ emotion_idx }}
        when 0 then 'admiration'
        when 1 then 'amusement'
        when 2 then 'anger'
        when 3 then 'annoyance'
        when 4 then 'approval'
        when 5 then 'caring'
        when 6 then 'confusion'
        when 7 then 'curiosity'
        when 8 then 'desire'
        when 9 then 'disappointment'
        when 10 then 'disapproval'
        when 11 then 'disgust'
        when 12 then 'embarrassment'
        when 13 then 'excitement'
        when 14 then 'fear'
        when 15 then 'gratitude'
        when 16 then 'grief'
        when 17 then 'joy'
        when 18 then 'love'
        when 19 then 'nervousness'
        when 20 then 'optimism'
        when 21 then 'pride'
        when 22 then 'realization'
        when 23 then 'relief'
        when 24 then 'remorse'
        when 25 then 'sadness'
        when 26 then 'surprise'
        when 27 then 'neutral'
        else 'unknown'
    end
{% endmacro %}

{% macro classify_confidence(confidence) %}
    case
        when {{ confidence }} < var('confidence_threshold') then 'low'
        when {{ confidence }} < 0.85 then 'medium'
        else 'high'
    end
{% endmacro %}

{% macro classify_entropy(entropy) %}
    case
        when {{ entropy }} > var('entropy_threshold') then true
        else false
    end
{% endmacro %}

{% macro should_trigger_active_learning(confidence, entropy, margin) %}
    case
        when {{ confidence }} < var('confidence_threshold') then true
        when {{ entropy }} > var('entropy_threshold') then true
        when {{ margin }} > var('margin_threshold') then true
        else false
    end
{% endmacro %}

{% macro get_ei_component(emotion_label) %}
    case {{ emotion_label }}
        when 'admiration' then 'empathy'
        when 'amusement' then 'self-awareness'
        when 'anger' then 'self-regulation'
        when 'annoyance' then 'self-regulation'
        when 'approval' then 'empathy'
        when 'caring' then 'empathy'
        when 'confusion' then 'self-awareness'
        when 'curiosity' then 'motivation'
        when 'desire' then 'motivation'
        when 'disappointment' then 'self-regulation'
        when 'disapproval' then 'social_skills'
        when 'disgust' then 'self-regulation'
        when 'embarrassment' then 'self-awareness'
        when 'excitement' then 'motivation'
        when 'fear' then 'self-regulation'
        when 'gratitude' then 'empathy'
        when 'grief' then 'self-regulation'
        when 'joy' then 'motivation'
        when 'love' then 'empathy'
        when 'nervousness' then 'self-regulation'
        when 'optimism' then 'motivation'
        when 'pride' then 'self-awareness'
        when 'realization' then 'self-awareness'
        when 'relief' then 'self-regulation'
        when 'remorse' then 'self-awareness'
        when 'sadness' then 'self-regulation'
        when 'surprise' then 'self-awareness'
        when 'neutral' then 'neutral'
        else 'unknown'
    end
{% endmacro %}
