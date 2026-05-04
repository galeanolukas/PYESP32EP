# PYESP32EP
 Procesador de efectos casero para guitarra

## Hardware - Circuito de Entrada DAC con LM324N

### ⚠️ La Característica Clave que Debes Conocer

La única "maña" que tiene el LM324N, y que debes recordar siempre, es que su voltaje de salida máximo es siempre unos 1.5V o 2V menor que su voltaje de alimentación.

**¿Qué significa esto?**: Si alimentas el LM324N con los 3.3V del ESP32, la salida del amplificador no podrá superar aproximadamente 1.8V.

**¿Es un problema?**: ¡No, en este caso es una ventaja! Resulta que el ESP32 espera en su entrada (pin ADC) señales entre 0V y 3.3V, pero mide con mayor precisión en el rango medio. Como tu LM324N nunca va a generar más de ~1.8V, estás protegiendo la entrada del ESP32 de forma natural y sin necesidad de componentes adicionales. Es una solución muy elegante.

### 🔌 Conexión Paso a Paso (LM324N + ESP32)

Este es el circuito más simple y efectivo para tu proyecto. Te recomiendo usar el amplificador No-Inversor porque es el más fácil de entender y tiene una alta impedancia de entrada, perfecta para las pastillas de guitarra.

#### Componentes del Preamplificador de Entrada

| Componente | Valor | Cantidad | Notas |
|------------|-------|----------|-------|
| Integrado principal | LM324N | 1 | Quad Op-Amp; usarás solo una de sus 4 secciones |
| Resistencia R1 | 1 MΩ | 1 | Para polarización y evitar ruido |
| Resistencia R2 | 10 kΩ | 1 | Fija la ganancia base |
| Resistencia/Potenciómetro R3 | 25 kΩ (lineal) | 1 | ¡El potenciómetro "B25K" de tu guitarra! |
| Capacitor C1 | 10 µF (electrolítico) | 1 | Para acoplar la salida y bloquear DC |
| Fuente de Alimentación | 3.3V | - | Directamente del pin del ESP32 |

**Componentes adicionales necesarios:**
- Protoboard, cables y jack para la guitarra

#### El Paso a Paso (Nombrando las patitas del LM324N):

El LM324N tiene 14 patitas. Nos vamos a concentrar en las del primer amplificador operacional, que son las patitas 1, 2, 3 y 4. La muesca o el círculo en el encapsulado te indica por dónde es la patita 1.

**Alimentación (Lo primero)**

1. Conecta la patita 4 (V+) al pin de 3.3V del ESP32.
2. Conecta la patita 11 (GND) al pin de GND del ESP32.

**Entrada de la Guitarra (Patita 3 - Entrada NO Inversora)**

1. La señal de tu guitarra (el "tip" del jack) va directo a la patita 3.
2. Coloca la resistencia de 1MΩ conectada también a la patita 3 y su otro extremo a GND. Esto evita que la entrada "flote" y genere ruido.

**Circuito de Ganancia (Patitas 1 y 2)**

1. Conecta la patita 2 (Entrada Inversora) a GND usando una resistencia de 10kΩ.
2. Conecta el potenciómetro de 50kΩ (o 100kΩ) entre la patita 1 (Salida) y la patita 2 (Entrada Inversora). Este potenciómetro controlará la ganancia (volumen/distorsión) de tu preamplificador.

**Salida hacia el ESP32 (Patita 1)**

1. La señal de salida la tomas de la patita 1.
2. Coloca el capacitor de 10µF en serie con la señal de salida (positivo hacia la patita 1, negativo hacia el ESP32). Esto elimina cualquier voltaje DC no deseado.
3. Conecta el otro lado del capacitor a un pin ADC del ESP32, por ejemplo, el GPIO 34.

## Hardware - Circuito de Salida PWM + Filtro RC

### Componentes del Circuito de Salida

| Componente | Cantidad | Notas |
|------------|----------|-------|
| Resistencia 270Ω | 1 | Parte del filtro PWM |
| Resistencia 100Ω | 1 | Parte del filtro PWM |
| Capacitor cerámico 10nF (103) | 1 | Filtro pasa-bajos |
| Capacitor cerámico 100nF (104) | 1 | Filtro adicional |
| Jack 3.5mm hembra | 1 | Para conectar auriculares |
| Resistencia 100kΩ | 1 | Pull-down opcional en salida |

