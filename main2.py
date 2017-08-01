#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2016 GPRC2-LMA <GPRC2-LMA@GPRC2-LMA-PC>

import networkx as nwx
import sys
from  functions_in_out import *
from functions2 import *
from graspv2 import *
from os import mkdir, chdir, path
from time import time

def main():

	""" entrada de dados (abrindo arquivos) """
	chdir(sys.path[0])
	if not path.exists("./Saídas"):
		mkdir("Saídas")
	Enlaces = abrir_arquivo("./Entradas/enlaces")
	OrigemLoc = abrir_arquivo("./Entradas/locomotivas")
	Manobras = abrir_arquivo("./Entradas/manobras")
	
	chdir("./Saídas")	

	""" criando grafo """
	layoutPatio = nwx.Graph()
	for elem in Enlaces:
		layoutPatio.add_edge(elem[1], elem[2], weight = int(elem[3]), name = elem[0])

	for i in range(len(Manobras)):
		man = Manobras[i]
		man[1] = pega_par_nos(layoutPatio, man[1])
		man[2] = pega_par_nos(layoutPatio, man[2])
		Manobras[i] = man
	
	for i in range(len(OrigemLoc)):
		ol = pega_par_nos(layoutPatio, OrigemLoc[i][1])
		OrigemLoc[i] = (OrigemLoc[i][0], ol)
	
	del(Enlaces)
	
	horizonteTempo = 20
	menorTempoAresta = 1
	
	Matriz = gerar_matriz_alocacao(list(layoutPatio.edges()), horizonteTempo, menorTempoAresta)
	ini = time()

	solucao = construir_solucao(layoutPatio, Manobras, OrigemLoc, Matriz, horizonteTempo, menorTempoAresta, "1")

	m_solucao = solucao[:]
	
	i = 1
	while i <= 2:
		Matriz = gerar_matriz_alocacao(list(layoutPatio.edges()), horizonteTempo, menorTempoAresta)
		solucao = construir_solucao(layoutPatio, Manobras, OrigemLoc, Matriz, horizonteTempo, menorTempoAresta, str(i))
		
		i += 1
		# if solucao[1] < m_solucao[1]:
		# 	m_solucao = solucao[:]
	print("Tarefa concluída")
	return 0

if __name__ == '__main__':
	main()