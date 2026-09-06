"""Servidor MCP stdio para a FacilApp SQL API, sem dependências externas."""
from __future__ import annotations

import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = os.environ.get("FACILAPP_BASE_URL", "https://sql.facilapp.com.br").rstrip("/")
ACCESS_TOKEN: str | None = None


def api_request(method: str, path: str, body: Any = None, authenticated: bool = True) -> Any:
    global ACCESS_TOKEN
    headers = {"Accept": "application/json", "User-Agent": "FacilApp-SQL-MCP/0.1.0"}
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if authenticated:
        if not ACCESS_TOKEN:
            raise RuntimeError("Autentique primeiro com facilapp_login.")
        headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
    request = Request(f"{BASE_URL}/{path.lstrip('/')}", data=data, headers=headers, method=method.upper())
    try:
        with urlopen(request, timeout=45) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {"ok": True, "status": response.status}
    except HTTPError as error:
        raw = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"FacilApp API retornou HTTP {error.code}: {raw}") from error
    except URLError as error:
        raise RuntimeError(f"Não foi possível acessar {BASE_URL}: {error.reason}") from error


TOOLS = [
    {"name": "facilapp_status", "description": "Verifica o status e a versão pública da FacilApp SQL API.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "facilapp_openapi", "description": "Obtém o contrato OpenAPI oficial da FacilApp SQL API.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "facilapp_login", "description": "Autentica por Client ID e Client Secret e mantém o Bearer somente na memória deste servidor MCP.", "inputSchema": {"type": "object", "properties": {"client_id": {"type": "string"}, "client_secret": {"type": "string"}, "scope": {"type": "string"}}, "required": ["client_id", "client_secret"]}},
    {"name": "facilapp_executar", "description": "Envia um pedido autenticado ao dispatcher POST /executar da FacilApp SQL API.", "inputSchema": {"type": "object", "properties": {"pedido": {"type": "object", "additionalProperties": True}}, "required": ["pedido"]}},
    {"name": "facilapp_request", "description": "Chama um endpoint documentado da FacilApp SQL API usando o Bearer em memória quando solicitado.", "inputSchema": {"type": "object", "properties": {"method": {"type": "string", "enum": ["GET", "POST", "PUT", "PATCH", "DELETE"]}, "path": {"type": "string"}, "body": {}, "authenticated": {"type": "boolean", "default": True}}, "required": ["method", "path"]}},
]


def call_tool(name: str, args: dict[str, Any]) -> Any:
    global ACCESS_TOKEN
    if name == "facilapp_status":
        return api_request("GET", "/status", authenticated=False)
    if name == "facilapp_openapi":
        return api_request("GET", "/swagger/v1/swagger.json", authenticated=False)
    if name == "facilapp_login":
        result = api_request("POST", "/oauth/login-simples", {"client_id": args["client_id"], "client_secret": args["client_secret"], "scope": args.get("scope")}, authenticated=False)
        ACCESS_TOKEN = result.get("access_token")
        safe = dict(result)
        if "access_token" in safe:
            safe["access_token"] = "armazenado somente na memória do MCP"
        return safe
    if name == "facilapp_executar":
        return api_request("POST", "/executar", args["pedido"], authenticated=True)
    if name == "facilapp_request":
        path = str(args["path"])
        if not path.startswith("/") or "://" in path:
            raise ValueError("Informe apenas um caminho local iniciado por /.")
        return api_request(args["method"], path, args.get("body"), args.get("authenticated", True))
    raise ValueError(f"Ferramenta desconhecida: {name}")


def response(request_id: Any, result: Any = None, error: dict[str, Any] | None = None) -> None:
    payload = {"jsonrpc": "2.0", "id": request_id}
    payload["error" if error else "result"] = error if error else result
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def main() -> None:
    for line in sys.stdin:
        try:
            message = json.loads(line)
            method, request_id = message.get("method"), message.get("id")
            if method == "initialize":
                response(request_id, {"protocolVersion": "2025-06-18", "capabilities": {"tools": {}}, "serverInfo": {"name": "facilapp-sql", "version": "0.1.0"}})
            elif method == "ping":
                response(request_id, {})
            elif method == "tools/list":
                response(request_id, {"tools": TOOLS})
            elif method == "tools/call":
                params = message.get("params") or {}
                try:
                    result = call_tool(params.get("name", ""), params.get("arguments") or {})
                    response(request_id, {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]})
                except Exception as error:
                    response(request_id, {"content": [{"type": "text", "text": str(error)}], "isError": True})
            elif request_id is not None:
                response(request_id, error={"code": -32601, "message": f"Método não suportado: {method}"})
        except Exception as error:
            response(None, error={"code": -32700, "message": str(error)})


if __name__ == "__main__":
    main()
