# 59: リリース名を版から始め、試用版へ案内する

- 仕様: REQ-16-3、docs/adr/0037
- 前提: カード58（rc.3公開）
- 規模の目安: 命名関数・テスト・workflowと文書

## 目的
公開済み全18件と今後の表示名を版・段階・JST公開日でそろえる。
正式版のLatestと試用版への導線を分かりやすくする。

## 読むもの
AGENTS.md、docs/DEVELOPMENT.md 1.5、docs/adr/0037、release_tag.py、両release workflow。

## 手順
1. 公開済み名前を保存し、nameのみを更新。タグ・添付・本文・公開区分を照合する。
2. release_name.pyを両workflowから呼び、日本語名をUTF-8でGITHUB_ENVへ保存する。
3. README冒頭にrc.3と正式版へのリンクを併記する。

## テスト
版・段階・日付、未対応タグ拒否、WindowsでUTF-8環境ファイルの往復、全18件の前後照合。

## 完了条件
- [x] 公開済み全18件の名前を変更し、ほかのメタデータ・添付の一致を確認
- [x] Pythonの命名と既存の版決定テストが成功
- [x] 全CI成功後にmerge commitで統合
- [x] READMEのmain反映を確認し、第二段階を再開

## 注意
rc.3をLatestにするために正式版へ変更しない。MSIの再ビルド・再公開は行わない。

## 完了記録

PR146は全9チェック（MSI含む）成功後、2026-10-09にmerge commit 3316acad2fd24c36ea3c4eb10153e8c7d6030ce2で統合。
GitHub APIでmainのREADMEにrc.3のMSI直接リンクと正式版リンクがあることを確認した。
第二段階はPR145/148で再開済み。ダッシュボードのPR147はbaseをmainへ変更し、CIを確認中。
