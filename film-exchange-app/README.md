# NEXORA — app de exchange cripto falsa (atrezzo para película)

App Android (APK) que imita un exchange de criptomonedas móvil. **Todos los datos son ficticios**:
no hay red, ni cuentas reales, ni dinero real. Pensada para rodaje.

La marca "NEXORA" es inventada, para no mostrar en la película el logo ni la marca de ninguna empresa real.

## Qué incluye
- **Home**: saldo total de **40,000.00 USDT**, PnL, botones Deposit/Withdraw/Trade y una lista de mercados con precios que se mueven cada segundo.
- **Markets**: 20 pares con volumen, precio y % de cambio, y buscador.
- **Trade (Spot)**: libro de órdenes en vivo, Buy/Sell, órdenes Limit/Market y slider de %. Las órdenes se ejecutan de verdad contra el saldo falso (si compras BTC, baja el USDT y el BTC aparece en Assets).
- **Gráfico**: velas con MA(7)/MA(25)/MA(99), volumen, temporalidades y trades en vivo.
- **Futures**, **Assets**, **Historial** (depósito de 40,000 USDT por TRC20), **Deposit** (dirección + QR), **Send/Withdraw** con un código 2FA que se rellena solo y pantalla de "Withdrawal Submitted".

## Ajustes de atrezzo (ocultos)
En **Home**, **toca 5 veces rápido el avatar (la letra redonda de arriba a la izquierda)** para abrir el panel oculto:
- Cambia el saldo USDT, el nombre de usuario, el UID y la etiqueta VIP.
- "Reset everything to 40,000 USDT" deja la app como al principio entre tomas.

Un solo toque en el avatar abre el perfil del usuario.

## Compilar
Requisitos: JDK 17+, Android SDK (platform 34, build-tools 34), Gradle 8.7+.
```
echo "sdk.dir=/ruta/al/android-sdk" > local.properties
gradle assembleRelease
# APK: app/build/outputs/apk/release/app-release.apk
```
Para editar la interfaz: `app/src/main/assets/index.html` (HTML/JS; se puede abrir en Chrome para previsualizarla).
