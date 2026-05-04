# ============================================================
# MANEJO DE ENTRADA/SALIDA DE AUDIO
# ============================================================

from machine import Pin, ADC, PWM
from config import *

# Inicialización de ADC
adc = ADC(Pin(PIN_ADC))
adc.atten(getattr(ADC, f'ATTN_{ADC_ATTENUATION}DB'))
adc.width(getattr(ADC, f'WIDTH_{ADC_WIDTH}BIT'))

# Inicialización de PWM
pwm_pin = PWM(Pin(PIN_PWM))
pwm_pin.freq(PWM_FREQUENCY)
pwm_pin.duty(0)

def adc_read():
    """Lee el ADC y retorna valor configurado"""
    return adc.read()

def pwm_write(value_8bit):
    """Escribe un valor de 8 bits (0-255) al PWM"""
    duty = int(value_8bit * PWM_DUTY_RANGE / 255)
    pwm_pin.duty(duty)

def sample_to_8bit(sample_adc):
    """Convierte muestra del ADC a 8 bits para PWM"""
    return int(sample_adc * 255 / (2**ADC_WIDTH - 1))
