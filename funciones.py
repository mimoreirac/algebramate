import numpy as np
# Algebra:

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
            if j == len(matriz[0]) - 1:
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
        return m_indep

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
    ImprimirMatriz(matriz, "Matriz extendida del sistema")
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
    print()
    print("Soluciones: ")
    print()
    print(f"X: {x}")
    print(f"Y: {y}")
    print(f"Z: {z}")
    print()
    
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
    matriz_base = matriz_coeficientes(matriz)
    independientes = terminos_indep(matriz)
    det_coeficientes = determinante_matriz(matriz_base)
    det_fraccionaria = 1 / determinante_matriz(matriz_base)
    resultado = multiplicacion_matrices(matriz_adjunta(matriz_base), independientes)
    resultado = multiplicacion_escalar(det_fraccionaria, resultado)
    x = float_a_entero(resultado[0][0])
    y = float_a_entero(resultado[1][0])
    z = float_a_entero(resultado[2][0])
    ImprimirMatriz(matriz, "Matriz extendida del sistema")
    ImprimirMatriz(matriz_base, "Matriz de coeficientes")
    ImprimirMatriz(independientes, "Términos independientes")
    print()
    print(f"Determinante de la matriz de coeficientes: {det_coeficientes}")
    ImprimirMatriz(cofactor_matriz(matriz_base), "Matriz adjunta")
    ImprimirMatriz(matriz_adjunta(matriz_base), "Matriz adjunta transpuesta.")
    ImprimirMatriz(multiplicacion_matrices(matriz_adjunta(matriz_base), independientes), "Multiplicacion de matriz adjunta, por matriz de independientes.")
    print()
    print("Soluciones: ")
    print()
    print(f"X: {x}")
    print(f"Y: {y}")
    print(f"Z: {z}")
    print()

    return resultado,x,y,z


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
    ImprimirMatriz(matriz, "Matriz extendida del sistema")
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

    resultado = terminos_indep(matriz)
    ImprimirMatriz(resultado, "Soluciones:")
    print()

    
    return matriz

# Matematicas:

def tipo_funcion():
    while True:
        print("¿Qué tipo de función desea resolver?")
        print("1. Lineal (ax + b)")
        print("2. Cuadrática (ax^2 + bx + c)")
        print("3. Cúbica (ax^3 + bx^2 + cx + d)")
        opcion = input("Ingrese su opción (1, 2, o 3): ")
        if opcion in ['1', '2', '3']:
            return int(opcion)
        print("Opción incorrecta. Por favor elija 1, 2, o 3.")

def leer_funcion(string_funcion, tipo_de_funcion):
    coeficientes = [0] * (tipo_de_funcion + 1)
    terminos = string_funcion.replace('-', '+-').split('+')
    for termino in terminos:
        if 'x^3' in termino:
            coeficientes[3] = float(termino.replace('x^3', '') or '1')
        elif 'x^2' in termino:
            coeficientes[2] = float(termino.replace('x^2', '') or '1')
        elif 'x' in termino:
            coeficientes[1] = float(termino.replace('x', '') or '1')
        else:
            coeficientes[0] = float(termino or '0')
    return coeficientes

def evaluar(coeficientes, x):
    return coeficientes[0] + coeficientes[1]*x + coeficientes[2]*x**2 + coeficientes[3]*x**3


def dominio_rango(coeficientes):
    dominio = "Todos los números reales"
    if coeficientes[3] != 0 or coeficientes[1] != 0:  # Cúbica y lineal
        rango = "Todos los números reales"
    elif coeficientes[2] != 0:  # Cuadrática
        vertice_y = evaluar(coeficientes, -coeficientes[1] / (2*coeficientes[2]))
        if coeficientes[2] > 0:
            rango = f"[{vertice_y}, +∞)"
        else:
            rango = f"(-∞, {vertice_y}]"
    else:  # Constante
        rango = str(coeficientes[0])
    return dominio, rango

def sacar_raices(coeficientes):
    grado = len(coeficientes) - 1
    if grado == 3:  # Cúbica
        raices = np.roots(coeficientes[::-1])  # NumPy recibe los coeficientes en orden ascendente
        return [root.real for raiz in raices if abs(root.imag) < 1e-10]  # Para utilizar solamente raíces reales
    elif grado == 2:  # Cuadrática
        a, b, c = coeficientes[2], coeficientes[1], coeficientes[0]
        discriminante = b**2 - 4*a*c
        if discriminante > 0:
            return [(-b + np.sqrt(discriminante)) / (2*a), (-b - np.sqrt(discriminante)) / (2*a)]
        elif discriminante == 0:
            return [-b / (2*a)]
        else:
            return []
    elif grado == 1:  # Lineal
        return [-coeficientes[0] / coeficientes[1]] if coeficientes[1] != 0 else []
    else:  # Constante
        return [] if coeficientes[0] != 0 else ["Todos los números reales"]

def puntos_corte(coeficientes):
    corte_y = coeficientes[0]
    corte_x = sacar_raices(coeficientes)
    return corte_x, corte_y

