# -*- coding: utf-8 -*-

from Tkinter import *
import ttk
import os
import datetime

lista_interfaces = []

root = Tk()

"""
netsh interface ipv4 show config name="Ethernet" & netsh interface ipv4 show config name="Wi-Fi"
"""

#CLASE INTERFACE
class interface():

	#CONSTRUCTOR
	def __init__(self,r,id,nome,conectado):
		self.r = r
		self.id = id
		self.nome = nome
		self.conectado = conectado
		
		self.dhcp = True
		
		self.ip = ""
		
		self.mascara = ""
		
		self.gateway = ""
		
		self.dns = ""
		
		self.cadro_conectado = ttk.Label(self.r, text="     ", relief="groove", background="green" if self.conectado else "red")
		self.texto_nome = ttk.Label(self.r, text=self.nome)
		self.boton_dhcp = ttk.Button(self.r, text="Habilitado" if self.dhcp else "Non", command=self.boton_dhcp,
							state="normal" if self.conectado else "disable")
		self.entrada_ip = ttk.Entry(self.r, text="", width=15, state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_mascara = ttk.Entry(self.r, text="", width=15, state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_gateway = ttk.Entry(self.r, text="", width=15, state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_dns = ttk.Entry(self.r, text="", width=15, state="normal" if self.conectado and not self.dhcp else "disable")
		self.boton = ttk.Button(self.r, text="CAMBIAR", width=15, state="normal" if self.conectado and not self.dhcp else "disable")
		
		#ESCRIBIR OS PARAMETROS NAS ENTRADAS DE TEXTO
		escribir_en(self.entrada_ip,self.ip,True)
		escribir_en(self.entrada_mascara,self.mascara,True)
		escribir_en(self.entrada_gateway,self.gateway,True)
		escribir_en(self.entrada_dns,self.dns,True)
	
	#FUNCION PARA EXECUTAR CANDO SE PULSE O BOTÓN DHCP
	def boton_dhcp(self):
		self.dhcp = False if self.dhcp else True
		
		#UPDATE
		
		self.boton_dhcp.configure(text = "Habilitado" if self.dhcp else "Non")
		self.entrada_ip.configure(state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_mascara.configure(state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_gateway.configure(state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_dns.configure(state="normal" if self.conectado and not self.dhcp else "disable")
		self.boton.configure(state="normal" if self.conectado and not self.dhcp else "disable")
		
#FUNCIÓN PARA VOLVER A CARGAR TODO
def actualizar():
	lista_interfaces = []
	interfaces_rede()
	app_init(root)
	
#FUNCION PARA ESCRIBIR ALGO EN UNHA ENTRADA DE TEXTO
def escribir_en(entrada,texto,borrar=False):
	estado = entrada.cget("state")
	entrada.config(state="normal")
	if borrar:
		entrada.delete(0,END)
		entrada.insert(END,texto)
	else:
		entrada.insert(END,texto)
	entrada.config(state=estado)
		
#FUNCIÓN QUE INSERTA AS INTERFACES NA LISTA lista_interfaces
def interfaces_rede():
	global lista_interfaces
	
	#GARDAR NUNHA VARIABLE A SALIDA DO COMANDO netsh interface show interface
	info_interfaces = os.popen("netsh interface show interface | more /S +3").read().splitlines()
	
	while "" in info_interfaces:
		info_interfaces.remove("")
	
	lista_interfaces = []
	
	#RECORRER A VARIABLE info_interfaces PARA SACAR OS DATOS (NOME E ESTADO) E INSERTALOS EN lista_interfaces
	for linea in range(len(info_interfaces)):
		
		if info_interfaces[linea].split()[0] == "Habilitado":
			nome_i = " ".join(info_interfaces[linea].split()[3:])
			conectado_i = True if info_interfaces[linea].split()[1] == "Conectado" else False
			lista_interfaces.append(interface(root,linea,nome_i,conectado_i))
			
interfaces_rede()
	
#FUNCIÓN QUE CONFIGURA E DEBUXA TODOS OS ELEMENTOS NA VENTANA
def app_init(r):

	#TITULO
	r.title("Configuración de Interfaces")
	
	#CONFIGURACION DA VENTANA
	r.resizable(width=False, height=True)
	r.minsize(0,200)
	
	#TEXTO, CAMPOS DE TEXTO E BOTÓNS SEGÚN INTERFACES
	
	Boton_actualizar = ttk.Button(r, text="ACTUALIZAR", command=actualizar)
	Boton_actualizar.grid(row=0, column=0, columnspan=2, pady=5, padx=5, sticky="w")
	ttk.Label(r, text="INTERFACES DE REDE", relief="groove", background="#C6F1F5", anchor="c").grid(row=1, column=1, pady=15, padx=5, sticky="we")
	ttk.Label(r, text="DHCP", relief="groove", background="#C6F1F5", anchor="c").grid(row=1, column=2, pady=15, padx=5, sticky="we")
	ttk.Label(r, text="IP", relief="groove", background="#C6F1F5", anchor="c").grid(row=1, column=3, pady=15, padx=5, sticky="we")
	ttk.Label(r, text="NETMASK", relief="groove", background="#C6F1F5", anchor="c").grid(row=1, column=4, pady=15, padx=5, sticky="we")
	ttk.Label(r, text="GATEWAY", relief="groove", background="#C6F1F5", anchor="c").grid(row=1, column=5, pady=15, padx=5, sticky="we")
	ttk.Label(r, text="DNS", relief="groove", background="#C6F1F5", anchor="c").grid(row=1, column=6, pady=15, padx=5, sticky="we")
	
	#DEBUXAR AS INTERFACES NA VENTANA
	for interface in lista_interfaces:
		interface.cadro_conectado.grid(row=interface.id+2, column=0, padx=10, sticky="w")
		interface.texto_nome.grid(row=interface.id+2, column=1, padx=5, sticky="we")
		interface.boton_dhcp.grid(row=interface.id+2, column=2, padx=5, sticky="we")
		interface.entrada_ip.grid(row=interface.id+2, column=3, padx=5, sticky="we")
		interface.entrada_mascara.grid(row=interface.id+2, column=4, padx=5, sticky="we")
		interface.entrada_gateway.grid(row=interface.id+2, column=5, padx=5, sticky="we")
		interface.entrada_dns.grid(row=interface.id+2, column=6, padx=5, sticky="we")
		interface.boton.grid(row=interface.id+2, column=7, padx=5, sticky="we")
		
	#CAMPO DE TEXTO CON BARRA DE SCROLL
	
	campo_texto=Text(r, height=10, width=85)
	campo_texto.grid(row=len(lista_interfaces)+2, column=0, columnspan=10, pady=30, padx=15, sticky="w")
	campo_texto.config(state="disable")
	
	escribir_en(campo_texto,">>> Inicio da aplicación: "+str(datetime.datetime.today()))
	
	barra_scroll = ttk.Scrollbar(r, command=campo_texto.yview)

	campo_texto.config(yscrollcommand=barra_scroll.set)
	
	barra_scroll.grid(row=len(lista_interfaces)+2, column=6, padx=10, pady=30, sticky="nse")
	barra_scroll.config(command=campo_texto.yview)

app_init(root)

mainloop()