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
		if grafo[elem[0]][elem[1]]["name"] == nome_linha:
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

def checarLinhaPorInstante (matriz, linha, instanteInicio, instanteFim,):
	# matriz ->  {("Ni","Nj"):[0,1,2,3,...],...}
	# linha -> ("Ni","Nj")
	# instanteInicio/instanteFim -> inteiro

	result = True
	if linha not in matriz.keys():
		linha = (linha[1],linha(0))
	i = instanteInicio
	while i <= instanteFim and result:
		if matriz[linha][i] != 0:
			result = result and False
	return result

def alocarLinha (matriz, linha, locomotiva, instanteInicio, instanteFim):
	# matriz ->  {("Ni","Nj"):[0,1,2,3,...],...}
	# linha -> ("Ni","Nj")
	# locomotiva -> "LMx"
	# instanteInicio/instanteFim -> inteiro
	a = linha
	if a not in matriz.keys():
		a = (linha[1], linha[0])
	for i in range (instanteInicio, instanteFim, 1):
		matriz[a][i] = locomotiva

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
	#instante = 0
	while i < (len(lst_tupTrajeto) - 1):
		instanteIni = int(floor(tempo//intDelta_tempo))
		"""Origem da Locomotiva'"""
		x = 0
		""" custo da linha de origem """
		custo_linha = nwxGrafo[lst_tupTrajeto[i][0]][lst_tupTrajeto[i][1]]["weight"]
		while x < (custo_linha/intDelta_tempo):
			# """" calculando o intervalo de tempo """
			# instante = int(floor(tempo//intDelta_tempo) + x)
            #
			# if lst_tupTrajeto[i] in dic_lstMatriz:
			# 	a = lst_tupTrajeto[i]
			# 	if checarLinha(nwxGrafo, a, dic_lstMatriz, tempo, intDelta_tempo):
			# 		# alocar linha #
			# 		dic_lstMatriz[a][instante] = strLocomotiva
			# 	else:
			# 		raise ExceptionLinhaOcupada
			# else:
			# 	b = (lst_tupTrajeto[i][1], lst_tupTrajeto[i][0])
			# 	if checarLinha(nwxGrafo, b, dic_lstMatriz, tempo, intDelta_tempo):
			# 		# alocar linha #
			# 		dic_lstMatriz[b][instante] = strLocomotiva
			# 	else:
			# 		raise ExceptionLinhaOcupada

			tempo += intDelta_tempo
			x += 1
		""" acertando valor de tempo """
		if custo_linha > intDelta_tempo and custo_linha % intDelta_tempo != 0:
			tempo -= (intDelta_tempo*x - custo_linha)
		elif custo_linha < intDelta_tempo:
			tempo -= (intDelta_tempo - custo_linha)
		instanteFim = int(ceil(tempo//intDelta_tempo))
		alocarLinha(dic_lstMatriz, lst_tupTrajeto[i], strLocomotiva, instanteIni, instanteFim)
		"""Origem da Locomotiva'"""

		""" define qual caminho tomar (yen ou 'dijkstra e esperar'?) """
		caminho = nwx.dijkstra_path(nwxGrafo, lst_tupTrajeto[i][1], lst_tupTrajeto[i + 1][0])
		caminho = delLinhaRepedtida(lst_tupTrajeto[0], caminho)
		""" define qual caminho tomar (yen ou 'dijkstra e esperar'?) """

		j = 0
		while j < (len(caminho) - 1):
			#instante = 0
			x = 0
			"""" calculando custo da linha """
			custo_linha = nwxGrafo[caminho[j]][caminho[j + 1]]["weight"]
			instanteIni = tempo
			""" enquanto x for menor que a relação entre o custo da linha e o delta_tempo """
			while x < (custo_linha/intDelta_tempo):
				# """ calculando o intervalo de tempo """
				# if int(floor(tempo//intDelta_tempo) + x) == instante:
				# 	instante+=1
                #
				# else: instante = int(floor(tempo//intDelta_tempo) + x)
                #
				# if (caminho[j], caminho[j + 1]) in dic_lstMatriz:
				# 	a = (caminho[j], caminho[j + 1])
				# 	if checarLinha(nwxGrafo, a, dic_lstMatriz, tempo, intDelta_tempo):
				# 		# alocar linha #
				# 		dic_lstMatriz[a][instante] = strLocomotiva
				# 	else:
				# 		raise ExceptionLinhaOcupada
				# else:
				# 	b = (caminho[j + 1], caminho[j])
				# 	if checarLinha(nwxGrafo, b, dic_lstMatriz, tempo, intDelta_tempo):
				# 		# alocar linha #
				# 		dic_lstMatriz[b][instante] = strLocomotiva
				# 	else:
				# 		raise ExceptionLinhaOcupada
				tempo = tempo + intDelta_tempo
				x += 1
			""" acertando valor de tempo """
			if custo_linha > intDelta_tempo and custo_linha % intDelta_tempo != 0:
				tempo -= (intDelta_tempo * x - custo_linha)
			elif custo_linha < intDelta_tempo:
				tempo -= (intDelta_tempo - custo_linha)
			instanteFim = tempo
			alocarLinha(dic_lstMatriz, (caminho[j], caminho[j + 1]), strLocomotiva, instanteIni, instanteFim)
			j += 1

		i += 1

	x = 0
	custo_linha = nwxGrafo[lst_tupTrajeto[i][0]][lst_tupTrajeto[i][1]]["weight"]
	instanteIni = tempo
	while x < (custo_linha/intDelta_tempo):
		# """ calculando o intervalo de tempo """
		# if int(floor(tempo//intDelta_tempo) + x) == instante:
		# 	instante+= 1
        #
		# else: instante = int(floor(tempo//intDelta_tempo) + x)
        #
		# if lst_tupTrajeto[i] in dic_lstMatriz:
		# 	a = lst_tupTrajeto[i]
		# 	if checarLinha(nwxGrafo, a, dic_lstMatriz, tempo, intDelta_tempo):
		# 		# alocar linha #
		# 		dic_lstMatriz[a][instante] = strLocomotiva
		# 	else:
		# 		raise ExceptionLinhaOcupada
		# else:
		# 	b = (lst_tupTrajeto[i][1], lst_tupTrajeto[i][0])
		# 	if checarLinha(nwxGrafo, b, dic_lstMatriz, tempo, intDelta_tempo):
		# 		# alocar linha #
		# 		dic_lstMatriz[b][instante] = strLocomotiva
		# 	else:
		# 		raise ExceptionLinhaOcupada

		tempo += intDelta_tempo
		x += 1
	""" acertando valor de tempo """
	if custo_linha > intDelta_tempo and custo_linha % intDelta_tempo != 0:
		tempo -= (intDelta_tempo * x - custo_linha)
	elif custo_linha < intDelta_tempo:
		tempo -= (intDelta_tempo - custo_linha)
	instanteFim = tempo
	alocarLinha(dic_lstMatriz, lst_tupTrajeto[i], strLocomotiva, instanteIni, instanteFim)

	return dic_lstMatriz

def avaliar_custo_c_dijkstra(grafo, solucao):
	indice = 1
	custo = 0
	while indice < len(solucao):
		custo += grafo[solucao[indice - 1][0]][solucao[indice - 1][1]]["weight"]
		custo += nwx.dijkstra_path_length(grafo, solucao[indice - 1][1], solucao[indice][0])
		indice += 1
	custo += grafo[solucao[indice - 1][0]][solucao[indice - 1][1]]["weight"]
	return custo