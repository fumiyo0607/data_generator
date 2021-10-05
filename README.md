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

## How to generate data
### トピック分布
- 各ステージごとに興味トピックを定義し、興味トピックへ等確率で所属する
- ユーザの興味の遷移の方法として２種類を仮定し、この種類ごとに (1) 収束ユーザ、(2) 未収束ユーザ とする
  - 収束ユーザ：ステージが進むごとに興味トピック が半減する
  - 未収束ユーザ：どのステージについても過去に興味トピックでなかったトピックのうち K/S 個のトピックを興味トピックとする   
![スクリーンショット 2021-10-05 16 51 59](https://user-images.githubusercontent.com/37897800/135982557-b38beffe-ef0a-47bb-bd7e-7f30bdd51781.png)



### 単語分布（アイテム分布）
トピック k (k=1,2,...,K) ごとに以下の正規分布を仮定し、この正規分布からアイテムIDをサンプリングする
- 平均： (k - 1/2) * I / K
- 分散： sigma

![image](https://user-images.githubusercontent.com/37897800/135982499-a96204aa-1cba-4ddc-84d7-379bd080b842.png)

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
