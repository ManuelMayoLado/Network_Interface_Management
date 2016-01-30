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

TAMANHO_VENTANA = [820,470]
ALTO_FRAME = 200
ALTO_LOG = 170

#CLASE APP

class App():
	def __init__(self):
		self.root = Tk()
		
		self.text_log = Text(self.root,relief="flat",state="disable")
		
		#FRAME IFACES
		
		canvas_iface = Canvas(self.root,relief="flat",borderwidth=0,background="#f9f9f9",
								highlightcolor="#f9f9ff",highlightbackground="#f9f9f9")
		self.frame_ifaces = Frame(canvas_iface,relief="flat",background="#f9f9f9")
		
		ifaces_scroll = ttk.Scrollbar(canvas_iface,orient="vertical",command=canvas_iface.yview)
		canvas_iface.configure(yscrollcommand=ifaces_scroll.set)

		canvas_iface.place(x=10,y=60,width=TAMANHO_VENTANA[0]-20,height=ALTO_FRAME)
		
		canvas_iface.create_window((0,0),window=self.frame_ifaces, anchor="nw")
		
		def onFrameConfigure(canvas):
			canvas.configure(scrollregion=canvas.bbox("all"))
		
		self.frame_ifaces.bind("<Configure>",lambda event, canvas_iface=canvas_iface: onFrameConfigure(canvas_iface))
		
		ifaces_scroll.place(x=TAMANHO_VENTANA[0]-35,y=0,width=17,height=ALTO_FRAME)
		
		self.interfaces = interfaces_rede(self)
		
		self.text_log.place(x=10,y=280,width=TAMANHO_VENTANA[0]-20,height=ALTO_LOG)
		escribir_en(self.text_log,str(time.strftime("%H:%M:%S"))+"  >>> Inicio da aplicación")
		
		estilo_global()
		
		app_init(self)
		
		#self.time_update()
	
		self.root.mainloop()
		
	#def time_update(self):
	#	escribir_en(self.text_log,str(time.strftime("%H:%M:%S")))
	#	self.root.after(1000, self.time_update)
		

