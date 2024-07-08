import os
import math
import pandas as pd
import matplotlib.pyplot as plt

# 表示するフレーム区間を指定する定数
FIRST_FRAME = 0 # Default : 0
LAST_FRAME = None # Default : None(Noneの場合は、FIRST_FRAME以降の全てのフレームを表示する)

# trajectoryの表示範囲設定用定数
WIDTH_SIZE_MIN = 700  # Default : 0
WIDTH_SIZE_MAX = 1050  # Default : 1920
HEIGHT_SIZE_MIN = 650  # Default : 1080
HEIGHT_SIZE_MAX = 150  # Default : 0

# 図を保存するために作成するディレクトリのpathを指定
DIR_PATH = './Figure'  # Default : './Figure'
# CSVファイルのパスを指定
CSV_FILE_PATH = '/DLC_data.csv'
# 図を保存する際のdpi(解像度)を指定
DPI = 300  # Default : 100

# length_of_1px関数用定数
LABEL1 = "LeftElbow"  # 任意の部位のラベル名1
LABEL2 = "LeftHand"  # 任意の部位のラベル名2
LENGTH = 350  # 実際の二点間の距離(mm)
FRAMES = 10  # 最初の何フレーム分を計算に使うか(カメラと被写体の距離が変わると長さも変わるため)

# length_of_1px関数用宣言
df_label1_x = pd.DataFrame()
df_label1_y = pd.DataFrame()
df_label2_x = pd.DataFrame()
df_label2_y = pd.DataFrame()


def plot_likelihood(x, y, name):  # 尤度を表す線グラフを作成する関数
    ax[0].plot(x, y)  # 線グラフの作成
    ax[0].set_xlabel("FrameIndex")  # X軸のラベル名設定
    ax[0].set_ylabel("Likelihood")  # Y軸のラベル名設定
    ax[0].set_title(f"{name} Label\'s Likelihood")  # グラフのタイトル設定
    ax[0].set_ylim(0.0, 1.0)  # Y軸の表示範囲の設定
    ax[0].set_facecolor("whitesmoke")  # 背景色の設定


def plot_trajectory(x, y, name, fig):  # ラベル部位の軌跡を散布図+矢印付き線グラフで作成する関数
    # 散布図の作成(s:点の大きさ、c:与えられた数値毎に色変化、cmap:カラーマップ)
    mappable = ax[1].scatter(x, y, s=3, c=df.index)
    ax[1].set_xlabel("x")  # x軸のラベル名設定
    ax[1].set_ylabel("y")  # Y軸のラベル名設定
    ax[1].set_title(f"{name}\'s trajectory")  # グラフのタイトル名設定
    ax[1].set_xlim(WIDTH_SIZE_MIN, WIDTH_SIZE_MAX)  # X軸の表示範囲の設定
    ax[1].set_ylim(HEIGHT_SIZE_MIN, HEIGHT_SIZE_MAX)  # Y軸の表示範囲の設定
    ax[1].set_facecolor("whitesmoke")  # 背景色の設定
    fig.colorbar(mappable, ax=ax[1])  # カラーバーを表示
    # 矢印付き線グラフの作成
    dxdy = calculate_dxdy(x, y)  # deltaXとdeltaYの計算
    ax[1].quiver(x, y, dxdy[0], dxdy[1], df.index,
                 angles='xy', scale_units='xy', scale=1, units='xy', width=0.5)  # 矢印の描写
    ax[1].grid()


def length_of_1px():  # 任意の2点間の距離から1px当たりの長さ(mm)を返す関数
    max_length = 0.0  # 任意の二点間の距離の最大値
    for i in range(FRAMES):
        length = math.sqrt(((df_label2_x[i] - df_label1_x[i])**2) +
                           ((df_label2_y[i] - df_label1_y[i])**2))
        if (length > max_length):
            max_length = length
    return LENGTH/max_length


def calculate_dxdy(x, y):  # deltaXとdeltaYを計算して返す関数
    dx = []
    dy = []
    for i in range(len(x)-1):
        dx.append(x[i+1]-x[i])
        dy.append(y[i+1]-y[i])
    dx.append(0.0)
    dy.append(0.0)
    return [dx, dy]


# 図を保存するディレクトリの作成
os.makedirs(DIR_PATH, exist_ok=True)  # ディレクトリが無ければ作成
os.chdir('./Figure')  # 作成したディレクトリに移動

# CSVファイルを読み込む
# 1行目が邪魔だから削除。2,3行目をヘッダーにしてマルチカラムのデータフレームにする
df_read = pd.read_csv(CSV_FILE_PATH, skiprows=1, header=[0, 1])

# 先頭列の削除
df_read.drop(columns=df_read.columns[0], axis=1, inplace=True)

# 各ラベルの名前を取得
# indexObjectのままだと扱いづらいのでlist型に変換
body_parts = df_read.columns.levels[0].tolist()
body_parts.remove('bodyparts')  # ラベル名じゃないから削除(df_readの該当列ごと削除しても残ったからここで対処)

# 各ラベル毎に処理
for body_part in body_parts:
    df = df_read.loc[FIRST_FRAME:LAST_FRAME, body_part]  # 各ラベル毎にデータフレームを作成
    if (body_part == LABEL1):  # 1px当たりの長さ計算用にグローバル変数(dataframe)に渡す
        df_label1_x = df.loc[:, 'x']
        df_label1_y = df.loc[:, 'y']
    if (body_part == LABEL2):  # 1px当たりの長さ計算用にグローバル変数(dataframe)に渡す
        df_label2_x = df.loc[:, 'x']
        df_label2_y = df.loc[:, 'y']
    # FigureとAxesを作成(2行1列,height_ratios:subplotの高さ比)
    fig, ax = plt.subplots(2, 1, tight_layout=True, width_ratios=[1], height_ratios=[
                           1, 3], figsize=(12, 8))
    # 尤度を表す線グラフを作成
    plot_likelihood(df.index,
                    df.loc[:, 'likelihood'], body_part)
    plot_trajectory(
        df.loc[:, 'x'], df.loc[:, 'y'], body_part, fig)  # 散布図を作成
    plt.savefig(f"{body_part}.png", dpi=DPI)  # 各グラフの保存

print(f'1px当たりの長さ:{length_of_1px()}(mm)')
# plt.show() # グラフの表示
