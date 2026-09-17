#!/bin/bash
# Health check for Portal service

echo "Checking Portal health..."

# Check database connectivity
echo "Checking database..."
python -c "
import sys
from portal.main import engine
try:
    with engine.connect() as conn:
        conn.execute('SELECT 1')
    print('✓ Database OK')
except Exception as e:
    print(f'✗ Database failed: {e}', file=sys.stderr)
    sys.exit(1)
"

# Check API availability
echo "Checking API..."
curl -s http://localhost:8000/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✓ API OK"
else
    echo "✗ API failed"
    exit 1
fi

echo "✓ All health checks passed"
