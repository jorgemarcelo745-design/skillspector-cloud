"""Gate estático: nunca instala nem executa conteúdo da skill."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, '-c', 'from skillspector.cli_entry import app; app()']
ENV = dict(os.environ, NO_COLOR='1', TERM='dumb', COLUMNS='160', LANGSMITH_TRACING='false', LANGCHAIN_TRACING_V2='false')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('alvo', help='URL ou caminho de uma skill')
    parser.add_argument('--reports', type=Path, default=ROOT / 'reports')
    args = parser.parse_args()
    args.reports.mkdir(parents=True, exist_ok=True)
    run = Path(tempfile.mkdtemp(prefix=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-'), dir=args.reports))
    decision = {'allowed': False, 'target': args.alvo, 'mode': 'static-only'}
    rc = 2
    try:
        if args.alvo.startswith('-'):
            raise ValueError('Alvo iniciado por hífen não é permitido')
        help_result = subprocess.run(CLI + ['scan', '--help'], capture_output=True, text=True, encoding='utf-8', errors='replace', env=ENV, timeout=300)
        (run / 'scan-help.txt').write_text(help_result.stdout + help_result.stderr, encoding='utf-8')
        flags = ['--no-llm', '--format', '--fail-on-findings', '--fail-on-incomplete']
        if help_result.returncode or any(flag not in help_result.stdout for flag in flags):
            raise ValueError('CLI indisponível ou opções exigidas não confirmadas')
        report = run / 'report.json'
        cmd = CLI + ['scan', args.alvo, '--no-llm', '--format', 'json', '--fail-on-findings', '--fail-on-incomplete']
        decision['command'] = cmd
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', env=ENV, timeout=300)
        (run / 'stdout.txt').write_text(result.stdout, encoding='utf-8')
        (run / 'stderr.txt').write_text(result.stderr, encoding='utf-8')
        decision['scanner_exit_code'] = result.returncode
        data = json.loads(result.stdout)
        report.write_text(json.dumps(data, indent=2, ensure_ascii=True), encoding='utf-8')
        issues = data.get('issues')
        completeness = data.get('analysis_completeness')
        if not isinstance(issues, list) or not isinstance(completeness, dict):
            raise ValueError('Estrutura JSON desconhecida: bloqueio preventivo')
        decision['issues_count'] = len(issues)
        decision['risk_assessment'] = data.get('risk_assessment')
        decision['analysis_completeness'] = completeness
        decision['severity_counts'] = dict(Counter(str(i.get('severity', 'unknown')) for i in issues))
        metadata = data.get('metadata', {})
        decision['llm_requested'] = metadata.get('llm_requested')
        decision['inference_usage'] = metadata.get('inference_usage')
        decision['allowed'] = (result.returncode == 0 and data.get('execution_successful') is True and completeness.get('is_complete') is True and not issues and data.get('suppressed_count', 0) == 0 and metadata.get('llm_requested') is False and metadata.get('inference_usage') == [])
        rc = 0 if decision['allowed'] else 1
        for issue in issues:
            print(json.dumps({k: issue.get(k) for k in ('id', 'severity', 'category', 'pattern', 'explanation', 'location')}, ensure_ascii=True))
    except (OSError, ValueError, TypeError, AttributeError, subprocess.SubprocessError) as error:
        decision['error'] = str(error)
    finally:
        decision['gate_exit_code'] = rc
        (run / 'decision.json').write_text(json.dumps(decision, indent=2, ensure_ascii=True), encoding='utf-8')
        print('LIBERADO PARA REVISÃO' if decision['allowed'] else 'BLOQUEADO')
        summary = {k: decision[k] for k in ('scanner_exit_code', 'gate_exit_code', 'issues_count', 'severity_counts', 'risk_assessment', 'error') if k in decision}
        if 'analysis_completeness' in decision:
            summary['coverage_percent'] = decision['analysis_completeness'].get('coverage_percent')
            summary['is_complete'] = decision['analysis_completeness'].get('is_complete')
        print(json.dumps(summary, indent=2, ensure_ascii=True))
        print(f'Relatórios: {run}')
    return rc


if __name__ == '__main__':
    sys.exit(main())
