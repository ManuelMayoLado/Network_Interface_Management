# -*- coding: utf-8 -*-

from Tkinter import *
import os
import time

window = [600,200]

lista_interfaces = []

root = Tk()

#CLASE INTERFACE
class interface():

	#CONSTRUCTOR
	def __init__(self,r,id,nome,conectado):
		self.r = r
		self.id = id
		self.nome = nome
		self.conectado = conectado
		self.dhcp = True if os.popen("netsh interface ipv4 show config "+str(self.nome)).read().split()[1] else False
		self.dns = None
		self.texto_nome = Label(self.r, text=self.nome, bg="lightgreen" if self.conectado else "indianred2")
		self.boton_dhcp = Button(self.r, text="Habilitado" if self.dhcp else "Non", relief="ridge", command=self.boton_dhcp,
							state="normal" if self.conectado else "disable")
		self.entrada_ip = Entry(self.r, text="", state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_mascara = Entry(self.r, text="", state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_dns = Entry(self.r, text="", state="normal" if self.conectado and not self.dhcp else "disable")
		self.boton = Button(self.r, text="CAMBIAR", state="normal" if self.conectado else "disable", relief="groove")
	
	#FUNCION PARA EXECUTAR CANDO SE PULSE O BOTÓN DHCP
	def boton_dhcp(self):
		self.dhcp = False if self.dhcp else True
		
		#UPDATE
		
		self.boton_dhcp.configure(text = "Habilitado" if self.dhcp else "Non")
		self.entrada_ip.configure(state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_mascara.configure(state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_dns.configure(state="normal" if self.conectado and not self.dhcp else "disable")
		
#FUNCIÓN PARA VOLVER A CARGAR TODO
def actualizar():
	lista_interfaces = []
	interfaces_rede()
	app_init(root)
		
#FUNCIÓN QUE INSERTA AS INTERFACES NA LISTA lista_interfaces
def interfaces_rede():
	global lista_interfaces
	
	#GARDAR NUNHA VARIABLE A SALIDA DO COMANDO netsh interface show interface
	info_interfaces = os.popen("netsh interface show interface").read().splitlines()
	
	lista_interfaces = []
	
	#RECORRER A VARIABLE info_interfaces PARA SACAR OS DATOS (NOME E ESTADO) E INSERTALOS EN lista_interfaces
	for linea in range(3,len(info_interfaces)-1):
	
		if info_interfaces[linea].split()[0] == "Habilitado":
			nome_i = " ".join(info_interfaces[linea].split()[3:])
			conectado_i = True if info_interfaces[linea].split()[1] == "Conectado" else False
			lista_interfaces.append(interface(root,linea-3,nome_i,conectado_i))
			
interfaces_rede()
	
#FUNCIÓN QUE CONFIGURA E DEBUXA TODOS OS ELEMENTOS NA VENTANA
def app_init(r):

	#TITULO
	r.title("DNS Edition")
	
	#CONFIGURACION DA VENTANA
	r.resizable(width=False, height=False)
	r.minsize(window[0], window[1])
	
	#TEXTO, CAMPOS DE TEXTO E BOTÓNS SEGÚN INTERFACES
	
	Boton_actualizar = Button(r, text="ACTUALIZAR", relief="groove", command=actualizar)
	Boton_actualizar.grid(row=0, column=0, pady=15, padx=10, sticky="w")
	Label(r, text="INTERFACES DE REDE", bg="lightblue").grid(row=1, column=0, pady=15, padx=10, sticky="we")
	Label(r, text="DHCP", bg="lightblue", width=15).grid(row=1, column=1, pady=15, padx=10, sticky="we")
	Label(r, text="IP", bg="lightblue", width=15).grid(row=1, column=2, pady=15, padx=10, sticky="we")
	Label(r, text="NETMASK", bg="lightblue", width=15).grid(row=1, column=3, pady=15, padx=10, sticky="we")
	Label(r, text="DNS", bg="lightblue").grid(row=1, column=4, pady=15, padx=10, sticky="we")
	
	#DEBUXAR AS INTERFACES NA VENTANA
	for interface in lista_interfaces:
		interface.texto_nome.grid(row=interface.id+2, column=0, padx=10, sticky="we")
		interface.boton_dhcp.grid(row=interface.id+2, column=1, padx=10, sticky="we")
		interface.entrada_ip.grid(row=interface.id+2, column=2, padx=10, sticky="w")
		interface.entrada_mascara.grid(row=interface.id+2, column=3, padx=10, sticky="w")
		interface.entrada_dns.grid(row=interface.id+2, column=4, padx=10, sticky="w")
		interface.boton.grid(row=interface.id+2, column=5, padx=10, sticky="w")
		
	#CAMPO DE TEXTO
	
	campo_texto=Text(r, height=10, width=90)
	campo_texto.grid(row=len(lista_interfaces)+3, column=0, columnspan=7, pady=30, padx=10, sticky="w")
	campo_texto.insert(END,">> Programa en desarrollo")
	
	barra_scroll = Scrollbar(r, command=campo_texto.yview)

	campo_texto.config(yscrollcommand=barra_scroll.set)
	
	barra_scroll.grid(row=len(lista_interfaces)+3, column=5, padx=10, pady=30, sticky="nsw")
	barra_scroll.config(command=campo_texto.yview)

app_init(root)

mainloop()