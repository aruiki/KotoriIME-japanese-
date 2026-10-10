<h1 align="center">Kotori日本語入力</h1>

<p align="center">
  <strong>AIが文脈まで読んで変換する、Windows向け日本語IME。</strong><br>
  Mozcベース・完全ローカル・GPUなしでも動作。
</p>

<p align="center">
  <a href="https://github.com/aruiki/Kotori-AI-Japanese-IME/releases/latest"><img alt="正式版" src="https://img.shields.io/github/v/release/aruiki/Kotori-AI-Japanese-IME?label=%E6%AD%A3%E5%BC%8F%E7%89%88&color=242C5C"></a>
  <a href="https://github.com/aruiki/Kotori-AI-Japanese-IME/releases"><img alt="ダウンロード数" src="https://img.shields.io/github/downloads/aruiki/Kotori-AI-Japanese-IME/total?label=%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89&color=242C5C"></a>
  <img alt="Windows 10 / 11" src="https://img.shields.io/badge/Windows-10%20%2F%2011-242C5C?logo=windows">
  <img alt="完全ローカル" src="https://img.shields.io/badge/AI-%E5%AE%8C%E5%85%A8%E3%83%AD%E3%83%BC%E3%82%AB%E3%83%AB-F25C2E">
</p>

<h2 align="center">
  <a href="https://github.com/aruiki/Kotori-AI-Japanese-IME/releases/latest/download/Kotori64.msi">⬇ Kotoriをインストール</a>
</h2>

<p align="center">
  Windows 10 / 11・64bit
</p>

---

## 文脈を読んで、変換を選ぶ

<p align="center">
  <img src="docs/images/examples.png" alt="Kotori日本語入力の変換例" width="880">
</p>

KotoriはMozcの候補を、AIが**文全体の意味から選び直します**。

「公園 / 公演」「制度 / 精度」「薬 / 訳」のような、読みだけでは決めにくい変換を文脈から判断します。

直前に確定した文章も文脈として利用できます。

---

## 実入力で88.4%

<p align="center">
  <img src="docs/images/ime-comparison.png" alt="IME実入力比較" width="880">
</p>

| IME | AJIMEE-Bench 198問 |
| --- | ---: |
| **Kotori日本語入力** | **88.4%** |
| Microsoft IME | 59.6% |
| Google 日本語入力 | 58.1% |

実際に各IMEへ読みを入力し、**Space 1回目の候補**を同じ条件で比較しています。

> Kotori beta.8 / Unreal、2026-10-01測定。現在版の再測定値ではありません。

測定方法・CSV・追加ベンチマーク → [eval/README.md](eval/README.md)

---

## Kotoriの特徴

- **文脈変換** — AIが文章全体から自然な候補を選択
- **入力中のAI予測** — 手を止めると変換と文章の続きを先回り
- **完全ローカル** — 入力した文章を外部サーバーへ送信しない
- **Mozcベース** — 学習・ユーザー辞書・操作感をそのまま利用
- **GPUなしでも動作** — 環境に合わせて自動調整
- **VRAMを自動解放** — 10分使わなければAIモデルをGPUから外す

通常のキー入力はMozcが処理するため、AIの計算で打鍵を待たせません。

---

## インストール

### 1. ダウンロード

**[Kotori64.msi をダウンロード](https://github.com/aruiki/Kotori-AI-Japanese-IME/releases/latest/download/Kotori64.msi)**

### 2. 実行

`Kotori64.msi` を開いてインストールします。

Windowsで「PCが保護されました」と表示された場合は、

**詳細情報 → 実行**

を選択してください。

### 3. 切り替える

**Windows + Space** → **Kotori日本語入力**

これで使えます。

---

## 動作環境

| | 必須 | おすすめ |
| --- | --- | --- |
| OS | Windows 10 1809以降 / 64bit | Windows 11 |
| メモリ | 8GB | 16GB |
| GPU | なくても動作 | Vulkan対応GPU / VRAM 3GB以上 |
| ディスク | 1.7GB | — |

NVIDIA / AMD / Intel Arcの専用GPUは自動検出します。

追加のAI環境やPythonなどをインストールする必要はありません。

---

## プライバシー

**変換もAIもPCの中だけで動作します。**

入力した文章、利用状況、テレメトリを外部サーバーへ送信しません。

詳しくは [使い方と困ったとき](docs/USER_GUIDE.md#データとプライバシー) を参照してください。

---

## ドキュメント

- [使い方・トラブル対処](docs/USER_GUIDE.md)
- [評価方法・ベンチマーク](eval/README.md)
- [性能測定](docs/PERFORMANCE.md)
- [設計記録](docs/adr/)
- [開発方法](docs/DEVELOPMENT.md)

不具合・誤変換・要望は [Issues](../../issues/new/choose) へお願いします。

---

## ライセンス

Kotoriのコードは **Apache License 2.0 / MIT License** のデュアルライセンスです。

Mozcへの変更はBSD-3-Clauseです。

第三者コンポーネントについては [docs/licenses.md](docs/licenses.md) を参照してください。

---

<h2 align="center">
  <a href="https://github.com/aruiki/Kotori-AI-Japanese-IME/releases/latest/download/Kotori64.msi">⬇ Kotori日本語入力を試す</a>
</h2>

<p align="center">
  無料・オープンソース・完全ローカル
</p>
