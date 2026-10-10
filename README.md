<h1 align="center">Kotori日本語入力</h1>

<p align="center">
  <strong>文脈を読んで、変換を選び直すAI日本語IME。</strong><br>
  Mozcの使いやすさはそのまま。AIはPC内だけで動作します。
</p>

<p align="center">
  <a href="https://github.com/aruiki/KotoriIME-japanese-/releases/latest"><img alt="正式版" src="https://img.shields.io/github/v/release/aruiki/KotoriIME-japanese-?label=%E6%AD%A3%E5%BC%8F%E7%89%88&color=242C5C"></a>
  <a href="https://github.com/aruiki/KotoriIME-japanese-/releases"><img alt="ダウンロード数" src="https://img.shields.io/github/downloads/aruiki/KotoriIME-japanese-/total?label=%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89&color=242C5C"></a>
  <img alt="Windows 10 / 11" src="https://img.shields.io/badge/Windows-10%20%2F%2011-242C5C?logo=windows">
  <img alt="オフライン" src="https://img.shields.io/badge/%E3%82%AA%E3%83%95%E3%83%A9%E3%82%A4%E3%83%B3-%E9%80%9A%E4%BF%A1%E3%81%AA%E3%81%97-F25C2E">
</p>

<h2 align="center">
  <a href="https://github.com/aruiki/KotoriIME-japanese-/releases/download/v1.1.0/Kotori64.msi">⬇ Kotori日本語入力をダウンロード</a>
</h2>

<p align="center">
  Windows 10 / 11・64bit
</p>

---

## 「こうえん」を、公園だけで終わらせない

通常のIMEが候補を作ったあと、KotoriはAIで**文全体の意味を見て候補を選び直します**。

<p align="center">
  <img src="docs/images/examples.png" alt="Kotori日本語入力の変換例" width="880">
</p>

| 入力 | 一般的な変換例 | Kotori |
| --- | --- | --- |
| かれはこうえんでこうえんをした | 彼は公園で公園をした | 彼は公園で**公演**をした |
| おんせいにんしきのせいどがあがった | 音声認識の制度が上がった | 音声認識の**精度**が上がった |
| あしたのかいぎはじゅうじからです | 明日の会議は従事からです | 明日の会議は**10時**からです |
| このやくはむずかしい | この薬は難しい | 文脈に応じて **この訳は難しい** |

直前に確定した文章も文脈として利用できます。

---

## Kotoriで変わること

<p align="center">
  <img src="docs/images/features.png" alt="Kotori日本語入力の特長" width="880">
</p>

**文脈で変換**  
同じ読みでも、文章の意味に合う候補をAIが選びます。

**Spaceを押す前から予測**  
入力を止めるとAIが裏で変換と続きを考えます。Tabから予測候補も選べます。

**完全オフライン**  
辞書もAIモデルもPC内にあります。入力した文章を外部サーバーへ送りません。

**Mozcベース**  
操作感、学習、ユーザー辞書はMozcをそのまま利用できます。

**GPUがなくても動作**  
専用GPUがなければ自動的にCPU向け設定になります。

**使わないときはVRAMを解放**  
10分間入力がなければAIモデルを外し、GPUメモリを空けます。

---

## 実入力で88.4%

<p align="center">
  <img src="docs/images/ime-comparison.png" alt="IME実入力比較" width="880">
</p>

AJIMEE-Bench 198問を**実際にIMEへ入力して比較**した結果です。

| IME | 正解率 |
| --- | ---: |
| **Kotori日本語入力** | **88.4%** |
| Microsoft IME | 59.6% |
| Google 日本語入力 | 58.1% |

同じ入力方法・同じ条件で、Space 1回目の候補を比較しています。

> この比較は2026-10-01時点の Kotori beta.8 / Unreal で測定したものです。  
> 現在版の再測定値ではありません。

評価方法・CSV・追加ベンチマークは [eval/README.md](eval/README.md) に公開しています。

---

## インストール

### 1. MSIをダウンロード

**[Kotori64.msi をダウンロード](https://github.com/aruiki/KotoriIME-japanese-/releases/download/v1.1.0/Kotori64.msi)**

### 2. インストーラーを実行

`Kotori64.msi` を開いてインストールします。

Windowsから「PCが保護されました」と表示された場合は、

**詳細情報 → 実行**

を選択してください。

### 3. Kotoriへ切り替える

インストール後、

**Windowsキー + Space**

から **Kotori日本語入力** を選択します。

これで使えます。

設定はデスクトップの **「Kotori日本語入力の設定」** から変更できます。

---

## 必要な環境

| | 必須 | おすすめ |
| --- | --- | --- |
| OS | Windows 10 1809以降 / 64bit | Windows 11 |
| メモリ | 8GB | 16GB |
| GPU | なくても動作 | Vulkan対応GPU / VRAM 3GB以上 |
| ディスク | 1.7GB | — |

NVIDIA / AMD / Intel Arc の専用GPUは自動検出します。

GPUのために追加ソフトを設定する必要はありません。

---

## AIは入力を遅くしない？

通常の1打鍵はMozcが処理するため、AIの計算完了を待ちません。

AIが時間内に変換できなかった場合も、Mozcの結果をそのまま表示します。

<p align="center">
  <img src="docs/images/lightness.png" alt="Kotori日本語入力の性能" width="880">
</p>

標準設定ではRTX 3060環境で、AI変換1回の中央値は約 **0.06秒** です。

---

## 仕組み

KotoriはMozcを置き換えるのではなく、**Mozcの変換結果をAIで補強します**。

<p align="center">
  <img src="docs/images/how.png" alt="Kotori日本語入力の仕組み" width="880">
</p>

1. Mozcと変換AIが候補を作る
2. AIが文脈に合う候補を評価する
3. 読みと一致することを辞書で確認する
4. 最も自然な候補を表示する

AIが読みにない単語を勝手に追加したり、ユーザー辞書の単語を書き換えたりすることはありません。

詳しい設計は [docs/adr/](docs/adr/) にあります。

---

## 困ったとき

使い方、アンインストール、データの保存場所、トラブル対処は

**[使い方と困ったとき](docs/USER_GUIDE.md)**

にまとめています。

不具合・誤変換は [Issues](https://github.com/aruiki/KotoriIME-japanese-/issues/new/choose) へお願いします。

---

## 開発者向け

- [開発方法](docs/DEVELOPMENT.md)
- [評価方法](eval/README.md)
- [性能測定](docs/PERFORMANCE.md)
- [設計記録](docs/adr/)
- [仕様](docs/SPEC.md)
- [開発規約](AGENTS.md)

---

## 開発を支援する

Kotoriは無料のオープンソースソフトウェアとして開発しています。

**[Stripeから開発を支援する](https://buy.stripe.com/cNi14m7jRdq005f0781ZS08)**

支援の有無による機能制限はありません。

---

## ライセンス

Kotoriのコードは **Apache License 2.0 / MIT License** のデュアルライセンスです。

Mozcへの変更はBSD-3-Clauseです。

同梱コンポーネントを含む詳細は [docs/licenses.md](docs/licenses.md) を参照してください。

---

<h2 align="center">
  <a href="https://github.com/aruiki/KotoriIME-japanese-/releases/download/v1.1.0/Kotori64.msi">⬇ Kotori日本語入力を試す</a>
</h2>

<p align="center">
  Windows 10 / 11・オフライン動作・GPUなしでも利用可能
</p>
