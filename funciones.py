def LLenarMatriz(nombre): # Para depuracion
    print("Ingrese los datos de la matriz", nombre)
    filas = int(input("Ingrese el número de filas: "))
    columnas = int(input("Ingrese el número de columnas: "))
    matriz = matriz_vacia(filas, columnas)
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            matriz[i][j] = float(input(f"Ingrese el número en la posición {i} , {j}: "))
        
    return matriz

def matriz_vacia(filas, columnas):
    return [[0 for _ in range(columnas)] for _ in range(filas)]

def ImprimirMatriz(matriz):
    for i in matriz:
        for j in i:
            print(j, end=" ")
        print()

def CuadradaONo(matriz):
    return len(matriz) == len(matriz[0])

def determinante_matriz(matriz): # Utilizando el metodo de Laplace
    if not CuadradaONo(matriz):
        raise ValueError("La matriz no es cuadrada (filas != columnas)")        
    else:
        if len(matriz) == 1:
            return matriz[0][0]

        if len(matriz) == 2:
            determinante = matriz[0][0] * matriz[1][1] - matriz[1][0] * matriz[0][1]
            return determinante
            
        # Recursivo, si la matriz es mayor a 2x2
        determinante = 0
        for j in range(len(matriz)):
            submatriz = [fila[:j] + fila[j+1:] for fila in matriz[1:]]            
            
            cofactor = matriz[0][j] * determinante_matriz(submatriz) * (-1) ** j
            determinante += cofactor

        return determinante
        

def llenar_sistema():
    print("Ingrese los datos del sistema de ecuaciones 3x3.")
    matriz = matriz_vacia(3, 4)
    for i in range(len(matriz)):
        print(f"Ingrese los valores de la ecuación {i+1}:")
        for j in range(len(matriz[0])):
            if j == columnas - 1:
                valor = float(input(f"Ingrese el valor independiente: "))
            else:
                valor = float(input(f"Ingrese el coeficiente de la variable {j+1}: "))
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

def float_a_entero(numero): # Para facilitar la lectura, si el número no es fraccionario
    if isinstance(numero, float) and numero.is_integer():
        return int(numero)
    return numero

def cramer(sistema):
    m1,m2,m3,m4 = matrices_modificadas(sistema)
    det_Ax = float_a_entero(determinante_matriz(m1))
    det_Ay = float_a_entero(determinante_matriz(m2))
    det_Az = float_a_entero(determinante_matriz(m3))
    det_A = float_a_entero(determinante_matriz(m4))
    if det_A == 0:
        raise ValueError("El sistema no tiene solución única (determinante del sistema es cero)")
    x,y,z = (float_a_entero(det_i / det_A) for det_i in (det_Ax, det_Ay, det_Az))

    return x,y,z

def transponer_matriz(matriz):
    return [[matriz[j][i] for j in range(len(matriz))] for i in range(len(matriz[0]))]

def cofactor_matriz(matriz):
    n = len(matriz)
    cofactor = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatriz = [row[:j] + row[j+1:] for row in (matriz[:i] + matriz[i+1:])]
            cofactor[i][j] = ((-1) ** (i+j)) * determinante_matriz(submatriz)
    return cofactor


def matriz_adjunta(matriz):
    cofactor = cofactor_matriz(matriz)
    return transponer_matriz(cofactor)

def multiplicacion_posible(matrizA, matrizB):
    return len(matrizA[0]) == len(matrizB)

def multiplicacion_matrices(matrizA, matrizB):
    if not multiplicacion_posible(matrizA, matrizB):
        raise ValueError("No se puede multiplicar estas matrices (numero de columnas de A != numero de filas de B)")
    else:        
        filas = len(matrizA)
        columnas = len(matrizB[0])
        matrizResultante = [[0 for _ in range(columnas)] for _ in range(filas)]
        for i in range(filas):
            for j in range(columnas):
                for k in range(len(matrizA[0])):
                    matrizResultante[i][j] += float_a_entero(matrizA[i][k] * matrizB[k][j])
        return matrizResultante

def multiplicacion_escalar(numero, matriz):
    resultado = matriz_vacia(len(matriz),len(matriz[0]))
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            resultado[i][j] = numero * matriz[i][j]
    return resultado

matrizA = [
    [1,0,0],
    [0,1,0],
    [0,0,1]
]

ImprimirMatriz(multiplicacion_escalar(5,matrizA))