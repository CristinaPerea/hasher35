#!/usr/bin/python
class HashingData:
	def __init__(self, hora, fichero, hashing):
		self.__hora = hora
		self.__fichero = fichero
		self.__hashing = hashing

	def __str__(self):
		mensaje = "[" + self.__hora + "] " + self.__hashing + " : " + self.__fichero + "\n"
		return mensaje

	def impresion(self):
		mensaje = "[" + self.__hora + "] " + self.__hashing + " : " + self.__fichero + "\n"
		return mensaje		

	__repr__ = __str__