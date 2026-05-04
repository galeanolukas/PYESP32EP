# ============================================================
# PROCESADOR DE AUDIO PARA GUITARRA - ESP32
# ============================================================

from machine import Timer
import time
import audio_io
import effects
import config

# Buffer para análisis
audio_buffer = [0] * config.BUFFER_SIZE
buffer_index = 0

# Configuración de efectos (cambiar a True para activar)
ENABLE_OVERDRIVE = False
ENABLE_DELAY = False

def audio_callback(timer):
    """Función que se ejecuta a la frecuencia de muestreo"""
    global buffer_index
    
    # 1. Leer guitarra
    guitar_sample = audio_io.adc_read()
    
    # 2. Aplicar efectos
    processed_sample = effects.process_audio(
        guitar_sample, 
        ENABLE_OVERDRIVE, 
        ENABLE_DELAY
    )
    
    # 3. Convertir y enviar a PWM
    sample_8bit = audio_io.sample_to_8bit(processed_sample)
    audio_io.pwm_write(sample_8bit)
    
    # 4. Guardar en buffer para análisis
    audio_buffer[buffer_index] = processed_sample
    buffer_index = (buffer_index + 1) % config.BUFFER_SIZE

def setup():
    """Configuración inicial del sistema"""
    print("=== Procesador de Audio Casero con ESP32 ===")
    print(f"Tasa de muestreo: {config.SAMPLE_RATE_HZ} Hz")
    print(f"Frecuencia PWM: {config.PWM_FREQUENCY} Hz")
    print(f"Pines: ADC={config.PIN_ADC}, PWM={config.PIN_PWM}")
    print()
    
    # Mostrar estado de efectos
    effects_active = []
    if ENABLE_OVERDRIVE:
        effects_active.append("Overdrive")
    if ENABLE_DELAY:
        effects_active.append("Delay")
    
    if effects_active:
        print(f"Efectos activados: {', '.join(effects_active)}")
    else:
        print("Efectos activados: Ninguno (pase directo)")
    
    print("🎸 ¡Toca tu guitarra! Deberías escuchar tu señal procesada.")
    print()
    
    # Configurar timer para muestreo en tiempo real
    timer = Timer(0)
    timer.init(freq=config.SAMPLE_RATE_HZ, mode=Timer.PERIODIC, callback=audio_callback)
    
    return timer

def main():
    """Programa principal"""
    timer = setup()
    
    try:
        while True:
            # Mostrar nivel de entrada (útil para debug)
            if audio_buffer:
                max_level = max(audio_buffer)
                bars = int(max_level / 100)
                print(f"Nivel: {'█' * bars}{'░' * (40 - bars)}", end="\r")
            time.sleep_ms(100)
            
    except KeyboardInterrupt:
        print("\n\nDeteniendo procesador de audio...")
        timer.deinit()
        print("Sistema detenido.")

if __name__ == "__main__":
    main()
