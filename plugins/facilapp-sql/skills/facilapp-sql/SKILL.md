---
name: facilapp-sql
description: Use a FacilApp SQL API para consultar status e OpenAPI, autenticar com Client ID e Secret, executar operações e acessar endpoints HTTP. Use quando o usuário mencionar FacilApp SQL, sql.facilapp.com.br ou pedir operações nesta API.
---

# FacilApp SQL

Use as ferramentas MCP `facilapp_*` para interagir com a API.

## Regras

- Consulte `facilapp_openapi` quando o formato de um endpoint não estiver claro.
- Use `facilapp_login` antes de uma chamada protegida.
- Nunca repita, registre ou exiba Client Secret e Bearer.
- Não invente rotas ou campos ausentes no OpenAPI.
- Trate operações de escrita como alterações externas e confirme o alvo exato.
- Preserve os dois modelos de autenticação: login completo e Client/Secret são adicionais, não substitutos.

## Fluxo normal

1. Verifique a disponibilidade com `facilapp_status`.
2. Autentique com `facilapp_login` quando necessário.
3. Use `facilapp_executar` para o dispatcher `/executar`.
4. Use `facilapp_request` para outros endpoints documentados.
