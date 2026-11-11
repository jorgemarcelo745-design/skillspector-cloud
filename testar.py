"""Testes reais do scanner e da decisão; não executa conteúdo das fixtures."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
incomplete = ROOT / 'tests' / 'incompleta'
incomplete.mkdir(exist_ok=True)
(incomplete / 'SKILL.md').write_text('---\nname: incompleta\ndescription: Resume texto.\n---\nResuma o texto fornecido.\n', encoding='utf-16')
results = []
for name, target, expected in [
    ('benigna', ROOT / 'tests' / 'benigna', 0),
    ('suspeita', ROOT / 'tests' / 'suspeita', 1),
    ('incompleta', incomplete, 1),
    ('inexistente', ROOT / 'tests' / 'nao-existe', 2),
]:
    reports = ROOT / 'reports' / name
    result = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'verificar_skill.py'), str(target), '--reports', str(reports)], capture_output=True, text=True, timeout=720)
    decisions = sorted(reports.glob('*/decision.json'), key=lambda p: p.stat().st_mtime_ns)
    decision = json.loads(decisions[-1].read_text()) if decisions else {}
    passed = result.returncode == expected
    if name == 'suspeita':
        passed &= decision.get('issues_count', 0) > 0
    if name == 'incompleta':
        passed &= decision.get('analysis_completeness', {}).get('is_complete') is False
    row = {'test': name, 'expected_exit': expected, 'actual_exit': result.returncode, 'passed': bool(passed), 'decision': decision, 'output': result.stdout, 'stderr': result.stderr}
    results.append(row)
    print(name, result.returncode, 'PASS' if passed else 'FAIL', flush=True)
(ROOT / 'reports' / 'test-results.json').write_text(json.dumps(results, indent=2, ensure_ascii=True), encoding='utf-8')
sys.exit(0 if all(row['passed'] for row in results) else 1)