#CLASE INTERFACE
class interface():

	#CONSTRUCTOR
	def __init__(self,appli,id,nome,conectado,ip,mascara,gateway,dns,dhcp):
		self.r = appli.root
		self.id = id
		self.nome = nome
		self.conectado = conectado
		self.ip = ip
		self.mascara = mascara
		self.gateway = gateway
		self.dns = dns
		self.dhcp = dhcp
		
		#BOTÓNS E CADROS DE TEXTO
		self.cadro_conectado = ttk.Label(appli.frame_ifaces, text="     ",
							relief="groove", background="green" if self.conectado else "red")
		
		self.texto_nome = ttk.Label(appli.frame_ifaces, text=self.nome, width=30)
		if self.dhcp == None:
			self.boton_dhcp = ttk.Button(appli.frame_ifaces, text="", state="disable")
		else:
			self.boton_dhcp = ttk.Button(appli.frame_ifaces, text="DHCP" if self.dhcp else "Estática",
							command=self.boton_dhcp, state="normal" if self.conectado else "disable")
							
		self.entrada_ip = ttk.Entry(appli.frame_ifaces, width=15,
								state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_mascara = ttk.Entry(appli.frame_ifaces, width=15,
								state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_gateway = ttk.Entry(appli.frame_ifaces, width=15,
								state="normal" if self.conectado and not self.dhcp else "disable")
		self.entrada_dns = ttk.Entry(appli.frame_ifaces, width=20,
								state="normal" if self.conectado else "disable")
		self.boton = ttk.Button(appli.frame_ifaces, text="CAMBIAR",
								command=self.boton_cambiar, state="normal" if self.conectado else "disable")
		#ESCRIBIR OS PARAMETROS NAS ENTRADAS DE TEXTO
		escribir_en(self.entrada_ip,self.ip,True)
		escribir_en(self.entrada_mascara,self.mascara,True)
		escribir_en(self.entrada_gateway,self.gateway,True)
		escribir_en(self.entrada_dns,self.dns,True)
	
	#FUNCION PARA EXECUTAR CANDO SE PULSE O BOTÓN DHCP
	def boton_dhcp(self):
		dhcp = False if self.boton_dhcp.cget("text") == "DHCP" else True
		
		#UPDATE
		
		self.boton_dhcp.configure(text = "DHCP" if dhcp else "Estática")
		self.entrada_ip.configure(state="normal" if self.conectado and not dhcp else "disable")
		self.entrada_mascara.configure(state="normal" if self.conectado and not dhcp else "disable")
		self.entrada_gateway.configure(state="normal" if self.conectado and not dhcp else "disable")
		self.entrada_dns.configure(state="normal" if self.conectado else "disable")
		self.boton.configure(state="normal" if self.conectado else "disable")
		
	def boton_cambiar(self):
		novo_dhcp = True if self.boton_dhcp.cget("text") == "DHCP" else False
		novo_ip = self.entrada_ip.get()
		novo_mask = self.entrada_mascara.get()
		novo_gateway = self.entrada_gateway.get()
		novo_dns = self.entrada_dns.get()
		print ("DHCP: "+str(novo_dhcp), "IP: "+novo_ip, "MASK: "+novo_mask,
				"GATEWAY: "+novo_gateway, "DNS: "+novo_dns)
		if not ([self.ip,self.mascara,self.gateway,self.dns,self.dhcp] == 
						[novo_ip,novo_mask,novo_gateway,novo_dns,novo_dhcp]):
			if Sistema_operativo == "Windows":
				cambio_config = False
				try:
					#GLOBAL
					if not ([self.ip,self.mascara,self.gateway,self.dhcp] ==
									[novo_ip,novo_mask,novo_gateway,novo_dhcp]):
						if novo_dhcp and not (novo_dhcp == self.dhcp):
							print("netsh interface ip set address name="+'"'+self.nome+"'"+" "+"source=dhcp")
							os.popen("netsh interface ip set address name="+'"'+self.nome+'"'+" "+"source=dhcp")
							cambio_config = True
						elif not novo_dhcp:
							os.popen("netsh interface ip set address name="+'"'+self.nome+'"'+" "+
										"static "+novo_ip+" "+novo_mask+" "+novo_gateway)
							print("netsh interface ip set address name="+'"'+self.nome+'"'+" "+
										"static "+novo_ip+" "+novo_mask+" "+novo_gateway)
							cambio_config = True
						else:
							print ">> Sen cambios na configuracion"
					else:
						print ">> Sen cambios na configuracion 2"
					#DNS
					if (not novo_dns == self.dns) or cambio_config:
						lista_dns = novo_dns.split(" ")
						if lista_dns[0]:
							for dns in range(len(lista_dns)):
								print("netsh interface ip add dnsserver name="+'"'+self.nome+'"'+
											" "+lista_dns[dns]+" "+
											"index="+str(dns))
								os.popen("netsh interface ip add dnsserver name="+'"'+self.nome+'"'+
											" "+lista_dns[dns]+" "+
											"index="+str(dns))
						else:
							print("netsh interface ip delete dnsserver name="+'"'+self.nome+'"'+" "+"all")
							os.popen("netsh interface ip delete dnsserver name="+'"'+self.nome+'"'+" "+"all")
					else:
						print ">> Sen cambios no DNS"
				except:
					print "ERROR! - Non puido cambiarse a configuracion"
			else:
				None
		else:
			print "Sen cambios"
				
#FUNCIÓN PARA VOLVER A CARGAR TODO, EXECUTASE AO PULSAR O BOTÓN "ACTUALIZAR"
def actualizar(appli):
	appli.interfaces = interfaces_rede(appli)
	app_init(appli)
	
#FUNCIÓN PARA ESCRIBIR ALGO EN UNHA ENTRADA DE TEXTO
def escribir_en(entrada,texto,borrar=False):
	estado = entrada.cget("state")
	entrada.config(state="normal")
	if borrar:
		entrada.delete(0,END)
		entrada.insert(END,texto)
	else:
		entrada.insert('1.0',texto+"\n")
	entrada.config(state=estado)

#FUNCIÓN QUE DETERMINA O ESTILO GLOBAL		
def estilo_global():
	#ttk.Style().configure("TFrame", background="#f9f9f9")
	ttk.Style().configure("TLabel", background="#f9f9f9")
	ttk.Style().configure("TCheckbutton", background="#f9f9f9")
		
#FUNCIÓN QUE INSERTA AS INTERFACES NA LISTA lista_interfaces
def interfaces_rede(appli):
	
	lista_interfaces = []
	
	info_interfaces = iface.datos_interfaces()
	
	for i in range(len(info_interfaces)):
		nome_i = info_interfaces[i][0]
		conectado_i = info_interfaces[i][2]['conectado']
		if conectado_i:
			lista_interfaces.append(
                interface(
                    appli,i,nome_i,conectado_i,info_interfaces[i][2]["addr"],info_interfaces[i][2]["netmask"],
                    info_interfaces[i][2]["gateway"]," ".join(info_interfaces[i][2]["dns"]),
					info_interfaces[i][2]["dhcp"]))
		else:
			lista_interfaces.append(interface(appli,i,nome_i,conectado_i,"","",info_interfaces[i][2]["gateway"],
					" ".join(info_interfaces[i][2]["dns"]),info_interfaces[i][2]["dhcp"]))
					
	#for i in info_interfaces:
	#	print i
					
	return sorted(lista_interfaces, key=lambda interface: interface.conectado, reverse=True)
	
#FUNCIÓN QUE CONFIGURA E DEBUXA TODOS OS ELEMENTOS NA VENTANA
def app_init(appli):

	#TITULO
	appli.root.title("Configuración de Interfaces de Rede")
	
	#CONFIGURACION DA VENTANA
	appli.root.resizable(width=False, height=False)
	appli.root.minsize(TAMANHO_VENTANA[0],TAMANHO_VENTANA[1])
	
	#TEXTO, CAMPOS DE TEXTO E BOTÓNS SEGÚN INTERFACES
	
	Boton_actualizar = ttk.Button(appli.root, text="ACTUALIZAR", command=lambda: actualizar(appli))
	Boton_actualizar.place(x=10,y=10)
	
	#DEBUXAR AS INTERFACES NA VENTANA
	
	num_row = 0
	nome_y = 5
	
	for interface in appli.interfaces:
		interface.cadro_conectado.grid(row=num_row, column=0, pady=5, padx=10,  sticky="w")
		interface.texto_nome.place(x=45,y=nome_y)
		num_row += 1
		interface.boton_dhcp.grid(row=num_row, column=0, pady=5, padx=5, sticky="we")
		ttk.Label(appli.frame_ifaces, text="IP:").grid(row=num_row, column=1, pady=5, padx=5, sticky="we")
		interface.entrada_ip.grid(row=num_row, column=2, pady=5, padx=5, sticky="we")
		ttk.Label(appli.frame_ifaces, text="MASK:").grid(row=num_row, column=3, pady=5, padx=5, sticky="we")
		interface.entrada_mascara.grid(row=num_row, column=4, pady=5, padx=5, sticky="we")
		ttk.Label(appli.frame_ifaces, text="GW:").grid(row=num_row, column=5, pady=5, padx=5, sticky="we")
		interface.entrada_gateway.grid(row=num_row, column=6, pady=5, padx=5, sticky="we")
		ttk.Label(appli.frame_ifaces, text="DNS:").grid(row=num_row, column=7, pady=5, padx=5, sticky="we")
		interface.entrada_dns.grid(row=num_row, column=8, pady=5, padx=5, sticky="we")
		interface.boton.grid(row=num_row, column=9, pady=5, padx=5, sticky="we")
		num_row += 1
		nome_y += 64
		
	#BARRA DE SCROLL LOG
		
	log_scroll = ttk.Scrollbar(appli.root)
	
	appli.text_log.config(yscrollcommand=log_scroll.set)
	log_scroll.config(command=appli.text_log.yview)
	
	log_scroll.place(x=TAMANHO_VENTANA[0]-25,y=TAMANHO_VENTANA[1]-(ALTO_LOG+20),width=17,height=ALTO_LOG)
	
	
if __name__ == "__main__":
	app = App()