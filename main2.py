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
from os import mkdir, chdir, path, listdir, remove
from time import time
from networkx import read_graphml

def main():
	chdir(sys.path[0])
	if not path.exists("./Saídas"):
		mkdir("Saídas")
	chdir("./Saídas")
	fileList = listdir("./")
	for file in fileList:
		remove("./"+file)

	""" entrada de dados (abrindo arquivos) """
	OrigemLoc = abrir_arquivo("../Entradas/locomotivas")
	Manobras = abrir_arquivo("../Entradas/manobras")
	''' opening graphml... only undirected graph '''
	layoutPatio = read_graphml("../Entradas/uvaranas.graphml")

	maxIterations = 50
	alpha = 1
	horizonteTempo = 360
	menorTempoAresta = 1

	Matriz = gerar_matriz_alocacao(list(layoutPatio.edges()), horizonteTempo, menorTempoAresta)

	""" criando grafo """
	# layoutPatio = nwx.Graph()
	# for elem in Enlaces:
	# 	layoutPatio.add_edge(elem[1], elem[2], weight = int(elem[3]), name = elem[0])

	for i in range(len(Manobras)):
		man = Manobras[i]
		man[1] = pega_par_nos(layoutPatio, man[1])
		man[2] = pega_par_nos(layoutPatio, man[2])
		Manobras[i] = man

	for i in range(len(OrigemLoc)):
		ol = pega_par_nos(layoutPatio, OrigemLoc[i][1])
		OrigemLoc[i] = (OrigemLoc[i][0], ol)

	solucao = construir_solucao(layoutPatio, Manobras, OrigemLoc, Matriz, horizonteTempo, menorTempoAresta, "1", alpha)
	m_solucao = solucao[:]

	i = 1
	while i < maxIterations:
		Matriz = gerar_matriz_alocacao(list(layoutPatio.edges()), horizonteTempo, menorTempoAresta)
		solucao = construir_solucao(layoutPatio, Manobras, OrigemLoc, Matriz, horizonteTempo, menorTempoAresta, str(i), alpha)
		i += 1
		# if solucao[1] < m_solucao[1]:
		# 	m_solucao = solucao[:]
	print("Tarefa concluída")
	return 0

if __name__ == '__main__':
	main()