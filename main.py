"""
疲労度計算アプリケーションのメイン実行ファイル
"""

import argparse
from data_preprocessing import preprocessing
from fatigue_calculator import calc_ree_per_sec, calc_max_score_and_std
from visualization import plot_fatigue_analysis
from config import get_config, update_config


def main():
    """
    メイン関数
    """
    parser = argparse.ArgumentParser(description='疲労度計算アプリケーション')
    parser.add_argument('--data', type=str, help='データファイルのパス')
    parser.add_argument('--output', type=str, help='出力ファイルのパス')
    parser.add_argument('--weight', type=float, help='体重 (kg)')
    parser.add_argument('--height', type=float, help='身長 (m)')
    parser.add_argument('--age', type=int, help='年齢 (歳)')
    
    args = parser.parse_args()
    
    # 設定の読み込み
    config = get_config()
    
    # コマンドライン引数による設定の更新
    if args.data:
        config['data_file'] = args.data
    if args.output:
        config['output_file'] = args.output
    if args.weight:
        config['personal_data']['weight'] = args.weight
    if args.height:
        config['personal_data']['height'] = args.height
    if args.age:
        config['personal_data']['age'] = args.age
    
    # データの前処理
    print(f"データファイル '{config['data_file']}' を読み込み中...")
    df = preprocessing(config['data_file'])
    print("データの前処理が完了しました。")
    
    # 個人データの取得
    personal_data = [
        config['personal_data']['weight'],
        config['personal_data']['height'],
        config['personal_data']['age']
    ]
    
    print(f"個人データ: 体重={personal_data[0]}kg, 身長={personal_data[1]}m, 年齢={personal_data[2]}歳")
    
    # 基礎代謝量の計算
    ree = calc_ree_per_sec(personal_data)
    print(f"基礎代謝量: {ree:.6f} kcal/sec")
    
    # 標準偏差と最大スコアの計算
    print("運動強度の計算中...")
    max_score, stds = calc_max_score_and_std(df)
    
    # 疲労度分析の実行と可視化
    print("疲労度分析の実行中...")
    final_hp, estimated_calories = plot_fatigue_analysis(
        stds, max_score, ree, config['output_file']
    )
    
    print(f"分析完了! 結果を '{config['output_file']}' に保存しました。")
    
    return final_hp, estimated_calories


if __name__ == '__main__':
    main()