#!/usr/bin/python

from config.ModuloConfigurador import Configurador
from datatype.HashingData import HashingData
import sys, os
import hashlib
import json
import time
import datetime
import codecs

BUF_SIZE = 65536

c = Configurador(".", 0, False, "sha1")
c.leerConfiguracion()
try:
	print(c)
except UnicodeEncodeError:
	print("Configuracion cargada: ")
	print("Ruta: " + c.getRuta())
	print("Intervalo: " + str(c.getIntervalo()))
	print("Modo Log: " + str(c.getVerbose()))
	print("Metodo HASH: " + c.getMetodo())
	

mapaInicial = {}
mapaComparado = {}

def clean():
	print("Borrando ficheros\n")
	ficheros = os.listdir("hashings")
	for f in ficheros:
		f = os.path.join("hashings",f)
		if os.path.isfile(f):
			os.remove(f)
	ficheros = os.listdir("comparaciones")
	for f in ficheros:
		f = os.path.join("comparaciones",f)
		if os.path.isfile(f):
			os.remove(f)

def hasher(fichero, metodo):
	if metodo == "md5":
		hasheador = hashlib.md5()
	elif metodo == "sha1":
		hasheador = hashlib.sha1()
	elif metodo == "sha256":
		hasheador = hashlib.sha256()
	elif metodo == "sha384":
		hasheador = hashlib.sha384()
	elif metodo == "sha224":
		hasheador = hashlib.sha224()
	elif metodo == "sha512":
		hasheador = hashlib.sha512()
	#print(fichero)
	if c.getVerbose():
		print ("[hasher.py] Hasheando en hasher(): " + fichero)


	with codecs.open(fichero, 'rb') as f:
		while True:
			data = f.read(BUF_SIZE)
			if not data:
				break
			hasheador.update(data)
	#print(type(hasheador.hexdigest()))
	return hasheador.hexdigest()

def imprimePorcentaje(contador, total):
	sys.stdout.write(str(contador) + " de " + str(total))
	sys.stdout.write("\r")

def inicializacion():
	total = 0
	contadorFicherosHasheados = 0
	ficheroSalida = open("hashings/salida.txt", "w")
	
	ruta = c.getRuta()
	if c.getVerbose():
		print("Se va a trabajar en: " + ruta)
	if os.path.isdir(ruta):	
		listaDirectorios = [ruta]

		for root, dirs, files in os.walk(ruta):
			if c.getVerbose():
				print("[hasher.py] Ficheros a analizar:")
				print(files)
			total += len(files)
		
		while len(listaDirectorios) != 0:
			rutaActual = listaDirectorios.pop()
			#print rutaActual
			listaFicheros = []
			try:
				listaFicheros = list(os.listdir(rutaActual))
			except:
				pass
				
			while len(listaFicheros) != 0:
				miCandidato = listaFicheros.pop()
				candidato = os.path.join(rutaActual, miCandidato)

				if not os.path.isdir(candidato):
					now = datetime.datetime.now()
					cadenaNow = ""
					cadenaNow += str(now.month)+"/"+str(now.day)+"/"+str(now.year)
					hasheo = hasher(candidato, c.getMetodo())
					h = HashingData(cadenaNow, candidato, hasheo)
					mapaInicial[candidato] = hasheo
					ficheroSalida.write(h.impresion())
					contadorFicherosHasheados += 1
					imprimePorcentaje(contadorFicherosHasheados, total)
				else:
					if c.getVerbose():
						print("[hasher.py] inicializacion() - Anado a directorios: " + candidato)
					listaDirectorios.append(candidato)

