#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  functions.py
#  
#  Copyright 2016 GPRC2-LMA <GPRC2-LMA@GPRC2-LMA-PC>

import networkx as nwx
from functions2 import *
from functions_in_out import (imprime_matriz_arquivo,imprime_trajeto_arquivo)

def gerar_RCL(grafo, manobras, linha_atual):
	dic_custos = {}
	RCL = manobras
	
	i = 0
	for elem in manobras:
		#dic_custos[(x,y)] -> {custo do caminho (inteiro), numero de saltos de X ate Y (inteiro)}
		dic_custos[tuple(elem[1:])] = (nwx.dijkstra_path_length(grafo,linha_atual[1],elem[1][0]),
									   len(nwx.dijkstra_path(grafo,linha_atual[1],elem[1][0]))-1)

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
	while i < max - 1:
		ult_seq = i
		while dic_custos[tuple(RCL[ult_seq][1:])][0] == dic_custos[tuple(RCL[ult_seq + 1][1:])][0]:
			if ult_seq + 1 != max - 1:
				ult_seq += 1
			else:
				break
		imax = ult_seq
		j = i
		while j >= i:

			maior = [i, dic_custos[tuple(RCL[i][1:])][1]]

			for k in range(j + 1):
				if dic_custos[tuple(RCL[k][1:])][1] >= maior[1]:
					maior = [k, dic_custos[tuple(RCL[k][1:])][1]]

			RCL[j], RCL[maior[0]] = RCL[maior[0]], RCL[j]
			j -= 1
		if i == ult_seq:
			i += 1
		else:
			i = ult_seq + 1
	return RCL

def construir_solucao(grafo, lst_manobras, lst_tupLocomotivas, dic_lstMatriz, tempo, intDelta_tempo, strSol, alpha = 1):
	from random import choice
	from math import floor
	manobras = lst_manobras[:]

	for p in range(len(lst_tupLocomotivas)):
		""" inicializacao """
		trajeto = []
		tempo_gasto = 0
		res_tempo = tempo_gasto > tempo
		tupOrigemLoc = lst_tupLocomotivas[p][1]
		strLocomotiva = lst_tupLocomotivas[p][0]

		trajeto.append(tupOrigemLoc)

		while (len(trajeto) != 1 + len(lst_manobras) * 2) and not res_tempo:

			RCL = gerar_RCL(grafo, manobras, trajeto[len(trajeto) - 1])
			if len(RCL) == 0:
				break
			limiteRCL = floor(len(RCL)*alpha)
			if limiteRCL == 0:	limiteRCL = 1
			elem_RCL = choice(RCL[0:limiteRCL])
			
			trajeto.append(elem_RCL[1])
			trajeto.append(elem_RCL[2])
			
			tempo_gasto = avaliar_custo_c_dijkstra(grafo, trajeto)
			res_tempo = tempo_gasto > tempo
			
			manobras.remove(elem_RCL)
		if res_tempo:
			del(trajeto[len(trajeto) - 1])
			del(trajeto[len(trajeto) - 1])	

		busca_local(grafo, trajeto)
		#preenchendo a matriz com trajeto escolhido
		preencher_matriz_aloc(grafo, dic_lstMatriz, strLocomotiva, trajeto, intDelta_tempo)
		#escrevendo a matriz em um arquivo
		# imprime_matriz_arquivo(grafo, dic_lstMatriz, "./mat"+strSol+str(p))
		# imprime_trajeto_arquivo(trajeto, strLocomotiva+strSol)

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

def avaliadorSolucao(matrizAlocacao, nomeLocomotivas):
	tempoLocomotivas = {}
	chaves = matrizAlocacao.keys()
	for loc in nomeLocomotivas:
		for chave in chaves:
			if loc in matrizAlocacao[chave]:
				if loc in tempoLocomotivas:	tempoLocomotivas[loc] += matrizAlocacao[chave].count(loc)
				else:	tempoLocomotivas[loc] = matrizAlocacao[chave].count(loc)
			else:	continue
	tempoLocomotivasValues = tempoLocomotivas.values()
	tempoMedioTrabalhoLocomotivas = sum(tempoLocomotivasValues)/len(tempoLocomotivasValues) # tempo médio de trabalho das locomotivas
	tempoLocomotivaTrabalhadora = max(tempoLocomotivasValues) # tempo da locomotiva que terminou as manobras por ultimo
	tempoLocomotivaPreguicosa = min(tempoLocomotivasValues) # tempo da locomotiva que terminou as manobras primeiro
	return (tempoMedioTrabalhoLocomotivas, tempoLocomotivaPreguicosa,
			tempoLocomotivaTrabalhadora)