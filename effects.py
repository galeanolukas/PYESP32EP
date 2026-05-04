# ============================================================
# EFECTOS DE AUDIO
# ============================================================

from config import *

# Buffers para efectos
delay_buffer = [0] * DELAY_BUFFER_SIZE
delay_index = 0

def hard_clip(sample):
    """Efecto de overdrive simple (hard clipping)"""
    amplified = int(sample * OVERDRIVE_GAIN)
    if amplified > OVERDRIVE_THRESHOLD:
        return OVERDRIVE_THRESHOLD
    elif amplified < 0:
        return 0
    return amplified

def delay_effect(sample):
    """Efecto de delay simple"""
    global delay_index
    delayed = delay_buffer[delay_index]
    delay_buffer[delay_index] = sample
    delay_index = (delay_index + 1) % len(delay_buffer)
    return int(sample * (1 - DELAY_AMOUNT) + delayed * DELAY_AMOUNT)

def process_audio(sample, enable_overdrive=False, enable_delay=False):
    """
    Aplica efectos a la muestra de audio
    """
    if enable_overdrive:
        sample = hard_clip(sample)
    
    if enable_delay:
        sample = delay_effect(sample)
    
    return sample
