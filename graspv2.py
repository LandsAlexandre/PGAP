#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  functions.py
#  
#  Copyright 2016 GPRC2-LMA <GPRC2-LMA@GPRC2-LMA-PC>

import networkx as nwx
from functions2 import *
from functions_in_out import imprime_matriz_arquivo

def gerar_RCL(grafo, manobras, linha_atual):
	dic_custos = {}
	RCL = manobras
	
	i = 0
	for elem in manobras:

		dic_custos[tuple(elem[1:])] = (nwx.dijkstra_path_length(grafo,linha_atual[1],elem[1][0]),len(nwx.dijkstra_path(grafo,linha_atual[1],elem[1][0]))-1)
		
	i = len(RCL) - 1
	while i >= 0:
		maior = [0, dic_custos[tuple(RCL[0][1:])][0]]
		
		for j in range(i + 1):
			if dic_custos[tuple(RCL[j][1:])][0] >= maior[1]:
				maior = [j, dic_custos[tuple(RCL[j][1:])][0]]
				
		RCL[i], RCL[maior[0]] = RCL[maior[0]], RCL[i]
		i -= 1

	i = 0
	max = len(RCL)
	while i < max:
		ult_seq = i
		while dic_custos[tuple(RCL[ult_seq][1:])][0] == dic_custos[tuple(RCL[ult_seq + 1][1:])][0]:
			ult_seq += 1
		imax = ult_seq
		j = i
		while j >= i:

			maior = [i, dic_custos[tuple(RCL[i][1:])[1]]]

			for k in range(j + 1):
				if dic_custos[tuple(RCL[k][1:])][1] >= maior[1]:
					maior = [k, dic_custos[tuple(RCL[k][1:])][1]]

			RCL[j], RCL[maior[0]] = RCL[maior[0]], RCL[j]
		if i == ult_seq:
			i += 1
		else:
			i = ult_seq + 1
	return RCL

def construir_solucao(grafo, lst_manobras, lst_tupLocomotivas, dic_lstMatriz, tempo, intDelta_tempo, strSol):
	from random import choice
	
	manobras = lst_manobras[:]

	for p in range(len(lst_tupLocomotivas)):
		""" inicializacao """
		trajeto = []
		tempo_gasto = 0
		res_tempo = tempo_gasto > tempo
		lst_origem = lst_tupLocomotivas[p][1]
		strLocomotiva = lst_tupLocomotivas[p][0]

		trajeto.append(lst_origem)

		while (len(trajeto) != 1 + len(lst_manobras) * 2) and not res_tempo:

			RCL = gerar_RCL(grafo, manobras, trajeto[len(trajeto) - 1])
			if len(RCL) == 0:
				break
			elem_RCL = choice(RCL)
			
			trajeto.append(elem_RCL[1])
			trajeto.append(elem_RCL[2])
			
			tempo_gasto = avaliar_custo_c_dijkstra(grafo, trajeto)
			res_tempo = tempo_gasto > tempo
			
			manobras.remove(elem_RCL)
		if res_tempo:
			del(trajeto[len(trajeto) - 1])
			del(trajeto[len(trajeto) - 1])	
		
		#atualizando localização da locomotiva
		lst_tupLocomotivas[p] = (lst_tupLocomotivas[p][0], trajeto[-1])
		busca_local(grafo, trajeto)
		#preenchendo a matriz com trajeto escolhido
		preencher_matriz_aloc(grafo, dic_lstMatriz, strLocomotiva, trajeto, intDelta_tempo)
		#escrevendo a matriz em um arquivo
		imprime_matriz_arquivo(grafo, dic_lstMatriz, "./mat"+strSol+str(p))

	return [trajeto, avaliar_custo_c_dijkstra(grafo, trajeto)]

def busca_local (grafo, solucao):
	custo = 0
	ind = 1
	while ind < len(solucao):
		custo += nwx.dijkstra_path_length(grafo, solucao[ind - 1][1], solucao[ind][0])
		ind += 1
	melhor_solucao = [solucao, custo]
	
	ind = 1
	while ind < len(solucao) - 2:
		
		# perturbacao #
		solucao[ind], solucao[ind + 2] = solucao[ind + 2], solucao[ind]
		solucao[ind + 1], solucao[ind + 3] = solucao[ind + 3], solucao[ind + 1]
		
		# calculando custo #
		custo_vizinho = avaliar_custo_c_dijkstra(grafo, solucao)
		
		if custo_vizinho < melhor_solucao[1]:
			melhor_solucao = [solucao, custo_vizinho]
		else:
			# desfazendo perturbacao #
			solucao[ind], solucao[ind + 2] = solucao[ind + 2], solucao[ind]
			solucao[ind + 1], solucao[ind + 3] = solucao[ind + 3], solucao[ind + 1]
		ind += 2
		
	
	return melhor_solucao