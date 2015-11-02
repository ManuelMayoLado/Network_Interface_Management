# -*- coding: utf-8 -*-

from Tkinter import *
import ttk
import os
import time

Sistema_operativo = "Linux" if os.name == "posix" else "Windows"

#CLASE APP

class App():
	def __init__(self):
		self.root = Tk()
		self.textbox = Text(self.root, height=10, width=85, state="disable")
		self.interfaces = interfaces_rede(self)
		app_init(self)
		self.root.mainloop()
		
	#def time_update(self):
	#	escribir_en(self.textbox,str(time.strftime("%H:%M:%S")))
	#	self.root.after(1000, self.time_update)
		

#CLASE INTERFACE
class interface():

	#CONSTRUCTOR
	def __init__(self,appli,id,nome,conectado):
		self.r = appli.root
		self.id = id
		self.nome = nome
		self.conectado = conectado
		
		INFO = os.popen("netsh interface ipv4 show config name=\""+self.nome+"\"").read().splitlines() if Sistema_operativo == "Windows" else ""
		
		while "" in INFO:
			INFO.remove("")
		while " " in INFO:
			INFO.remove(" ")

		for i in INFO:
			print i
		
		try:
			self.dhcp = False if INFO[1].split()[2] == "No" else True
		
			if self.conectado:
				self.ip = INFO[2].split()[2].replace(" ","") if INFO[2].split()[1] == "IP:" else ""
				self.mascara = INFO[3].split()[5].replace(")","").replace(" ","") if INFO[3].split()[0].replace(" ","") == "Prefijo" else ""
				self.gateway = ""
				self.dns = ""
			else:
				self.ip, self.mascara, self.gateway, self.dns = "", "", "", ""
		except:
			self.dhcp = None
			self.ip, self.mascara, self.gateway, self.dns = "", "", "", ""
			self.conectado = False
			escribir_en(appli.textbox,">>> PROBLEMA AO CARGAR A CONFIGURACIÓN DE REDE DE <"+self.nome+">")
		
		#BOTÓNS E CADROS DE TEXTO
		self.cadro_conectado = ttk.Label(self.r, text="     ", relief="groove", background="green" if self.conectado else "red")
		
		self.texto_nome = ttk.Label(self.r, text=self.nome)
		if self.dhcp == None:
			self.boton_dhcp = ttk.Button(self.r, text="", state="disable")
		else:
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
	print "Non esta habilitado"
	
#FUNCION PARA ESCRIBIR ALGO EN UNHA ENTRADA DE TEXTO
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
	info_interfaces = os.popen("netsh interface show interface | more /S +3").read().splitlines() if Sistema_operativo == "Windows" else None
	
	while "" in info_interfaces:
		info_interfaces.remove("")
	
	#RECORRER A VARIABLE info_interfaces PARA SACAR OS DATOS (NOME E ESTADO) E INSERTALOS EN lista_interfaces
	for linea in range(len(info_interfaces)):
		
		if info_interfaces[linea].split()[0] == "Habilitado":
			nome_i = " ".join(info_interfaces[linea].split()[3:])
			conectado_i = True if info_interfaces[linea].split()[1] == "Conectado" else False
			lista_interfaces.append(interface(appli,linea,nome_i,conectado_i))
			
	return lista_interfaces
	
#FUNCIÓN QUE CONFIGURA E DEBUXA TODOS OS ELEMENTOS NA VENTANA
def app_init(appli):
	
	global campo_texto

	#TITULO
	appli.root.title("Configuración de Interfaces")
	
	#CONFIGURACION DA VENTANA
	appli.root.resizable(width=False, height=True)
	appli.root.minsize(0,200)
	
	#TEXTO, CAMPOS DE TEXTO E BOTÓNS SEGÚN INTERFACES
	
	Boton_actualizar = ttk.Button(appli.root, text="ACTUALIZAR", command=actualizar)
	Boton_actualizar.grid(row=0, column=0, columnspan=2, pady=5, padx=5, sticky="w")
	ttk.Label(appli.root, text="INTERFACES DE REDE", relief="groove", background="#C6F1F5", anchor="c").grid(row=1, column=1, pady=15, padx=5, sticky="we")
	ttk.Label(appli.root, text="DHCP", relief="groove", background="#C6F1F5", anchor="c").grid(row=1, column=2, pady=15, padx=5, sticky="we")
	ttk.Label(appli.root, text="IP", relief="groove", background="#C6F1F5", anchor="c").grid(row=1, column=3, pady=15, padx=5, sticky="we")
	ttk.Label(appli.root, text="NETMASK", relief="groove", background="#C6F1F5", anchor="c").grid(row=1, column=4, pady=15, padx=5, sticky="we")
	ttk.Label(appli.root, text="GATEWAY", relief="groove", background="#C6F1F5", anchor="c").grid(row=1, column=5, pady=15, padx=5, sticky="we")
	ttk.Label(appli.root, text="DNS", relief="groove", background="#C6F1F5", anchor="c").grid(row=1, column=6, pady=15, padx=5, sticky="we")
	
	#DEBUXAR AS INTERFACES NA VENTANA
	for interface in appli.interfaces:
		interface.cadro_conectado.grid(row=interface.id+2, column=0, padx=10, sticky="w")
		interface.texto_nome.grid(row=interface.id+2, column=1, padx=5, sticky="we")
		interface.boton_dhcp.grid(row=interface.id+2, column=2, padx=5, sticky="we")
		interface.entrada_ip.grid(row=interface.id+2, column=3, padx=5, sticky="we")
		interface.entrada_mascara.grid(row=interface.id+2, column=4, padx=5, sticky="we")
		interface.entrada_gateway.grid(row=interface.id+2, column=5, padx=5, sticky="we")
		interface.entrada_dns.grid(row=interface.id+2, column=6, padx=5, sticky="we")
		interface.boton.grid(row=interface.id+2, column=7, padx=5, sticky="we")
		
	#DEBUXAR O CAMPO DE TEXTO CON BARRA DE SCROLL
	
	appli.textbox.grid(row=len(appli.interfaces)+2, column=0, columnspan=10, pady=30, padx=15, sticky="w")
	
	barra_scroll = ttk.Scrollbar(appli.root, command=appli.textbox.yview)

	appli.textbox.config(yscrollcommand=barra_scroll.set)
	
	barra_scroll.grid(row=len(appli.interfaces)+2, column=6, padx=10, pady=30, sticky="nse")
	barra_scroll.config(command=appli.textbox.yview)
	
	escribir_en(appli.textbox,">>> Inicio da aplicación: "+str(time.strftime("%H:%M:%S")))
	
if __name__ == "__main__":
	app = App()