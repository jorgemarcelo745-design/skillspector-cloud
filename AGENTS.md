# Verificação obrigatória antes da instalação de skills

Antes de instalar qualquer nova skill, executar `bash scripts/verificar-skill.sh URL_OU_CAMINHO` nesta pasta. Para integração em outro repositório, copiar esta política e ajustar o caminho do script.

Instalação bloqueada por padrão: somente considerar a instalação após saída 0, relatório JSON válido, execução bem-sucedida, `analysis_completeness.is_complete` explicitamente verdadeiro, zero issues e zero supressões. Qualquer erro, timeout, opção ausente, esquema desconhecido ou cobertura incompleta bloqueia. Nunca ignorar o código de saída; nunca usar `|| true` para autorizar instalação.

Usar exclusivamente `--no-llm --format json --fail-on-findings --fail-on-incomplete`. Não usar baselines, supressões, exclusões ou credenciais para contornar achados. Não executar arquivos da skill durante a verificação. Não instalar automaticamente a skill analisada.

Revisar os riscos e limitações do relatório. A análise estática não garante ausência de vulnerabilidades. Uma liberação vale somente para o conteúdo analisado: preferir caminho local em quarentena e instalar exatamente a mesma cópia após revisão; qualquer alteração ou atualização exige nova verificação. Para URL mutável, baixar em quarentena e reanalisar a cópia exata antes de instalar.

Não chamar APIs pagas, publicar serviços ou alterar credenciais. A política orienta o agente, mas não intercepta instalações feitas fora deste fluxo.
