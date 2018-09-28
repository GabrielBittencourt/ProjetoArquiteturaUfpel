mypath = "C:\\Users\\xBitt\\Desktop\\contas\\"
maskpath = "C:\\Users\\xBitt\\Desktop\\mascara.jpg"

import glob2 #Módulo glob para abrir todos os arquivos .xyz do diretorio
from PIL import Image as PILImage# Importando o módulo Pillow para abrir a imagem no script
import pytesseract # Módulo para a utilização da tecnologia OCR
import cv2 #Resize
from wand.image import Image #PDF para JPG
from os import listdir
from os.path import isfile, join
import os
import csv

i = 0
j = 0
numeroUC = []
# pdf2jpg
for f in listdir(mypath):
	if f.endswith('.pdf'):
		numeroUC.insert(i, os.path.basename(os.path.splitext(f)[0]))
		i=i+1
		with Image(filename=f, resolution=200) as img:
			img.compression_quality = 99
			if i < 10:
				img.save(filename="contabaixa"+str(0)+str(i)+".jpg")
			else:
				img.save(filename="contabaixa"+str(i)+".jpg")
	else:
		pass
# Resizing
for f in listdir(mypath):
	if f.endswith('0.jpg'):
		j=j+1
		with Image(filename=f) as img:
		    img.resize(2480, 3508)
		    if j < 10:
		    	img.save(filename= "contabaixaresized"+str(0)+str(j)+".jpg")
		    else:
		    	img.save(filename= "contabaixaresized"+str(j)+".jpg")
	else:
		pass

# -- mascara

i=0
img1 = cv2.imread(maskpath)
try:
	for img2 in listdir(mypath):
		if i < 9:
			img2 = cv2.imread('contabaixaresized'+str(0)+str(i+1)+'.jpg')
			dst = img1 & img2
			gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
			cv2.imwrite('contabaixa_mascara'+str(0)+str(i+1)+'.jpg', gray)
			i=i+1
		else:
			img2 = cv2.imread('contabaixaresized'+str(i+1)+'.jpg')
			dst = img1 & img2
			gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
			cv2.imwrite('contabaixa_mascara'+str(i+1)+'.jpg', gray)
			i=i+1
except:
	pass

# -- jpg2txt

i=1
vetortemplate = ['Numero da UC', 'Consumo kWh', 'Faturamento', 'Vencimento', 'Total em Reais\n']
try:
	for text in listdir(mypath):
		vetor = []
		if i < 10:
			text = pytesseract.image_to_string(PILImage.open('contabaixa_mascara'+str(0)+str(i)+'.jpg')) # Extraindo o texto da imagem
		else:
			text = pytesseract.image_to_string(PILImage.open('contabaixa_mascara'+str(i)+'.jpg')) # Extraindo o texto da imagem
		vetor = vetortemplate + text.split()
		vetor.insert(5, numeroUC[i-1])
		# vetor[9] = vetor[9]+' '+vetor[10]
		vetor.pop(10)
		if i < 10:
			file = open("contabaixatxt" + str(0) + str(i) + ".txt","a")
		else:
			file = open("contabaixatxt" + str(i) + ".txt","a")
		
		i=i+1
		
		if i == 2:
			j=0
		else:
			j=5

		while j < len(vetor):
			if vetor[j] == 'Total':
				file.write("")
			elif vetor[j] == 'em':
				file.write("")
			elif vetor[j] == 'Reais':
				file.write("")
			elif vetor[j] == 'Total em Reais\n':
				file.write(vetor[j])
			elif j==len(vetor)-1:
				file.write(vetor[j])
			else:
				file.write(vetor[j]+';')
			
			j += 1
		
except:
	pass

# -- concat

filenames = glob2.glob(mypath + '*.txt')

try:
	with open('saida.txt', 'w') as f:
	    for file in filenames:
	        with open(file) as infile:
	            f.write(infile.read()+'\n')
	        os.remove(file)
except:
	pass

# txt 2 csv

with open('saida.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",") for line in stripped if line)
    with open('saida2.csv', 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(lines)

# Remove jpg
filenames = glob2.glob(mypath + '*.jpg')
for file in filenames:
	os.remove(file)
