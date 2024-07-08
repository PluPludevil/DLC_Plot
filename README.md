# DLC_Plot
 Python code for DeepLabCut's data plotting graph
## 目次
- 作成環境
- 概要
    - このPythonコードでできること
    - 出力例と使用オプション
- 使用方法
    - 手順
    - オプション設定時の注意点
    - Tips
        - ファイルのパス名取得法(mac)
        - Pythonコードの説明を表示

## 作成環境
MacBook Air
- macOS：Ventura13.5
- Python 3.9.6
- Visual Studio Code：Version: 1.89.0 (Universal)


## 概要
DLCで出力されたcsvデータを読み込んでグラフを作成するPythonコード。*(DLCで作成したcsvファイルなら汎用的に使用可能)*

### このPythonコードでできること
- 各ラベル毎に以下の処理を実行
	- 尤度の線グラフを作成(縦軸：尤度、横軸：フレーム)
	- ラベル点の軌跡を点と矢印で表すグラフを作成(縦軸：y座標、横軸：x座標、色：フレーム、矢印：ラベル点の動き)
	- 上記二つのグラフを合わせてpng形式で保存(ラベル名.png)
- 任意の2点間の距離から1px当たりの長さ(mm)を求めてターミナルに出力
- グラフ作成時のオプション一覧*コード内の定数を書き換え*
	- CSVファイルのパスを指定
	- 作成した図の保存先を指定
    - グラフを表示するフレームの区間を指定
    - 軌跡を表すグラフのx座標とy座標の表示範囲の指定
    - 図を保存する際のdpi(解像度)を指定
    - 1px当たりの長さを求める
        - 任意の2点間の指定
        - 2点間実際の距離の指定
        - 最初の何フレーム分を計算に使うか指定
### 出力例と使用オプション
![image_for_readme](https://github.com/PluPludevil/DLC_Plot/assets/138640051/d910185f-eef3-417e-8115-13f29ffafa49)

図：上のグラフが尤度、下のグラフが軌跡
- オプション設定
    - CSVファイルのパス「./DLC_data.csv」
    - 図の保存先「./Figure」
    - グラフを表示するフレームの区間「0~500」
    - 軌跡を表すグラフのx座標とy座標の表示範囲「x座標：700~1050、y座標：650~150」
    - 図を保存する際のdpi(解像度)「300dpi」
    - 1px当たりの長さを求める
        - 出力例「1px当たりの長さ:2.4203148629553235(mm)」
        - 任意の2点間「LeftElbowとLeftHand」
        - 2点間の実際の距離「350mm」
        - 最初の何フレーム分を計算に使うか「10」

## 使用方法
### 手順
1. Pythonコード内でcsvファイルのパスを設定([! 必須])
2. その他のオプション用定数を設定([>* 任意])
3. 「python DLC_PlotFigures.py」を実行([>* Pythonファイルのあるディレクトリに移動してから実行する必要がある])
### オプション設定時の注意点
- **シングルクウォート「'」やダブルクウォート「"」は消さないでください**
- **csvファイルのパスは必ず設定してください*
- **「その他のオプション用定数」は必要なければデフォルトの値を設定してください(空白❌)**
- *DLCのy座標値は上下が逆になっていることに注意*

### Tips
#### ファイルのパス名取得法(mac)
ファイルを右クリック→「option」キーを押すとパス名をコピーする項目が出る

#### Pythonコードの説明を表示
以下のコマンドをターミナルで実行(ファイル名に.pyは不要)
- ターミナルに表示する場合は`pydoc ファイル名`
- html形式で出力する場合`pydoc -w ファイル名`


