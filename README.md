# SkillSpector: verificação estática antes de instalar skills

Origem oficial: https://github.com/NVIDIA/SkillSpector

Revisão fixada: `5f0f73dd204ad2454cca4ad63b06e60ad1ec3648` (versão declarada 2.12.0).

## No Codex Cloud (Linux, Python 3.12 ou superior)

Copiar esta pasta para o repositório de destino e executar a partir dela:

```bash
bash scripts/setup.sh
.venv/bin/python scripts/testar.py
bash scripts/verificar-skill.sh ./caminho/da/skill
bash scripts/verificar-skill.sh https://github.com/autor/repositorio
```

Incorporar a política de `AGENTS.md` ao AGENTS.md raiz do repositório. Não sobrescrever outras instruções existentes.

O setup baixa somente o scanner e suas dependências em `.venv`. O pacote oficial inclui bibliotecas de provedores LLM, mas o verificador sempre passa `--no-llm`; não exige chaves nem realiza inferência paga. Dependências não estão fixadas transitivamente: registrar `pip freeze` e repetir os testes em cada ambiente novo.

## Decisão e relatórios

O script shell chama o verificador Python usando o ambiente isolado. Aceita URL ou caminho; não aceita opções arbitrárias para o scanner. Cada execução cria uma pasta exclusiva em `reports`, evitando reutilizar resultados antigos. Salva ajuda da CLI, saída, erros, relatório original do scanner quando disponível e `decision.json`. Quando o scanner não produz JSON, a decisão permanece JSON e registra o erro; não é apresentada como relatório de análise bem-sucedida.

Código 0: análise estática concluída sem issues, pronta para revisão. Código 1: achados, cobertura incompleta ou outra condição de veto no relatório. Código 2: falha de execução, CLI ausente, timeout ou relatório inválido/ausente. Qualquer código diferente de zero bloqueia.

Não há comando de instalação de skills neste pacote. Para usar como gate, um instalador precisa verificar o retorno e instalar somente a mesma cópia local previamente analisada, após revisão. Não instalar novamente a partir de uma URL mutável após uma análise antiga.

## Limites

Análise completa significa completa para o escopo e modo estático do scanner; não equivale a prova de segurança nem a análise semântica por LLM. URLs externas e conteúdo fora do escopo podem exigir nova inspeção. `AGENTS.md` é uma regra para agentes, não um bloqueio global do sistema operacional.

Os testes usam o scanner real: saudação benigna, instruções suspeitas de bypass e download/execução, SKILL.md UTF-16 ilegível pelo scanner e caminho inexistente. As instruções suspeitas são somente texto e nunca são executadas. `reports/test-results.json` guarda os resultados efetivos.
