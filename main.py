# -*- coding: utf-8 -*-

#
# FUNCIONA EN WINDOWS E EN LINUX
#
# GUI basada en <Tkinter>
# Configuración das interfaces basado en:
#	Windows -> netsh
#	Linux 	-> ifconfig

from Tkinter import *
import ttk
import os
import time

import iface

Sistema_operativo = "Linux" if os.name == "posix" else "Windows"

#CLASE APP

class App():
	def __init__(self):
		self.root = Tk()
		self.textbox = Text(self.root, height=10, width=85, state="disable")
		escribir_en(self.textbox,">>> Inicio da aplicación: "+str(time.strftime("%H:%M:%S")))
		self.frame_titulos = ttk.Frame(self.root, relief="groove")
		self.frame_ifaces = ttk.Frame(self.root, relief="groove")
		self.interfaces = interfaces_rede(self)
		self.frame_titulos.grid(padx=40, row=1, column=0, columnspan=7)
		self.frame_ifaces.grid(padx=10, pady=5, row=2, column=0, columnspan=8)
		app_init(self)
		#self.time_update()
		self.root.mainloop()
		
	#def time_update(self):
	#	escribir_en(self.textbox,str(time.strftime("%H:%M:%S")))
	#	self.root.after(1000, self.time_update)
		

