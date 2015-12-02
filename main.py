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
		self.log = ttk.Treeview(self.root, columns=["log"], show="headings", selectmode="none")
		self.log.heading("log", text="Log")
		actualizar_log(self.log,str(time.strftime("%H:%M:%S"))+"  >>> Inicio da aplicación")
		self.listbox_interfaces = ttk.Treeview(self.root, columns=["ifaces"], show="headings", selectmode="browse")
		self.frame_config = ttk.Frame(relief="groove")
		self.interfaces = interfaces_rede(self)
		self.listbox_interfaces.place(x=10, y=60, width=200, height=200)
		app_init(self)
	#	self.time_update()
		self.root.mainloop()
		
	#def time_update(self):
	#	actualizar_log(self.log,str(time.strftime("%H:%M:%S")))
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
		#self.cadro_conectado = ttk.Label(appli.frame_ifaces, text="     ", relief="groove", background="green" if self.conectado else "red")
		
		#self.texto_nome = ttk.Label(appli.frame_ifaces, text=self.nome, width=30)
		#if self.dhcp == None:
		#	self.boton_dhcp = ttk.Button(appli.frame_ifaces, text="", state="disable")
		#else:
		#	self.boton_dhcp = ttk.Button(appli.frame_ifaces, text="Habilitado" if self.dhcp else "Non", command=self.boton_dhcp,
		#					state="normal" if self.conectado else "disable")
							
							
		#self.entrada_ip = ttk.Entry(appli.frame_ifaces, width=15, state="normal" if self.conectado and not self.dhcp else "disable")
		#self.entrada_mascara = ttk.Entry(appli.frame_ifaces, width=15, state="normal" if self.conectado and not self.dhcp else "disable")
		#self.entrada_gateway = ttk.Entry(appli.frame_ifaces, width=15, state="normal" if self.conectado and not self.dhcp else "disable")
		#self.entrada_dns = ttk.Entry(appli.frame_ifaces, width=15, state="normal" if self.conectado else "disable")
		#self.boton = ttk.Button(appli.frame_ifaces, text="CAMBIAR", width=15, command=self.boton_cambiar, state="normal" if self.conectado else "disable")
		
		#ESCRIBIR OS PARAMETROS NAS ENTRADAS DE TEXTO
		#escribir_en(self.entrada_ip,self.ip,True)
		#escribir_en(self.entrada_mascara,self.mascara,True)
		#escribir_en(self.entrada_gateway,self.gateway,True)
		#escribir_en(self.entrada_dns,self.dns,True)
	
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
def actualizar(appli):
	appli.listbox_interfaces = ttk.Treeview(appli.root, columns=["ifaces"], show="headings")
	appli.interfaces = interfaces_rede(appli)
	appli.listbox_interfaces.place(x=10, y=60, width=200, height=200)
	app_init(appli)
	
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
	
def actualizar_log(treeview,texto):
	treeview.insert("","end",values=[texto])
	
def actualizar_configuracion(appli):
		ttk.Label(appli.frame_config, text="DHCP:").grid(row=0, column=0, padx=10, pady=25, sticky="we")
		ttk.Label(appli.frame_config, text="IP:").grid(row=1, column=0, padx=10, pady=10, sticky="we")
		ttk.Label(appli.frame_config, text="NETMASK:").grid(row=2, column=0, padx=10, pady=10, sticky="we")
		ttk.Label(appli.frame_config, text="GATEWAY:").grid(row=3, column=0, padx=10, pady=10, sticky="we")
		
#FUNCIÓN QUE INSERTA AS INTERFACES NA LISTA lista_interfaces
def interfaces_rede(appli):
	
	lista_interfaces = []
	
	#GARDAR NUNHA VARIABLE A SALIDA DO COMANDO netsh interface show interface
	
	#info_interfaces = os.popen("netsh interface show interface | more /S +3").read().splitlines() if Sistema_operativo == "Windows" else None
	
	info_interfaces = iface.datos_interfaces()
	
	for i in range(len(info_interfaces)):
		nome_i = info_interfaces[i][0]
		conectado_i = info_interfaces[i][2]['conectado']
		if conectado_i:
			lista_interfaces.append(
                interface(
                    appli,i,nome_i,conectado_i,info_interfaces[i][2]["addr"],info_interfaces[i][2]["netmask"],
                    info_interfaces[i][2]["gateway"]," ".join(info_interfaces[i][2]["dns"])))
		else:
			lista_interfaces.append(interface(appli,i,nome_i,conectado_i,"","",info_interfaces[i][2]["gateway"],
					" ".join(info_interfaces[i][2]["dns"])))
					
	for i in info_interfaces:
		print i
					
	return sorted(lista_interfaces, key=lambda interface: interface.conectado, reverse=True)
	
