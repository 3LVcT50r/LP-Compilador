# HinNer

Este es el readme del proyecto de LP "HinNer".

Este programa consiste en el interprete de una expresión tipo Haskell.

Programa hecho para la asignatura de LP del grado de Ingeniería Informática 
en la FIB.

## Qué es HinNer?

Este programa consiste en un pequeño interprete de expresiones tipo Haskell, 
como por ejemplo:

    2 
    x
    (+) 2 x 
    \x -> (+) 2 x

También es capaz de reconocer variables y gestionar variables con tipos, por
ejemplo:

    2 :: N 
    (+) :: N -> N -> N

Estas varibles se guardarán y se usarán para la inferencia de tipos al
utilizarlas en una expresión de arriba.

También, hay una tabla en la parte inferior de la página que muestra la 
cantidad de variables declaradas con su respectivo tipo.

Al escribir una expresión, se generará un árbol semántico que representa la 
expresión, donde en la parte superior de cada nodo se verá el nombre de la 
variable , un @ o una lambda dependiendo de si es una aplicación o una
abstracción. En la parte inferior se verá el tipo inicial del nodo, donde puede
ser un tipo declarado, si la variable ya estaba declarada, o una letra
minúscula, si la variable no está declarada o es una aplicación o abstracción.

Después se generará un nuevo arbol, con los tipos inferidos correctamente según 
la expresión y una tabla con cada asignación de los tipos desconocidos
previamente con el tipo inferido.

## Instrucciones de uso

### Instalación

Para usar el interprete es necesario tener las librerias:

- Python3
- Antlr4
- Antlr4 tools para python 
- Streamlit

Para Antlr es recomendable usar la versión más nueva posible, siendo exactos
la versión 4.13.1

### Uso del interprete

Para el uso del interprete se tendrá que poner una expresión correcta 
gramaticalmente hablando, sino saltará un mensaje de error.

Para el uso de la declaración de variables, los tipos solo pueden ser mayusculas.
Para el nombre de la variable no importa.


## Juegos de pruebas

A parte de los juegos de pruebas ya dados por el enunciado, algunos juegos
curiosos a probar son:

1o- Este juego de pruebas prueba la ejecución de una expresión donde no hay 
casi variables declaradas, y el árbol de inferencia debería de estar casi
repleto de letras

    (*) ((+) 2 x) ((-) 3 y)

2o- Este juego de pruebas prueba la inferencia de una expresión con una doble 
abstracción.

    \x -> \y -> (+) ((+) 2 x) ((-) 2 y)

3o- Este juego de pruebas prueba lo que ocurre cuando una abstraccion esta 
dentro de una aplicacion.

    (+) ((\x -> (+) 2 x) 2) 2






















