import socket
import sys
import math
from threading import Thread
import time
import hashlib
import os

#---Getting Ip and Port--
IP = "127.0.0.1"
PORT = int(sys.argv[1])
#-----------------------
def hash_calc(data,cond):
	global IP
	if cond == "port":
		h = (IP + str(data)).encode('utf-8')
	elif cond == "file":
		h = (str(data)).encode('utf-8')
	h= hashlib.sha1(h)
	h= h.hexdigest()
	h = h[0] + h[1]
	h = int(h,16)
	return h
def file_download(filename,p):
	if node.port == p:
		print("File has been downloaded....")
		return
	global IP
	ready = "121" + filename
	s = socket.socket()
	s.connect((IP,p))
	s.send(ready.encode())
	with open(filename,'wb') as f:
		while True:
			data = s.recv(1024)
			pata = data.decode()
			if pata == "yes":
				break
			f.write(data)
		print("Download Done")
		f.close()
	s.close()
def get_file(filename,node):
	global IP
	check = os.path.isfile(filename)
	if check == True:
		print("File already present..still want to download ?")
		dec = input()
		if dec == "no":
			return
	if filename not in node.files:
		node.files.append(filename)
	ok = "ok"
	done = "done"
	msg = "777" + filename
	scene = "121" + filename
	recvd = ''
	f_hash = hash_calc(filename,"file")
	#f = open(filename,'wb')
	node.make_fingerTable()
	s = socket.socket()
	s.connect((IP,node.successor))
	s.sendall(msg.encode())
	data = s.recv(10)
	data = data.decode()
	if data[0:3] == "yes":
		print("file foundddddd")
		#s.sendall(scene.encode())
		with open(filename,'wb') as f:
			while True:
				ja = s.recv(1024)
				lpp = ja.decode()
				if lpp == "yes":
					break
				print("Recvd is: ")
				#print(ja)
				f.write(ja)
				#print("write done..")
			print("closing fileee...")
			f.close()
		#s.sendall(done.encode())
		print("Obtained File....")
		s.close()
		return
	elif data[0:3] == "noo":
		#s.close()
		while data[0:3] != "yes":
			s.close()
			pk = int(data[3:])
			if pk == node.port:
				print("No one in network have this file...")
				break
				return
			s = socket.socket()
			s.connect((IP,pk))
			s.sendall(msg.encode())
			data = s.recv(10)
			data = data.decode()
		s.sendall(scene.encode())
		with open(filename,'rb') as f:
			while True:
				jarv = s.recv(1024)
				jk = jarv.decode()
				if jk == "yes":
					break
				f.write(jarv)
			f.close()
		#s.sendall(done.encode())
		print("Download Done !!!")
		s.close()
		return

def file_insert(filename,node):
	global IP
	hop = str(node.port)
	check = os.path.isfile(filename)
	if check == False:
		print("Invalid filename...")
		return
	ff = filename.encode('utf-8')
	f = hashlib.sha1(ff)
	f = f.hexdigest()
	f = f[0] + f[1]
	file_hash = int(f,16)
	node_hash = node.id
	node.make_fingerTable()
	if node.predecessor == node.port and node.successor == node.port:
		print("Saving on myself..")
		node.files.append(filename)
		return
	index = -1
	if file_hash > node_hash:
		for i in range(len(node.ftp)):
			if file_hash < node.ftp[i]:
				index = node.fingertable[i]
		if index == -1:
			index = node.successor
		print("Got the node for the file")
		print(index)
		s = socket.socket()
		s.connect((IP,index))
		se = "999" + filename
		s.sendall(se.encode())
		time.sleep(0.5)
		s.sendall(hop.encode())
		print("File Sent ...")
		s.close()
		return
	else:
		print("I am responsible for this file..")
		if file_hash not in node.files:
			node.files.append(filename)
		return

def menu_function():
	print("Type 1 for Successor and Predecessor")
	print("Type 2 for FingerTable")
	print("Type 3 to PUT a file")
	print("Type 4 to GET a file")
	print("Type close to exit")

