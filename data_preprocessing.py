"""
データ前処理関連の機能を提供するモジュール
"""

import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt


def filter_data(data):
    """
    データにバタワースローパスフィルタを適用する
    
    Args:
        data: フィルタリングするデータ
        
    Returns:
        フィルタリング後のデータ
    """
    b, a = butter(4, 10/(100/2), btype='low')
    data_filtered = filtfilt(b, a, data)
    return data_filtered


def preprocessing(path):
    """
    CSVファイルからデータを読み込み、前処理を行う
    
    Args:
        path (str): CSVファイルのパス
        
    Returns:
        pd.DataFrame: 前処理済みのデータフレーム
    """
    df = pd.read_csv(path)
    
    # 加速度データの変換
    df['Accel1X'] = df['Accel1X'] * 9.8 * 16 / 2**15
    df['Accel1Y'] = df['Accel1Y'] * 9.8 * 16 / 2**15
    df['Accel1Z'] = df['Accel1Z'] * 9.8 * 16 / 2**15
    
    # ジャイロデータの変換
    df['Gyro1X'] = df['Gyro1X'] * 2000 / 2**15
    df['Gyro1Y'] = df['Gyro1Y'] * 2000 / 2**15
    df['Gyro1Z'] = df['Gyro1Z'] * 2000 / 2**15
    
    # 合成加速度の計算
    df['Composite Accel'] = np.sqrt(df['Accel1X']**2 + df['Accel1Y']**2 + df['Accel1Z']**2)
    df['Composite Gyro'] = np.sqrt(df['Gyro1X']**2 + df['Gyro1Y']**2 + df['Gyro1Z']**2)
    
    # フィルタリング済み合成加速度の計算
    composite_accel = np.sqrt(df['Accel1X']**2 + df['Accel1Y']**2 + df['Accel1Z']**2)
    df['Composite Accel Filtered'] = filter_data(composite_accel.to_numpy())
    df['Composite Accel Filtered - 1G'] = df['Composite Accel Filtered'] - 9.80665
    
    # ジャークの計算
    jerk = np.diff(df['Composite Accel Filtered']) * 100
    jerk_padded = np.insert(jerk, 0, 0)
    df['Jerk'] = jerk_padded
    
    # 不要な列の削除
    if 'Unnamed: 8' in df.columns:
        df.drop(columns='Unnamed: 8', inplace=True)
    
    return df