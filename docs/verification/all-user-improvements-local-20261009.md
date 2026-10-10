# 全改善案のローカル検証（2026-10-09、カード64）

配布準備中。新しい公開リリースではない。元の公開版はv1.1.0-rc.3。
CLIセッション、Qt描画、MSI内容、インストール済みWindows TSFを区別する。
本記録は後続のソース・MSIで過去の失敗を上書きしない。

## 対象

実リポジトリ: aruiki/KotoriIME-japanese-、枝codex/complete-user-improvements。
正本C:/Users/aruik/mzcorrection、build C:/Users/aruik/mzicons。
Mozc固定コミットa069a88d4cb5c011de0f9aebb6c149a1c808d904。
make_patches.shから再生成し、新規cloneへ0001〜0003の適用と112入力の完全一致を確認。
入力とパッチのSHA-256は同名JSONとC:/Users/aruik/kotori-first-check/all-request-rc4-source-manifest.json。
BUILD_OSS/BUILDは6330。公開rc.3の3.34.6322.100より先頭3項目を上げた。

## 実装とローカル確認

| 項目 | 結果と境界 |
| --- | --- |
| 初回のAI評価と生成補正 | 既定有効。読みは即時、候補だけ非同期で待つ。実モデルで「ちょと待ってください」→「ちょっと待ってください」、初回約1017ms、直接Space約1.2msで同じ文。足の例も初回/直接Space一致。すべての誤入力を直すものではない。 |
| 誤入力への生成寄与 | 同じEXEのOFF/ON15文で採用1件。誤入力10文の初回期待一致は3→4。採点差5.0、名前/数値/文法保護を保持。6文は改善せず。Tab取消後のSpaceは世代を失効するので、直接Spaceの証拠に使わない。 |
| 続き予測 | 29文中8文で続き。計算が落ち着いた表示とTabは29文で相違0。最初の本文表示の後に続きへ更新する2文では初回とTabに相違あり。初回=最終と呼ばない。 |
| 正常文の保護 | 100文の共有補正関数・実辞書/実モデルで変更0。別の正常文100文OFF/ONセッションは両方Space100/100、生成採用0。ただし集計が不正UTF-8のログで失敗したため、全体PASSとは扱わない。原票は保存。 |
| 不正UTF-8 | 予測を採点/保存/表示する前に拒否。LM回帰50ケースPASS。「五十歩百歩の」の実モデルセッションも異常終了なし。ログの採用件数はバイト列から数え、プロトコルの厳密UTF-8読取は維持。 |
| 意味の候補とフォーカス | ユーザーのカブトムシの長文でSpace2は「特長は」へ。他の文節は変化なし。AIが7文節にまとめたFIXED_BOUNDARYでの失敗を修正。Nuance9/Engine86ケースPASS。境界/読み/固定値/保護属性を維持。 |
| 英語の候補 | index/effect/internetが初回一覧、Tab、Spaceに存在することを最終EXEで確認。 |
| 文字種 | 末尾と副候補の表示だけを除去。内部ID/F6〜F10、既存の文節操作・学習を保持。関連Session189ケースPASS。 |
| Kotoriダッシュボード | 名称/AIの実状態/CPU/メモリ/推移/支援ボタンを統合。Windows QPAの100/150/200%でGUI2ケースPASS、画面確認。隔離profile/mock clientで設定は保存しない。入力中の実画面ではない。 |
| CPUだけの起動と即Space | 開発PCをCPU強制、冷間10文字/冷間長文/12秒準備後の足の例の3セッションが正常終了。冷間Space約1.2/5.7ms、準備後約249ms。冷間の最大打鍵応答約148ms。実際の低性能PCの証拠ではない。冷間長文は通常変換へ戻り「なんと行って」となる。 |

候補を待つ上限を超えると通常変換へ戻す。モデル未準備の状況まで、すべての初回候補を補正できたとは主張しない。
生成する補正は40文字以下・一字の読み違いと局所の表記を対象にし、一般的な自由な文章の書換えは行わない。

## 品質

