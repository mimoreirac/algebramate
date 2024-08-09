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

def DeterminanteMatriz(matriz): # Utilizando el metodo de Laplace
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

def matrices_modificadas(matriz): # Para poder utilizar el metodo de Cramer
    matrices = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(4)] # Lista de matrices para generar 4 matrices 3x3

    for i in range(4): # matrices
        for j in range(3): # filas
            for k in range(3): # columnas
                if i < 3 and k == i:
                    matrices[i][j][k] = matriz[j][3] # Cambia la columna por términos independientes
                else:
                    matrices[i][j][k] = matriz[j][k] # Para la última matriz, descarta los independientes

    return matrices[0], matrices[1], matrices[2], matrices[3]

def float_a_entero(numero): # Facilidad de lectura, si el número no es fraccionario
    if isinstance(numero, float) and numero.is_integer():
        return int(numero)
    return numero


sistemaA = llenar_sistema()
ImprimirMatriz(sistemaA)
print()
m1,m2,m3,m4 = matrices_modificadas(sistemaA)
print()
ImprimirMatriz(m1)
print()
ImprimirMatriz(m2)
print()
ImprimirMatriz(m3)
print()
ImprimirMatriz(m4)