# 61: Kotoriとして開けるダッシュボードを作る

- 仕様: 利用者の追加要望、REQ-6-4、REQ-14-2、REQ-15-2
- 前提: 59（表示名・README案内の統合）
- 関係: 57（設定画面の整理）、ADR0046

## 目的
設定ツールを別のソフトに見せず、Kotoriとして開けるようにする。
タイトル、ショートカット、スタートメニューをKotoriへそろえ、最初の画面をダッシュボードにする。
Windowsの操作感を保ち、AI状態と実測のCPU・RAM・計算量を数値・ゲージ・グラフで確認できるようにする。
開発支援ボタンはダッシュボードとAI設定、README・使い方案内に置く。

## 読むもの
config_dialog.cc、gui/base/util.cc、lm_rewriter.cc、installer_oss_64bit.wxs、USER_GUIDE.md。

## テストと完了条件
- [x] Windowsを含めQtタイトルとWiXのNameをKotoriへ統一。ツールのTarget/Argumentsを保持
- [x] 実測CPU・RAMと計算量を表示。取得できない値は未確認とし、古い/別プロセスの状態を拒否
- [x] 数値・ゲージ・直近60秒までのCPUグラフを実装。入力処理へ計測用I/Oを追加しない
- [x] 支援ページは明示的なクリックでブラウザーを開く
- [x] Windows QPAで通常/150%表示を確認。設定を保存しない画面テストと既存LMテストが成功
- [x] 実辞書・実モデルの隔離セッションでPIDと計算量の更新を確認（実TSFの代替ではない）
- [x] 最終パッチの新規cloneへの適用確認
- [ ] MSIを含む全CIが成功
- [ ] 全CI成功後にmerge commitで統合

旧rc.3の公開済みMSIは変更しない。rc.3の導入手順には旧表示名も併記する。
検証の範囲は `docs/verification/2026-10-09-dashboard.md`。
