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
