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

	maxIterationParameter = [50, 100, 200, 500]
	alphaParameter = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
	horizonteTempo = 360
	menorTempoAresta = 1


	for i in range(len(Manobras)):
		man = Manobras[i]
		man[1] = pega_par_nos(layoutPatio, man[1])
		man[2] = pega_par_nos(layoutPatio, man[2])
		Manobras[i] = man
	nomeLocomotivas = []
	for i in range(len(OrigemLoc)):
		ol = pega_par_nos(layoutPatio, OrigemLoc[i][1])
		OrigemLoc[i] = (OrigemLoc[i][0], ol)
		nomeLocomotivas.append(OrigemLoc[i][0])
	results = {}
	for maxI in maxIterationParameter:
		for alpha in alphaParameter:
			for j in range(1000):
				Matriz = gerar_matriz_alocacao(list(layoutPatio.edges()), horizonteTempo, menorTempoAresta)
				construir_solucao(layoutPatio, Manobras, OrigemLoc, Matriz, horizonteTempo, menorTempoAresta, "1", alpha)
				melhorSolucao = Matriz.copy()
				melhorTempoMaior, melhorTempoMenor, melhorTempoMaior = avaliadorSolucao(melhorSolucao, nomeLocomotivas)
				aux = melhorTempoMaior

				i = 1
				while i < maxI:
					Matriz = gerar_matriz_alocacao(list(layoutPatio.edges()), horizonteTempo, menorTempoAresta)
					construir_solucao(layoutPatio, Manobras, OrigemLoc, Matriz, horizonteTempo, menorTempoAresta, str(i), alpha)
					tempoMedio, tempoMenor, tempoMaior = avaliadorSolucao(Matriz, nomeLocomotivas)

					if tempoMaior < melhorTempoMaior:
						melhorSolucao = Matriz.copy()
						melhorTempoMaior = tempoMaior
					i += 1
				if (maxI,alpha) in results:
					results[(maxI,alpha)].append((aux, melhorTempoMaior))
				else:
					results[(maxI,alpha)] = [(aux, melhorTempoMaior)]
				print("m", maxI, "a", alpha, "nRes", j + 1)
	imprime_dic_arquivo(results, "./results5")
	print("Tarefa concluída")
	return 0

if __name__ == '__main__':
	main()