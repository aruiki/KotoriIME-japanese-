# Kotori: MSP cabinetを導入せず読取りで確認する。
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Patch,
      [Parameter(Mandatory)][string]$TargetMsi,
      [Parameter(Mandatory)][string]$OutputJson)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
Add-Type -TypeDefinition @'
using System;
using System.IO;
using System.Text;
using System.Collections.Generic;
using System.Runtime.InteropServices;
public static class KotoriPatchInspection {
  [DllImport("msi.dll", CharSet=CharSet.Unicode)] static extern uint MsiOpenDatabaseW(string p, IntPtr mode, out uint db);
  [DllImport("msi.dll", CharSet=CharSet.Unicode)] static extern uint MsiDatabaseOpenViewW(uint db, string sql, out uint view);
  [DllImport("msi.dll")] static extern uint MsiViewExecute(uint v, uint record);
  [DllImport("msi.dll")] static extern uint MsiViewFetch(uint v, out uint record);
  [DllImport("msi.dll")] static extern uint MsiRecordReadStream(uint r, uint f, byte[] buf, ref uint bytes);
  [DllImport("msi.dll")] static extern uint MsiCloseHandle(uint h);
  static void Check(uint code) { if(code != 0) throw new InvalidDataException("MSI error " + code); }
  public static string[] CabinetFiles(string patch) {
    uint db=0,view=0;
    var result = new List<string>();
    try {
      Check(MsiOpenDatabaseW(patch,new IntPtr(32),out db)); // READONLY | PATCHFILE
      Check(MsiDatabaseOpenViewW(db,"SELECT Data FROM _Streams",out view));
      Check(MsiViewExecute(view,0));
      uint record;
      uint rc;
      while((rc=MsiViewFetch(view,out record)) == 0) {
        try {
          uint bytes=0;
          Check(MsiRecordReadStream(record,1,null,ref bytes));
          if(bytes < 36 || bytes > 100*1024*1024) continue;
          var data = new byte[bytes];
          Check(MsiRecordReadStream(record,1,data,ref bytes));
          if(data[0]!='M'||data[1]!='S'||data[2]!='C'||data[3]!='F') continue;
          uint offset = BitConverter.ToUInt32(data,16);
          ushort count = BitConverter.ToUInt16(data,28);
          using(var memory=new MemoryStream(data))
          using(var reader=new BinaryReader(memory)) {
            memory.Position=offset;
            for(int i=0;i<count;i++) {
              memory.Position += 16;
              var name=new List<byte>();
              byte b;
              while((b=reader.ReadByte())!=0) name.Add(b);
              result.Add(Encoding.UTF8.GetString(name.ToArray()));
            }
          }
        } finally { MsiCloseHandle(record); }
      }
      if(rc!=259) Check(rc);
    } finally { if(view!=0) MsiCloseHandle(view); if(db!=0) MsiCloseHandle(db); }
    if(result.Count==0) throw new InvalidDataException("MSPにcabinet payloadがありません。");
    return result.ToArray();
  }
}
'@
$Patch = (Resolve-Path -LiteralPath $Patch).Path
$TargetMsi = (Resolve-Path -LiteralPath $TargetMsi).Path
$installer = New-Object -ComObject WindowsInstaller.Installer
$db = $installer.OpenDatabase($TargetMsi,0)
$view = $db.OpenView('SELECT File, FileName FROM File')
$names = @{}
try {
    [void]$view.Execute()
    while ($row = $view.Fetch()) {
        $names[$row.StringData(1)] = ($row.StringData(2) -split '\|')[-1]
        [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($row)
    }
} finally {
    [void]$view.Close()
    [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($view)
    [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($db)
}
$entries = @([KotoriPatchInspection]::CabinetFiles($Patch) | ForEach-Object {
    if (!$names.ContainsKey($_)) { throw "未知のpayload IDです: $_" }
    [ordered]@{id=$_; name=$names[$_]}
})
if (@($entries | Where-Object { $_.name -like '*.gguf' }).Count -gt 0) { throw 'モデルが差分に含まれています。' }
$receipt = [ordered]@{
    scope='read-only MSP cabinet inspection, not an install test'
    patch_sha256=(Get-FileHash -LiteralPath $Patch).Hash.ToLowerInvariant()
    payload_files=$entries; model_files_absent=$true
}
$receipt | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $OutputJson -Encoding utf8
$receipt | ConvertTo-Json -Depth 5
