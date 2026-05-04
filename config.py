# ============================================================
# CONFIGURACIÓN DEL SISTEMA DE AUDIO
# ============================================================

# Pines de hardware
PIN_ADC = 34          # GPIO para entrada de guitarra (ADC1_CH6)
PIN_PWM = 25          # GPIO para salida PWM

# Configuración ADC
ADC_ATTENUATION = 11  # 11DB para rango 0-3.6V
ADC_WIDTH = 12        # Resolución 12 bits (0-4095)

# Configuración PWM
PWM_FREQUENCY = 78000  # Frecuencia PWM ~78 kHz
PWM_DUTY_RANGE = 1023 # Rango duty cycle (10 bits)

# Configuración de muestreo
SAMPLE_RATE_HZ = 20000
SAMPLE_PERIOD_US = int(1000000 / SAMPLE_RATE_HZ)

# Buffers
BUFFER_SIZE = 256
DELAY_BUFFER_SIZE = 1000

# Parámetros de efectos (ajustables)
OVERDRIVE_GAIN = 2.0
OVERDRIVE_THRESHOLD = 3000
DELAY_AMOUNT = 0.3     # Mezcla de delay (0 a 1)
