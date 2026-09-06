# Plugin Codex — FacilApp SQL

Plugin MCP para o Codex consultar a documentação, autenticar por Client/Secret e chamar a API FacilApp SQL.

## Instalação

No Windows, execute `Sincronizar-Plugin-FacilApp.ps1`. O script baixa a versão publicada, registra o marketplace local e instala o plugin no Codex.

Depois abra uma nova tarefa do Codex e peça, por exemplo: `Verifique o status da API FacilApp SQL`.

## Segurança

O Client Secret e o Bearer não são gravados pelo plugin. Eles permanecem somente na memória da sessão MCP.

Documentação da API: https://sql.facilapp.com.br/docs/
