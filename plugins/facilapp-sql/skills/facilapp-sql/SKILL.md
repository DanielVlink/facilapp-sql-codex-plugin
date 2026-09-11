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
- O cadastro de usuário contém empresa, sistema, usuário e senha; não existe cadastro separado de credencial.
- No endpoint `/oauth/login-simples`, `client_id` é encaminhado internamente como usuário e `client_secret` como senha.
- Não envie `scope` no login simples; envie somente `client_id` e `client_secret`.
- Diferencie `listar_tabelas`, que retorna nomes de tabelas, de `consultar`, que retorna registros.
- A atualização do banco interno ocorre automaticamente na inicialização; não procure nem use endpoint público de atualização estrutural.
- A API completa automaticamente o `FacilAppSQL.ini` na inicialização: cria somente seções e chaves ausentes com valores padrão e nunca apaga ou substitui valores existentes.
- `ServidorHTTP.TimeoutSegundos` usa 180 segundos quando o campo estiver ausente.
- `IA.TimeoutSegundos` usa 300 segundos quando estiver ausente e controla exclusivamente as consultas à OpenAI, inclusive busca na web.
- Instalação, atualização e desinstalação preservam o INI e os bancos existentes.
- Para importar menus, use `facilapp_importar_menu`. A pasta deve conter `MenuData.js`, `MenuSuperiorData.js` e `DashboardData.js`; somente `MenuData.js` não pode estar vazio.
- Para consultar endereço por CEP, use `facilapp_consultar_cep`. Informe 8 dígitos, com ou sem máscara; a consulta não exige chave externa.

## Fluxo normal

1. Verifique a disponibilidade com `facilapp_status`.
2. Autentique com `facilapp_login` quando necessário.
3. Use `facilapp_listar_tabelas` para descobrir as tabelas existentes.
4. Use `facilapp_consultar` para consultar registros de uma tabela.
5. Use `facilapp_executar` para as demais funções do dispatcher `/executar`.
6. Use `facilapp_request` para outros endpoints documentados.