def monotonia(coeficientes):
    grado = len(coeficientes) - 1
    if grado == 3:  # Cúbica
        a, b, c, d = coeficientes[3], coeficientes[2], coeficientes[1], coeficientes[0]
        # Coeficientes de la derivada
        coef_derivada = [3*a, 2*b, c]
        # Encontrar puntos críticos
        puntos_criticos = np.roots(coef_derivada)
        criticos_reales = [x.real for x in puntos_criticos if abs(x.imag) < 1e-10]
        criticos_reales.sort()

        if len(criticos_reales) == 2:
            x1, x2 = criticos_reales
            if 3*a*x1**2 + 2*b*x1 + c > 0:
                return f"Decreciente (-∞, {x1:.2f}), creciente ({x1:.2f}, {x2:.2f}), decreciente ({x2:.2f}, +∞)"
            else:
                return f"Creciente (-∞, {x1:.2f}), decreciente ({x1:.2f}, {x2:.2f}), creciente ({x2:.2f}, +∞)"
        elif len(criticos_reales) == 1:
            x1 = criticos_reales[0]
            if 3*a*x1**2 + 2*b*x1 + c > 0:
                return f"Decreciente (-∞, {x1:.2f}), Creciente ({x1:.2f}, +∞)"
            else:
                return f"Creciente (-∞, {x1:.2f}), Decreciente ({x1:.2f}, +∞)"
        else:
            return "Creciente" if a > 0 else "Decreciente"

    elif grado == 2:  # Cuadrática
        a, b, c = coeficientes[2], coeficientes[1], coeficientes[0]
        vertice_x = -b / (2*a)
        if a > 0:
            return f"Decreciente (-∞, {vertice_x:.2f}), creciente ({vertice_x:.2f}, +∞)"
        else:
            return f"Creciente (-∞, {vertice_x:.2f}), decreciente ({vertice_x:.2f}, +∞)"

    elif grado == 1:  # Lineal
        return "Creciente" if coeficientes[1] > 0 else "Decreciente"

    else:  # Constante
        return "Constante"

def menu_funciones():
    tipo_func = tipo_funcion()
    while True:
        if tipo_func == 1:
            string_funcion = input("Ingrese una función lineal (ej: 2x + 1): ")
        elif tipo_func == 2:
            string_funcion = input("Ingrese una función cuadrática (ej: 2x^2 + 3x - 1): ")
        else:
            string_funcion = input("Ingrese una función cúbica (ej: 2x^3 + 3x^2 - x + 1): ")
        
        # if validate_function(string_funcion, tipo_func):
        #     break
        # print("Invalid function format. Please try again.")
        break
    
    coeficientes = leer_funcion(string_funcion, tipo_func)
    
    dominio, rango = dominio_rango(coeficientes)
    monotonia = monotonia(coeficientes)
    corte_x, corte_y = puntos_corte(coeficientes)
    
    print(f"Dominio: {dominio}")
    print(f"Rango: {rango}")
    print(f"Monotonía: {monotonia}")
    print(f"Puntos de corte con x: {corte_x}")
    print(f"Puntos de corte con y: {corte_y}")
############################################### Ejecucion: ########################

def menu_principal():
    while True:
        print("Bienvenido a la calculadora. ¿Qué tipo de problema desea resolver?")
        print("1. Funciones")
        print("2. Sistemas de Ecuaciones 3x3")
        print("3. Salir")
        opcion = input("Ingrese su opción (1, 2, o 3): ")
        if opcion in ['1', '2', '3']:
            return int(opcion)
        print("Opción incorrecta. Por favor elija 1, 2, o 3.")

def menu_sistemas():
    while True:
        print("¿Qué método desea aplicar?")
        print("1. Método de Cramer")
        print("2. Método de Álgebra Matricial")
        print("3. Método de Gauss-Jordan")
        print("4. Salir")
        opcion = input("Ingrese su opción (1, 2, 3 o 4): ")
        if opcion in ['1', '2', '3', '4']:
            return int(opcion)
        print("Opción incorrecta. Por favor elija 1, 2, 3 o 4.")


opcion = menu_principal()
while True:
    match opcion:
        case 1:
            break
        case 2:
            while True:
                opcion = menu_sistemas()
                match opcion:
                    case 1:
                        print("Método de Cramer")
                        cramer(llenar_sistema())
                    case 2:
                        print("Método de Álgebra Matricial")
                        algebra_matricial(llenar_sistema())
                    case 3:
                        print("Método de Gauss-Jordan")
                        gauss_jordan(llenar_sistema())
                    case 4:
                        break
        case 3:
            break
        
        


# matrizA = [
#     [2,6,1,7],
#     [1,2,-1,-1],
#     [5,7,-4,9]
# ]


# matrizB,independiente = matriz_independientes(matrizA)
# ImprimirMatriz(matrizB)
# print()
# ImprimirMatriz(independiente)
# print()

# ressss,x,y,z = algebra_matricial(matrizA)
# ImprimirMatriz(ressss)
# print(x,y,z)

# ImprimirMatriz(gauss_jordan(matrizA))
# ImprimirMatriz(matrizA, "Matriz inicial")
# valor1,valor2,valor3 = cramer(matrizA)
# print(valor1,valor2,valor3)
# menu_funciones()
