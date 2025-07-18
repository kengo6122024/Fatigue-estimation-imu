"""
設定ファイル
"""

# デフォルト設定
DEFAULT_CONFIG = {
    'data_file': 'test_data.csv',
    'output_file': 'fatigue_analysis.png',
    'personal_data': {
        'weight': 70,     # kg
        'height': 1.78,   # m
        'age': 25         # 歳
    },
    'initial_hp': 100,
    'filter_params': {
        'order': 4,
        'cutoff_freq': 10,
        'sampling_rate': 100
    },
    'analysis_params': {
        'chunk_size': 100,
        'moving_average_window': 15,
        'exercise_threshold': 3,
        'consecutive_count_required': 15
    }
}


def get_config():
    """
    設定を取得する
    
    Returns:
        dict: 設定辞書
    """
    return DEFAULT_CONFIG.copy()


def update_config(new_config):
    """
    設定を更新する
    
    Args:
        new_config (dict): 新しい設定
        
    Returns:
        dict: 更新された設定
    """
    config = get_config()
    config.update(new_config)
    return config