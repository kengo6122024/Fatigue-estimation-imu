"""
可視化関連の機能を提供するモジュール
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import japanize_matplotlib
from fatigue_calculator import calc_fatigue


def seconds_to_time_string(x, pos):
    """
    秒数を時間文字列に変換する
    
    Args:
        x (float): 秒数
        pos: 位置（未使用）
        
    Returns:
        str: 時間文字列
    """
    hours = int(x // 3600)
    minutes = int((x % 3600) // 60)
    seconds = int(x % 60)
    
    if hours > 0:
        return f'{hours:02}時{minutes:02}分{seconds:02}秒'
    else:
        return f'{minutes:02}分{seconds:02}秒'


def plot_fatigue_analysis(stds, max_score, ree, output_path='fatigue_analysis.png'):
    """
    疲労度分析のグラフを作成・表示する
    
    Args:
        stds (np.array): 標準偏差の配列
        max_score (np.array): 最大スコアの配列
        ree (float): 基礎代謝量
        output_path (str): 出力ファイルパス
        
    Returns:
        tuple: (final_hp, estimated_calories)
    """
    hp, total_heal_increase, exercise_intensity, sup_hp = calc_fatigue(stds, max_score, ree)
    
    plt.figure(figsize=(20, 10))
    
    # 体力消費量のプロット
    plt.subplot(3, 1, 1)
    plt.plot(hp, label='現在HP')
    plt.plot(sup_hp, label='体力上限')
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(seconds_to_time_string))
    plt.title('体力消費量', fontsize=16)
    plt.xlabel('時間', fontsize=14)
    plt.ylabel('体力', fontsize=14)
    plt.grid(True)
    plt.legend()
    
    # 運動強度のプロット
    plt.subplot(3, 1, 2)
    plt.plot(exercise_intensity, label='運動強度')
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(seconds_to_time_string))
    plt.title('運動強度', fontsize=16)
    plt.xlabel('時間', fontsize=14)
    plt.ylabel('強度', fontsize=14)
    plt.grid(True)
    plt.legend()
    
    # 回復量のプロット
    plt.subplot(3, 1, 3)
    plt.plot(total_heal_increase, label='減衰後回復量')
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(seconds_to_time_string))
    plt.title('回復量', fontsize=16)
    plt.xlabel('時間', fontsize=14)
    plt.ylabel('値', fontsize=14)
    plt.grid(True)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.show()
    
    # 結果の表示
    final_hp = round(hp[-1])
    estimated_calories = ree * stds.sum()
    
    print(f'残りのHPは{final_hp}です。')
    print(f'推定消費カロリーは {estimated_calories:.1f} [kcal] です。')
    
    return final_hp, estimated_calories