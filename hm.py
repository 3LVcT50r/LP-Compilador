from __future__ import annotations

from antlr4 import *
from hmLexer import hmLexer
from hmParser import hmParser
from hmVisitor import hmVisitor

import streamlit as st
from dataclasses import dataclass
from pickle import dumps, loads
import pandas as pd
import string

######################################################################
#                           CLASES
######################################################################

# Excepcion para el error de tipo
class ErrorTipus(Exception):
    pass

# Excepcion para el error de las minusculas
class ErrorMinusculas(Exception):
    pass

# Excepcion para el error del numero de letras
class ErrorLetras(Exception):
    pass

# Creacion de la clase Arbre
class Buit:
    pass

@dataclass
class Node:
    val: str
    tip: [str]
    esq: Arbre
    dre: Arbre

Arbre = Node | Buit

######################################################################
#                           VISITORS
######################################################################


# Funcion que retorna el tipo segun el valor
# Funcion auxiliar para el tipusVisitor
counter = 0
def lookupTip(tip):
    global counter
    for i in auxtabla:
        if tip == i[0]:
            return i[1]
    aux = string.ascii_lowercase[counter]
    counter += 1
    if tip == 'λ':
        pass
    elif tip == '@':
        pass
    else:
        auxtabla.append((tip, aux))
    return aux


# Funcion que visita el arbol para decorarlo
def tipusVisitor(arb):
    if isinstance(arb, Buit):
        return
    
    arb.tip = lookupTip(arb.val)
    if arb.val in tabla_simbolos:
        tabla_simbolos[arb.val][1].append(arb)
    else:
        tablaInf.append(arb.tip)
        if arb.tip in tabla_simbolos:
            tabla_simbolos[arb.tip][1].append(arb)
        else:
            tabla_simbolos[arb.tip] = [[], [arb]]
    tipusVisitor(arb.esq)
    tipusVisitor(arb.dre)


# Parser para pasar de un tipo [] al Str
def parserTipo(tipoList):
    if (len(tipoList) == 1):
        return tipoList[0]
    else:
        tipoStr = "("
        iterador = 0
        for i in tipoList:
            if (iterador == 0):
                tipoStr += f"{i}"
            elif isinstance(i, list):
                tipoStr += " -> " + parserTipo(i)
            else:
                tipoStr += " -> " + f"{i}"
            iterador += 1
        tipoStr += ")"
        return tipoStr


# Funcion que calcula la inferencia de tipos
def inferenciaTipus(arb):
    if not isinstance(arb,  Buit):
        if arb.val == 'λ':
            inferenciaTipus(arb.esq)
            inferenciaTipus(arb.dre)

            tip_esq = arb.esq.tip
            tip_dre = arb.dre.tip

            if isinstance(tip_esq, list):
                aux = tip_esq.copy()
                aux.append(tip_dre)
                tabla_simbolos[arb.tip][0] = aux
                arb.tip = aux
            else:
                aux = tip_esq
                auxlist = [aux, tip_dre]
                tabla_simbolos[arb.tip][0] = auxlist
                arb.tip = auxlist
            
        elif arb.val == '@':
            # Recorrer el arbol bottom-up y ir comprobando
            inferenciaTipus(arb.esq)
            inferenciaTipus(arb.dre)
            
            if isinstance(arb.esq, Buit):
                raise ErrorTipus('Es imposible llegar aqui')

            tip_esq = arb.esq.tip
            tip_dre = arb.dre.tip
            tip_act = arb.tip
            
            if isinstance(tip_act, list):
                # Esto no deberia de ocurrir, pero por si acaso
                pass
            else:
                # Si los 2 son tipos validos -> COMPROBAR
                if isinstance(tip_esq, list) and isinstance(tip_dre, list):
                    # Si uno de los 2 es una lista vacia, lanzar excepcion
                    try:
                        if tip_esq[0] != tip_dre[0]:
                            raise ErrorTipus(f'{parserTipo(tip_esq[0])} vs {parserTipo(tip_dre[0])}')
                    except IndexError as e:
                        raise ErrorTipus('No suficientes funciones')

                    #Asignarle el tipo al actual
                    aux, *new_tip_act = tip_esq
                    if len(new_tip_act) == 0:
                        raise ErrorTipus(f'{parserTipo(aux)} vs {parserTipo(new_tip_act)}')
                    if len(new_tip_act) == 1 and isinstance(new_tip_act[0], list):
                        # print(new_tip_act[0])
                        new_tip_act = new_tip_act[0]

                    tabla_simbolos[tip_act][0] = new_tip_act
                    arb.tip = new_tip_act

                # Si el esq no es tipo valido
                elif isinstance(tip_dre, list):
                    aux = tip_dre.copy()
                    aux.append(tip_act)

                    # print(tip_act)
                    # printTable(tabla_simbolos)
                    tabla_simbolos[tip_esq][0] = aux


                    arb.esq.tip = tabla_simbolos[tip_esq][0]

                # Si el dre no es tipo valido
                elif isinstance(tip_esq, list):
                    aux, *new_tip_act = tip_esq
                    
                    if len(new_tip_act) == 0:
                        raise ErrorTipus(f'{parserTipo(aux)} vs {parserTipo(new_tip_act)}')
                    # Asignar valor a la derecha
                    tabla_simbolos[tip_dre][0] = [aux]

                    if len(tabla_simbolos[tip_dre][1]) > 1:
                        for i in tabla_simbolos[tip_dre][1]:
                            i.tip = [aux]

                    arb.dre.tip = [aux]

                    #Asignar valor al actual
                    if len(new_tip_act) == 1 and isinstance(new_tip_act[0], list):
                        new_tip_act = new_tip_act[0]
                    tabla_simbolos[tip_act][0] = new_tip_act
                    arb.tip = new_tip_act

                # Si ninguno es valido
                else:
                    tabla_simbolos[tip_esq][0] = [tip_dre, tip_act]

                    arb.esq.tip = tabla_simbolos[tip_esq][0]

        else:
            # No nos interesa quedarnos en las ojas o mas bien en las variables
            pass

        # dot_code = dibujar_grafo(arb)
        # st.graphviz_chart(dot_code)
        # print("------")
        # printTable(tabla_simbolos)



