import pandas as pd
import matplotlib.pyplot as plt

# CSVファイルのパスを指定
csv_file_path = 'DLC_data.csv'

# CSVファイルを読み込む
df = pd.read_csv(csv_file_path, skiprows=1,header=[0, 1]) # 1行目が邪魔だから削除。2,3行目をヘッダーにしてマルチカラムのデータフレームにする

# 先頭列の削除
df.drop(columns = df.columns[0], axis=1,inplace=True)

# 各ラベルの名前を取得
body_parts = df.columns.levels[0].tolist() # indexObjectのままだと扱いづらいのでlist型に変換
body_parts.remove('bodyparts') # ラベル名じゃないから削除(dfの該当列ごと削除しても残ったからここで対処)

# 各ラベル毎に処理
for body_part in body_parts:
    df2 = df.loc[:,body_part]
    # print(body_part)
    # print(df2.head(2))