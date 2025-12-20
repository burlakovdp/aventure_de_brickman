import tkinter as tk
import os.path
"""
Ce que nous dit Wikipédia
=========================

Le portable pixmap file format (PPM), le portable graymap file
format (PGM) et le portable bitmap file format (PBM) sont des formats
de fichier graphique utilisés pour les échanges. Ils ont été définis
et sont utilisés par le projet NetPBM. Ils proposent des
fonctionnalités élémentaires et sont utilisés pour convertir les
fichiers de type pixmap, graymap et bitmap entre différentes
plateformes. Plusieurs applications désignent cet ensemble de trois
formats comme le format PNM (portable anymap


Portable Bitmap File Format (PBM)
=================================

Ces fichiers possèdent l’extension « .pbm ». En pratique l’image est
représentée par une matrice de pixel ; chaque pixels étant représenté
par un booléen (True -> blanc, False -> noir)


Portable Graymap File Format (PGM)
==================================

Ces fichiers possèdent l’extension « .pgm ». En pratique l’image est
représentée par une matrice de pixel ; chaque pixels étant représenté
par un octet (0 -> noir, 255 -> blanc, toutes les valeurs entre 0 et
255 -> gris)



Portable Pixmap File Format (PPM)
====================================

Ces fichiers possèdent l’extension « .ppm ». En pratique l’image est
représentée par une matrice de pixels ; chaque pixels étant représenté
par un triplet d’octet correspondant à sa couleur au format RGB

"""

## déclaration des fonctions exportées lors du from pnm import *
__all__ = ['voir_matrice','voir_fichier','fichier_vers_matrice','matrice_vers_fichier']

##########################
##                      ##
##      Utilitaires     ##
##                      ##
##########################

class FormatError(Exception): pass