def arreglarTipos():
    cambios = True
    while cambios:
        cambios = False
        # Pasa por todas las keys
        for i_c in reversed(tabla_simbolos):
            cont = 0
            for j_c in tabla_simbolos[i_c][0]:
                if not isinstance(j_c,list) and j_c in string.ascii_lowercase:
                    cambios = True
                    if len(tabla_simbolos[j_c][0]) == 1:
                        tabla_simbolos[i_c][0][cont] = tabla_simbolos[j_c][0][0]
                    elif len(tabla_simbolos[j_c][0]) == 0:
                        cambios = False
                    else:
                        tabla_simbolos[i_c][0][cont] = tabla_simbolos[j_c][0]
                cont += 1
                
        
# Visitor y contructor del arbol / declaracio
class EvalVisitor(hmVisitor):
    def visitRoot(self, ctx):
        [expr] = list(ctx.getChildren())
        return self.visit(expr)

    def visitExprs(self, ctx):
        [expr, eof] = list(ctx.getChildren())
        return self.visit(expr)

    def visitDecla(self, ctx):
        [expr, eof] = list(ctx.getChildren())
        return self.visit(expr)

    def visitDecl(self, ctx):
        [var, aux, tipus] = list(ctx.getChildren())
        return (var.getText(), self.visit(tipus))

    def visitIdBasic(self, ctx):
        [tip] = list(ctx.getChildren())
        if tip.getText() in string.ascii_lowercase:
            raise ErrorMinusculas("")
        if len(tip.getText()) != 1:
            raise ErrorLetras("")
        return [tip.getText()]

    def visitIdComplex(self, ctx):
        [tip1, aux, tip2] = list(ctx.getChildren())
        if tip1.getText() in string.ascii_lowercase:
            raise ErrorMinusculas("")
        if len(tip1.getText()) != 1:
            raise ErrorLetras("")
        lista = [tip1.getText()]
        lista.extend(self.visit(tip2))
        return lista

    def visitParentesis(self, ctx):
        [aux1, expr, aux2] = list(ctx.getChildren())
        return self.visit(expr)

    def visitIdVal(self, ctx):
        [expr] = list(ctx.getChildren())
        return self.visit(expr)

    def visitNumVal(self, ctx):
        [expr] = list(ctx.getChildren())
        return self.visit(expr)

    def visitId(self, ctx):
        [id] = list(ctx.getChildren())
        return Node(id.getText(), [], Buit(), Buit())

    def visitNum(self, ctx):
        [val] = list(ctx.getChildren())
        return Node(val.getText(), [], Buit(), Buit())

    def visitLambdaDecl(self, ctx):
        [expr] = list(ctx.getChildren())
        return self.visit(expr)

    def visitLambdaFunc(self, ctx):
        [aux1, id, aux2, expr] = list(ctx.getChildren())
        return Node("λ", [], self.visit(id), self.visit(expr))

    def visitAplicacio(self, ctx):
        [expr1, expr2] = list(ctx.getChildren())
        return Node("@", [], self.visit(expr1), self.visit(expr2))


######################################################################
#               Funciones de escritura y copia
######################################################################

