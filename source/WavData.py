
# numpy
import numpy as np

class WavData:
    '''
    リニアPCMデータを表すクラス。
    サンプルレートとサンプル列をパックしてるだけ。
    '''
    def __init__(self) -> None:
        '''
        デフォルトコンストラクタ。
        '''
        self.sample_rate: int = None
        self.samples: np.ndarray = None

    def __init__(self, sample_rate: int, samples: np.ndarray) -> None:
        '''
        コンストラクタ。
        '''
        self.sample_rate = sample_rate
        self.samples = samples