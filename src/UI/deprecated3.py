def graficarDataset(self,k):
        valorDeSeparacionX = (self.datos.maxX()-self.datos.minX())*0.1
        valorDeSeparacionY = (self.datos.maxY()-self.datos.minY())*0.1
        limiteInferiorX = self.datos.minX() - valorDeSeparacionX
        limiteSuperiorX =self.datos.maxX() + valorDeSeparacionX
        limiteInferiorY = self.datos.minY() - valorDeSeparacionY
        limiteSuperiorY =self.datos.maxY() + valorDeSeparacionY
        pyplot.clf()
        grafico = pyplot.figure(figsize=(8,8))
        ax = grafico.add_subplot()
        ax.plot(limiteInferiorX,limiteInferiorY)
        if self.obtenerRA():
            ax.set_aspect(1)
        if(len(self.datos.clases)>9):
            self.colores = colors.CSS4_COLORS
        else:
            self.colores = colors.TABLEAU_COLORS
        
        #divisionX = (self.datos.maxX() + valorDeSeparacionX - self.datos.minX() + valorDeSeparacionY) / (self.numero_de_divisiones)
        #divisionY = (self.datos.maxY() + valorDeSeparacionY - self.datos.minY() + valorDeSeparacionY) / (self.numero_de_divisiones)
        #print(divisionX)
        pyplot.xlim(limiteInferiorX,limiteSuperiorX)
        pyplot.ylim(limiteInferiorY,limiteSuperiorY)

        pyplot.xlabel(self.datos.atributos[0])
        pyplot.ylabel(self.datos.atributos[1])

        xDelBucle = limiteInferiorX
        yDelBucle = limiteInferiorY
        
        if(self.obtenerRejilla()):
            while(xDelBucle<limiteSuperiorX):
                pyplot.axvline(x = xDelBucle,linestyle = '-',marker = ",",linewidth=0.2)
                xDelBucle = xDelBucle + self.obtenerCelda()
            while(yDelBucle<limiteSuperiorY):
                pyplot.axhline(y = yDelBucle,linestyle = '-',marker = ",",linewidth=0.2)
                yDelBucle = yDelBucle + self.obtenerCelda()

        self.diccionario = {}
        i = 0
        lista = list(self.colores.items())
        for clase in self.datos.clases:
            self.diccionario[clase] = lista[i][0]
            i = i + 1

        
        puntosEntrenamiento = self.datos.obtenerDatosEntrenamiento(self.porcentajeEntrenamiento)

        for punto in puntosEntrenamiento:
            pyplot.plot(punto[0],punto[1],marker = '.',color = self.diccionario[punto[2]])
            
        leyendas = []
        for clase in self.datos.clases:
            leyendas.append(Line2D([0],[0],lw=4,marker='o',color=self.diccionario[clase]))
        pyplot.legend(leyendas, self.datos.clases)

        if (self.radioCuadrado.isChecked()==True):
            self.insertarGrid(grafico,ax,limiteInferiorX,limiteSuperiorX,limiteInferiorY,limiteSuperiorY,k,self.obtenerCelda())
        else:
            self.insertarCirculos(grafico,ax,limiteInferiorX,limiteSuperiorX,limiteInferiorY,limiteSuperiorY,k,self.obtenerCelda())
        #Crear cuadrados
        
        grafico.show()