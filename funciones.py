import matplotlib.pyplot as plt # Para gráficas
import numpy as np # Para puntos de corte de función cúbica
import math # Para sacar raíz cuadrada para fórmula general
import numpy.polynomial.polynomial as poly # Para función cúbica

# Algebra:

def determinante_cero(determinante):
    return determinante == 0

def validar_numero(ingreso): # Valida que no se ingresen datos que no sean números
    while True:
        try:
            return float(input(ingreso))
        except ValueError:
            print("Por favor, ingrese un número válido.")

def matriz_vacia(filas, columnas): # Genera matriz vacía de filas x columnas
    return [[0 for _ in range(columnas)] for _ in range(filas)]

def float_a_entero(numero): # Para facilitar la lectura, si el número no es fraccionario
    if isinstance(numero, float) and numero.is_integer():
        return int(numero)
    return numero

# def ImprimirMatriz(matriz, paso=""): # Recibe una matriz, y opcionalemente imprime paso
#     print(f"\n{paso}")
#     print()
#     ancho = max(len(f"{j:.2f}") for i in matriz for j in i) # Aumenta el ancho de las columnas de acuerdo al ancho del término mas grande, para mejorar presentación
#     for i in matriz:
#         for j in i:
#             print(f"{j:{ancho}.2f}", end="  ") # Formato para números
#         print()

def ImprimirMatriz(matriz, paso="", precision=2): # Tomado de la implementación de Said Navarrete, con modificaciones
    filas = len(matriz)
    columnas = len(matriz[0])
    
    # Formato dinámico
    formato = f"{{:>7.{precision}f}}"

    print(f"\n{paso}")
    print()
    
    # Imprimir borde superior
    print("┌" + "───────" * columnas + "┐")
    
    # Imprimir filas
    for fila in matriz:
        print("│", end="")
        print(" ".join(formato.format(valor) for valor in fila), end="")
        print(" │")
    
    # Borde inferior
    print("└" + "───────" * columnas + "┘")

def CuadradaONo(matriz):
    return len(matriz) == len(matriz[0])

def determinante_matriz(matriz): # Utilizando el metodo de Laplace, toma una matriz y entrega el determinante de la misma
    if not CuadradaONo(matriz):
        raise ValueError("La matriz no es cuadrada (filas != columnas)") # Validación de errores
        return None       
    else:
        if len(matriz) == 1: # Si la matriz es 1x1 su determinante es el único término
            return matriz[0][0]

        if len(matriz) == 2:
            determinante = matriz[0][0] * matriz[1][1] - matriz[1][0] * matriz[0][1] # Si es matriz 2x2 multiplica y resta en cruz
            return determinante
            
        # Recursivo, si la matriz es mayor a 2x2
        determinante = 0
        for j in range(len(matriz)):
            submatriz = [fila[:j] + fila[j+1:] for fila in matriz[1:]] # Utiliza la primera fila y crea subfactores para proceder con el método de laplace    
            
            cofactor = matriz[0][j] * determinante_matriz(submatriz) * (-1) ** j # Para cambiar los signos de los cofactores multiplica por -1 elevado al índice de la columna
            determinante += cofactor

        return determinante
        
def llenar_sistema(): # Hace que el usuario llene una matriz 3x4 que representa un sistema de ecuaciones 3x3
    print("Ingrese los datos del sistema de ecuaciones 3x3.")
    matriz = matriz_vacia(3, 4)
    for i in range(len(matriz)):
        print(f"Ingrese los valores de la ecuación {i+1}:")
        for j in range(len(matriz[0])):
            if j == len(matriz[0]) - 1:
                valor = float(validar_numero(f"Ingrese el valor independiente: "))
            else:
                valor = float(validar_numero(f"Ingrese el coeficiente de la variable {j+1}: "))
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

    return matrices[0], matrices[1], matrices[2] # Genera las matrices modificadas Ax, Ay, y Az

