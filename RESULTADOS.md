# Resultado efetivamente verificado

Executado em 11/11/2026 no Windows local conectado a este chat. Este chat não tinha acesso a uma sessão Codex Cloud nem Bash/Linux configurado. Portanto, os testes abaixo validam o núcleo Python com o scanner real; os scripts `.sh` e a instalação no Cloud permanecem pendentes de execução naquele ambiente.

Instalação isolada em `work/venv`, a partir do clone oficial NVIDIA/SkillSpector, revisão `5f0f73dd204ad2454cca4ad63b06e60ad1ec3648`. A versão instalada, confirmada por pip, é 2.12.0. As opções `--no-llm`, `--format`, `--fail-on-findings` e `--fail-on-incomplete` foram confirmadas na ajuda da CLI instalada, guardada nas pastas de cada teste.

| Teste real | Scanner | Verificador | Achados | Cobertura estática | Resultado |
|---|---:|---:|---:|---:|---|
| Benigna | 0 | 0 | 0 | 100%, completa | Liberada para revisão |
| Suspeita | 1 | 1 | 2 | 100%, completa | Bloqueada |
| SKILL.md UTF-16 ilegível | 2 | 1 | 1 | 0%, incompleta | Bloqueada |
| Caminho inexistente | 2 | 2 | Sem relatório do scanner | Não determinada | Bloqueada |

Na suspeita, o scanner identificou `P1 / Instruction Override` e `SC2 / External Script Fetching`, ambos HIGH. O risco agregado foi 42 / MEDIUM / CAUTION; o bloqueio ocorre com qualquer achado, independentemente da pontuação.

Os relatórios das três análises que produziram JSON registram `llm_requested: false` e `inference_usage: []`. Não houve execução do conteúdo das fixtures, instalação de skills analisadas, uso de APIs pagas, publicação de serviços ou alteração de credenciais.

A primeira rodada foi preservada em `reports/initial-test-results.json`: houve timeout inicial de ajuda e a restrição de `--output` no Windows. O prazo foi ajustado e a captura passou a usar stdout, conforme orientação do próprio scanner. A rodada final está em `reports/test-results.json`, com quatro testes aprovados. Cada execução tem pasta própria; falhas anteriores não foram apagadas nem usadas para liberar análise nova.

O bloqueio do verificador foi demonstrado localmente para achados, análise incompleta e erro. A proteção no Codex Cloud não está concluída: copiar o pacote, incorporar AGENTS.md e executar `bash scripts/setup.sh` e `.venv/bin/python scripts/testar.py` lá. A política em AGENTS.md foi criada também na raiz deste espaço local; não constitui interceptação global de instalações.
