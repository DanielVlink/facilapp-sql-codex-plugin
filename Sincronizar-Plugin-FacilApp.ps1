[CmdletBinding()]
param(
    [string]$Destino = (Join-Path $env:LOCALAPPDATA 'FacilApp\Plugins\facilapp-sql-codex-plugin')
)

$ErrorActionPreference = 'Stop'
$url = 'https://github.com/DanielVlink/facilapp-sql-codex-plugin/archive/refs/heads/main.zip'
$zip = Join-Path $env:TEMP 'facilapp-sql-codex-plugin.zip'
$pastaTemporaria = Join-Path $env:TEMP 'facilapp-sql-codex-plugin-extraido'

Remove-Item -LiteralPath $zip -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $pastaTemporaria -Recurse -Force -ErrorAction SilentlyContinue
Invoke-WebRequest -Uri $url -OutFile $zip
Expand-Archive -LiteralPath $zip -DestinationPath $pastaTemporaria -Force

$origem = Get-ChildItem -LiteralPath $pastaTemporaria -Directory | Select-Object -First 1
if (-not $origem) { throw 'Não foi possível localizar os arquivos do plugin baixado.' }

New-Item -ItemType Directory -Force -Path $Destino | Out-Null
Copy-Item -LiteralPath (Join-Path $origem.FullName '*') -Destination $Destino -Recurse -Force

$codex = Get-Command codex -ErrorAction SilentlyContinue
if (-not $codex) {
    Write-Host "Plugin sincronizado em: $Destino"
    Write-Warning 'O comando Codex não foi encontrado. Abra o Codex e execute a instalação do marketplace dessa pasta.'
    exit 0
}

& $codex.Source plugin marketplace add $Destino
& $codex.Source plugin add 'facilapp-sql@facilapp'
Write-Host 'Plugin FacilApp SQL sincronizado e instalado. Abra uma nova tarefa do Codex para usar as ferramentas MCP.'