def terminos_indep(matriz): # Para generar la matriz de términos independientes de una matriz 3x4 (la última columna solamente)
    if not len(matriz) == 3 or not len(matriz[0]) == 4:
        raise ValueError("No es una matriz 3x4")
    else:
        m_indep = matriz_vacia(len(matriz),1)
        for i in range(len(m_indep)):
                for j in range(len(m_indep[0])):
                    m_indep[i][j] = matriz[i][3] # El índice 3 corresponde a la columna 4 (la última)
        return m_indep

def matriz_coeficientes(matriz): # Genera la matriz regular "A" descartando los términos independientes
    if not len(matriz) == 3 or not len(matriz[0]) == 4:
        raise ValueError("No es una matriz 3x4")
    else:
        matrizA = matriz_vacia(3,3)
        for i in range(len(matrizA)):
            for j in range(len(matrizA[0])):
                matrizA[i][j] = matriz[i][j]
        return matrizA

def cramer(matriz): # Aplica la resolución del sistema por el método de cramer
    try:
        matrices_mod = matrices_modificadas(matriz) # Crea las matrices en una lista
        etiquetas = ["Ax", "Ay", "Az"] # Para presentación
        ImprimirMatriz(matriz, "Matriz extendida del sistema")
        for i, m in enumerate(matrices_mod):
            ImprimirMatriz(m, f"Matriz modificada {etiquetas[i]}") # Imprime cada matriz modificada utilizando las etiquetas creadas
        
        matriz_coef = matriz_coeficientes(matriz)
        ImprimirMatriz(matriz_coef, "Matriz de coeficientes A") # Imprime la matriz de coeficientes "A"

        determinantes = [float_a_entero(determinante_matriz(m)) for m in matrices_mod] # Genera una lista de los determinantes de cada matriz modificada
        det_A = float_a_entero(determinante_matriz(matriz_coef)) # Determinante de la matriz A
        print()
        for i, etiqueta in enumerate(etiquetas):
            print(f"Determinante {etiqueta}: {determinantes[i]}") # Imprime los determinantes para el usuario
        
        print(f"Determinante A: {det_A}")
        
        if det_A == 0:
            raise ValueError("El sistema no tiene solución única (determinante de coeficientes es cero)") # Para evitar error de division por 0
        else: 
            x, y, z = (float_a_entero(det_i / det_A) for det_i in determinantes) # Divide el determinante de cada matriz modificada, por el determinante de la matriz A
            print()
            print("Soluciones: ")
            print()
            print(f"X: {x}")
            print(f"Y: {y}")
            print(f"Z: {z}")
            print()
            
            return x,y,z
    except ValueError as e:
        print(f"Error: {e}")
        return None


def transponer_matriz(matriz): # Cambia filas por columnas
    return [[matriz[j][i] for j in range(len(matriz))] for i in range(len(matriz[0]))]

def cofactor_matriz(matriz): # Genera la matriz de cofactores necesaria para obtener la matriz adjunta
    n = len(matriz)
    cofactor = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatriz = [row[:j] + row[j+1:] for row in (matriz[:i] + matriz[i+1:])]
            cofactor[i][j] = ((-1) ** (i+j)) * determinante_matriz(submatriz)
    return cofactor

def matriz_adjunta(matriz): # Toma una matriz, genera la matriz de cofactores, y finalmente la transpone
    cofactor = cofactor_matriz(matriz)
    return transponer_matriz(cofactor)

def multiplicacion_posible(matrizA, matrizB): # Revisa que dos matrices puedan ser multiplicadas para prevenir errores
    return len(matrizA[0]) == len(matrizB)

def multiplicacion_matrices(matrizA, matrizB): # Multiplica dos matrices
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

def multiplicacion_escalar(numero, matriz): # Multiplica un número escalar, por una matriz (cada elemento de la matriz se multiplica por el escalar)
    resultado = matriz_vacia(len(matriz),len(matriz[0]))
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            resultado[i][j] = numero * matriz[i][j]
    return resultado

