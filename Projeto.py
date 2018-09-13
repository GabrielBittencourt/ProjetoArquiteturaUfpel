mypath = "Caminho do .py (C:....)"
mascaestaaqui = "Caminho do arquivo mascara.jpg (C:...\mascara.jpg)"
import glob2
from PIL import Image as PILImage# Importando o módulo Pillow para abrir a imagem no script
import pytesseract # Módulo para a utilização da tecnologia OCR
import cv2
from wand.image import Image
from os import listdir
from os.path import isfile, join
import os
import xlwt
import xlrd

i = 0
j = 0

# pdf2jpg
for f in listdir(mypath):
	if f.endswith('.pdf'):
		i=i+1
		with Image(filename=f, resolution=200) as img:
			img.compression_quality = 99
			img.save(filename="contabaixa"+str(i)+".jpg")
	else:
		pass

# Resizing
for f in listdir(mypath):
	if f.endswith('0.jpg'):
		j=j+1
		with Image(filename=f) as img:
		    img.resize(2480, 3508)
		    img.save(filename= "contabaixaresized"+str(j)+".jpg")
	else:
		pass

# -- mascara

i=0
img1 = cv2.imread(mascaestaaqui)
try:
	for img2 in listdir(mypath):
		img2 = cv2.imread('contabaixaresized'+str(i+1)+'.jpg')
		dst = img1 & img2
		gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
		cv2.imwrite('contabaixa_mascara'+str(i+1)+'.jpg', gray)
		i=i+1
except:
	pass

# -- jpg2txt

i=1
try:
	for text in listdir(mypath):
		text = pytesseract.image_to_string(PILImage.open('contabaixa_mascara'+str(i)+'.jpg'), -psm 11) # Extraindo o texto da imagem
		file = open("contabaixatxt" + str(i) + ".txt","w")
		file.write(text)
		print(text)
		i=i+1
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

# -- xls

textfiles = [ join(mypath,f) for f in listdir(mypath) if isfile(join(mypath,f)) and '.txt' in  f]

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False        


style = xlwt.XFStyle()
style.num_format_str = '###000'  

for textfile in textfiles:
    f = open(textfile, 'r+')
    row_list = []
    for row in f:
        row_list.append(row.split('|'))
    column_list = zip(*row_list)
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Sheet1')
    i = 0
    for column in column_list:
        for item in range(len(column)):
            value = column[item].strip()
            if is_number(value):
                worksheet.write(item, i, float(value), style=style)
            else:
                worksheet.write(item, i, value)
        i+=1
    workbook.save(textfile.replace('.txt', '.xls'))

filenames = glob2.glob(mypath + '*.jpg')
for file in filenames:
	if(file != 'mascara.jpg'):
		os.remove(file)
# except:
# 	pass