### 🔌 Conexión del Circuito de Salida

Este circuito convierte la señal PWM del ESP32 en una señal analógica adecuada para auriculares o amplificadores.

**Configuración del Filtro RC**

1. Conecta la resistencia de 270Ω en serie con la salida PWM del ESP32
2. Conecta la resistencia de 100Ω después de la resistencia de 270Ω
3. Conecta el capacitor de 10nF (103) entre la unión de las dos resistencias y GND
4. Conecta el capacitor de 100nF (104) en paralelo con el de 10nF para un filtrado adicional

**Salida hacia Auriculares**

1. Toma la señal filtrada del punto entre las dos resistencias
2. Conecta esta señal al pin "tip" del jack 3.5mm hembra
3. Conecta el pin "sleeve" del jack a GND
4. Opcional: Coloca la resistencia de 100kΩ como pull-down en la salida para evitar ruido cuando no hay señal

**Recomendaciones:**
- Usa un pin PWM del ESP32 que soporte alta frecuencia (ej: GPIO 25, 26, 32)
- Configura el PWM a una frecuencia de al menos 31.25kHz para buena calidad de audio
- El filtro RC elimina la componente de alta frecuencia del PWM, dejando solo la señal de audio

## 📋 Tabla de Referencia Rápida de Componentes

| Referencia | Valor | Ubicación en el circuito | Código de colores (1ra, 2da, 3ra, 4ta) |
|------------|-------|-------------------------|----------------------------------------|
| R1 (preamp) | 1 MΩ | Patita 3 del LM324N a GND | Marrón, Negro, Verde, Dorado |
| R2 (preamp) | 10 kΩ | Patita 2 del LM324N a GND | Marrón, Negro, Naranja, Dorado |
| R3 (preamp) | 25 kΩ | Entre patitas 1 y 2 del LM324N (feedback) | Es tu potenciómetro B25K (no es resistencia fija) |
| R1 (filtro RC) | 270 Ω | Desde GPIO 25 del ESP32 al nodo A | Rojo, Violeta, Marrón, Dorado |
| R2 (filtro RC) | 100 Ω | Desde nodo A al nodo B (segunda etapa) | Marrón, Negro, Marrón, Dorado |

## 💻 Software - Estructura del Código MicroPython

El proyecto está organizado en módulos para facilitar el mantenimiento y la extensibilidad:

### Archivos del Proyecto

- **`main.py`** - Programa principal que configura el sistema y maneja el bucle principal
- **`config.py`** - Todas las constantes de configuración (pines, frecuencias, parámetros de efectos)
- **`audio_io.py`** - Manejo de entrada/salida de audio (ADC y PWM)
- **`effects.py`** - Implementación de efectos de audio (overdrive, delay)

### Cómo Usar el Código

1. **Sube los archivos al ESP32** usando Thonny o tu IDE preferido
2. **Configura los efectos** editando las variables en `main.py`:
   ```python
   ENABLE_OVERDRIVE = True   # Cambiar a True para activar overdrive
   ENABLE_DELAY = False      # Cambiar a True para activar delay
   ```
3. **Ajusta parámetros** en `config.py` según necesites:
   - `OVERDRIVE_GAIN` - Ganancia del efecto overdrive
   - `OVERDRIVE_THRESHOLD` - Umbral de clipping
   - `DELAY_AMOUNT` - Cantidad de mezcla de delay (0.0 a 1.0)

### Características del Software

- **Muestreo en tiempo real** a 20kHz para calidad de audio profesional
- **Procesamiento asíncrono** usando timers del ESP32
- **Buffer circular** para efectos de delay
- **Monitor de nivel** en tiempo real para debugging
- **Modular y extensible** - fácil agregar nuevos efectos

### Flujo de Audio

1. **Entrada**: Guitarra → LM324N → ADC (GPIO 34)
2. **Procesamiento**: Efectos configurados (overdrive, delay)
3. **Salida**: PWM (GPIO 25) → Filtro RC → Auriculares/Amplificador
