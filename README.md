<h1 align="center">Kotori日本語入力</h1>

<p align="center">
  <strong>AIで、もっと正確な日本語入力へ。</strong><br>
  文脈を理解するAIで、従来のIMEを大きく上回る変換精度を目指したWindows向け日本語IME。
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

---

## AIで、変換精度を大きく引き上げる

KotoriはMozcをベースに、AIが複数の変換候補を**文章全体の文脈から評価**します。

読みだけでは判断しにくい同音異義語や、前後の文章によって意味が変わる表現でも、より自然な候補を選びます。

<p align="center">
  <img src="docs/images/ime-comparison.png" alt="IME実入力比較" width="880">
</p>

| IME | AJIMEE-Bench 198問 |
| --- | ---: |
| **Kotori日本語入力** | **88.4%** |
| Microsoft IME | 59.6% |
| Google 日本語入力 | 58.1% |

実際に各IMEへ同じ読みを入力し、Spaceを1回押したときの第1候補を比較しています。

> Kotori beta.8 / Unreal、2026-10-01測定。現在版の再測定値ではありません。

[測定方法・データを見る](eval/README.md)

---

## 変換例

<p align="center">
  <img src="docs/images/examples.png" alt="Kotori日本語入力の変換例" width="880">
</p>

| 読み | Mozc | Kotori |
| --- | --- | --- |
| かれはこうえんでこうえんをした | 彼は公園で公園をした | 彼は公園で**公演**をした |
| おんせいにんしきのせいどがあがった | 音声認識の制度が上がった | 音声認識の**精度**が上がった |
| あしたのかいぎはじゅうじからです | 明日の会議は従事からです | 明日の会議は**10時**からです |

---

## ほかにも便利なポイント

### カタカナから英語へ

カタカナ語を入力すると、そのまま英語表記も変換候補に出せます。

- アーキテクチャ → `architecture`
- アクセシビリティ → `accessibility`
- コンフィギュレーション → `configuration`
- レストラン → `restaurant`

31,068の読み・36,402組の英語表記を収録しており、辞書の追加インストールは不要です。

### AI予測

入力中に、変換候補や文章の続きを先回りして生成します。

### 完全ローカル

AIも辞書もPC内で動作し、入力した文章を外部サーバーへ送信しません。

### GPUなしでも動作

専用GPUがない環境では、自動的にCPU向け設定へ切り替わります。

### Mozcベース

Mozcの操作感、学習、ユーザー辞書をそのまま利用できます。