def hexa(couleur):
    S="0123456789ABCDEF"
    (r,g,b)=couleur
    rr = S[r//16] + S[r%16]
    gg = S[g//16] + S[g%16]
    bb = S[b//16] + S[b%16]
    return "#"+rr+gg+bb


def fichier_vers_liste(nom_fichier) :
    """Lit le fichier et renvoie la liste des chaines de caractères
    élémentaires qu'il contient. Chaque chaîne de caractère
    élémentaire est délimitée par des espaces ou des retours à la
    ligne.
    """

    return [y for x in open(nom_fichier).readlines() \
              for y in x.strip('\n').split('#')[0].split(' ') if y != '']



###############################
##                           ##
##     Matrice de pixels     ##
##                           ##
###############################

def dimensions(M):
    return (len(M),len(M[0]))


def matrice_vide(n,m):
    return [ [None] * m for i in range(n)]


def matrice_booléens(L,n,m):
    couleurs = {"0":0 , "1":1} # 0 blanc 1 noir
    M = matrice_vide(n,m)
    for i in range(n):
        for j in range(m):
            M[i][j] = couleurs[L[i*m+j]]
    return M


def matrice_couleur(L,couleur_max,n,m):
    M = matrice_vide(n,m)
    k=0
    for i in range(n):
        for j in range(m):
            r = int(L[k+0])*255//couleur_max
            g = int(L[k+1])*255//couleur_max
            b = int(L[k+2])*255//couleur_max            
            assert max(r,g,b) < 256
            M[i][j] = (r,g,b)
            k += 3
    return M
    

def matrice_octets(L,couleur_max,n,m):
    M = matrice_vide(n,m)
    for i in range(n):
        for j in range(m):
            k=i*m+j
            M[i][j] = int(L[k])*255//couleur_max
    return M



###############################
##                           ##
##     Fonction  d’import    ##
##                           ##
###############################

def pbm_vers_matrice(nom_fichier):
    try:
        L = fichier_vers_liste(nom_fichier)
        Format = L[0]
        assert Format=='P1'
        Largeur = int(L[1])
        Hauteur = int(L[2])
        M=matrice_booléens(L[3:],Hauteur,Largeur)
    except:
        raise FormatError("Format invalide")
    return M


def pgm_vers_matrice(nom_fichier):
    try:
        L = fichier_vers_liste(nom_fichier)
        Format = L[0]
        assert Format=='P2'
        largeur = int(L[1])
        hauteur = int(L[2])
        couleur_max = int(L[3])
        if couleur_max != 255:
            print("[Warning] La couleur maximum n’est pas 255.",end=" ")
            print("Recalcul des couleurs en octet.")
        M=matrice_octets(L[4:],couleur_max,hauteur,largeur)
    except:
        raise FormatError("Format invalide")
    return M


def ppm_vers_matrice(nom_fichier):
    try:
        L = fichier_vers_liste(nom_fichier)
        Format = L[0]
        assert Format=='P3'
        largeur = int(L[1])
        hauteur = int(L[2])
        couleur_max = int(L[3])
        if couleur_max != 255:
            print("[Warning] La couleur maximum n’est pas 255.",end=" ")
            print("Recalcul des couleurs en octet.")
        M=matrice_couleur(L[4:],couleur_max,hauteur,largeur)
    except:
        raise FormatError("Format invalide")
    return M
    

def fichier_vers_matrice(nom_fichier):
    if not os.path.isfile(nom_fichier):
        raise FileNotFoundError(f"Le fichier « {nom_fichier} » n’existe pas.")
    extensions = nom_fichier[-4:]
    if extensions == ".ppm":
        return ppm_vers_matrice(nom_fichier)
    elif extensions == ".pgm":
        return pgm_vers_matrice(nom_fichier)
    elif extensions == ".pbm":
        return pbm_vers_matrice(nom_fichier)
    else:        
        raise FormatError("Nom de fichier invalide")



###############################
##                           ##
##    Fonction d’affichage   ##
##                           ##
###############################

def matrice_rgb(M):
    (n,m)=dimensions(M)
    RGB=matrice_vide(n,m)
    if   type(M[0][0]) == bool:
        f = (lambda n: (255*(1-n),255*(1-n),255*(1-n)))
    elif type(M[0][0]) == int:
        f = (lambda n: (n,n,n))
    else:
        f = (lambda n: n)
    for i in range(n):
        for j in range(m):
            RGB[i][j] = f(M[i][j])
    return RGB


def affiche_pixel(M,i,j,pixel_size,quadrillage):
    if quadrillage and pixel_size >= 10:
        bordure='1'
    else:
        bordure='0'        
    couleur = hexa(M[i][j])
    p = ( j   *pixel_size, i    *pixel_size)
    q = ((j+1)*pixel_size, (i+1)*pixel_size)
    Dessin.create_rectangle(p,q,fill=couleur,width=bordure)


def voir_matrice(M,quadrillage=False,nom="Afficheur d’image PNM"):
    global Dessin
    RGB = matrice_rgb(M)
    Hauteur,Largeur = dimensions(RGB)    
    taille_maximale = 800
    taille_pixel = min(taille_maximale//Hauteur, taille_maximale//Largeur)
    root = tk.Tk()
    root.title(nom)
    Dessin = tk.Canvas(root,width=Largeur*taille_pixel,height=Hauteur*taille_pixel)
    Dessin.pack()
    bouton_quitter=tk.Button(root,text='Quitter',command=root.destroy)
    bouton_quitter.pack()
    
    for i in range(Hauteur) :
        for j in range(Largeur) :
            affiche_pixel(RGB,i,j,taille_pixel,quadrillage)
    root.mainloop()

        
def voir_fichier(nom_fichier,quadrillage=False) :
    M=fichier_vers_matrice(nom_fichier)
    voir_matrice(M,quadrillage=quadrillage,nom=nom_fichier)
    


###############################
##                           ##
##     Fonction  d’export    ##
##                           ##
###############################

def matrice_vers_ppm(M,nom_fichier):
    f = open(nom_fichier,'w',encoding='utf-8')
    f.write('P3\n')
    (n,m)=dimensions(M)
    f.write(f'{m} {n}\n')
    f.write("255\n")
    for i in range(n):
        for j in range(m):
            r,g,b = M[i][j]
            f.write(f'{r} {g} {b}\n')
        f.write("\n")
    f.close()


def matrice_vers_pgm(M,nom_fichier):
    f = open(nom_fichier,'w',encoding='utf-8')
    f.write('P2\n')
    (n,m)=dimensions(M)
    f.write(f'{m} {n}\n')
    f.write("255\n")
    for i in range(n):
        ligne=""
        for j in range(m):
            suivant = f"{M[i][j]} "
            if len(ligne)+len(suivant) > 70:
                f.write(ligne+"\n")
                ligne=suivant
            else:
                ligne += suivant
        f.write(ligne+"\n")
    f.close()


def matrice_vers_pbm(M,nom_fichier):
    f = open(nom_fichier,'w',encoding='utf-8')
    f.write('P1\n')
    (n,m)=dimensions(M)
    f.write(f'{m} {n}\n')
    for i in range(n):
        ligne=""
        for j in range(m):
            suivant = f"{int(M[i][j])} "
            if len(ligne)+len(suivant) > 70:
                f.write(ligne+"\n")
                ligne=suivant
            else:
                ligne += suivant
        f.write(ligne+"\n")
    f.close()
                

def matrice_vers_fichier(M,nom_fichier):
    extensions = nom_fichier[-4:]
    if extensions == ".ppm":
        matrice_vers_ppm(M,nom_fichier)
    elif extensions == ".pgm":
        matrice_vers_pgm(M,nom_fichier)
    elif extensions == ".pbm":
        matrice_vers_pbm(M,nom_fichier)
    else:        
        raise FormatError("Nom de fichier invalide")
 
