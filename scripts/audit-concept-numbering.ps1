[CmdletBinding()]
param(
    [string]$VaultRoot
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($VaultRoot)) {
    $scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
    $VaultRoot = Split-Path -Parent $scriptDirectory
}

$vaultRootResolved = (Resolve-Path -LiteralPath $VaultRoot -ErrorAction Stop).Path
$conceptRoot = Join-Path $vaultRootResolved 'Knowledge\Concepts'

if (-not (Test-Path -LiteralPath $conceptRoot -PathType Container)) {
    throw "Concept root not found: $conceptRoot"
}

$utf8 = New-Object System.Text.UTF8Encoding($false, $true)
$prefixPattern = '(?i)^(?:(?:C\d{1,3}|\d{1,3}|[\u3007\u4E00\u4E8C\u4E09\u56DB\u4E94\u516D\u4E03\u516B\u4E5D\u5341\u767E\u5343\u4E24\u96F6]+)\s*(?:[-_\u3001\uFF0E:\uFF1A)\uFF09]\s*|\.(?!\d)\s*|\s+)|[\(\uFF08]\s*(?:\d+|[\u3007\u4E00\u4E8C\u4E09\u56DB\u4E94\u516D\u4E03\u516B\u4E5D\u5341\u767E\u5343\u4E24\u96F6]+)\s*[\)\uFF09]\s*|\u7B2C\s*(?:\d+|[\u3007\u4E00\u4E8C\u4E09\u56DB\u4E94\u516D\u4E03\u516B\u4E5D\u5341\u767E\u5343\u4E24\u96F6]+)\s*(?:\u7AE0|\u8282|\u8BFE|\u90E8\u5206|\u5C42)\s*(?:[-_\u3001\uFF0E.:\uFF1A)\uFF09]\s*)?)'
$issues = New-Object System.Collections.Generic.List[object]

function Get-StrictUtf8Text {
    param([string]$Path)
    return $utf8.GetString([System.IO.File]::ReadAllBytes($Path))
}

function Get-RelativeVaultPath {
    param([string]$Path)
    $prefix = $vaultRootResolved + [System.IO.Path]::DirectorySeparatorChar
    if ($Path.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $Path.Substring($prefix.Length)
    }
    return $Path
}

function Test-IdentityPrefix {
    param(
        [string]$Value,
        [string]$Path,
        [string]$Location
    )

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return
    }

    $candidate = $Value.Trim().Trim('"', "'")
    if ($candidate -match $prefixPattern) {
        $issues.Add([pscustomobject]@{
            Path = $Path
            Location = $Location
            Value = $candidate
        })
    }
}

$conceptFiles = @(Get-ChildItem -LiteralPath $conceptRoot -Recurse -File -Filter '*.md')

foreach ($file in $conceptFiles) {
    $relativePath = Get-RelativeVaultPath -Path $file.FullName
    Test-IdentityPrefix -Value $file.BaseName -Path $relativePath -Location 'filename'

    $text = Get-StrictUtf8Text -Path $file.FullName
    $frontmatterMatch = [regex]::Match($text, '\A---\r?\n(?<body>[\s\S]*?)\r?\n---')
    if ($frontmatterMatch.Success) {
        $frontmatter = $frontmatterMatch.Groups['body'].Value

        foreach ($field in @('name', 'title', 'concept_id', 'section')) {
            $fieldMatch = [regex]::Match($frontmatter, "(?m)^$field\s*:\s*(?<value>[^\r\n]+?)\s*$")
            if ($fieldMatch.Success) {
                Test-IdentityPrefix -Value $fieldMatch.Groups['value'].Value -Path $relativePath -Location "frontmatter.$field"
            }
        }

        $aliasBlockMatch = [regex]::Match($frontmatter, '(?ms)^aliases\s*:\s*(?<inline>\[[^\r\n]*\])?\s*\r?\n?(?<block>(?:[ \t]+-[^\r\n]*\r?\n?)*)')
        if ($aliasBlockMatch.Success) {
            $inlineAliases = $aliasBlockMatch.Groups['inline'].Value.Trim('[', ']')
            if (-not [string]::IsNullOrWhiteSpace($inlineAliases)) {
                foreach ($alias in ($inlineAliases -split ',')) {
                    Test-IdentityPrefix -Value $alias -Path $relativePath -Location 'frontmatter.aliases'
                }
            }
            foreach ($aliasLine in ($aliasBlockMatch.Groups['block'].Value -split '\r?\n')) {
                if ($aliasLine -match '^\s+-\s+(?<value>.+?)\s*$') {
                    Test-IdentityPrefix -Value $Matches['value'] -Path $relativePath -Location 'frontmatter.aliases'
                }
            }
        }
    }

    foreach ($headingMatch in [regex]::Matches($text, '(?m)^#{1,6}\s+(?<value>.+?)\s*$')) {
        Test-IdentityPrefix -Value $headingMatch.Groups['value'].Value -Path $relativePath -Location 'heading'
    }

    foreach ($mermaidMatch in [regex]::Matches($text, '(?ms)```mermaid\s*(?<body>.*?)```')) {
        foreach ($labelMatch in [regex]::Matches($mermaidMatch.Groups['body'].Value, '[\[\{]\s*["'']?(?<label>[^\]\}"'']+?)["'']?\s*[\]\}]')) {
            Test-IdentityPrefix -Value $labelMatch.Groups['label'].Value -Path $relativePath -Location 'mermaid label'
        }
    }
}

foreach ($file in $conceptFiles) {
    $relativePath = Get-RelativeVaultPath -Path $file.FullName
    $text = Get-StrictUtf8Text -Path $file.FullName

    foreach ($linkMatch in [regex]::Matches($text, '!?\[\[(?<body>[^\]]+)\]\]')) {
        $body = $linkMatch.Groups['body'].Value.Replace('\|', '|')
        $parts = $body -split '\|', 2
        $target = ($parts[0] -split '#', 2)[0].Replace('\', '/')
        $targetLeaf = ($target -split '/')[-1]
        Test-IdentityPrefix -Value $targetLeaf -Path $relativePath -Location 'wikilink target'

        if ($parts.Count -eq 2) {
            Test-IdentityPrefix -Value $parts[1] -Path $relativePath -Location 'wikilink alias'
        }
    }
}

if ($issues.Count -gt 0) {
    Write-Output "concept numbering audit: FAIL ($($issues.Count) issue(s))"
    foreach ($issue in ($issues | Sort-Object Path, Location, Value)) {
        Write-Output "- $($issue.Path) [$($issue.Location)]: $($issue.Value)"
    }
    exit 1
}

Write-Output "concept numbering audit: PASS ($($conceptFiles.Count) concept-area Markdown files)"
exit 0
