# 0044. 検証済みMSIを同じファイルのままリリースに使う

- 状態: 今回のrc.3公開に適用
- 日付: 2026-10-09
- 関係: ユーザーの「最新版をリリースして本日は終える」「チェックは大掛かりにしなくてよい」、カード58、ADR0037

## 背景と判断

アイコン更新のPR142はローカルで本体・MSIのbuildを確認し、公開用CIでもMSIをbuild、導入・実入力・削除まで検証する。
同じソースをもう一度フルbuildする代わりに、CIが検証したMSIそのものをrc.3へ公開する。
キー入力や精度の条件は変更しない。未完成のLLM補正・英語候補は追加しない。

## 必須条件

1. PRの全CIが成功し、該当PRがmainへmerge commitで統合されていること。
2. MSIのbuild・単体テスト・導入・実入力・削除が同じrunで成功していること。
3. ソースhead、CIのcheckout commit、run ID、公開用commitを記録すること。公開用commitとCIソースの差分は文書と公開ノートだけに限る。
4. パッチ・workflow・training・依存固定・mozc/VERSIONなどbuildへ影響するファイルに差があれば再利用しない。通常のmainからのworkflow_dispatchへ戻る。
5. MSIはCI artifactから取得し、検証記録にあるMSIのSHA-256と一致することを確認する。MSI自体を編集しない。
6. ProductVersionの先頭3項目が前の公開版より大きいこと。コード署名・未検証範囲を公開ノートに明記する。
7. CI artifactのMSIとSHA-256をGitHub Releasesへ公開し、公開後check_release.pyで取得し直して確認する。公開MSI内のC案アイコンも照合する。

rcは引き続きプレリリースで、Latestにはしない。ソースと成果物の出所は公開記録に残す。
通常の公開はmainからMozc (Windows)を手動実行する。再利用できない場合やコード変更を含む場合は通常手順を使う。
