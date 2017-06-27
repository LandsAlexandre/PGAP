#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  functions_in_out.py
#  
#  Copyright 2016 GPRC2-LMA <GPRC2-LMA@GPRC2-LMA-PC>

""" entrada e saída de dados"""
def abrir_arquivo(strNomeArq):
	strVetor = []
	arq = open(strNomeArq, "r")
	linha = arq.readline()
	linha = arq.readline()
	while linha:
		linha = linha.replace("\n","")
		strVetor.append(linha.split(" "))
		linha = arq.readline()
	arq.close()
	return strVetor
	
def imprime_matriz(matriz, lPatio):
	chaves = list(matriz.keys())
	for i in range (len(chaves)):
		print(lPatio[chaves[i][0]][chaves[i][1]]["name"], end = "\t")
		for j in range(len(matriz[chaves[i]])):
			print(matriz[chaves[i]][j], end = "\t")
		print()

def imprime_matriz_arquivo(nwxGrafo, matriz, arquivo):
	a = open(arquivo, "w")
	chaves = list(matriz.keys())
	chaves = sorted(chaves)
	for i in range (len(chaves)):
		a.write(nwxGrafo[chaves[i][0]][chaves[i][1]]["name"]+"\t")
		for j in range (len(matriz[chaves[i]])):
			a.write(matriz[chaves[i]][j]+"\t")
		a.write("\n")
	a.close()

def imprime_trajeto_arquivo(trajeto , nomeArquivo):
	a = open(nomeArquivo, "w")
	a.write(trajeto[0][0]+"\t"+trajeto[0][1]+"\t")
	for i in range (1,len(trajeto)):
		a.write(trajeto[i][0]+"\t"+trajeto[i][1]+"\t")

""" entrada e saída de dados"""