#CLASE INTERFACE
class interface():

	#CONSTRUCTOR
	def __init__(self,appli,id,nome,conectado,ip,mascara,gateway,dns):
		self.r = appli.root
		self.id = id
		self.nome = nome
		self.conectado = conectado
		self.ip = ip
		self.mascara = mascara
		self.gateway = gateway
		self.dns = dns
		
		self.dhcp = None
		
		#BOTÓNS E CADROS DE TEXTO
		self.cadro_conectado = ttk.Label(appli.frame_ifaces, text="     ", relief="groove", background="green" if self.conectado else "red")
		
		self.texto_nome = ttk.Label(appli.frame_ifaces, text=self.nome, width=30)
		if self.dhcp == None:
			self.boton_dhcp = ttk.Button(appli.frame_ifaces, text="", state="disable")
		else:
			self.boton_dhcp = ttk.Button(appli.frame_ifaces, text="Habilitado" if self.dhcp else "Non", command=self.boton_dhcp,
							state="normal" if self.conectado else "disable")
							
							
		self.entrada_ip = ttk.Entry(appli.frame_ifaces, width=15, state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_mascara = ttk.Entry(appli.frame_ifaces, width=15, state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_gateway = ttk.Entry(appli.frame_ifaces, width=15, state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_dns = ttk.Entry(appli.frame_ifaces, width=15, state="normal" if self.conectado else "disable")
		self.boton = ttk.Button(appli.frame_ifaces, text="CAMBIAR", width=15, command=self.boton_cambiar, state="normal" if self.conectado else "disable")
		
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
		self.entrada_dns.configure(state="normal" if self.conectado else "disable")
		self.boton.configure(state="normal" if self.conectado else "disable")
		
	def boton_cambiar(self):
		print ("DHCP:",self.boton_dhcp.cget("text"), "IP:",self.entrada_ip.get(), "MASK:",self.entrada_mascara.get(),
				"GATEWAY:",self.entrada_gateway.get(), "DNS:",self.entrada_dns.get())
		
#FUNCIÓN PARA VOLVER A CARGAR TODO
def actualizar(apli):
	apli.interfaces = interfaces_rede(apli)
	app_init(apli)
	
#FUNCIÓN PARA ESCRIBIR ALGO EN UNHA ENTRADA DE TEXTO
def escribir_en(entrada,texto,borrar=False):
	estado = entrada.cget("state")
	entrada.config(state="normal")
	if borrar:
		entrada.delete(0,END)
		entrada.insert(END,texto)
	else:
		entrada.insert(END,texto+"\n")
	entrada.config(state=estado)
		
#FUNCIÓN QUE INSERTA AS INTERFACES NA LISTA lista_interfaces
def interfaces_rede(appli):
	
	lista_interfaces = []
	
	#GARDAR NUNHA VARIABLE A SALIDA DO COMANDO netsh interface show interface
	
	#info_interfaces = os.popen("netsh interface show interface | more /S +3").read().splitlines() if Sistema_operativo == "Windows" else None
	
	info_interfaces = iface.datos_interfaces()
	
	for i in range(len(info_interfaces)):
		nome_i = info_interfaces[i][0]
		conectado_i = True if 'addr' in info_interfaces[i][2] else False
		if conectado_i:
			lista_interfaces.append(
                interface(
                    appli,i,nome_i,conectado_i,info_interfaces[i][2]["addr"],info_interfaces[i][2]["netmask"],
                    info_interfaces[i][2]["gateway"]," ".join(info_interfaces[i][2]["dns"])))
		else:
			lista_interfaces.append(interface(appli,i,nome_i,conectado_i,"","",info_interfaces[i][2]["gateway"],
					" ".join(info_interfaces[i][2]["dns"])))
	
	return lista_interfaces
	
#FUNCIÓN QUE CONFIGURA E DEBUXA TODOS OS ELEMENTOS NA VENTANA
def app_init(appli):

	#TITULO
	appli.root.title("Configuración de Interfaces de Rede")
	
	#CONFIGURACION DA VENTANA
	appli.root.resizable(width=False, height=True)
	appli.root.minsize(0,200)
	
	#TEXTO, CAMPOS DE TEXTO E BOTÓNS SEGÚN INTERFACES
	
	Boton_actualizar = ttk.Button(appli.root, text="ACTUALIZAR", command=lambda: actualizar(appli))
	Boton_actualizar.grid(row=0, column=0, columnspan=2, pady=5, padx=5, sticky="w")
	ttk.Label(appli.frame_titulos, text="INTERFACES DE REDE", relief="groove", background="#C6F1F5", anchor="c", width=30).grid(row=1, column=1, sticky="we")
	ttk.Label(appli.frame_titulos, text="DHCP", relief="groove", background="#C6F1F5", anchor="c", width=10).grid(row=1, column=2, sticky="we")
	ttk.Label(appli.frame_titulos, text="IP", relief="groove", background="#C6F1F5", anchor="c", width=20).grid(row=1, column=3, sticky="we")
	ttk.Label(appli.frame_titulos, text="NETMASK", relief="groove", background="#C6F1F5", anchor="c", width=20).grid(row=1, column=4, sticky="we")
	ttk.Label(appli.frame_titulos, text="GATEWAY", relief="groove", background="#C6F1F5", anchor="c", width=20).grid(row=1, column=5, sticky="we")
	ttk.Label(appli.frame_titulos, text="DNS", relief="groove", background="#C6F1F5", anchor="c", width=20).grid(row=1, column=6, sticky="we")
	
	#DEBUXAR AS INTERFACES NA VENTANA

	for interface in appli.interfaces:
		interface.cadro_conectado.grid(row=interface.id, column=0, pady=5, padx=10,  sticky="w")
		interface.texto_nome.grid(row=interface.id, column=1, pady=5, padx=5, sticky="we")
		interface.boton_dhcp.grid(row=interface.id, column=2, pady=5, padx=5, sticky="we")
		interface.entrada_ip.grid(row=interface.id, column=3, pady=5, padx=5, sticky="we")
		interface.entrada_mascara.grid(row=interface.id, column=4, pady=5, padx=5, sticky="we")
		interface.entrada_gateway.grid(row=interface.id, column=5, pady=5, padx=5, sticky="we")
		interface.entrada_dns.grid(row=interface.id, column=6, pady=5, padx=5, sticky="we")
		interface.boton.grid(row=interface.id, column=7, pady=5, padx=5, sticky="we")
		
	#DEBUXAR O CAMPO DE TEXTO CON BARRA DE SCROLL
	
	appli.textbox.grid(row=len(appli.interfaces)+2, column=0, columnspan=7, pady=30, padx=15, sticky="w")
	
	barra_scroll = ttk.Scrollbar(appli.root, command=appli.textbox.yview)

	appli.textbox.config(yscrollcommand=barra_scroll.set)
	
	barra_scroll.grid(row=len(appli.interfaces)+2, column=6, padx=10, pady=30, sticky="nse")
	barra_scroll.config(command=appli.textbox.yview)
	
if __name__ == "__main__":
	app = App()