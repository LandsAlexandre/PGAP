#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  functions.py
#  
#  Copyright 2016 GPRC2-LMA <GPRC2-LMA@GPRC2-LMA-PC>

import networkx as nwx

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

# def checarCaminho(nwxGrafo, dic_lstMatriz, lstCaminho, strLocomotiva, intTempo, intDelta_tempo):
	# result = True
	# instante = int(intTempo//intDelta_tempo)
	# j = 0
	# while j < (len(lstCaminho) - 1):
		
		# x = 0
		# custo_linha = nwxGrafo[lstCaminho[j]][lstCaminho[j + 1]]["weight"]
		
		# while x < (custo_linha/intDelta_tempo):
			# while int(intTempo//intDelta_tempo) == instante:
				# instante += 1
				# print("@#$%")
			# instante = int(intTempo//intDelta_tempo)
			
			# if (lstCaminho[j], lstCaminho[j + 1]) in dic_lstMatriz:
				# a = (lstCaminho[j], lstCaminho[j + 1])
				# result = result and (dic_lstMatriz[a][instante] == strLocomotiva or dic_lstMatriz[a][instante])
			# else:
				# b = (lstCaminho[j + 1], lstCaminho[j])
				# result = result and (dic_lstMatriz[b][instante] == strLocomotiva or dic_lstMatriz[b][instante])
			
			# intTempo = intTempo + intDelta_tempo
			# x += 1
		# j += 1
	# return result

def preencher_matriz_aloc(nwxGrafo, dic_lstMatriz, strLocomotiva, lst_tupTrajeto, intDelta_tempo):
	from math import floor
	i = 0
	tempo = 0
	while i < (len(lst_tupTrajeto) - 1):
		
		instante = 0
		x = 0
		custo_linha = nwxGrafo[lst_tupTrajeto[i][0]][lst_tupTrajeto[i][1]]["weight"]
		while x < (custo_linha/intDelta_tempo):
			instante = int(floor(tempo//intDelta_tempo))
			
			if lst_tupTrajeto[i] in dic_lstMatriz:
				while dic_lstMatriz[lst_tupTrajeto[i]][instante] == strLocomotiva:
					instante += 1
				dic_lstMatriz[lst_tupTrajeto[i]][instante] = strLocomotiva
			else:
				a = (lst_tupTrajeto[i][1], lst_tupTrajeto[i][0])
				while dic_lstMatriz[a][instante] == strLocomotiva:
					instante += 1
				dic_lstMatriz[a][instante] = strLocomotiva
			
			tempo = tempo + intDelta_tempo
			x += 1
		tempo -= intDelta_tempo - custo_linha%intDelta_tempo
		""" define qual caminho tomar (yen ou 'dijkstra e esperar'?) """
		caminho = nwx.dijkstra_path(nwxGrafo, lst_tupTrajeto[i][1], lst_tupTrajeto[i + 1][0])
		""" define qual caminho tomar (yen ou 'dijkstra e esperar'?) """

		j = 0
		while j < (len(caminho) - 1):
			instante = 0
			x = 0
			custo_linha = nwxGrafo[caminho[j]][caminho[j + 1]]["weight"]
			
			while x < (custo_linha/intDelta_tempo):
				instante = int(floor(tempo//intDelta_tempo))


				if (caminho[j], caminho[j + 1]) in dic_lstMatriz:
					a = (caminho[j], caminho[j + 1])
					while dic_lstMatriz[a][instante] == strLocomotiva:
						instante += 1
					dic_lstMatriz[a][instante] = strLocomotiva

				else:
					b = (caminho[j + 1], caminho[j])
					while dic_lstMatriz[b][instante] == strLocomotiva:
						instante += 1
					dic_lstMatriz[b][instante] = strLocomotiva
				
				tempo = tempo + intDelta_tempo
				x += 1
			tempo -= intDelta_tempo - custo_linha%intDelta_tempo
			j += 1
		i += 1
	
	x = 0
	custo_linha = nwxGrafo[lst_tupTrajeto[i][0]][lst_tupTrajeto[i][1]]["weight"]
	
	while x < (custo_linha/intDelta_tempo):
		instante = int(floor(tempo//intDelta_tempo))
		
		if lst_tupTrajeto[i] in dic_lstMatriz:
			while dic_lstMatriz[lst_tupTrajeto[i]][instante] == strLocomotiva:
				instante += 1
			dic_lstMatriz[lst_tupTrajeto[i]][instante] = strLocomotiva
		else:
			a = (lst_tupTrajeto[i][1], lst_tupTrajeto[i][0])
			while dic_lstMatriz[a][instante] == strLocomotiva:
				instante += 1
			dic_lstMatriz[a][instante] = strLocomotiva
		
		tempo = tempo + intDelta_tempo
		x += 1
	tempo -= intDelta_tempo - custo_linha%intDelta_tempo
	
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