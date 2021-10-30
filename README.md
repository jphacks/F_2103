# Blicky【手・顔リアルタイム検出型バーチャルマウス】

<img width="1000" alt="Blicky" src="https://user-images.githubusercontent.com/60843722/139441696-b396d9d3-5c5f-4b04-9561-63c639787e6c.png">

## 製品概要
### 背景(製品開発のきっかけ、課題等）
新型コロナウイルスの感染拡大防止策として、日常生活のあらゆる場面で"**非接触化**"が注目されるようになりました。

特に、キーボードとマウスの操作を必要とする「PC」や、タッチパネルを搭載した「タブレット型端末」を不特定多数の人が利用する場合、その消毒作業にはやはり限界があります。
最近では、モニターに取り付けて数cm離れた位置から操作できる「非接触タッチパネル」も注目されていますが、初期導入費用が高いのが現状です。

**Blicky（ブリッキー）**
はそのような課題をテクノロジーで解決します。
**Blicky**
はユーザーのポーズ検出によってPCのマウスを自由自在に操作するデスクトップアプリです。
利用者は、自身の"**手**"と"**目**"を使って思い通りにマウスを動かすことができます。

### 製品説明（具体的な製品の説明）
**Blicky**
はユーザーのポーズをリアルタイムで検出することによって、PCマウスを自由自在に操作するデスクトップアプリです。

|人差し指を移動させる|片目をつむる|ピースサインをつくる|
| ------------- | ------------- | ------------- |
|<img width="759" alt="cursor" src="https://user-images.githubusercontent.com/60843722/139424668-b5dbcf1f-faaa-4d98-8408-e40bcb909cba.png">|<img width="761" alt="click" src="https://user-images.githubusercontent.com/60843722/139424688-ad3a9855-ef18-4909-922e-427231fb18ac.png">|<img width="761" alt="scroll" src="https://user-images.githubusercontent.com/60843722/139424700-8e454074-7158-4976-9fca-11eb0485ef45.png">|

現在は、上記の3種類のマウス操作に対応しています。 

### 特長
#### 1. 機械学習を使ったリアルタイムトラッキング機能

* 機械学習を用いて高精度かつ高速に利用者の手と目を検出します
* 両目によるまばたきは検出せず、意図的なウィンクのみをクリックとして認識します

#### 2. 内蔵カメラ（またはWebカメラ）搭載のあらゆるWindows PCで利用可能

* 検出に必要なカメラさえあれば、どんなPCでもexeファイルを実行するだけで利用できます
* 完全にスタンドアローンなアプリであるため、面倒なインストールは一切不要です

#### 3. 多種多様な場面で使える

* 感染防止対策に限らず、接触が好ましくない様々な場面で活用できます
* 手が汚れる現場でのパソコン操作や、来場者の登録情報確認、ポインターを使わないプレゼンテーションなど、多くの活用事例が考えられます

#### 4. 物理的なマウス操作との使い分け可能

* バーチャルマウスは、利用者が任意のタイミングで停止/再開することができます
* 手がカメラの検出範囲内にないときは、いつも通りマウスを操作することが可能です

### 解決出来ること
感染症拡大防止策をとりながらのデバイス操作が可能になる

### 使い方
以下のリンクからzipファイルをダウンロードして解凍し、フォルダ内の**main.exe**を実行するだけで簡単に利用できます。

（ダウンロードには数分かかる場合があります）

https://www.dropbox.com/s/olor5fjmqw04mxz/main.zip?dl=0

<div align="center">
<img width="" alt="menu" src="https://user-images.githubusercontent.com/60843722/139415612-698816da-6fa8-41b5-b42e-f9fdb064296d.png">
</div>

直感的に理解しやすい操作ばかりなので、PC操作が不安な人でも心配なくご利用いただけます。

#### デモ動画はこちら（[YouTube](https://www.youtube.com/watch?v=XIHMB315h9A)）
[![alt設定](http://img.youtube.com/vi/XIHMB315h9A/0.jpg)](https://www.youtube.com/watch?v=XIHMB315h9A)


### 今後の展望
* 片目だけ瞬き（ウィンク）をするのが苦手なユーザーが、自身でパラメーターを調節できるようにする
* 指先の軌跡のデータを学習させることによってジェスチャーを分類し、より多くの操作を実現可能にする

### 注力したこと（こだわり等）
* なるべく直感的に理解しやすくするために、左右Clickを左右Blink（まばたき）に対応させたこと
* 片目のみの瞬きを高精度に検出するため、左右の目の開き具合の相対値を判定に利用したこと
* バーチャルマウスの移動が見やすくなるようにアプリ内で軌跡を可視化したこと
* スクロール速度を、人差し指と中指の開き具合によって自由調節できるようにしたこと

## 開発技術
### 活用した技術
#### API・データ
* [学習済みモデル](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)（顔のランドマーク検出用）

#### フレームワーク・ライブラリ・モジュール
* [MediaPipe](https://google.github.io/mediapipe/)
* [Dlib](http://dlib.net/)
* [OpenCV](https://opencv.org/)
* [PyInstaller](https://www.pyinstaller.org/)

### 独自技術
#### ハッカソンで開発した独自機能・技術
* 手のポーズ検出と目の瞬き検出を同時に行えるように、それぞれの機能をインスタンス化しました
* (両目ではなく)片目のみの瞬きを高精度に検出するため、左右の目の開き具合の相対値を判定に利用しました
* 顔認識に用いたC++ライブラリのDlibを含めてexe化することによって、あらゆるWindows環境でアプリを実行できるようにしました