def algebra_matricial(matriz): # Aplica la resolución del sistema con el método de álgebra lineal de matrices
    matriz_base = matriz_coeficientes(matriz) # Matriz A
    independientes = terminos_indep(matriz) # Matriz 3x1 de términos independientes
    det_coeficientes = determinante_matriz(matriz_base) # Determinante de A
    if determinante_cero(det_coeficientes):
        # raise ValueError("El sistema no tiene solución única (determinante de coeficientes es cero)") # Para evitar error de division por 0
        print("El sistema no tiene solución única (determinante de coeficientes es cero)")
        return None
    else:
        det_fraccionaria = 1 / determinante_matriz(matriz_base) # Convierte al determinante de A en un número fraccionario para utilizar la multiplicación escalar
        resultado = multiplicacion_matrices(matriz_adjunta(matriz_base), independientes) # Multiplica la matriz adjunta y transpuesta de A, por la matriz de términos independientes
        resultado = multiplicacion_escalar(det_fraccionaria, resultado) # Multiplica el resultado por el determinante fraccionario para obtener las soluciones del sistema
        x = float_a_entero(resultado[0][0])
        y = float_a_entero(resultado[1][0])
        z = float_a_entero(resultado[2][0])
        ImprimirMatriz(matriz, "Matriz extendida del sistema") # Para comunicar el procedimiento al usuario
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


def volver_uno(matriz, pivote): # Convierte al pivote (elemento de la diagonal principal) en 1 dividiendolo para si mismo, y divide al resto de elementos de la fila por el mismo término
    col = len(matriz[0])
    if matriz[pivote][pivote] == 0:
        raise ValueError("No se puede dividir para 0")

    divisor = matriz[pivote][pivote]
    for j in range(col):
        matriz[pivote][j] /= divisor
    ImprimirMatriz(matriz, f"Después de volver 1 el pivote en la fila {pivote + 1}") # Imprime la matriz resultante después de convertir al pivote en 1
    

def volver_cero(matriz, fila, columna): # Convierte a los elementos que no son pivote en 0 al restarlos por sí mismos
    col = len(matriz[0])
    if matriz[fila][columna] != 0:
        multiplicando = matriz[fila][columna]
        for j in range(col):
            matriz[fila][j] -= multiplicando * matriz[columna][j]
    ImprimirMatriz(matriz, f"Después de volver 0 el elemento en la fila {fila + 1}, columna {columna + 1}")


def gauss_jordan(matriz): # Aplica la resolución del sistema utilizando el método de Gauss-Jordan
    n = len(matriz)
    ImprimirMatriz(matriz, "Matriz extendida del sistema")
    for i in range(n):
        # Encontrar el pivote
        elemento_max = abs(matriz[i][i]) # Busca al número mayor de una columna para evitar que hayan ceros en la diagonal principal
        fila_max = i
        for k in range(i + 1, n):
            if abs(matriz[k][i]) > elemento_max:
                elemento_max = abs(matriz[k][i])
                fila_max = k

        # Intercambiar filas
        if fila_max != i:
            matriz[i], matriz[fila_max] = matriz[fila_max], matriz[i]
            ImprimirMatriz(matriz, f"Después de intercambiar la fila {i + 1} con la fila {fila_max + 1}") # Informa al usuario de cada paso realizado.

        volver_uno(matriz, i)

        for j in range(n):
            if i != j:
                volver_cero(matriz, j, i)

    resultado = terminos_indep(matriz)
    ImprimirMatriz(resultado, "Soluciones:")
    print()

    
    return matriz

# Matematicas:

def leer_funcion(funcion, tipo): # Convierte una función ingresada como string a una lista de coeficientes en orden ascendiente (primer elemento es independiente, segundo corresponde a x^1, tercero a x^2, y cuarto a x^3)
    try:
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
    except ValueError:
        print("Función no válida. Por favor, ingrese una función válida.")
        return None

def derivar(coeficientes): # Calcula la derivada de una función polinómica
    derivada = [0] * len(coeficientes)
    for i in range(1, len(coeficientes)):
        derivada[i-1] = coeficientes[i] * i # Multiplica al coeficiente por el índice que corresponde a su exponente
    return derivada

def corte_y(coeficientes): # El punto de corte en y es el término independiente, por lo cual se accesa directamente
    return coeficientes[0]

def corte_x(coeficientes, grado): # Encuentra los puntos de corte utilizando fórmulas
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

