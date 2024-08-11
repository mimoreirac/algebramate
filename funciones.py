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

def float_a_entero(numero): # Para facilitar la lectura, si el número no es fraccionario
    if isinstance(numero, float) and numero.is_integer():
        return int(numero)
    return numero

def ImprimirMatriz(matriz, paso=""):
    print(f"\n{paso}")
    print()
    ancho = max(len(f"{j:.2f}") for i in matriz for j in i)
    for i in matriz:
        for j in i:
            print(f"{j:{ancho}.2f}", end="  ")
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
    matrices = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(3)] # Lista de matrices para generar 3 matrices 3x3

    for i in range(3): # matrices
        for j in range(3): # filas
            for k in range(3): # columnas
                matrices[i][j][k] = matriz[j][3] # Cambia la columna por términos independientes
                if k == i:
                    matrices[i][j][k] = matriz[j][3]  # Cambia la columna i por términos independientes
                else:
                    matrices[i][j][k] = matriz[j][k]  # Mantiene los coeficientes originales

    return matrices[0], matrices[1], matrices[2]

def terminos_indep(matriz):
    if not len(matriz) == 3 or not len(matriz[0]) == 4:
        raise ValueError("No es una matriz 3x4")
    else:
        m_indep = matriz_vacia(len(matriz),1)
        for i in range(len(m_indep)):
                for j in range(len(m_indep[0])):
                    m_indep[i][j] = matriz[i][3]

def matriz_coeficientes(matriz):
    if not len(matriz) == 3 or not len(matriz[0]) == 4:
        raise ValueError("No es una matriz 3x4")
    else:
        matrizA = matriz_vacia(3,3)
        for i in range(len(matrizA)):
            for j in range(len(matrizA[0])):
                matrizA[i][j] = matriz[i][j]
        return matrizA

def cramer(matriz):
    matrices_mod = matrices_modificadas(matriz)
    etiquetas = ["Ax", "Ay", "Az"]
    
    for i, m in enumerate(matrices_mod):
        ImprimirMatriz(m, f"Matriz modificada {etiquetas[i]}")
    
    matriz_coef = matriz_coeficientes(matriz)
    ImprimirMatriz(matriz_coef, "Matriz de coeficientes A")

    determinantes = [float_a_entero(determinante_matriz(m)) for m in matrices_mod]
    det_A = float_a_entero(determinante_matriz(matriz_coef))
    print()
    for i, etiqueta in enumerate(etiquetas):
        print(f"Determinante {etiqueta}: {determinantes[i]}")
    
    print(f"Determinante A: {det_A}")
    
    if det_A == 0:
        raise ValueError("El sistema no tiene solución única (determinante de coeficientes es cero)")
    x, y, z = (float_a_entero(det_i / det_A) for det_i in determinantes)
    
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

def algebra_matricial(matriz):
    matriz_base,independientes = matriz_independientes(matriz)
    det_base = 1 / determinante_matriz(matriz_base)
    resultado = multiplicacion_matrices(matriz_adjunta(matriz_base), independientes)
    resultado = multiplicacion_escalar(det_base, resultado)
    x = float_a_entero(resultado[0][0])
    y = float_a_entero(resultado[1][0])
    z = float_a_entero(resultado[2][0])
    return resultado,x,y,z

###### Probando cosas para Gauss
def volver_uno(matriz, pivote):
    col = len(matriz[0])
    if matriz[pivote][pivote] == 0:
        raise ValueError("No se puede dividir para 0")

    divisor = matriz[pivote][pivote]
    for j in range(col):
        matriz[pivote][j] /= divisor
    ImprimirMatriz(matriz, f"Después de volver 1 el pivote en la fila {pivote + 1}")
    

def volver_cero(matriz, fila, columna):
    col = len(matriz[0])
    if matriz[fila][columna] != 0:
        multiplicando = matriz[fila][columna]
        for j in range(col):
            matriz[fila][j] -= multiplicando * matriz[columna][j]
    ImprimirMatriz(matriz, f"Después de volver 0 el elemento en la fila {fila + 1}, columna {columna + 1}")


def gauss_jordan(matriz):
    n = len(matriz)
    ImprimirMatriz(matriz, "Matriz inicial")
    for i in range(n):
        # Encontrar el pivote
        elemento_max = abs(matriz[i][i])
        fila_max = i
        for k in range(i + 1, n):
            if abs(matriz[k][i]) > elemento_max:
                elemento_max = abs(matriz[k][i])
                fila_max = k

        # Intercambiar filas
        if fila_max != i:
            matriz[i], matriz[fila_max] = matriz[fila_max], matriz[i]
            ImprimirMatriz(matriz, f"Después de intercambiar la fila {i + 1} con la fila {fila_max + 1}")

        volver_uno(matriz, i)

        for j in range(n):
            if i != j:
                volver_cero(matriz, j, i)
    return matriz
############################################### Ejecucion: ########################

matrizA = [
    [2,6,1,7],
    [1,2,-1,-1],
    [5,7,-4,9]
]
# matrizB,independiente = matriz_independientes(matrizA)
# ImprimirMatriz(matrizB)
# print()
# ImprimirMatriz(independiente)
# print()

# ressss,x,y,z = algebra_matricial(matrizA)
# ImprimirMatriz(ressss)
# print(x,y,z)

# ImprimirMatriz(gauss_jordan(matrizA))
ImprimirMatriz(matrizA, "Matriz inicial")
valor1,valor2,valor3 = cramer(matrizA)
print(valor1,valor2,valor3)



