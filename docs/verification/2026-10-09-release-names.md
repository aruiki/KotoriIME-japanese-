# リリースの表示名変更（2026-10-09）

全18件を `TAG — 正式版/ベータ版N/リリース候補N（YYYY-MM-DD）` へ変更した。
日付は各releaseのpublished_atをJSTへ変換した日付。タグ名は変更していない。

REST PATCHのpayloadはnameのみ。各更新の直前にも旧名と同一性を確認した。
更新後に全件を再取得し、id・tag・target・本文・draft/prerelease・公開日時・URLと
全assetのid・名前・容量・digest・URL・作成日時を前の記録と照合して一致を確認した。
LatestのAPIもv1.0.0のまま。ダウンロード回数とupdated_atは照合対象外。

前後の一覧と照合結果は同名JSON。全API原本はリポジトリ外の
`C:\Users\aruik\kotori-first-check\release-names-before-20261009.json` と
`release-names-after-20261009.json` に保存した。

release_name.pyはタグを維持して段階を付ける。日付を指定しない場合はJSTの当日。
自動処理はMSI公開を行うステップで名前を作成し、UTF-8でGITHUB_ENVへ保存する。

変更は命名・README・記録のみ。本体の変換精度や実アプリでの挙動を再検証した記録ではない。
rc.3のMSIハッシュ・版・未署名/プレリリース区分は既存のrc3-release記録どおり。
