def melhor_caminho(obj1,obj2,passo):
	posicao1 = (obj1.getX(), obj1.getY())
	posicao2 = (obj2.getX(), obj2.getY())
	distancias = {}
	distancias["esquerda"] = abs(posicao1[0]-passo-posicao2[0])+abs(posicao1[1]-posicao2[1])
	distancias["direita"] = abs(posicao1[0]+passo-posicao2[0])+abs(posicao1[1]-posicao2[1])
	distancias["cima"] = abs(posicao1[0]-posicao2[0])+abs(posicao1[1]-passo-posicao2[1])
	distancias["baixo"] = abs(posicao1[0]-posicao2[0])+abs(posicao1[1]-+passo-posicao2[1])
	maior = min(distancias.values())
	if distancias["direita"] == maior:
		return "direita"
	elif distancias["esquerda"] == maior:
		return "esquerda"
	elif distancias["baixo"] == maior:
		return "baixo"
	elif distancias["cima"] == maior:
		return "cima"

def pinar(obj1,obj2,x,y):
	if obj2.getLado() == 1:
		obj1.setX(obj2.getX()+x)
		obj1.setY(obj2.getY()+y)
		if obj1.getLado() == -1:
			obj1.virarX()
			obj1.mudarLado()
	else:
		obj1.setX(obj2.getX()-x+obj2.getSize()[0]-obj1.getSize()[0])
		obj1.setY(obj2.getY()+y)
		if obj1.getLado() == 1:
			obj1.virarX()
			obj1.mudarLado()

def colidiu(obj1, obj2):
	x1 = obj1.getX()
	y1 = obj1.getY()
	tamanho1 = obj1.getSize()
	x2 = obj2.getX()
	y2 = obj2.getY()
	tamanho2 = obj2.getSize()
	testeX1 = (x2<x1<x2+tamanho2[0]) or (x2<x1+tamanho1[0] < x2+tamanho2[0])
	testeX2 = (x1<x2<x1+tamanho1[0]) or (x1<x2+tamanho2[0] < x1+tamanho1[0])
	
	testeY1 = (y2 < y1 < y2+tamanho2[1]) or (y2 < y1 + tamanho1[1] < y2+tamanho2[1])
	testeY2 = (y1 < y2 < y1+tamanho1[1]) or (y1 < y2 + tamanho2[1] < y1+tamanho1[1])
	
	if (testeX1 or testeX2) and (testeY1 or testeY2):
		return True
	return False
