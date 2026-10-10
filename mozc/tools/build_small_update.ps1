# Kotori: ローカルMSP試作。実機へ導入せず、公開MSIを変更しない。
# 対象GUIDの正規化は私的な更新imageだけ。実機・rollback・後続MSI移行は別途検証が必要。
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$BaseMsi,
    [Parameter(Mandatory)][string]$TargetMsi,
    [Parameter(Mandatory)][string]$BaseEvidence,
    [Parameter(Mandatory)][string]$TargetEvidence,
    [Parameter(Mandatory)][string]$Wix,
    [Parameter(Mandatory)][string]$OutputDirectory,
    [Parameter(Mandatory)][switch]$Prototype
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (!$Prototype) { throw '実機検証前の試作にのみ使用できます。' }
$BaseMsi = (Resolve-Path -LiteralPath $BaseMsi).Path
$TargetMsi = (Resolve-Path -LiteralPath $TargetMsi).Path
$Wix = (Resolve-Path -LiteralPath $Wix).Path
if ($BaseMsi -eq $TargetMsi) { throw '元MSIと更新MSIは別のファイルが必要です。' }
$baseline = Get-Content -LiteralPath $BaseEvidence -Raw | ConvertFrom-Json
$target = Get-Content -LiteralPath $TargetEvidence -Raw | ConvertFrom-Json
$baseHash = (Get-FileHash -LiteralPath $BaseMsi -Algorithm SHA256).Hash.ToLowerInvariant()
$targetHash = (Get-FileHash -LiteralPath $TargetMsi -Algorithm SHA256).Hash.ToLowerInvariant()
if ($baseHash -ne $baseline.msi_sha256 -or $targetHash -ne $target.msi_sha256) {
    throw 'MSIのハッシュが検証記録と一致しません。'
}
$models = @($baseline.model_sha256.PSObject.Properties | Sort-Object Name)
$updatedModels = @($target.model_sha256.PSObject.Properties | Sort-Object Name)
if ($models.Count -ne 3 -or $updatedModels.Count -ne 3) { throw '3モデルの検証記録が必要です。' }
for ($i = 0; $i -lt 3; ++$i) {
    if ($models[$i].Name -ne $updatedModels[$i].Name -or
        $models[$i].Value -ne $updatedModels[$i].Value) { throw 'モデル更新は軽量差分の対象外です。' }
}
$installer = New-Object -ComObject WindowsInstaller.Installer
function Read-Property($database, [string]$name) {
    $view = $database.OpenView('SELECT `Value` FROM `Property` WHERE `Property`=''' + $name + '''')
    try { [void]$view.Execute(); $row = $view.Fetch(); if (!$row) { throw "MSIに$nameがありません。" }; return $row.StringData(1) }
    finally { [void]$view.Close(); [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($view) }
}
function Read-Identity([string]$path) {
    $db = $installer.OpenDatabase($path, 0)
    try {
        return [ordered]@{
            product_code = Read-Property $db 'ProductCode'
            upgrade_code = Read-Property $db 'UpgradeCode'
            version = Read-Property $db 'ProductVersion'
            language = Read-Property $db 'ProductLanguage'
        }
    } finally { [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($db) }
}
$baseId = Read-Identity $BaseMsi
$targetId = Read-Identity $TargetMsi
if ($baseId.upgrade_code -ne $targetId.upgrade_code -or $baseId.language -ne $targetId.language) {
    throw '製品系列または言語が異なります。'
}
if ($baseId.version -ne $baseline.product_version -or $targetId.version -ne $target.product_version) {
    throw 'MSIの版が検証記録と一致しません。'
}
$oldVersion = [version]$baseId.version
$newVersion = [version]$targetId.version
if ($newVersion -le $oldVersion -or ($newVersion.Major -eq $oldVersion.Major -and
    $newVersion.Minor -eq $oldVersion.Minor -and $newVersion.Build -eq $oldVersion.Build)) {
    throw 'Windows Installerが区別できる上位版が必要です。'
}
[void][guid]::Parse($baseId.product_code)
$OutputDirectory = [IO.Path]::GetFullPath($OutputDirectory)
if (Test-Path -LiteralPath $OutputDirectory) { throw '既存の出力を上書きしません。新しい出力フォルダーを指定してください。' }
[void](New-Item -ItemType Directory -Path $OutputDirectory)
$privateImage = Join-Path $OutputDirectory 'private-update-image.msi'
Copy-Item -LiteralPath $TargetMsi -Destination $privateImage
(Get-Item -LiteralPath $privateImage).IsReadOnly = $false
$db = $installer.OpenDatabase($privateImage, 1)
try {
    $view = $db.OpenView('UPDATE `Property` SET `Value`=''' + $baseId.product_code + ''' WHERE `Property`=''ProductCode''')
    try { [void]$view.Execute() } finally { [void]$view.Close(); [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($view) }
    [void]$db.Commit()
} finally { [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($db) }
$patchFile = Join-Path $OutputDirectory ('Kotori-' + $baseId.version + '-to-' + $targetId.version + '-prototype.msp')
$escape = { param([string]$text) [Security.SecurityElement]::Escape($text) }
$baseXml = & $escape $BaseMsi
$updateXml = & $escape $privateImage
$source = @"
<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs">
  <Patch AllowRemoval="yes" DisplayName="Kotori $($targetId.version) 更新試作"
         Description="Kotoriのモデルを再利用するローカル検証用更新"
         Manufacturer="Kotori Project" Classification="Update"
         MoreInfoURL="https://github.com/aruiki/KotoriIME-japanese-/releases">
    <Media Id="1" Cabinet="update.cab">
      <PatchBaseline Id="Baseline" BaselineFile="$baseXml" UpdateFile="$updateXml">
        <Validate ProductId="yes" ProductLanguage="yes" UpgradeCode="yes"
                  ProductVersion="Update" ProductVersionOperator="Equal" />
      </PatchBaseline>
    </Media>
    <PatchFamily Id="KotoriLocalUpdate" Version="$($targetId.version)" />
  </Patch>
</Wix>
"@
$sourceFile = Join-Path $OutputDirectory 'Patch.wxs'
[IO.File]::WriteAllText($sourceFile, $source, [Text.UTF8Encoding]::new($false))
[GC]::Collect()
[GC]::WaitForPendingFinalizers()
& $Wix build $sourceFile -out $patchFile *> (Join-Path $OutputDirectory 'build.log')
if ($LASTEXITCODE -ne 0) { throw "MSP生成失敗。build.logを確認してください（$LASTEXITCODE）。" }
if ((Get-Item -LiteralPath $patchFile).Length -ge 100MB) { throw '差分が100MiB以上です。モデルの混入を確認してください。' }
if ((Get-FileHash -LiteralPath $BaseMsi).Hash.ToLowerInvariant() -ne $baseHash -or
    (Get-FileHash -LiteralPath $TargetMsi).Hash.ToLowerInvariant() -ne $targetHash) { throw '元MSIが変化しました。公開しないでください。' }
& (Join-Path $PSScriptRoot 'inspect_small_update.ps1') -Patch $patchFile -TargetMsi $TargetMsi -OutputJson (Join-Path $OutputDirectory 'cabinet-inspection.json') *> (Join-Path $OutputDirectory 'inspection.log')
$receipt = [ordered]@{
    scope = 'local prototype package only; not installed or published'
    base_source = $baseline.source_commit; target_source = $target.source_commit
    base_msi_sha256 = $baseHash; target_msi_sha256 = $targetHash
    base_identity = $baseId; target_identity = $targetId
    private_update_identity = Read-Identity $privateImage
    model_sha256 = $target.model_sha256
    patch_sha256 = (Get-FileHash -LiteralPath $patchFile).Hash.ToLowerInvariant()
    patch_size_bytes = (Get-Item -LiteralPath $patchFile).Length
    original_msi_unchanged = $true
    cabinet_model_files_absent = $true
    native_install = 'unperformed'; rollback = 'unperformed'; later_major_upgrade = 'unperformed'
}
$receipt | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath (Join-Path $OutputDirectory 'prototype-receipt.json') -Encoding utf8
Write-Output ($receipt | ConvertTo-Json -Depth 7)