RTX 3060、通常Standard、同梱モデル。
AJIMEE-Bench（文脈あり）183/200=91.5%、90%以上の条件を満たした。
最終報告専用heldoutは289/300=96.3%、調整には使わなかった。
work50/50、chat47/50、tech50/50、name47/50、num45/50、news50/50。
これは変換器の評価であり、Microsoft IME/Google日本語入力との実入力比較ではない。
最終のFIXED_BOUNDARY修正前の変換器EXEで実施し、EXE/モデル/データSHAは各原票のmanifestに記録。
後続は意味の別候補と日本語コメントの変更だけで、先頭候補の選択・モデル・辞書を変更していない。

## 原票

全原票はC:/Users/aruik/kotori-first-check/に保存。
- all-request-ajimee-final.json/.json.manifest.json、all-request-heldout-final.json/.json.manifest.json
- all-request-prediction-29-final.json、all-request-focused-15-final.json
- all-request-typing-final-direct.json、all-request-lifecycle-final.json
- all-request-normal-100-shared-final.json、all-request-normal-100-before-utf8-analysis.json
- all-request-nuance-final.json（失敗）、all-request-nuance-boundary-final.json（修正後）
- all-request-english-final-{index,effect,internet}.json、all-request-cpu-final-summary.json
- all-request-utf8-final-tests.log、all-request-nuance-boundary-tests.log、all-request-nuance-gui-150-final-tests.log
- all-request-gui-final-{100,150,200}/、all-request-patches-rc4-final.log

## 配布の残り

最終のMSIをローカルでbuildし、内容・ProductVersion・同梱モデル/ライセンス・ハッシュを検査する。
19:23の以前のMSIはこの後の補正修正前なので配布しない。
インストール済みTIPでのアプリ入力・上書き更新・アンインストールは未実施。
Windows Computer UseのInitializeは規定の回復を含め3回タイムアウトしたため停止した。
専用runner用installer_smoke/IMEBenchの保護条件は偽装しない。
MSI展開、CLI成功、GUIの描画を実機受け入れPASSへ置き換えない。
完成した成果物ができてから、残る実機確認を具体的に提示する。

## 最終ローカルMSI（21:07完成）

- ソース25cd371b1b916cdb81577c87beff37e0def12bc9、112入力manifest 6587c1691d86b239737dd97abf883c05cbafef5886c7503372ba65730f1c75b4。
- build終了0、949.23秒。MSIは1,568,378,880 byte（約1.46 GiB）。
- ProductVersion/同梱serverは3.34.6330.100、前のrc.3/このPCの導入版3.34.6322.100より先頭3項目が大きい。
- SHA-256: 86dc529a3d1ce6e10f0a51dfd7e033b3620eea9b3c8373daf9004e0b8c4094ec。
- 署名NotSigned。通常版のLatestにはしない。
- check_release.py --localの管理展開は出力先ができないまま5分以上停止し、検査用clientだけを停止した。元の非0終了/記録を保存。共有Windows Installerサービスは停止していない。
- WiX 5.0.2の読み取り専用decompileでMSIを変更せず9.37秒で展開。check_release.pyの同梱/除外/サイズ/版の条件を同じまま確認した。導入試験ではない。
- 45ファイル。3モデルと17runtime DLLのハッシュは実モデル評価に使った既存ファイルと一致。
- server/tool/TIP64は最終buildの出力と同一、3アイコンと2背景は正本と同一。設定ショートカットはデスクトップ/メニューともKotori。
- 境界修正後の最終converterもAJIMEE183/200=91.5%（32秒）。対象112入力のハッシュを再確認。元のmanifestのgit commit欄はMozc cache側のHEADであり、配布ソースは上記25cd371とoverlay SHAで対応させる。原票は変更しない。
- 完成ファイル: C:/Users/aruik/kotori-first-check/rc4-release-20261009-25cd371/Kotori64.msi、同.sha256、source-manifest.json、release-evidence.json。

実機の上書き導入・メモ帳等の初回/Tab/Space・削除は引き続き未確認。現在のインストール済みバイナリは6322のまま。
公開承認は利用者から既にある。残っているのは同じ許可の再取得ではなく、実機受け入れの結果。
