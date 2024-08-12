import matplotlib.pyplot as plt
import numpy as np
import math
import numpy.polynomial.polynomial as poly

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

def leer_funcion(funcion, tipo): 
    coeficientes = [0] * (tipo + 1)
    terminos = funcion.replace('-', '+-').split('+')
    for termino in terminos:
        termino = termino.strip()
        if termino == '-x': # Para evitar errores, si el coeficiente de un término negativo es 1
            coeficientes[1] = -1.0
        elif termino == '-x^2':
            coeficientes[2] = -1.0
        elif termino == '-x^3':
            coeficientes[3] = -1.0
        elif 'x^3' in termino:
            coeficientes[3] = float(termino.replace('x^3', '') or '1')
        elif 'x^2' in termino:
            coeficientes[2] = float(termino.replace('x^2', '') or '1')
        elif 'x' in termino:
            coeficientes[1] = float(termino.replace('x', '') or '1')
        elif termino:
            coeficientes[0] = float(termino)
    return coeficientes

def derivar(coeficientes):
    derivada = [0] * len(coeficientes)
    for i in range(1, len(coeficientes)):
        derivada[i-1] = coeficientes[i] * i
    return derivada

def corte_y(coeficientes):
    return coeficientes[0]

def corte_x(coeficientes, grado):
    if grado == 1: # Ecuación lineal
        a = coeficientes[1]
        b = coeficientes[0]
        if a == 0:
            if b == 0:
                return "Existen infinitas soluciones"  # 0 = 0 
            else:
                return "No existe solución"  # b ≠ 0 y a = 0 (no se puede dividir por 0)
        else:
            return -b / a
    elif grado == 2: # Ecuación cuadrática
        a = coeficientes[2]
        b = coeficientes[1]
        c = coeficientes[0]
        discriminante = b**2 - 4*a*c

        if discriminante > 0:
            x1 = (-b + math.sqrt(discriminante)) / (2 * a) # Fórmula general
            x2 = (-b - math.sqrt(discriminante)) / (2 * a)
            return x1, x2
        elif discriminante == 0:
            return -b / (2 * a) # Solo existe una raíz
        else:
            return "No tiene punto de corte con el eje X" # Raíces complejas

def monotonia_cubica(derivada):    
    c,b,a,d = derivada
    discriminante = b**2 - 4 * a * c

    if discriminante > 0:
        # Dos puntos criticos
        x1 = (-b + np.sqrt(discriminante)) / (2 * a)
        x2 = (-b - np.sqrt(discriminante)) / (2 * a)
        critical_points = [x1, x2]
    elif discriminante == 0:
        # Un solo punto critico
        x = -b / (2 * a)
        critical_points = [x]
    else:
        # No existen puntos críticos reales, la función es solamente creciente o decreciente.
        critical_points = []

    if a > 0:
        return "Creciente en los intervalos (-∞, {1}) y ({0}, +∞) , Decreciente en ({1}, {0})".format(*critical_points) if len(critical_points) == 2 else "Creciente en (-∞, +∞)"
    elif a < 0:
        return "Decreciente en los intervalos (-∞, {1}) y ({0}, +∞) , Creciente en ({1}, {0})".format(*critical_points) if len(critical_points) == 2 else "Decreciente en (-∞, +∞)"


def etiquetar_func(coeficientes, grado):
    x = np.linspace(-10, 10, 100) # Genera eje x
    if grado == 1:        
        # Función lineal: y = ax + b
        a = coeficientes[1]
        b = coeficientes[0]

        if b > 0:
            nombre_func = f"y = {a}x + {b}"
        elif b < 0:
            nombre_func = f"y = {a}x - {abs(b)}"
        else:  # b == 0
            nombre_func = f"y = {a}x"

        y = a * x + b
        return x, y, nombre_func
    elif grado == 2:
        # Función cuadrática
        a = coeficientes[2]
        b = coeficientes[1]
        c = coeficientes[0]

        if b > 0:
            nombre_func = f"y = {a}x^2 + {b}x"
        elif b < 0:
            nombre_func = f"y = {a}x^2 - {abs(b)}x"
        else:  # b == 0
            nombre_func = f"y = {a}x^2"

        if c > 0:
            nombre_func += f" + {c}"
        elif c < 0:
            nombre_func += f" - {abs(c)}"
        
        y = a * x**2 + b * x + c

    elif grado == 3:
        a = coeficientes[3]
        b = coeficientes[2]
        c = coeficientes[1]
        d = coeficientes[0]
        nombre_func = f"y = {a}x^3"
        if b != 0:
            nombre_func += f" + {b}x^2" if b > 0 else f" - {abs(b)}x^2"
        if c != 0:
            nombre_func += f" + {c}x" if c > 0 else f" - {abs(c)}x"
        if d != 0:
            nombre_func += f" + {d}" if d > 0 else f" - {abs(d)}"
        y = a * x**3 + b * x**2 + c * x + d
    else:
        raise ValueError("Esta función solo acepta funciones lineales, cuadráticas y cúbicas")
    
    return x, y, nombre_func

def dibujar_grafica(x, y, nombre_func):
    plt.plot(x, y, label=nombre_func, color='blue')
    plt.title(f"Gráfica de {nombre_func}")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.axhline(linewidth=2, color='black') # Resalta los ejes en el plano
    plt.axvline(linewidth=2, color='black')
    plt.ylim(-10, 10)
    plt.show()