class ChordNode(object):
	def __init__(self,port,hashed):
		self.port = port
		self.id = hashed
		self.successor = port
		self.predecessor = port
		self.fingertable = []
		self.ftp = []
		self.files = []
	def make_fingerTable(self):
		global IP
		self.fingertable = []
		sucs = []
		hash_sucs = []
		if self.successor == self.port:
			#self.fingertable.append(self.port)
			#print("Exiting")
			return
		s_suc = self.successor
		#sucs.append(s_suc)
		while True:
			#print("Looping thru sucs")
			if s_suc == self.port:
				break
			try:
				sucs.append(s_suc)
				s_sock = socket.socket()
				s_sock.connect((IP,s_suc))
				msg = "101" 
				s_sock.send(msg.encode())
				ns = s_sock.recv(10)
				ns = int(ns.decode())
				#print("suc recvd is")
				#print(ns)
				#sucs.append(ns)
				time.sleep(0.5)
				nss = s_sock.recv(64)
				nss = int(nss.decode())
				hash_sucs.append(nss)
				s_sock.close()
				#print("GOINGGGGG")
			except socket.error as err:
				print("error")
				return
			s_suc = ns
		j = 0
		while j<6:
			#print("Looping thru powasss")
			power = pow(2,j)
			if power > 16:
				break
			val = self.port + power
			#print(val)
			for i in range(len(sucs)):
				#print("val in succ")
				#print(val)
				if val == sucs[i]:
					self.fingertable.append(val)
					self.ftp.append(hash_sucs[i])
			j += 1
			#print("POWERSSSSS")
		#print("FingerTable has been Made")
		if len(self.fingertable) == 0:
			self.fingertable.append(self.successor)

def server_process(node,sock):
	global IP
	bb = "both"
	yes = "yes"
	nbb = "not both"
	response = sock.recv(64)
	response = response.decode()
	if response[0:3] == "101":
		m = str(node.successor)
		sock.send(m.encode())
		time.sleep(0.5)
		hl = str(node.id)
		sock.send(hl.encode())
		#print("succ send done")
		return
	elif response[0:3] == "102":
		m = str(node.predecessor)
		sock.send(m.encode())
		#print("pred send done")
		return
	elif response[0:3] == "103":
		n = int(response[3:])
		node.successor = n
		#print("succ done")
		return
	elif response[0:3] == "104":
		n = int(response[3:])
		node.predecessor = n
		#print("pred done")
		return
	elif response[0:3] == "999":
		filename = response[3:]
		f_hash = hash_calc(filename,"file")
		n_hash = node.id
		caller = sock.recv(10)
		caller = int(caller.decode())
		if f_hash < n_hash:
			node.files.append(filename)
			file_download(filename,caller)
		else:
			print("What the eff")
			sop = socket.socket()
			sop.connect((IP,node.successor))
			pl = "888" + filename
			sop.sendall(pl.encode())
			time.sleep(0.5)
			poper = str(caller)
			sop.sendall(poper.encode())
			sop.close()
		return
	elif response[0:3] == "888":
		filename = response[3:]
		f_hash = hash_calc(filename,"file")
		caller = sock.recv(10)
		caller = int(caller.decode())
		node.files.append(filename)
		file_download(filename,caller)
		return
	elif response[0:3] == "777":
		filename = response[3:]
		check = os.path.isfile(filename)
		if check == True:
			sock.sendall(yes.encode())
			time.sleep(0.5)
			print("Sending File..//..")
			with open(filename,'rb') as file:
				for data in file:
					#print(data)
					sock.sendall(data)
					#k = sock.recv(10)
					#k = k.decode()
					#if k == "done":
						#file.close()
						#return
				time.sleep(0.5)
				sock.send(yes.encode())
				file.close()
			return
		else:
			syu = "noo" + str(node.successor)
			sock.sendall(syu.encode())
			return
	elif response[0:3] == "121":
		fila = response[3:]
		print("Sending File....")
		with open(fila,'rb') as f:
			for data in f:
				sock.sendall(data)
			time.sleep(0.5)
			sock.sendall(yes.encode())
			f.close()
		return
	#If nothing above happens then it means response is a port so,
	n_port = int(response)
	#print(n_port)
	if(node.successor == node.port and node.predecessor == node.port):
		node.successor = n_port
		node.predecessor = n_port
		sock.send(bb.encode()) #shows that no other node is there in DHT. 
		#print("bb done")
	else:
		sock.send(nbb.encode()) #needs stablization
		#print("nbb done")
		mm = "110"
		nmm = "111"
		ttt = str(node.successor)
		tt = str(node.port)
		t = str(node.predecessor)
		if (node.port > n_port and ((n_port > node.predecessor and node.port > node.predecessor) or (n_port < node.predecessor and node.port < node.predecessor))):
			node.predecessor = n_port
			st_send = mm + t 
			sock.send(st_send.encode())
			time.sleep(0.5)
			#print("st_send  done")
			sock.send(tt.encode())
			#print("tt send done")
		elif (node.port < n_port and node.predecessor > node.port and n_port > node.predecessor):
			node.predecessor = n_port
			stt = mm + t 
			sock.send(stt.encode())
			time.sleep(0.5)
			#print("stt send done")
			sock.send(tt.encode())
			#print("tt stt send done")
		else:
			#print("entered iot done")
			iot = nmm + ttt
			sock.send(iot.encode())
			#print("iot send done")
