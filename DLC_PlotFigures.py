import os
import pandas as pd
import matplotlib.pyplot as plt

# trajectoryの表示範囲設定用定数
WIDTH_SIZE_MIN = 700 # Default : 0
WIDTH_SIZE_MAX = 1100 # Default : 1920
HEIGHT_SIZE_MIN = 650 # Default : 1080
HEIGHT_SIZE_MAX = 150 # Default : 0

# 図を保存するために作成するディレクトリのpathを指定
DIR_PATH = './Figure' # Default : './Figure'
# CSVファイルのパスを指定
CSV_FILE_PATH = './DLC_data.csv'

# 尤度を表す線グラフを作成する関数
def plot_likelihood(x,y,name):
    ax[0].plot(x,y) # 線グラフの作成
    ax[0].set_xlabel("FrameIndex") # X軸のラベル名設定
    ax[0].set_ylabel("Likelihood") # Y軸のラベル名設定
    ax[0].set_title(f"{name} Label\'s Likelihood") # グラフのタイトル設定
    ax[0].set_ylim(0.0,1.0) # Y軸の表示範囲の設定
    ax[0].set_facecolor("whitesmoke")  # 背景色の設定

# ラベル部位の軌跡を散布図で作成する関数
def plot_trajectory(x,y,name,fig):
    mappable = ax[1].scatter(x, y,s=3,c=df2.index) # 散布図の作成(s:点の大きさ、c:与えられた数値毎に色変化、cmap:カラーマップ)
    ax[1].set_xlabel("x") # x軸のラベル名設定
    ax[1].set_ylabel("y") # Y軸のラベル名設定
    ax[1].set_title(f"{name}\'s trajectory") # グラフのタイトル名設定
    ax[1].set_xlim(WIDTH_SIZE_MIN,WIDTH_SIZE_MAX) # X軸の表示範囲の設定
    ax[1].set_ylim(HEIGHT_SIZE_MIN,HEIGHT_SIZE_MAX) # Y軸の表示範囲の設定
    ax[1].set_facecolor("whitesmoke") # 背景色の設定
    fig.colorbar(mappable,ax=ax[1]) # カラーバーを表示
    ax[1].grid()

# 図を保存するディレクトリの作成
os.makedirs(DIR_PATH,exist_ok=True) # ディレクトリが無ければ作成
os.chdir('./Figure') # 作成したディレクトリに移動

# CSVファイルを読み込む
df = pd.read_csv(CSV_FILE_PATH, skiprows=1,header=[0, 1]) # 1行目が邪魔だから削除。2,3行目をヘッダーにしてマルチカラムのデータフレームにする

# 先頭列の削除
df.drop(columns = df.columns[0], axis=1,inplace=True)

# 各ラベルの名前を取得
body_parts = df.columns.levels[0].tolist() # indexObjectのままだと扱いづらいのでlist型に変換
body_parts.remove('bodyparts') # ラベル名じゃないから削除(dfの該当列ごと削除しても残ったからここで対処)

# 各ラベル毎に処理
for body_part in body_parts:
    df2 = df.loc[:,body_part] # 各ラベルのデータ毎にデータフレームを作成
    fig, ax = plt.subplots(2,1,tight_layout=True,width_ratios=[1],height_ratios=[1, 3], figsize=(12,8)) # FigureとAxesを作成(2行1列,height_ratios:subplotの高さ比)
    plot_likelihood(df2.index,df2.loc[:,'likelihood'],body_part) # 尤度を表す線グラフを作成
    plot_trajectory(df2.loc[:,'x'],df2.loc[:,'y'],body_part,fig) # 散布図を作成
    plt.savefig(f"{body_part}.png")# 各グラフの保存

# plt.show() # グラフの表示