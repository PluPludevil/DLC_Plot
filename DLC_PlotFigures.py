#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
DLCで出力されたcsvデータを読み込んでグラフを作成するPythonコード。
DLCで作成したcsvファイルなら汎用的に使用可能
↓できること↓
各ラベル毎に以下の処理を実行
・尤度の線グラフを作成
・ラベル点の軌跡を点と矢印で表すグラフを作成
・上記二つのグラフを合わせてpng形式で保存(ラベル名.png)
任意の2点間の距離から1px当たりの長さ(mm)を求めてターミナルに出力
グラフ作成時のオプション一覧
・CSVファイルのパスを指定
・作成した図の保存先を指定
・グラフを表示するフレームの区間を指定
・軌跡を表すグラフのx座標とy座標の表示範囲の指定
・図を保存する際のdpi(解像度)を指定
・1px当たりの長さを求める
	・任意の2点間の指定
	・2点間実際の距離の指定
	・最初の何フレーム分を計算に使うか指定
"""

__author__ = 'PluPludevil'
__version__ = '1.0.2'
__date__ = '2024/06/24 (Created: 2024/06/03)'

import os
import math
import pandas as pd
import matplotlib.pyplot as plt

# ↓↓↓オプション用定数↓↓↓
# 表示するフレーム区間を指定する定数
FIRST_FRAME = 0  # Default : 0
LAST_FRAME = None  # Default : None(Noneの場合は、FIRST_FRAME以降の全てのフレームを表示する)

# trajectoryの表示範囲設定用定数
WIDTH_SIZE_MIN = 700  # Default : 0
WIDTH_SIZE_MAX = 1050  # Default : 1920
HEIGHT_SIZE_MIN = 550  # Default : 1080
HEIGHT_SIZE_MAX = 650  # Default : 0

# 図を保存するために作成するディレクトリのpathを指定
DIR_PATH = './Figure'  # Default : './Figure'
# CSVファイルのパスを指定
CSV_FILE_PATH = '/Users/katotakuma/Desktop/motion_capture/trained_data/Karate_kihonn-KatoTakuma-2024-05-12/videos/空手基本動作_ゆっくりDLC_resnet50_Karate_kihonnMay12shuffle1_100000.csv'
# 図を保存する際のdpi(解像度)を指定
DPI = 300  # Default : 100

# length_of_1px関数用定数
LABEL1 = ""  # 任意の部位のラベル名1、Default : ""
LABEL2 = ""  # 任意の部位のラベル名2、Default : ""
LENGTH = 350  # 実際の二点間の距離(mm)
FRAMES = 10  # 最初の何フレーム分を計算に使うか(カメラと被写体の距離が変わると長さも変わるため)、Default : 10
# ↑↑↑オプション用定数↑↑↑


class ForPlot:
    """
    グラフのプロット用クラス
    """

    def __init__(self, df, body_part):
        self.x = df.loc[:, 'x']
        self.y = df.loc[:, 'y']
        self.likelihood = df.loc[:, 'likelihood']
        self.name = body_part
        self.frame_index = df.index
        self.df_length = len(df.index)

    def set(self, df, body_part):
        """
        各パラメータ設定用関数
        """
        self.x = df.loc[:, 'x']
        self.y = df.loc[:, 'y']
        self.likelihood = df.loc[:, 'likelihood']
        self.name = body_part
        self.frame_index = df.index
        self.df_length = len(df.index)

    def calculate_dxdy(self):
        """
        deltaXとdeltaYを計算して返す関数
        """
        dx = []
        dy = []
        for i in range(self.df_length-1):
            dx.append(self.x[i+1]-self.x[i])
            dy.append(self.y[i+1]-self.y[i])
        dx.append(0.0)
        dy.append(0.0)
        return [dx, dy]


def plot_likelihood(df, ax):
    """
    尤度を表す線グラフを作成する関数
    """
    ax[0].plot(df.frame_index, df.likelihood)  # 線グラフの作成
    ax[0].set_xlabel("FrameIndex")  # X軸のラベル名設定
    ax[0].set_ylabel("Likelihood")  # Y軸のラベル名設定
    ax[0].set_title(f"{df.name} Label\'s Likelihood")  # グラフのタイトル設定
    ax[0].set_ylim(0.0, 1.0)  # Y軸の表示範囲の設定
    ax[0].set_facecolor("whitesmoke")  # 背景色の設定


def plot_trajectory(df, fig, ax):
    """
    ラベル部位の軌跡を散布図+矢印付き線グラフで作成する関数
    """
    # 散布図の作成(s:点の大きさ、c:与えられた数値毎に色変化、cmap:カラーマップ)
    mappable = ax[1].scatter(df.x, df.y, s=3, c=df.frame_index)
    ax[1].set_xlabel("x")  # x軸のラベル名設定
    ax[1].set_ylabel("y")  # Y軸のラベル名設定
    ax[1].set_title(f"{df.name}\'s trajectory")  # グラフのタイトル名設定
    ax[1].set_xlim(WIDTH_SIZE_MIN, WIDTH_SIZE_MAX)  # X軸の表示範囲の設定
    ax[1].set_ylim(HEIGHT_SIZE_MIN, HEIGHT_SIZE_MAX)  # Y軸の表示範囲の設定
    ax[1].set_facecolor("whitesmoke")  # 背景色の設定
    fig.colorbar(mappable, ax=ax[1])  # カラーバーを表示
    # 矢印付き線グラフの作成
    dxdy = df.calculate_dxdy()  # deltaXとdeltaYの計算
    ax[1].quiver(df.x, df.y, dxdy[0], dxdy[1], df.frame_index,
                 angles='xy', scale_units='xy', scale=1, units='xy', width=0.5)  # 矢印の描写
    ax[1].grid()


def length_of_1px(df_for_length):
    """
    任意の2点間の距離から1px当たりの長さ(mm)を返す関数
    """
    max_length = 0.0  # 任意の二点間の距離の最大値
    for i in range(FRAMES):
        length = math.sqrt(((df_for_length.loc[i, 'x2'] - df_for_length.loc[i, 'x1'])**2) +
                           ((df_for_length.loc[i, 'y2'] - df_for_length.loc[i, 'y1'])**2))
        if length > max_length:
            max_length = length
    return LENGTH/max_length


def preparation():
    """
    図を保存するディレクトリの作成
    CSVファイルを読み込んでデータフレームに格納・整形
    各ラベルの名前を取得
    返す変数：整形したデータフレーム、各ラベルの名前
    """
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
    # ラベル名じゃないから削除(df_readの該当列ごと削除しても残ったからここで対処)
    body_parts.remove('bodyparts')
    return df_read, body_parts


def process_each_label_separately(df_read, body_parts, df_for_length):
    """
    各ラベル毎に処理(グラフ作成と図の保存)
    """
    for body_part in body_parts:
        df = df_read.loc[FIRST_FRAME:LAST_FRAME, body_part]  # 各ラベル毎にデータフレームを作成
        df_for_plot = ForPlot(df, body_part)
        if body_part == LABEL1:  # 1px当たりの長さ計算用にグローバル変数(dataframe)に渡す
            df_for_length["x1"] = df.loc[:, 'x']
            df_for_length["y1"] = df.loc[:, 'y']
        if body_part == LABEL2:  # 1px当たりの長さ計算用にグローバル変数(dataframe)に渡す
            df_for_length["x2"] = df.loc[:, 'x']
            df_for_length["y2"] = df.loc[:, 'y']
        # FigureとAxesを作成(2行1列,height_ratios:subplotの高さ比)
        fig, ax = plt.subplots(2, 1, tight_layout=True, width_ratios=[1], height_ratios=[
            1, 3], figsize=(12, 8))
        # 尤度を表す線グラフを作成
        plot_likelihood(df_for_plot, ax)
        plot_trajectory(
            df_for_plot, fig, ax)  # 散布図を作成
        plt.savefig(f"{body_part}.png", dpi=DPI)  # 各グラフの保存


def main():
    """
    各関数を実行して、図の作成と1px当たりの長さを出力するメインプログラム（main関数）。
    """
    df_for_length = pd.DataFrame()  # length_of_1px用変数
    df_read, body_parts = preparation()  # 読み込み等の下準備
    process_each_label_separately(
        df_read, body_parts, df_for_length)  # 各ラベル毎に処理(グラフ作成と図の保存)
    if (LABEL1 != "" and LABEL2 != ""): # オプションで任意の2点を指定している場合
        print(f'1px当たりの長さ:{length_of_1px(df_for_length)}(mm)')


if __name__ == '__main__':
    import sys
    sys.exit(main())