#FUNCIÓN QUE CONFIGURA E DEBUXA TODOS OS ELEMENTOS NA VENTANA
def app_init(appli):

	#TITULO
	appli.root.title("Configuración de Interfaces de Rede")
	
	#CONFIGURACION DA VENTANA
	appli.root.resizable(width=False, height=False)
	appli.root.minsize(680,470)
	
	#TEXTO, CAMPOS DE TEXTO E BOTÓNS SEGÚN INTERFACES
	
	Boton_actualizar = ttk.Button(appli.root, text="ACTUALIZAR", command=lambda: actualizar(appli))
	Boton_actualizar.place(x=10,y=10)
	#ttk.Label(appli.frame_titulos, text="INTERFACES DE REDE", relief="groove", background="#C6F1F5", anchor="c", width=30).grid(row=1, column=1, sticky="we")
	#ttk.Label(appli.frame_titulos, text="DHCP", relief="groove", background="#C6F1F5", anchor="c", width=10).grid(row=1, column=2, sticky="we")
	#ttk.Label(appli.frame_titulos, text="IP", relief="groove", background="#C6F1F5", anchor="c", width=20).grid(row=1, column=3, sticky="we")
	#ttk.Label(appli.frame_titulos, text="NETMASK", relief="groove", background="#C6F1F5", anchor="c", width=20).grid(row=1, column=4, sticky="we")
	#ttk.Label(appli.frame_titulos, text="GATEWAY", relief="groove", background="#C6F1F5", anchor="c", width=20).grid(row=1, column=5, sticky="we")
	#ttk.Label(appli.frame_titulos, text="DNS", relief="groove", background="#C6F1F5", anchor="c", width=20).grid(row=1, column=6, sticky="we")
	
	#DEBUXAR AS INTERFACES NA VENTANA
	
	appli.listbox_interfaces.heading("ifaces", text="Interfaces de Rede")
	
	for interface in appli.interfaces:
		appli.listbox_interfaces.insert("","end",values=[interface.nome], 
				tags="conectada" if interface.conectado else "desconectada")
	#	interface.cadro_conectado.grid(row=interface.id, column=0, pady=5, padx=10,  sticky="w")
	#	interface.texto_nome.grid(row=interface.id, column=1, pady=5, padx=5, sticky="we")
	#	interface.boton_dhcp.grid(row=interface.id, column=2, pady=5, padx=5, sticky="we")
	#	interface.entrada_ip.grid(row=interface.id, column=3, pady=5, padx=5, sticky="we")
	#	interface.entrada_mascara.grid(row=interface.id, column=4, pady=5, padx=5, sticky="we")
	#	interface.entrada_gateway.grid(row=interface.id, column=5, pady=5, padx=5, sticky="we")
	#	interface.entrada_dns.grid(row=interface.id, column=6, pady=5, padx=5, sticky="we")
	#	interface.boton.grid(row=interface.id, column=7, pady=5, padx=5, sticky="we")
	
	#COLOR DAS INTERFACES
	
	appli.listbox_interfaces.tag_configure("conectada", background="#eeffe5")
	appli.listbox_interfaces.tag_configure("desconectada", background="#ffd8cc")
	
	#DEBUXAR O CAMPO DE TEXTO (LOG) CON BARRA DE SCROLL
	
	appli.log.place(x=10,y=300,width=650,height=150)
	
	yscroll_log = ttk.Scrollbar(orient="vertical",command=appli.log.yview)
	
	appli.log.configure(yscrollcommand=yscroll_log.set)
	
	yscroll_log.place(x=650,y=300,height=150)
	
	#DEBUXAR AS BARRAS DE SCROOL DA CAIXA DAS INTERFACES
	
	yscroll_ifaces = ttk.Scrollbar(orient="vertical",command=appli.listbox_interfaces.yview)
	xscroll_ifaces = ttk.Scrollbar(orient="horizontal",command=appli.listbox_interfaces.xview)
	
	appli.listbox_interfaces.configure(yscrollcommand=yscroll_ifaces.set, xscrollcommand=xscroll_ifaces.set)
	
	yscroll_ifaces.place(x=200,y=60,height=200)
	xscroll_ifaces.place(x=10,y=258,width=190)
	
	#DEBUXAR O FRAME DAS CONFIGURACIÓNS
	
	appli.frame_config.place(x=250,y=60,width=400,height=200)
	
	actualizar_configuracion(appli)
	
	appli.listbox_interfaces.column("ifaces",width=195)
	
	ttk.Style().configure("TFrame", background="#f9f9f9")
	ttk.Style().configure("TLabel", background="#f9f9f9")
	
if __name__ == "__main__":
	app = App()