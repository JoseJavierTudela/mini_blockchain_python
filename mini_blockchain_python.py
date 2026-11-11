import hashlib, json, time
#hashlib: trae funciones hash, como SHA-256 (la que usa Bitcoin). Un hash convierte cualquier dato en una cadena de longitud fija. Si cambias un solo carácter de la entrada, el resultado cambia por completo.
#json: convierte un diccionario de Python en texto, porque el hash trabaja con bytes y no con diccionarios.
#time: nos da la hora actual para el sello de tiempo del bloque.

# Función para generar un hash de un bloque
def hash_bloque (bloque: dict) -> str:
    contenido = json.dumps(bloque, sort_keys = True).encode()
    return hashlib.sha256(contenido).hexdigest()
#json.dumps(bloque, sort_keys=True): convierte el diccionario en texto JSON. 
#El sort_keys=True ordena las claves siempre igual. Es importante: {"a":1,"b":2} y {"b":2,"a":1} son el mismo diccionario, pero como texto serían distintos y darían hashes diferentes. Con las claves ordenadas, el mismo bloque da siempre el mismo hash.
#.encode(): pasa el texto a bytes, que es lo que SHA-256 necesita.
#hashlib.sha256(contenido): calcula el hash.
#.hexdigest(): lo muestra como texto hexadecimal de 64 caracteres.

#Funcion para crear un nuevo bloque
def crear_bloque(indice, transacciones, hash_previo):
    return {
        "indice": indice,
        "timestamp": time.time(),
        "transacciones": transacciones,
        "hash_previo": hash_previo,
    }

#indice: la posición del bloque en la cadena (0, 1, 2...).
#timestamp: el momento de creación (time.time() da los segundos desde 1970).
#transacciones: la lista de operaciones que guarda.
#hash_previo: el hash del bloque anterior. Este campo es el eslabón de la cadena.
#Lo que se guarda aquí no es el hash del propio bloque, sino el del anterior. El hash del bloque actual se calcula cuando hace falta, con hash_bloque.

#Bloque Genesis: el primer bloque de la cadena.
cadena = [crear_bloque(0, ["Bloque Genesis"], "0" * 64)] 

#crear_bloque(0, [], "0" * 64): índice 0, sin transacciones ([]) y un hash_previo inventado. "0" * 64 son 64 ceros, la misma longitud que un hash SHA-256, para que sea coherente.
#Los corchetes [...] crean una lista con ese bloque dentro. La lista cadena será nuestra blockchain.
transaccion_bloque1 =["Ana le pasa a Luis 5 Bitcoins"]
transaccion_bloque2 =["Luis le pasa a Eva 3 Bitcoins"]
#Bucle para añadir nuevos bloques
for i, txs in enumerate([transaccion_bloque1, transaccion_bloque2], start=1):
    cadena.append(crear_bloque(i, txs, hash_bloque(cadena[-1])))

#[["Ana->Luis: 5"], ["Luis->Eva: 2"]]: una lista con dos listas. Cada lista interna son las transacciones de un bloque, aquí de juguete (textos simples). El primer bloque tendrá “Ana envía 5 a Luis” y el segundo “Luis envía 2 a Eva”.
#enumerate(..., start=1): va entregando cada elemento junto con un contador que empieza en 1. Así, i es el índice del bloque y txs sus transacciones.
#cadena[-1]: el último bloque de la cadena (el índice -1 en Python es el final).
#hash_bloque(cadena[-1]): calcula la huella de ese último bloque.
#crear_bloque(i, txs, ...): crea el nuevo bloque apuntando al hash del anterior.
#cadena.append(...): lo añade al final. 

#Comprobar la cadena

def es_valida(cadena): 
    for i in range(1, len(cadena)):
        bloque_actual = cadena[i]
        bloque_anterior = cadena[i-1]
        if bloque_actual ["hash_previo"] != hash_bloque(bloque_anterior):
            return False
    return True 
#for i in range(1, len(cadena)): va recorriendo cada bloque desde el segundo al último.
#bloque_actual = cadena[i]: el bloque actual que se está comprobando.
#bloque_anterior = cadena[i-1]: el bloque anterior (el anterior al actual).
#bloque_actual ["hash_previo"] != hash_bloque(bloque_anterior): si el hash del bloque anterior no coincide con el hash del bloque actual, la cadena no es válida.
#return False: si la cadena no es válida, devuelve False.
#return True: si la cadena es válida, devuelve True.

#Comprobar la cadena
print(es_valida(cadena))

#Mostrar la cadena
print(cadena)

#Simular un ataque a la cadena
cadena[1]["transacciones"] = ["Ana le pasa a Luis 500 Bitcoins"]

print(es_valida(cadena))
print(cadena)