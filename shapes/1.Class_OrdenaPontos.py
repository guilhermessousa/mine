class Point:

#GEOPANDAS
#teste

    def indexa_pontos(pts):
        pts_cp1 = pts.copy()
        pts_cp2 = pts_cp1.copy()
        for ponto in pts_cp1:
            ponto.insert(3,-1)
        x = pts_cp1[0][1]
        y = pts_cp1[0][2]
        pts_cp2.sort(key = lambda p: (p[1]-x)**2+(p[2]-y)**2)
        p_i = pts_cp2[-1]
        pts_cp2.remove(p_i)
        i=2
        for ponto2 in pts_cp1:
            if ponto2[1]==p_i[1] and ponto2[2]==p_i[2]:
                ponto2[3] = 1
                break
        while len(pts_cp2) > 1:
            pts_cp2.sort(key = lambda p: (p[1]-p_i[1])**2+(p[2]-p_i[2])**2)
            for ponto3 in pts_cp1:
                if ponto3[1]==pts_cp2[0][1] and ponto3[2]==pts_cp2[0][2]:
                    ponto3[3] = i
                    break
            p_i = pts_cp2[0]
            pts_cp2.remove(p_i)
            i+=1
        for ponto4 in pts_cp1:
            if ponto4[1]==pts_cp2[0][1] and ponto4[2]==pts_cp2[0][2]:
                ponto4[3] = i
                break
        Ordem = []
        for ponto5 in pts_cp1:
            Ordem.append(ponto5[3])
        return Ordem

    def cria_pontos(acronym,long,lat):
        pontos = []
        for I, acr in enumerate(acronym):
            pontos.append([acr, long[I], lat[I]])
        return pontos