def client_process(node,sock,n_port):
	global IP
	oo = "103"   #update successor
	ooo = "104"  #update predecessor
	i = str(node.port)
	sock.send(i.encode())
	res = sock.recv(64)
	res = res.decode()
	cond = True
	while cond:
		if res == "both":
			node.successor = n_port
			node.predecessor = n_port
			cond = False
		elif res == "not both":
			says = sock.recv(64)
			says = says.decode()
			if says[0:3] == "110":
				pred = int(says[3:])
				node.predecessor = pred
				time.sleep(0.5)
				suc = sock.recv(10)
				suc = int(suc.decode())
				node.successor = suc
				time.sleep(0.5)
				s = socket.socket()
				s.connect((IP,pred))
				st_to = oo + i 
				s.send(st_to.encode())
				time.sleep(0.5)
				s2 = socket.socket()
				s2.connect((IP,suc))
				st_too = ooo + i
				s2.send(st_too.encode())
				cond = False
			elif says[0:3] == "111":
				prt = int(says[3:])
				soc = socket.socket()
				sock = soc
				sock.connect((IP,prt))
				sock.send(i.encode())
				res = sock.recv(64)
	#Creating GUI
	menu_function()
	user = input()
	while user != "close":
		if user == "1":
			print ("Node port = "+ str (node.port))
			print ("Node successor = "+ str (node.successor))
			print ("Node predecessor = "+ str (node.predecessor))
		elif user == "2":
			node.make_fingerTable()
			print(node.fingertable)
		elif user == "3":
			#PUT
			print("Enter Name of File: ")
			fi = input()
			file_insert(fi,node)
		elif user == "4":
			#GET
			print("Enter Name of file you want to download: ")
			filename = input()
			get_file(filename,node)
		menu_function()
		user = input()
	#if the current node is going to exit then inform successor of predecessor and predecessor of successor
	ii = ooo + str(node.predecessor)
	iii = oo + str(node.successor)
	tempsock = socket.socket()
	tempsock.connect((IP,node.successor))
	tempsock.send(ii.encode())
	tempsock.close()
	tempsock2 = socket.socket()
	tempsock2.connect((IP,node.predecessor))
	tempsock2.send(iii.encode())
	tempsock2.close()
	#sock.recv(10)
	#print("wesy hee")
	os._exit(0)

if __name__ == "__main__":
	print("Welcome to DC++")
	addr = (IP + str(PORT)).encode('utf-8')
	port_hash = hashlib.sha1(addr)
	port_hash = port_hash.hexdigest()
	port_hash = port_hash[0]+port_hash[1]
	port_hash = int(port_hash,16)
	node = ChordNode(PORT,port_hash)
	s = socket.socket()
	s.bind((IP,PORT))
	s.listen(10)
	known = input("Do you know any other node in network?")
	if known == "yes":
		p = input("Enter the port of node: ")
		p = int(p)
		ss = socket.socket()
		ss.connect((IP,p))
		print("You're now part of DC++")
		Thread(target=client_process, args=(node,ss,p,)).start()
		while True:
			conn,addr = s.accept()
			#print("New Member connected.")
			Thread(target=server_process, args=(node,conn,)).start()
	elif known == "no":
		print("Server is listening...")
		ss = socket.socket()
		ss.connect((IP,PORT))
		Thread(target=client_process, args=(node,ss,PORT,)).start()
		while True:
			conn,addr = s.accept()
			#print("New Member added.")
			Thread(target=server_process, args=(node,conn,)).start()



















