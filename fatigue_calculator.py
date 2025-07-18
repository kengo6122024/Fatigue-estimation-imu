"""
疲労度計算関連の機能を提供するモジュール
"""

import numpy as np
import math


def calc_ree_per_sec(personal_data):
    """
    Ten-Haafの式による基礎代謝量（REE）を秒あたりで計算する
    
    Args:
        personal_data (list): [体重(kg), 身長(m), 年齢(歳)]
        
    Returns:
        float: 秒あたりの基礎代謝量
    """
    weight, height, age = personal_data
    return (11.936 * weight + 587.728 * height - 8.19 * age + 191.027 + 29.279) / (24 * 60 * 60)


def fix_min_and_max(arr, min_val=0, max_val=100):
    """
    配列の値を最小値と最大値で制限する
    
    Args:
        arr (np.array): 処理対象の配列
        min_val (int): 最小値
        max_val (int): 最大値
        
    Returns:
        np.array: 制限された配列
    """
    arr = np.where(arr > max_val, max_val, arr)
    arr = np.where(arr < min_val, min_val, arr)
    return arr


def valid_convolve(xx, size):
    """
    移動平均を計算する
    
    Args:
        xx (np.array): 入力データ
        size (int): 移動平均のウィンドウサイズ
        
    Returns:
        np.array: 移動平均後のデータ
    """
    b = np.ones(size) / size
    xx_mean = np.convolve(xx, b, mode="same")
    n_conv = math.ceil(size / 2)
    
    # 端部の補正
    xx_mean[0] *= size / n_conv
    for i in range(1, n_conv):
        xx_mean[i] *= size / (i + n_conv)
        xx_mean[-i] *= size / (i + n_conv - (size % 2))
    
    return xx_mean


def heal(std):
    """
    標準偏差に基づく回復量を計算する
    
    Args:
        std (float): 標準偏差
        
    Returns:
        float: 回復量
    """
    return 0 if std > 3 else 0.04


def calc_energy_expenditure(std, ree, max_score):
    """
    エネルギー消費量を計算する
    
    Args:
        std (float): 標準偏差
        ree (float): 基礎代謝量
        max_score (float): 最大スコア
        
    Returns:
        float: エネルギー消費量
    """
    return std * ree * max_score


def calc_ee_increase(x):
    """
    エネルギー消費の増加係数を計算する
    
    Args:
        x (float): 連続運動時間（分）
        
    Returns:
        float: 増加係数
    """
    return x / 20 + 1.0 if x < 20 else 2.0


def calc_heal_increase(x):
    """
    回復量の増加係数を計算する
    
    Args:
        x (float): 連続回復時間（分）
        
    Returns:
        float: 増加係数
    """
    return (0.5 + 9.5 * np.exp(-0.5 * (x - 1)**2)) / 3


def count_over_threshold(lst, threshold):
    """
    リストの末尾から閾値を超える要素の連続数を数える
    
    Args:
        lst (list): 対象リスト
        threshold (float): 閾値
        
    Returns:
        int: 連続数
    """
    count = 0
    for element in reversed(lst):
        if element > threshold:
            count += 1
        else:
            break
    return count


def get_start_index(std):
    """
    運動開始のインデックスを取得する
    
    Args:
        std (list): 標準偏差のリスト
        
    Returns:
        int: 開始インデックス
    """
    threshold = 3
    consecutive_count = 0
    start_index = -1
    consecutive_count_required = 15
    
    for i, value in enumerate(std):
        if value > threshold:
            consecutive_count += 1
            if consecutive_count == consecutive_count_required:
                start_index = i - consecutive_count_required + 1
                break
        else:
            consecutive_count = 0
    
    return start_index


def calc_max_score_and_std(df):
    """
    合成加速度の標準偏差と最大値による係数を計算する
    
    Args:
        df (pd.DataFrame): データフレーム
        
    Returns:
        tuple: (max_score, stds)
    """
    def calc_composite_accel_score(max_value):
        """最大値から係数を決定する"""
        if max_value >= 10:
            return (max_value / 10)**3 / 64
        else:
            return 1 / 64
    
    # 100行ごとに分割
    chunks = [df.iloc[i:i + 100] for i in range(0, df.shape[0], 100)]
    
    max_values = np.array([chunks[i]['Composite Accel Filtered'].max() 
                          for i in range(len(chunks) - 1)])
    stds = np.array([chunks[i]['Composite Accel Filtered'].std() 
                    for i in range(len(chunks) - 1)])
    max_score = np.array([calc_composite_accel_score(max_values[i]) 
                         for i in range(len(max_values))])
    
    # 移動平均により平滑化
    stds = valid_convolve(stds, 15)
    max_score = valid_convolve(max_score, 15)
    
    return max_score, stds


def calc_fatigue(stds, max_score, ree, initial_hp=100):
    """
    疲労度を計算する
    
    Args:
        stds (np.array): 標準偏差の配列
        max_score (np.array): 最大スコアの配列
        ree (float): 基礎代謝量
        initial_hp (int): 初期HP
        
    Returns:
        tuple: (HP, total_heal_increase, exercise_intensity, sup_HP)
    """
    hp_list = []
    total_heal = []
    total_std = []
    total_heal_increase = []
    
    sup_hp = np.zeros(len(stds))
    sup_hp[0] = initial_hp
    
    start_index = get_start_index(stds)
    
    for i in range(len(stds)):
        if i <= start_index:
            hp_list.append(initial_hp)
            sup_hp[i] = initial_hp
            total_std.append(stds[i])
            total_heal.append(0)
            total_heal_increase.append(0)
        else:
            # 連続運動・回復時間の計算
            min_consecutive_exercise = count_over_threshold(total_std, 3) / 60
            min_consecutive_heal = count_over_threshold(total_heal, 0) / 60
            
            # エネルギー消費量の計算
            ee_i = calc_energy_expenditure(stds[i], ree, max_score[i])
            ee_increase_i = calc_ee_increase(min_consecutive_exercise)
            
            # 回復量の計算
            heal_i = heal(stds[i])
            heal_increase_i = calc_heal_increase(min_consecutive_heal)
            
            # HP更新
            hp_i = np.minimum(
                hp_list[i-1] - ee_i * ee_increase_i + heal_i * heal_increase_i,
                sup_hp[i-1]
            )
            hp_list.append(hp_i)
            
            # 体力上限の更新
            if hp_list[i] <= hp_list[i-1]:
                sup_hp[i] = np.maximum(
                    sup_hp[i-1] + 0.3 * (hp_list[i] - hp_list[i-1]) + 100 / (24 * 60 * 60),
                    20
                )
            else:
                sup_hp[i] = sup_hp[i-1] + 100 / (24 * 60 * 60)
            
            total_std.append(stds[i])
            total_heal.append(heal_i)
            total_heal_increase.append(heal_i * heal_increase_i)
    
    hp_array = np.array(hp_list)
    total_heal_increase = np.array(total_heal_increase)
    
    # 正規化
    hp_array = hp_array * 100 / initial_hp
    sup_hp = sup_hp * 100 / initial_hp
    
    # 範囲制限
    hp_array = fix_min_and_max(hp_array)
    
    # 運動強度の計算
    exercise_intensity = stds * max_score
    
    return hp_array, total_heal_increase, exercise_intensity, sup_hp