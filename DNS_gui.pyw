# -*- coding: utf-8 -*-

from Tkinter import *
import os
import datetime as d

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
		self.dhcp = True if os.popen("netsh interface ipv4 show config name=\""+str(self.nome)+"\" | findstr DHCP").read().split()[2]=="S\xa1" else False
		
		ip = os.popen("netsh interface ipv4 show config name=\""+str(self.nome)+"\" | findstr IP").read().split()
		self.ip = ip[2] if len(ip) > 2 else ""
		
		mascara = os.popen("netsh interface ipv4 show config name=\""+str(self.nome)+"\" | findstr Prefijo").read().split()
		self.mascara = mascara[5][:len(mascara[5])-1] if len(mascara) > 4 else ""
		
		gateway = os.popen("netsh interface ipv4 show addresses name=\""+str(self.nome)+"\" | findstr Puerta").read().split()
		self.gateway = gateway[4] if len(gateway) > 4 else ""
		
		dns = os.popen("netsh interface ipv4 show dns name=\""+str(self.nome)+"\"").read().splitlines()
		self.dns = dns[2][49:].replace(" ","") if len(dns) > 2 and dns[2][49:].replace(" ","") != "ninguno" else ""
		
		self.texto_nome = Label(self.r, text=self.nome, bg="lightgreen" if self.conectado else "indianred1")
		self.boton_dhcp = Button(self.r, text="Habilitado" if self.dhcp else "Non", relief="ridge", command=self.boton_dhcp,
							state="normal" if self.conectado else "disable",
							bg="slategray1" if self.dhcp else "azure2")
		self.entrada_ip = Entry(self.r, text="", state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_mascara = Entry(self.r, text="", state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_gateway = Entry(self.r, text="", state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_dns = Entry(self.r, text="", state="normal" if self.conectado and not self.dhcp else "disable")
		self.boton = Button(self.r, text="CAMBIAR", state="normal" if self.conectado and not self.dhcp else "disable", relief="groove",
							bg="azure2" if self.conectado and not self.dhcp else "lightgray")
		
		#ESCRIBIR OS PARAMETROS NAS ENTRADAS DE TEXTO
		escribir_en(self.entrada_ip,self.ip,True)
		escribir_en(self.entrada_mascara,self.mascara,True)
		escribir_en(self.entrada_gateway,self.gateway,True)
		escribir_en(self.entrada_dns,self.dns,True)
	
	#FUNCION PARA EXECUTAR CANDO SE PULSE O BOTÓN DHCP
	def boton_dhcp(self):
		self.dhcp = False if self.dhcp else True
		
		#UPDATE
		
		self.boton_dhcp.configure(text = "Habilitado" if self.dhcp else "Non",bg="slategray1" if self.dhcp else "azure2")
		self.entrada_ip.configure(state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_mascara.configure(state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_gateway.configure(state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_dns.configure(state="normal" if self.conectado and not self.dhcp else "disable")
		self.boton.configure(state="normal" if self.conectado and not self.dhcp else "disable",
							bg="azure2" if self.conectado and not self.dhcp else "lightgray")
		
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
	
	Boton_actualizar = Button(r, text="ACTUALIZAR", relief="groove", command=actualizar)
	Boton_actualizar.grid(row=0, column=0, pady=15, padx=10, sticky="w")
	Label(r, text="INTERFACES DE REDE", bg="lightblue", relief="groove").grid(row=1, column=0, pady=15, padx=10, sticky="we")
	Label(r, text="DHCP", bg="lightblue", relief="groove").grid(row=1, column=1, pady=15, padx=10, sticky="we")
	Label(r, text="IP", bg="lightblue", relief="groove").grid(row=1, column=2, pady=15, padx=10, sticky="we")
	Label(r, text="NETMASK", bg="lightblue", relief="groove").grid(row=1, column=3, pady=15, padx=10, sticky="we")
	Label(r, text="GATEWAY", bg="lightblue", relief="groove").grid(row=1, column=4, pady=15, padx=10, sticky="we")
	Label(r, text="DNS", bg="lightblue", relief="groove").grid(row=1, column=5, pady=15, padx=10, sticky="we")
	
	#DEBUXAR AS INTERFACES NA VENTANA
	for interface in lista_interfaces:	
		interface.texto_nome.grid(row=interface.id+2, column=0, padx=10, sticky="we")
		interface.boton_dhcp.grid(row=interface.id+2, column=1, padx=10, sticky="we")
		interface.entrada_ip.grid(row=interface.id+2, column=2, padx=10, sticky="we")
		interface.entrada_mascara.grid(row=interface.id+2, column=3, padx=10, sticky="we")
		interface.entrada_gateway.grid(row=interface.id+2, column=4, padx=10, sticky="we")
		interface.entrada_dns.grid(row=interface.id+2, column=5, padx=10, sticky="we")
		interface.boton.grid(row=interface.id+2, column=6, padx=10, sticky="we")
		
	#CAMPO DE TEXTO CON BARRA DE SCROLL
	
	campo_texto=Text(r, height=10, width=100)
	campo_texto.grid(row=len(lista_interfaces)+2, column=0, columnspan=6, pady=30, padx=25, sticky="w")
	campo_texto.config(state="disable")
	
	escribir_en(campo_texto,"Inicio da aplicación: "+str(d.datetime.today()))
	
	barra_scroll = Scrollbar(r, command=campo_texto.yview)

	campo_texto.config(yscrollcommand=barra_scroll.set)
	
	barra_scroll.grid(row=len(lista_interfaces)+2, column=5, padx=10, pady=30, sticky="nse")
	barra_scroll.config(command=campo_texto.yview)

app_init(root)

mainloop()