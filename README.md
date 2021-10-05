# data_generator
時系列トピックモデル用のデータ生成スクリプト

## Usage
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
-未収束ユーザのBOWの取得
```
random_bow = generator.seq_random_bow
```