def monotonia_cubica(derivada): # Por complejidad, para las ecuaciones cúbicas se utiliza una función separada para determinar los intervalos de monotonía
    c,b,a,d = derivada # Asigna los coeficientes de la derivada a términos para aplicar la función general
    discriminante = b**2 - 4 * a * c

    if discriminante > 0:
        # Dos puntos criticos
        x1 = (-b + np.sqrt(discriminante)) / (2 * a)
        x2 = (-b - np.sqrt(discriminante)) / (2 * a)
        puntos_criticos = [x1, x2]
    elif discriminante == 0:
        # Un solo punto critico
        x = -b / (2 * a)
        puntos_criticos = [x]
    else:
        # No existen puntos críticos reales, la función es solamente creciente o decreciente.
        puntos_criticos = []

    if a > 0:
        return "Creciente en los intervalos (-∞, {1}) y ({0}, +∞) , Decreciente en ({1}, {0})".format(*puntos_criticos) if len(puntos_criticos) == 2 else "Creciente en (-∞, +∞)"
    elif a < 0:
        return "Decreciente en los intervalos (-∞, {1}) y ({0}, +∞) , Creciente en ({1}, {0})".format(*puntos_criticos) if len(puntos_criticos) == 2 else "Decreciente en (-∞, +∞)"


def etiquetar_func(coeficientes, grado): # Genera un string para poder etiquetar la función en la gráfica, así como las variables para matplotlib
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

def dibujar_grafica(x, y, nombre_func): # Utiliza matplotlib para realizar el gráfico
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


def graficar_funcion(coeficientes, grado): # Genera los datos de la función y llama a dibujar_gráfica
    if grado == 1:
        x, y, nombre_func = etiquetar_func(coeficientes, grado)
        dibujar_grafica(x, y, nombre_func)
    elif grado == 2:
        x, y, nombre_func = etiquetar_func(coeficientes, grado)
        dibujar_grafica(x, y, nombre_func)
    elif grado == 3:
        x, y, nombre_func = etiquetar_func(coeficientes, grado)
        dibujar_grafica(x, y, nombre_func)


def lineal(funcion): # Obtiene los valores de las funciones lineales
    grado = 1
    dominio = "Todos los números reales."
    rango = "Todos los números reales."
    coeficientes = leer_funcion(funcion, grado)
    derivada = derivar(coeficientes)
    x = corte_x(coeficientes, grado)
    y = corte_y(coeficientes)
    if derivada[0] > 0: # Simplemente analiza el término independiente en la derivada para determinar si es creciente o decreciente
        monotonia = "Creciente (-∞,+∞)"
    else:
        monotonia = "Decreciente (-∞,+∞)"
    print()
    print(f"Dominio: {dominio}")
    print(f"Rango: {rango}")
    print(f"Monotonía: {monotonia}")
    print(f"Punto de corte en X: {x}")
    print(f"Punto de corte en Y: {y}")
    graficar_funcion(coeficientes, grado)
    return dominio, rango, monotonia, x, y

def cuadratica(funcion): # Obtiene los valores de las funciones lineales
    grado = 2
    dominio = "Todos los números reales."
    coeficientes = leer_funcion(funcion, grado)
    derivada = derivar(coeficientes)
    extremo_x = corte_x(derivada, 1) # Para poder determinar el rango, sacamos el punto de corte de la derivada que corresponde al extremo
    extremo_y = ((extremo_x ** 2) * coeficientes[2]) + (extremo_x * coeficientes[1]) + coeficientes[0] # Con el extremo de x, reemplazamos y sacamos el punto extremo en y
    x = corte_x(coeficientes, grado)
    y = corte_y(coeficientes)
    if derivada[1] < 0: # Analizando el coeficiente de x^1 en la derivada y utilizando los puntos extremos que determinamos antes
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

