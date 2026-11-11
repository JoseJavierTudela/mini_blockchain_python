import hashlib, json, time


# Función para generar un hash de un bloque
def hash_bloque (bloque: dict) -> str:
    contenido = json.dumps(bloque, sort_keys = True).encode()
    return hashlib.sha256(contenido).hexdigest()
#Funcion para crear un nuevo bloque
def crear_bloque(indice, transacciones, hash_previo):
    return {
        "indice": indice,
        "timestamp": time.time(),
        "transacciones": transacciones,
        "hash_previo": hash_previo,
        "nonce": 0, #Nonce: número aleatorio que se va añadiendo hasta que el hash sea válido.
    }
    
#Dificultad: cuantos ceros al principio del hash queremos.
#Prefijo: los ceros que queremos que tenga el hash.
dificultad = 4
prefijo = "0" * dificultad
#Funcion para minar un bloque
def minar_bloque(bloque):
    while not hash_bloque(bloque).startswith(prefijo):
        bloque["nonce"] += 1
    return bloque

#Bloque Genesis: el primer bloque de la cadena.
cadena = [minar_bloque(crear_bloque(0, ["Bloque Genesis"], "0" * 64))] 


transaccion_bloque1 =["Ana le pasa a Luis 5 Bitcoins"]
transaccion_bloque2 =["Luis le pasa a Eva 3 Bitcoins"]
#Bucle para añadir nuevos bloques
for i, txs in enumerate([transaccion_bloque1, transaccion_bloque2], start=1):
    cadena.append(minar_bloque(crear_bloque(i, txs, hash_bloque(cadena[-1]))))


def es_valida(cadena): 
    if not hash_bloque(cadena[0]).startswith(prefijo):
        return False

    for i in range(1, len(cadena)):
        bloque_actual = cadena[i]
        bloque_anterior = cadena[i-1]
        if bloque_actual ["hash_previo"] != hash_bloque(bloque_anterior):
            return False
        if not hash_bloque(bloque_actual).startswith(prefijo):
            return False
    return True 
     
print(es_valida(cadena))  # True
print(json.dumps(cadena, indent=2))  # mira los nonce y hash_previo