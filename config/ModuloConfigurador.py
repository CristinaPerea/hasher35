#!/usr/bin/python
# -*- coding: utf-8 -*-
# Clase que representa el configurador de la aplicacion
import os
from xml.dom import minidom

class Configurador:

	def __init__(self, ruta, intervalo=0, verbose=False, metodo="md5"):
		self.setRuta(ruta)
		self.setIntervalo(intervalo)
		self.setVerbose(verbose)
		self.setMetodo(metodo)
	
	def __str__(self):
		ruta = self.getRuta()
		mensaje = "Configuracion cargada: \n"
		mensaje += "\n\n"
		mensaje += "Ruta: " + ruta + "\n"
		mensaje += "Intervalo: " + str(self.getIntervalo()) + "\n"
		mensaje += "Modo Log: " + str(self.getVerbose()) + "\n"
		mensaje += "Metodo HASH: " + self.getMetodo()
		return mensaje

	def setRuta(self, ruta):
		if os.path.isdir(ruta):
			self.__ruta = ruta
		else:
			print("Error de argumento ruta, se inicializara por defecto a .")
			self.__ruta = "."

	def setVerbose(self, verbose):
		if str(verbose) != 'True' and str(verbose) != 'False':
			print("Error en el argumento verbose, se inicializara a False")
			self.__verbose = False
		elif str(verbose) == "True":
			self.__verbose = True
		else:
			self.__verbose = False

	def setIntervalo(self, intervalo):
		intervalo = int(intervalo)
		if intervalo < 0:
			print("Error, intervalo negativo, se inicializara a 10 minutos")
			self.__intervalo = 10*60
		else:
			self.__intervalo = intervalo * 60

	def setMetodo(self, metodo):
		metodo = str(metodo)
		if metodo != "sha1" and metodo != "sha224" and metodo != "md5" and metodo != "sha256" and metodo != "sha384" and metodo != "sha512":
			print("Error, el metodo debe ser un string, se inicializara a md5")
			self.__metodo = "md5"
		else:
			self.__metodo = metodo

	def getMetodo(self):
		return self.__metodo

	def getIntervalo(self):
		return self.__intervalo

	def getRuta(self):
		return self.__ruta

	def getVerbose(self):
		return self.__verbose

	def leerConfiguracion(self):
		xmldoc = minidom.parse('config/configuracion.xml')
		ruta = xmldoc.getElementsByTagName("ruta")[0].firstChild.data
		#print ruta
		self.setRuta(ruta)
		self.setVerbose(xmldoc.getElementsByTagName("verbose")[0].firstChild.data)
		self.setIntervalo(xmldoc.getElementsByTagName("intervalo")[0].firstChild.data)
		self.setMetodo(xmldoc.getElementsByTagName("metodo")[0].firstChild.data)

