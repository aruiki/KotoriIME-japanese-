# 61: 設定の入口と画面名をKotoriへ統一する

- 仕様: 利用者の表示名統一の依頼、REQ-16-3
- 前提: 59（表示名・README案内の統合）
- 規模の目安: GUI1箇所、WiX3箇所、文書

## 目的
設定ツールを別のソフトに見せず、Kotoriとして開けるようにする。
設定画面のタイトル、デスクトップとスタートメニューのショートカット名・フォルダ名をKotoriへそろえる。

## 読むもの
config_dialog.cc、installer_oss_64bit.wxs、USER_GUIDE.md。

## テストと完了条件
- [x] QtのタイトルとWiXのNameを確認し、ツールを開くTarget/Argumentsを保持
- [x] パッチを元ソースから再生成し、新規cloneへ3パッチが適用できる
- [x] Windows設定ツールのbuild成功
- [ ] MSI CIが成功
- [ ] 全CI成功後にmerge commitで統合

旧rc.3の公開済みMSIは変更しない。rc.3の導入手順には旧表示名も併記する。
