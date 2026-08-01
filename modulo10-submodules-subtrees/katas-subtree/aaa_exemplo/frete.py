def calcular_frete(peso_kg, distancia_km):
    if peso_kg <= 0 or distancia_km <= 0:
        raise ValueError("Peso e distancia devem ser positivos")
    elif peso_kg <= 5 and distancia_km <= 50:
        return 0
    else:
        return peso_kg * 2 + distancia_km * 0.5
