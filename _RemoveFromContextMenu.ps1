$iniFile = Get-Content -RAW .\config.ini
$rawValues = [regex]::matches($iniFile, "(?smi)(?<=file_types =\s*\n)(.+)(?=\nuse_hevc)").value -split '\s+' | where {$_}

$rawValues | ForEach-Object {
    nircmd elevate powershell "Remove-Item -LiteralPath HKLM:\SOFTWARE\Classes\SystemFileAssociations\$_\shell\customCmds -Recurse"
}

nircmd elevate powershell "Remove-Item -LiteralPath HKLM:\SOFTWARE\Classes\Directory\shell\customCmds\shell\convertvideo -Recurse"

nircmd elevate powershell "Remove-Item -LiteralPath HKLM:\SOFTWARE\Classes\Directory\Background\shell\customCmds\shell\convertvideo -Recurse"


Wait-Process -Name nircmd
nircmd stdbeep