# Funcion para copiar una la tabla del estado
def ini_auxtabla():
    lista = []
    for i in estado.tabla:
        lista.append(i)
    return lista


# Funcion que inicializa la tabla de simbolos
def ini_tabla_simbolos():
    tabla_s = {}
    for i in estado.tabla:
        tabla_s[i[0]] = [i[1], []]
    return tabla_s


# Funcion que hace la tabla final de inferencia
def ini_tabla_Inf():
    tabla_s = []
    for i in tablaInf:
        if len(tabla_simbolos[i][0]) == 0:
            aux = (i,i)
            tabla_s.append(aux)
        else:
            aux = (i, parserTipo(tabla_simbolos[i][0]))
            tabla_s.append(aux)
    return set(tabla_s)


# Dibujar grafo
def dibujar_grafo(arbre):
    dot_code = ""

    def recorrer_arbol(nodo):
        nonlocal dot_code
        if isinstance(nodo, Buit):
            return

        dot_code += f'    {id(nodo)} [label="{nodo.val}\n{parserTipo(nodo.tip)}"];\n'

        if isinstance(nodo.esq, Node):
            dot_code += f'    {id(nodo)} -> {id(nodo.esq)};\n'
            recorrer_arbol(nodo.esq)

        if isinstance(nodo.dre, Node):
            dot_code += f'    {id(nodo)} -> {id(nodo.dre)};\n'
            recorrer_arbol(nodo.dre)

    recorrer_arbol(arbre)
    dot_code = "digraph G {\n" + dot_code + "}"
    return dot_code


# Parser para pasar de la tabla del estado a la tabla de la interficie
def parserTabla(tabla):
    nueva_tabla = []
    if isinstance(tabla, list):
        for i in tabla:
            aux = (i[0], parserTipo(i[1]))
            nueva_tabla.append(aux)
        df = pd.DataFrame(nueva_tabla, columns=["", "Tipus"])

    return df


######################################################################
#                           DEBUG
######################################################################

# DEBUG FUNCTION
# Funcion que printea la tabla de simbolos sin las dependencias
def printTable(table):
    for i,j in table.items():
        print(f'{i} :: {j[0]}')


# DEBUG FUNCTION
# Función para imprimir el árbol binario
def imprimir_arbol(raiz, prefijo='', es_ultimo=True):
    print(prefijo, '|- ', raiz.val, ' ', raiz.tip, sep='')

    prefijo += '    ' if es_ultimo else '|   '

    if not isinstance(raiz.esq, Buit):
        imprimir_arbol(raiz.esq, prefijo, False)
    if not isinstance(raiz.dre, Buit):
        imprimir_arbol(raiz.dre, prefijo, True)

######################################################################
#                           MAIN
######################################################################

# MAIN
estado = st.session_state

if not estado.get('tabla'):
    estado.tabla = [
    ("2", ["N"]),
    ("(+)", ["N", "N", "N"])
    ]

# Por cada variable, hay una tupla (tipo, lista de nodos)     
tabla_simbolos = ini_tabla_simbolos()

st.title("Calculadora d'expresions Haskell")

input = st.text_input("Escriu l'expressió")
if st.button("fer"):
    input_stream = InputStream(input)

    lexer = hmLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = hmParser(token_stream)
    tree = parser.root()

    if parser.getNumberOfSyntaxErrors() == 0:
        visitor = EvalVisitor()
        try:
            arb = visitor.visit(tree)
            tablaInf = []

            # Dibujar grafo
            if isinstance(arb, Node):
                auxtabla = ini_auxtabla()
                tipusVisitor(arb)

                dot_code = dibujar_grafo(arb)
                st.graphviz_chart(dot_code)
                
                try:    
                    arbTip = arb
                    inferenciaTipus(arbTip)
                    # dot_code = dibujar_grafo(arbTip)
                    # st.graphviz_chart(dot_code)
                    arreglarTipos()


                    dot_code = dibujar_grafo(arbTip)
                    st.graphviz_chart(dot_code)

                    st.table(ini_tabla_Inf())
                except ErrorTipus as e:
                    st.write("Type error: ", str(e))

                # printTable(tabla_simbolos)

            # Hacer cosas con los tipos
            else:
                estado.tabla.append(arb)
                tabla_simbolos[arb[0]] = [arb[1], []]

        except ErrorMinusculas as e:
            st.write("Los tipos solo pueden contenter un letra en Mayusculas")
        except ErrorLetras as e:
            st.write("Los tipos solo pueden contenter una letra")


    else:
        st.write("Error de sintaxis")
        st.write(tree.toStringTree(recog=parser))

    st.write(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')

st.table(parserTabla(estado.tabla))
