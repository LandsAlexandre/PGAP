#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  functions.py
#  
#  Copyright 2016 GPRC2-LMA <GPRC2-LMA@GPRC2-LMA-PC>

import networkx as nwx
class ExceptionLinhaOcupada(Exception):
	# EXCEÇÂO -> ocorre quando uma locomot
	# tenta ocupar uma linha ja ocupada #
	def __init__(self):
		super(ExceptionLinhaOcupada, self).__init__("O trem bateu, pois a linha está ocupada!")

def pega_par_nos(grafo, nome_linha):
	for elem in grafo.edges():
		if grafo[elem[0]][elem[1]]["id"] == nome_linha:
			if int(elem[0][1:]) > int(elem[1][1:]):
				""" padronizando saida """
				return (elem[1], elem[0])
			return tuple(elem)

def gerar_matriz_alocacao (lstLinhas, intTempo, intMenorTempo):
	matriz_alocacao = {}
	for i in range (len(lstLinhas)):
		instantes_linha = []
		j = 0
		while j <= (intTempo//intMenorTempo):
			instantes_linha.append("0")
			j += 1
		matriz_alocacao[lstLinhas[i]] = instantes_linha
	return matriz_alocacao

def checarLinha (nwxGrafo, tupLinha, dic_lstMatriz, intTempoAtual, intdelta_tempo):
	# retorna False se a linha
	# estiver ocupada e True caso contrario
	result = True
	i = 0
	instante_atual = intTempoAtual//intdelta_tempo
	custo = nwxGrafo[tupLinha[0]][tupLinha[1]]["weight"]
	x=0
	while x < (custo/intdelta_tempo):
		if dic_lstMatriz[tupLinha][instante_atual+x] != "0":
			result = result and False
		x += 1
	return result

def checarLinhaPorInstante (matriz, linha, instanteInicio, instanteFim):
	# matriz ->  {("Ni","Nj"):[0,1,2,3,...],...}
	# linha -> ("Ni","Nj")
	# instanteInicio/instanteFim -> inteiro

	result = True
	if linha not in matriz.keys():
		linha = (linha[1],linha[0])
	i = instanteInicio
	while i < instanteFim and result:
		if matriz[linha][i] != "0":
			result = result and False
		i += 1
	return result

def alocarLinha (matriz, linha, locomotiva, instanteInicio, instanteFim):
	# matriz ->  {("Ni","Nj"):[0,1,2,3,...],...}
	# linha -> ("Ni","Nj")
	# locomotiva -> "LMx"
	# instanteInicio/instanteFim -> inteiro
	if checarLinhaPorInstante(matriz, linha, instanteInicio, instanteFim):
		a = linha
		if a not in matriz.keys():
			a = (linha[1], linha[0])
		for i in range (instanteInicio, instanteFim, 1):
			matriz[a][i] = locomotiva
	else:
		raise ExceptionLinhaOcupada

def encontrarProximoIntervaloDisponivel(matriz, linha, instanteInicio, instanteFim):
	while not checarLinhaPorInstante(matriz, linha, instanteInicio, instanteFim):
		instanteInicio += 1
		instanteFim += 1
	return (instanteInicio, instanteFim)

def delLinhaRepedtida(tupLinha, caminho):
	tupPrimeiraLinhaCaminho = tuple(caminho[0:2])
	if tupLinha == tupPrimeiraLinhaCaminho or (tupLinha[1], tupLinha[0]) == tupPrimeiraLinhaCaminho:
		del(caminho[0])
		del(caminho[0])
	return caminho

def preencher_matriz_aloc(nwxGrafo, dic_lstMatriz, strLocomotiva, lst_tupTrajeto, intDelta_tempo):
	from math import (floor, ceil)
	i = 0
	tempo = 0

	while i < (len(lst_tupTrajeto) - 1):
		instanteIni = int(floor(tempo//intDelta_tempo))

		"""Origem da Locomotiva'"""

		""" custo da linha de origem """
		custo_linha = nwxGrafo[lst_tupTrajeto[i][0]][lst_tupTrajeto[i][1]]["weight"]

		tempo += custo_linha

		instanteFim = int(ceil(tempo//intDelta_tempo))

		try:
			alocarLinha(dic_lstMatriz, lst_tupTrajeto[i], strLocomotiva, instanteIni, instanteFim)
		except ExceptionLinhaOcupada:
			instanteIni, instanteFim = encontrarProximoIntervaloDisponivel(dic_lstMatriz, lst_tupTrajeto[i],
																		   instanteIni, instanteFim)
			alocarLinha(dic_lstMatriz, lst_tupTrajeto[i], strLocomotiva, instanteIni, instanteFim)
		"""Origem da Locomotiva'"""

		""" define qual caminho tomar (yen ou 'dijkstra e esperar'?) """
		caminho = nwx.dijkstra_path(nwxGrafo, lst_tupTrajeto[i][1], lst_tupTrajeto[i + 1][0])
		caminho = delLinhaRepedtida(lst_tupTrajeto[0], caminho)
		""" define qual caminho tomar (yen ou 'dijkstra e esperar'?) """
		j = 0
		while j < (len(caminho) - 1):

			"""" calculando custo da linha """
			custo_linha = nwxGrafo[caminho[j]][caminho[j + 1]]["weight"]
			instanteIni = tempo

			tempo += custo_linha

			instanteFim = tempo
			try:
				alocarLinha(dic_lstMatriz, (caminho[j], caminho[j + 1]), strLocomotiva, instanteIni, instanteFim)
			except ExceptionLinhaOcupada:
				instanteIni, instanteFim = encontrarProximoIntervaloDisponivel(dic_lstMatriz, (caminho[j], caminho[j + 1]),
																			   instanteIni, instanteFim)
				alocarLinha(dic_lstMatriz, (caminho[j], caminho[j + 1]), strLocomotiva, instanteIni, instanteFim)
			j += 1

		i += 1

	custo_linha = nwxGrafo[lst_tupTrajeto[i][0]][lst_tupTrajeto[i][1]]["weight"]
	instanteIni = tempo

	tempo += custo_linha
	instanteFim = tempo

	try:
		alocarLinha(dic_lstMatriz, lst_tupTrajeto[i], strLocomotiva, instanteIni, instanteFim)
	except ExceptionLinhaOcupada:
		instanteIni, instanteFim = encontrarProximoIntervaloDisponivel(dic_lstMatriz, lst_tupTrajeto[i],
																	   instanteIni, instanteFim)
		alocarLinha(dic_lstMatriz, lst_tupTrajeto[i], strLocomotiva, instanteIni, instanteFim)
	return dic_lstMatriz

def avaliar_custo_c_dijkstra(grafo, solucao):
	indice = 1
	custo = 0
	while indice < len(solucao):
		edge = grafo[solucao[indice - 1][0]][solucao[indice - 1][1]]
		custo += edge["weight"]
		custo += nwx.dijkstra_path_length(grafo, solucao[indice - 1][1], solucao[indice][0])
		indice += 1
	custo += grafo[solucao[indice - 1][0]][solucao[indice - 1][1]]["weight"]
	return custo