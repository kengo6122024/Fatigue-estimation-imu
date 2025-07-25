# IMUセンサーを用いたアスリート向けリアルタイム疲労推定システム

[English README](README.md) | [日本語版](README_ja.md)

## 概要
本アプリケーションは、IMU（慣性計測装置）センサーデータに基づいて、アスリートの体力と疲労状態をリアルタイムで算出することを目標として開発されたプログラムである。加速度センサーとジャイロセンサーのデータを処理し、身体状況、体力消費、疲労レベルのリアルタイムモニタリングと可視化・分析機能を提供する。

## 機能
- **リアルタイムIMUデータ処理**: IMUセンサーからの加速度・ジャイロデータを処理
- **アスリートパフォーマンス監視**: 選手の体力・疲労状態をリアルタイムで算出
- 3軸センサーデータからの合成加速度とジャーク計算
- ノイズ除去のためのバタワースローパスフィルタによる信号フィルタリング
- Ten-Haaf式による安静時エネルギー消費量（REE）の計算
- 適応アルゴリズムによる動的な体力消費・回復計算
- インタラクティブグラフによるリアルタイムデータ可視化
- トレーニング分析のための消費カロリー推定

## インストール
```bash
pip install -r requirements.txt
```

## 使用方法

### 基本的な使用方法
```bash
python main.py
```

### コマンドライン引数での設定
```bash
python main.py --data your_data.csv --weight 65 --height 1.70 --age 30 --output result.png
```

### 引数の説明
- `--data`: データファイルのパス（デフォルト: test_data.csv）
- `--weight`: 体重 (kg)（デフォルト: 70）
- `--height`: 身長 (m)（デフォルト: 1.78）
- `--age`: 年齢 (歳)（デフォルト: 25）
- `--output`: 出力ファイルのパス（デフォルト: fatigue_analysis.png）

## アルゴリズム & コア計算式

コアとなるHP（ヒットポイント）計算は以下の数学的モデルに従う：

```math
HP_n = min(HP_{n-1} - EE_n \cdot{EE\_increase}_n + heal_n \cdot {heal\_increase}_n, {sup\_{HP}}_{n-1})
```

ここで、エネルギー消費項 `EE_n × EE_increase_n` は体力減衰を、回復項 `heal_n × heal_increase_n` は体力回復を表す。

各変数の説明：
- `HP_n`: タイムステップnでのヘルスポイント
- `EE_n`: タイムステップnでのエネルギー消費量
- `EE_increase_n`: エネルギー消費増幅係数
- `heal_n`: 基本回復率
- `heal_increase_n`: 回復増幅係数
- `sup_HP_{n-1}`: タイムステップn-1での最大HP制限

### 主要コンポーネント:
1. **エネルギー消費量 (EE)**: `EE = std × REE × max_score`
2. **REE計算**: 基礎代謝率のためのTen-Haaf式
3. **増幅係数**: 連続運動・回復期間に基づく
4. **適応型HP上限**: 疲労蓄積に基づいて調整される動的最大HP

## 入力データ形式
CSVファイルには以下の列が必要です：
- Accel1X, Accel1Y, Accel1Z: 加速度データ
- Gyro1X, Gyro1Y, Gyro1Z: ジャイロデータ

## 出力
- 体力消費、運動強度、回復量を示すグラフ
- 最終HP値
- 推定消費カロリー

## プロジェクト構造
```
├── main.py                # メイン実行ファイル
├── data_preprocessing.py  # データ前処理モジュール
├── fatigue_calculator.py  # 疲労度計算モジュール
├── visualization.py       # 可視化モジュール
├── config.py             # 設定ファイル
├── requirements.txt      # 依存関係
├── test_data.csv        # サンプルテストデータ
└── README.md           # 英語版README
└── README_ja.md        # このファイル
```

## モジュール説明

### data_preprocessing.py
- データの読み込みと前処理
- 加速度・ジャイロデータの変換
- 信号フィルタリング処理

### fatigue_calculator.py
- 基礎代謝率の計算
- 疲労度と回復量の計算
- 運動強度の計算

### visualization.py
- グラフの作成と表示
- 結果の可視化

### config.py
- アプリケーション設定管理
- デフォルト値の定義

## 開発・カスタマイズ
設定を変更する場合は `config.py` を編集してください。各モジュールは独立しているため、個別に拡張や修正が可能。

## 応用分野
- スポーツ科学研究
- アスリートトレーニング監視
- リハビリテーション医学
- フィットネス・ヘルスケア
- バイオメカニクス分析