-- Test: Ensure all 28 GoEmotions labels are present
-- Expected: 28 rows, one per emotion

select
    emotion_label,
    count(*) as label_count
from {{ ref('stg_emotion_labels') }}
group by emotion_label
having count(*) > 1
-- Should return 0 rows (no duplicates)