def comparacion():
	total = 0
	contadorFicherosHasheados = 0
	now = time.strftime("%d%m%Y%H%M%S")
	nombreFichero = "hashings/salida" + str(now) + ".txt"
	nombreFicheroErrores = "comparaciones/errores" + str(now) + ".txt"
	cambios = 0
	ficheroSalida = open(nombreFichero, "w")	
	ficheroErrores = open(nombreFicheroErrores, "w")
	ruta = c.getRuta()
	global mapaComparado
	#print ruta
	if os.path.isdir(ruta):	
		#c.escribirConfiguracion()
		listaDirectorios = [ruta]
		#print listaDirectorios
		for root, dirs, files in os.walk(ruta):
			#print files
			total += len(files)
		while len(listaDirectorios) != 0:
			rutaActual = listaDirectorios.pop()
			#print rutaActual
			listaFicheros = list(os.listdir(rutaActual))
			while len(listaFicheros) != 0:
				miCandidato = listaFicheros.pop()
				candidato = os.path.join(rutaActual, miCandidato)
				#print candidato
				if not os.path.isdir(candidato):
					now = datetime.datetime.now()
					cadenaNow = ""
					cadenaNow += str(now.month)+"/"+str(now.day)+"/"+str(now.year)
					hasheo = hasher(candidato, c.getMetodo())
					h = HashingData(cadenaNow, candidato, hasheo)
					mapaComparado[candidato] = hasheo
					ficheroSalida.write(h.impresion())
					contadorFicherosHasheados += 1
					imprimePorcentaje(contadorFicherosHasheados, total)
				else:
					#print "Anado a directorios: " + candidato
					listaDirectorios.append(candidato)

	# Comparacion
	global mapaInicial 
	mapaInicialTemporal = dict(mapaInicial)
	mapaTemporal = {}
	lista = []
	for key in mapaComparado:
		lista.append(key)
		if key in mapaInicialTemporal:
			hash1 = mapaComparado[key]
			hash2 = mapaInicialTemporal[key]
			if hash1 != hash2:
				ficheroErrores.write("El fichero " + key + " no mantiene su integridad\n")
				cambios += 1
		else:
			ficheroErrores.write("El fichero " + key + " es nuevo\n")
			cambios += 1
			keyNueva = str(key)
			valueNuevo = hasher(keyNueva, c.getMetodo())
			mapaTemporal[keyNueva] = valueNuevo
			ficheroSalidaOriginal = open("hashings/salida.txt", "a")
			now = time.strftime("%c")
			h = HashingData(now, key, valueNuevo)
			ficheroSalidaOriginal.write(str(h))
	
	for x in lista:
		if x in mapaInicialTemporal:
			del mapaInicialTemporal[x]
		del mapaComparado[x]

	if mapaInicialTemporal:
		for key in mapaInicialTemporal:
			ficheroErrores.write("El fichero " + key + " se ha eliminado\n")
			cambios += 1

	mapaInicial.update(mapaTemporal)
	print("Numero total de cambios = " + str(cambios))

def main():
	clean()
	configuracionOriginal = Configurador(c.getRuta(), c.getIntervalo(), c.getVerbose(), c.getMetodo())
	if configuracionOriginal.getVerbose():
		print("==== Configuracion Original Cargada ====\n")
		try:
			print(c)
		except UnicodeEncodeError:
			print("Configuracion cargada: ")
			print("Ruta: " + configuracionOriginal.getRuta())
			print("Intervalo: " + str(configuracionOriginal.getIntervalo()))
			print("Modo Log: " + str(configuracionOriginal.getVerbose()))
			print("Metodo HASH: " + configuracionOriginal.getMetodo())
		print("==== Fin de la Configracion Original ===\n")
	global mapaInicial
	inicializacion()
	espera = c.getIntervalo()
	sincambios = True
	while espera != 0 and sincambios:
		time.sleep(espera)
		c.leerConfiguracion()
		espera = c.getIntervalo()
		if configuracionOriginal.getMetodo() == c.getMetodo() and configuracionOriginal.getRuta() == c.getRuta():
			comparacion()
		else:
			print("[Error] No se puede cambiar en caliente el metodo o la ruta a hashear, reinicie con la nueva configuracion")
			sincambios = False

main()
