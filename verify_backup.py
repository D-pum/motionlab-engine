"""Verify the backed-up payload against its recorded SHA-256 manifest."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
records = json.loads((root / 'BACKUP-MANIFEST.json').read_text(encoding='utf-8'))['files']
errors = []
for entry in records:
    path = root / entry['path']
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
        errors.append(entry['path'])
if errors:
    raise SystemExit('Missing or changed payload files:\n' + '\n'.join(errors))
print(f'PASS: {len(records)} payload files match the backup manifest.')
