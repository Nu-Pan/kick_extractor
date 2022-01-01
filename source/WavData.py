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
        self.sample_rate: int = sample_rate
        self.samples: np.ndarray = samples
    
    def length_in_samples(self):
        '''
        長さを総サンプル数で得る
        '''
        if self.samples is None:
            return None
        if self.samples.ndim == 1:
            return self.samples.size
        else:
            return self.samples.shape[1]

    def length_in_sec(self):
        '''
        長さを秒で得る
        '''
        length_in_samples = self.length_in_samples()
        if length_in_samples is None:
            return None
        if self.sample_rate is None:
            return None
        return length_in_samples / self.sample_rate
