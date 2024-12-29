import numpy as np
import av


def numpy_to_audioframe(array, sample_rate=48000):
    """
    将Numpy数组转换为PyAV AudioFrame

    参数:
        array: shape为(960, 1)的numpy数组, dtype为int16
        sample_rate: 采样率,默认48000Hz

    返回:
        av.AudioFrame: PyAV音频帧对象
    """
    # 创建音频帧，指定正确的格式
    frame = av.AudioFrame(
        samples=len(array),          # 采样点数
        layout='mono',               # 单声道
        format='s16',               # 有符号16位整数
    )
    frame.rate = sample_rate
    frame.pts = 0

    # 确保数组是一维的
    if array.ndim == 2:
        array = array.squeeze()

    # 将数据复制到帧的平面中
    frame.planes[0].update(array.tobytes())

    return frame


# 使用示例
array = np.random.randint(-32768, 32767, (960, 1), dtype=np.int16)
audio_frame = numpy_to_audioframe(array)
