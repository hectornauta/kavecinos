 def insertarGrid(self,grafico,origenX,origenY,k,division):
        coordenadas = list()
        cuadrados = []
        salto = division/2
        saltoDelCuadrado = division
        x = origenX + salto
        y = origenX + salto
        xDelCuadrado = origenX
        yDelCuadrado = origenY
        random.seed(0)
        ax = grafico.add_subplot()
        ax.plot([origenX,division*self.numero_de_divisiones],[origenY,division*self.numero_de_divisiones])
        ax.set_aspect(1)
        print(self.numero_de_divisiones)

        for i in range(self.numero_de_divisiones):
            x = origenX
            xDelCuadrado = origenX
            for j in range(self.numero_de_divisiones):
                if ((random.randint(0,5))==0):
                    color = 'b'
                else:
                    color = 'g'
                cuadrado = mpatches.Rectangle((xDelCuadrado,yDelCuadrado),saltoDelCuadrado,saltoDelCuadrado,angle = 0.0,color=color, alpha=0.5)
                #grafico.patches.extend([pyplot.Rectangle((x,y),saltoDelCuadrado,saltoDelCuadrado,
                                  #fill=True, color=color, alpha=0.5, zorder=1000,
                                  #transform=grafico.transFigure, figure=grafico)])
                cuadrados.append(cuadrado)
                ax.add_patch(cuadrado)
                x = x + saltoDelCuadrado
                xDelCuadrado = xDelCuadrado + saltoDelCuadrado
            y = y + saltoDelCuadrado
            yDelCuadrado = yDelCuadrado + saltoDelCuadrado
        #for c in cuadrados:
            #print(str(c) + "/n")
    def graficarDataset(self):
        self.numero_de_divisiones = 10 #El video mostraba ~68 (?)
        #logging.debug(archivo.x)
        #print(self.datos.datosCompletos)
        valorDeSeparacion = 1
        pyplot.clf()
        #grafico,ax = pyplot.subplots()
        grafico = pyplot.figure(figsize=(8,8))
        self.colores = colors.TABLEAU_COLORS #10 colores de momento
        
        divisionX = (self.datos.maxX() + valorDeSeparacion - self.datos.minX() + valorDeSeparacion) / (self.numero_de_divisiones)
        divisionY = (self.datos.maxY() + valorDeSeparacion - self.datos.minY() + valorDeSeparacion) / (self.numero_de_divisiones)
        #print(divisionX)
        pyplot.xlim(self.datos.minX() - valorDeSeparacion,self.datos.maxX() + valorDeSeparacion)
        pyplot.ylim(self.datos.minY() - valorDeSeparacion,self.datos.maxY() + valorDeSeparacion)

        for i in range(self.numero_de_divisiones + 1):
            pyplot.axvline(x = self.datos.minX() - valorDeSeparacion + divisionX * i)
            pyplot.axhline(y = self.datos.minY() - valorDeSeparacion + divisionY * i)

        diccionario = {}
        i = 0
        lista = list(self.colores.items())
        for clase in self.datos.clases:
            diccionario[clase] = lista[i][0]#.replace('tab:','')
            i = i + 1
        for punto in self.datos.datosCompletos:
            #print(diccionario[punto[2]])
            pyplot.plot(punto[0],punto[1],marker = 'o',color = diccionario[punto[2]])
        #pyplot.grid()
        origenX = self.datos.minX() - valorDeSeparacion
        origenY = self.datos.minY() - valorDeSeparacion
        k = 7
        self.insertarGrid(grafico,origenX,origenY,k,divisionX)
        #Crear cuadrados
        
        grafico.show()