def cubica(funcion): # Obtiene los valores de las funciones cúbicas
    grado = 3
    dominio = "Todos los números reales."
    rango = "Todos los números reales."
    coeficientes = leer_funcion(funcion, grado)
    derivada = derivar(coeficientes)
    cortes_x = poly.polyroots(coeficientes) #La libreria numpy.polinomials es más moderna y acepta una lista de coeficientes en orden ascendente
    y = corte_y(coeficientes) # No es necesario una librería para los cortes en y porque siguen correspondiendo al coeficiente independiente
    print()
    print(f"Dominio: {dominio}")
    print(f"Rango: {rango}")
    print(f"Monotonía: {monotonia_cubica(derivada)}") # Llama a la función de monotonía cúbica antes definida para obtener los intervalos
    for i, corte in enumerate(cortes_x, start=1):
        print(f"Punto de corte x{i}: {corte}")
    print(f"Punto de corte en Y: {y}")
    graficar_funcion(coeficientes, grado)
    return dominio, rango, cortes_x, y

# Menus

def menu_principal():
    while True:
        print()
        print("┌" + "───────" * 4 + "┐")
        print()
        print("Bienvenido a la calculadora. ¿Qué tipo de problema desea resolver?")
        print("1. Funciones Matemáticas")
        print("2. Sistemas de Ecuaciones 3x3")
        print("3. Salir")
        print("└" + "───────" * 4 + "┘")
        opcion = input("Ingrese su opción (1, 2, o 3): ")
        match opcion:
            case "1":
                menu_funciones()
            case "2":
                menu_sistemas()                
            case "3":
                print()
                print("Adiós...")
                return
            case _:
                print()
                print("Opción incorrecta. Por favor elija 1, 2, o 3.")

def menu_sistemas():
    while True:
        print()
        print("┌" + "───────" * 4 + "┐")
        print()
        print("¿Qué método desea aplicar?")
        print("1. Método de Cramer")
        print("2. Método de Álgebra Matricial")
        print("3. Método de Gauss-Jordan")
        print("4. Volver al menú principal.")
        print("└" + "───────" * 4 + "┘")
        opcion = input("Ingrese su opción (1, 2, 3 o 4): ")
        match opcion:
            case "1":
                print("Método de Cramer")
                cramer(llenar_sistema())
            case "2":
                print("Método de Álgebra Matricial")
                algebra_matricial(llenar_sistema())
            case "3":
                print("Método de Gauss-Jordan")
                gauss_jordan(llenar_sistema())
            case "4":
                return
            case _:
                print("Opción incorrecta. Por favor elija 1, 2, 3 o 4.")

def menu_funciones():
    while True:
        print()
        print("┌" + "───────" * 4 + "┐")
        print()
        print("¿Qué tipo de función?")
        print("1. Lineal")
        print("2. Cuadrática")
        print("3. Cúbica")
        print("4. Volver al menú principal.")
        print("└" + "───────" * 4 + "┘")
        opcion = input("Ingrese su opción (1, 2, 3 o 4): ")
        match opcion:
            case "1":
                print("Funciones lineales")
                funcion = input("Ingrese una función lineal, ej: (2x+1) y = ")
                coeficientes = leer_funcion(funcion, 1)
                if coeficientes is None or len(coeficientes) != 2:
                    print("Función lineal no válida.")
                else:
                    lineal(funcion)
            case "2":
                print("Funciones cuadráticas")
                funcion = input("Ingrese una función cuadrática, ej: (3x^2-2x+1) y = ")
                coeficientes = leer_funcion(funcion, 2)
                if coeficientes is None or len(coeficientes) != 3:
                    print("Función cuadratica no válida.")
                elif coeficientes[2] == 0:  # Confirma que sea una función cuadrática
                    print("No es una función cuadrática, parece ser una función lineal.")
                else:
                    cuadratica(funcion)
            case "3":
                print("Funciones cúbicas")
                funcion = input("Ingrese una función cúbica, ej: (x^3+2x^2+x+-5) y = ")
                coeficientes = leer_funcion(funcion, 3)
                if coeficientes is None or len(coeficientes) != 4:
                    print("Función cubica no válida.")
                elif coeficientes[3] == 0:  # Confirma que sea una función lineal
                    print("No es una función cúbica, parece ser una función de menor grado.")
                else:
                    cubica(funcion)
            case "4":
                return
            case _:
                print("Opción incorrecta. Por favor elija 1, 2, 3 o 4.")


menu_principal()
    