def graficar_funcion(coeficientes, grado):
    # x = np.linspace(-10, 10, 100) # Genera eje x
    if grado == 1:
        x, y, nombre_func = etiquetar_func(coeficientes, grado)
        dibujar_grafica(x, y, nombre_func)
    elif grado == 2:
        x, y, nombre_func = etiquetar_func(coeficientes, grado)
        dibujar_grafica(x, y, nombre_func)
    elif grado == 3:
        x, y, nombre_func = etiquetar_func(coeficientes, grado)
        dibujar_grafica(x, y, nombre_func)


def lineal(funcion):
    grado = 1
    dominio = "Todos los números reales."
    rango = "Todos los números reales."
    coeficientes = leer_funcion(funcion, grado)
    derivada = derivar(coeficientes)
    x = corte_x(coeficientes, grado)
    y = corte_y(coeficientes)
    if derivada[0] > 0:
        monotonia = "Creciente ]-∞,+∞["
    else:
        monotonia = "Decreciente ]-∞,+∞["
    print()
    print(f"Dominio: {dominio}")
    print(f"Rango: {rango}")
    print(f"Monotonía: {monotonia}")
    print(f"Punto de corte en X: {x}")
    print(f"Punto de corte en Y: {y}")
    graficar_funcion(coeficientes, grado)
    return dominio, rango, monotonia, x, y

def cuadratica(funcion):
    grado = 2
    dominio = "Todos los números reales."
    coeficientes = leer_funcion(funcion, grado)
    derivada = derivar(coeficientes)
    extremo_x = corte_x(derivada, 1)
    extremo_y = ((extremo_x ** 2) * coeficientes[2]) + (extremo_x * coeficientes[1]) + coeficientes[0]
    x = corte_x(coeficientes, grado)
    y = corte_y(coeficientes)
    if derivada[1] < 0:
        monotonia = f"Creciente (-∞,{extremo_x}), Decreciente ({extremo_x},+∞)"
        rango = f"(-∞,{extremo_y}]"
    else:
        monotonia = f"Decreciente (-∞,{extremo_x}), Creciente ({extremo_x},+∞)"
        rango = f"(+∞,{extremo_y}]"
    print()
    print(f"Dominio: {dominio}")
    print(f"Rango: {rango}")
    print(f"Monotonía: {monotonia}")
    print(f"Punto de corte en X: {x}")
    print(f"Punto de corte en Y: {y}")
    graficar_funcion(coeficientes, grado)
    return dominio, rango, monotonia, x, y

def cubica(funcion):
    grado = 3
    dominio = "Todos los números reales."
    rango = "Todos los números reales."
    coeficientes = leer_funcion(funcion, grado)
    derivada = derivar(coeficientes)
    cortes_x = poly.polyroots(coeficientes) #La libreria numpy.polinomials es más moderna y acepta una lista de coeficientes en orden ascendente
    y = corte_y(coeficientes)
    print()
    print(f"Dominio: {dominio}")
    print(f"Rango: {rango}")
    print(f"Monotonía: {monotonia_cubica(derivada)}")
    for i, corte in enumerate(cortes_x, start=1):
        print(f"Punto de corte x{i}: {corte}")
    print(f"Punto de corte en Y: {y}")
    graficar_funcion(coeficientes, grado)
    return dominio, rango, cortes_x, y

# Menus

def menu_principal():
    while True:
        print()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print()
        print("Bienvenido a la calculadora. ¿Qué tipo de problema desea resolver?")
        print("1. Funciones Matemáticas")
        print("2. Sistemas de Ecuaciones 3x3")
        print("3. Salir")
        opcion = int(input("Ingrese su opción (1, 2, o 3): "))
        match opcion:
            case 1:
                menu_funciones()
            case 2:
                menu_sistemas()                
            case 3:
                print()
                print("Adiós...")
                return
            case _:
                print("Opción incorrecta. Por favor elija 1, 2, o 3.")

def menu_sistemas():
    while True:
        print()
        print("¿Qué método desea aplicar?")
        print("1. Método de Cramer")
        print("2. Método de Álgebra Matricial")
        print("3. Método de Gauss-Jordan")
        print("4. Volver al menú principal.")
        opcion = int(input("Ingrese su opción (1, 2, 3 o 4): "))
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
                return
            case _:
                print("Opción incorrecta. Por favor elija 1, 2, 3 o 4.")

def menu_funciones():
    while True:
        print()
        print("¿Qué tipo de función?")
        print("1. Lineal")
        print("2. Cuadrática")
        print("3. Cúbica")
        print("4. Volver al menú principal.")
        opcion = int(input("Ingrese su opción (1, 2, 3 o 4): "))
        match opcion:
            case 1:
                print("Funciones lineales")
                funcion = input("Ingrese una función lineal, ej: (2x+1) y = ")
                # if len(leer_funcion(funcion, 1)) > 2:
                #     raise ValueError("Función incorrecta")
                lineal(funcion)
            case 2:
                print("Funciones cuadráticas")
                cuadratica(input("Ingrese una función cuadrática, ej: (3x^2-2x+1) y = "))
            case 3:
                print("Funciones cúbicas")
                cubica(input("Ingrese una función cúbica, ej: (x^3-x^2-2x+1) y = "))
            case 4:
                return
            case _:
                print("Opción incorrecta. Por favor elija 1, 2, 3 o 4.")


menu_principal()
    
