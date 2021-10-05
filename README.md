# data_generator
時系列トピックモデル用の擬似閲覧履歴データ生成スクリプト

## Parameters

| parameter | discripiton  |default setting | 
| ---- | ---- |---- |
| U | ユーザ数 |None|
| I | アイテム数 |None|
| K | トピック数（2^n）|None|
| S | ステージ数（変更不可）|nt(np.log2(K)) + 1 |
| noise_rate | 各トピックの所属確率の最小値を決定すパラメータ | 0.3 |
| p_min 　　　| 各トピックの所属確率の最小値（変更不可）|(1/K) * noise_rate|
| item_num_s | １ステージあたりの購買回数|200|
| sigma      | 単語分布の分散| I / (K*6) |
| seq_num    | 同一トピックのアイテムが連続して出現する回数|1|

## Usage
詳細は `example.ipython` を参照
- インスタンスの作成
```
generator = Generator(U=1000,I=1600,K=8, item_num_s=50, noise_rato=0.05, seq_num=5)
```
- 単語分布の表示
```
generator.show_item_distribution()
```
- 収束ユーザのBOWの取得
```
seq_bow = generator.sequential_bow
```
- 未収束ユーザのBOWの取得
```
random_bow = generator.seq_random_bow
```
