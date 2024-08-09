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
            submatriz = [[0 for _ in range(len(matriz)-1)] for _ in range(len(matriz)-1)]
            for i in range(1, len(matriz)):
                col = 0
                for k in range(len(matriz)):
                    if k != j:
                        submatriz[i-1][col] = matriz[i][k]
                        col += 1
            
            cofactor = matriz[0][j] * DeterminanteMatriz(submatriz) * (-1) ** j
            determinante += cofactor
        
        return determinante


matrizA = LLenarMatriz("A")
determinanteA = DeterminanteMatriz(matrizA)

ImprimirMatriz(matrizA)
print()
print(f"El determinante es {determinanteA}")
