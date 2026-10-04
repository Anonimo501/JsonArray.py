# JsonArray.py

Este script esta pensado para ayudar a crear un Json Array para atacar los codigos 2FA u OTPs mas especificamente para los ataques de Batching Attack, ver mas en https://portswigger.net/web-security/authentication/password-based/lab-broken-brute-force-protection-multiple-credentials-per-request.

Un ataque de batching (agrupamiento) en GraphQL permite enviar múltiples operaciones en una sola solicitud HTTP POST para evadir límites de tasa (rate limiting) o realizar ataques de fuerza bruta.

## Batching Attack (Ataque por lotes)

Este ataque no solo sirve para los codigos OTP tambien sirve para probar muchas contraseñas en una unica solicitud o request de burpsuite.

Es el nombre técnico más preciso para esta técnica. En lugar de enviar 1,000 peticiones HTTP con una contraseña cada una, agrupas (haces un "batch") de miles de contraseñas en un solo arreglo JSON y realizas una única petición.

<img width="764" height="373" alt="Image" src="https://github.com/user-attachments/assets/958a2b6f-8c84-4c2c-aa17-f46a9fac524e" />

Al ejecutar el scritp creara un archivo con el array conpleto, listo para copiar y agregar a la peticion de burpsuite.

<img width="298" height="155" alt="image" src="https://github.com/user-attachments/assets/d0248b7d-1a27-4e90-8218-97c7e62550c7" />

## Ejemplo

· Intercepta y envía la petición: Captura la solicitud de login con el Proxy y envíala al Repeater.

· Modifica el cuerpo de la petición: Cambia el valor del campo password (o code) de un string a un array de strings en formato JSON. La petición debería verse así:
 
  json
  
 {
 
    "username": "carlos",
    "password": ["123456", "password", "qwerty", "correct_password", "..."]
 
 }
  
· Envía y analiza: Al enviar esta única petición, el servidor (si es vulnerable) iterará internamente por toda la lista. Un código de estado 302 Found o una respuesta de éxito indicará que una de las contraseñas fue la correcta. Luego solo debes copiar la cookie de sesión de la respuesta para secuestrar la cuenta.
