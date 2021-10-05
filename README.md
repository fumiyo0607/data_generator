# data_generator
時系列トピックモデル用の擬似閲覧履歴データ生成スクリプト

## Parameters

| parameter | discripiton  |default setting | 
| ---- | ---- |---- |
| U | ユーザ数 |None|
| I | アイテム数 |None|
| K | トピック数（2^n）|None|
| S | ステージ数（変更不可）|K|
| noise_rate | 各トピックの所属確率の最小値を決定すパラメータ | 0.3 |
| p_min 　　　| 各トピックの所属確率の最小値（変更不可）|(1/K) * noise_rate|
| item_num_s | １ステージあたりの購買回数|200|
| sigma      | 単語分布の分散| I / (K*6) |
| seq_num    | 同一トピックのアイテムが連続して出現する回数|1|

## How to generate data
### トピック分布
- 各ステージごとに1つのトピック（興味トピック）に所属する
- このトピック以外の所属確率は (1/K) * noise_rate となる
- ステージが変わるごとに過去の興味トピック以外のトピックを興味トピックとする

<img width="1408" alt="スクリーンショット 2021-10-06 1 57 52" src="https://user-images.githubusercontent.com/37897800/136068672-9ee92ee6-0636-44fb-affc-9b6668d42f6c.png">



### 単語分布（アイテム分布）
トピック k (k=1,2,...,K) ごとに以下の正規分布を仮定し、この正規分布からアイテムIDをサンプリングする
- 平均： (k - 1/2) * I / K
- 分散： sigma

![image](https://user-images.githubusercontent.com/37897800/135982499-a96204aa-1cba-4ddc-84d7-379bd080b842.png)

### 閲覧履歴（BOW）
- 長さ U の list として作成される
- リストの各要素にはアイテムID（0,1,...,I-1）が格納されている

## Usage
詳細は `exmaple.ipynb` を参照
モデルの入力
- インスタンスの作成
```
generator = Generator(U=1000,I=1600, K=8, item_num_s=50, noise_rato=0.05, seq_num=1)
```
- 単語分布の表示
```
generator.show_item_distribution()
```
- ユーザのBOWの取得 (list)
```
bow = generator.bow
```
