def LLenarMatriz(nombre):
    print("Ingrese los datos de la matriz", nombre)
    filas = int(input("Ingrese el número de filas: "))
    columnas = int(input("Ingrese el número de columnas: "))
    matriz = [[0 for _ in range(columnas)] for _ in range(filas)]
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            matriz[i][j] = float(input(f"Ingrese el número en la posición {i} , {j}: "))
        
    return matriz

def ImprimirMatriz(matriz):
    for i in matriz:
        for j in i:
            print(j, end=" ")
        print()

def CuadradaONo(matriz):
    if(len(matriz) != len(matriz[0])):
        matrizcuadrada = False
    else:
        matrizcuadrada = True

    return matrizcuadrada

def DeterminanteMatriz(matriz): # Para obtener determinante utilizando el metodo de Laplace
    if CuadradaONo(matriz):
        if len(matriz) == 1:
            return matriz[0][0]

        if len(matriz) == 2:
            determinante = matriz[0][0] * matriz[1][1] - matriz[1][0] * matriz[0][1]
            return determinante
            
        # Recursivo, si la matriz es mayor a 2x2
        determinante = 0
        for j in range(len(matriz)):
            submatriz = [fila[:j] + fila[j+1:] for fila in matriz[1:]]            
            
            cofactor = matriz[0][j] * DeterminanteMatriz(submatriz) * (-1) ** j
            determinante += cofactor

        return determinante

def llenar_sistema():
    print("Ingrese los datos del sistema de ecuaciones 3x3.")
    filas = 3
    columnas = 4
    matriz = [[0 for _ in range(columnas)] for _ in range(filas)]
    for i in range(len(matriz)):
        print(f"Ingrese los valores de la ecuación {i+1}:")
        for j in range(len(matriz[0])):
            if j == columnas - 1:
                valor = float(input(f"Ingrese el valor independiente: "))
            else:
                valor = float(input(f"Ingrese el coeficiente de la variable x{j+1}: "))
            matriz[i][j] = valor
        
    return matriz


# matrizA = LLenarMatriz("A")
# determinanteA = DeterminanteMatriz(matrizA)

# ImprimirMatriz(matrizA)
# print()
# print(f"El determinante es {determinanteA}")

ecuacion1 = llenar_sistema()
ImprimirMatriz(ecuacion1)
