$f = 'HKLM\SOFTWARE\Classes\SystemFileAssociations'
$d = 'HKLM\SOFTWARE\Classes\Directory'
$m = 'shell\customCmds'
$s = 'shell\customCmds\shell\convertvideo'

$iniFile = Get-Content -RAW .\config.ini
$rawValues = [regex]::matches($iniFile, "(?smi)(?<=file_types =\s*\n)(.+)(?=\nuse_hevc)").value -split '\s+' | where {$_}

$rawValues | ForEach-Object {
    nircmd elevatecmd regsetval sz "$f\$_\$m" "MUIVerb" "Custom Commands"
    nircmd elevatecmd regsetval sz "$f\$_\$m" "SubCommands" "~x00"
    nircmd elevatecmd regsetval expand_sz "$f\$_\$m" "Icon" "%SYSTEMROOT%\System32\shell32.dll,-16773"

    nircmd elevatecmd regsetval sz "$f\$_\$s" "MUIVerb" "Convert Video"
    nircmd elevatecmd regsetval expand_sz "$f\$_\$s" "Icon" "%SYSTEMROOT%\System32\imageres.dll,-5357"

    nircmd elevatecmd regsetval sz "$f\$_\$s\command" "~x00" "powershell -command ~qSet-Location \~q$PSScriptRoot\~q; py -m convertvideo \~q%1\~q~q"
}

nircmd elevatecmd regsetval sz "$d\$s" "MUIVerb" "Convert Videos"
nircmd elevatecmd regsetval expand_sz "$d\$s" "Icon" "%SYSTEMROOT%\System32\imageres.dll,-5357"
nircmd elevatecmd regsetval sz "$d\$s\command" "~x00" "powershell -command ~qSet-Location \~q$PSScriptRoot\~q; py -m convertvideo \~q%1\~q~q"

nircmd elevatecmd regsetval sz "$d\background\$s" "MUIVerb" "Convert Videos"
nircmd elevatecmd regsetval expand_sz "$d\background\$s" "Icon" "%SYSTEMROOT%\System32\imageres.dll,-5357"
nircmd elevatecmd regsetval sz "$d\background\$s\command" "~x00" "powershell -command ~qSet-Location \~q$PSScriptRoot\~q; py -m convertvideo \~q%W\~q~q"


Wait-Process -Name nircmd
nircmd stdbeep