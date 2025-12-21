import tkinter as tk
import pnm
import random

root = tk.Tk()
root.title("Aventure de Brickman")
root.state('zoomed')

Hauteur = 820
Largeur = 980
delta = 20
delta_min = 10
bg_couleur = "black"

tag_interface = "interface"
tag_mure = "mure"
tag_brickman = "brickman"
tag_adversaire = "adversaire"
tag_gagner = "gagner"
tag_limbo = "limbo"
tag_tuto = "tuto"
tag_kitsoin = "kitsoin"
tag_transition = "transition"
tag_boss = "boss"

Dessin=tk.Canvas(root,height=Hauteur,width=Largeur,bg=bg_couleur)
Dessin.pack()


def carre(cords, couleur, couleur_outline, tag):
    x0, y0, x1, y1 = cords
    Dessin.create_rectangle(x0, y0, x1, y1, fill=couleur, outline=couleur_outline, tags=tag)

def cord_transformer(x, y, delta):
    x0 = (x*delta)+3
    y0 = (y*delta)+3
    x1 = x*delta+delta+3
    y1 = y*delta+delta+3
    return (x0, y0, x1, y1)

def affiche_matrice(M, x0, y0, delta, couleur, bordure_couleur, tag):
        columns, lines = pnm.dimensions(M)
        for i in range(columns):
            for j in range(lines):
                if M[i][j] == 1:
                    carre(cord_transformer(j+x0, i+y0, delta), couleur, bordure_couleur, tag)

def affiche_matrice_rgb(M, x0, y0, delta, bordure, tag ):
        columns, lines = pnm.dimensions(M)
        for i in range(columns):
            for j in range(lines):
                carre(cord_transformer(j+x0,i+y0, delta), pnm.hexa(M[i][j]), bordure, tag)

class Interface():
    def __init__(self):
        self.lampe_etat = True
        self.lumiere_etat = False
        self.lampe_lumiere_etat = False
        self.titre_etat = False
        self.lignes_etat = False
        self.lignes_min_etat = False
        self.logo_etat = False
        self.projet_etat = False
        self.temps = 0
        self.tic = 10
        self.sante_statut_etat = False
        self.brickman_sante_position_X0 = 1
        self.brickman_sante_position_Y = 39
        self.boss_sante_position_X0 = 1
        self.boss_sante_position_Y = 1
        self.ligne_sante = 47
        self.lampe = pnm.ppm_vers_matrice("./interface/logo/lampe.ppm")
        self.lumiere = pnm.ppm_vers_matrice("./interface/logo/lumiere.ppm")
        self.titre = pnm.ppm_vers_matrice("./interface/logo/titre.ppm")
        self.logo = pnm.ppm_vers_matrice("./interface/logo/logo.ppm")
        self.projet = pnm.pbm_vers_matrice("./interface/logo/projet.ppm")
        self.affichage()

    def affichage(self):
        Dessin.delete(tag_interface)
        if self.lampe_etat:
            self.creer_lampe()
        if self.lampe_lumiere_etat:
            self.creer_lumiere_lampe()
        if self.titre_etat:
            self.creer_titre()
        if self.lignes_etat:
            self.creer_lignes(delta)
        if self.lignes_min_etat:
            self.creer_lignes(delta_min)
        if self.logo_etat:
            self.creer_logo()
        if self.projet_etat:
            self.creer_projet()
        if carte.niv_chargeur >= 0 and brickman.vie_etat:
            self.brickman_sante_statut()
            #self.sante_statut_etat = True
        if carte.niv_chargeur == 4 and brickman.vie_etat:
            self.boss_sante_statut()
        
    def creer_lignes(self, delta):
        x0 = 3
        for _ in range(Largeur//delta):
            Dessin.create_line(x0+delta, 0, x0+delta, Hauteur+2, fill='grey')
            x0 += delta
        y0 = 3
        for _ in range(Hauteur//delta):
            Dessin.create_line(0, y0+delta, Largeur+3, y0+delta, fill='grey')
            y0 += delta

    def creer_ligne_carre(self, x0, y0, x1, y1, couleur, couleur_outline):
        if x0 == x1:
            if y0 < y1:
                for i in range(y0, y1+1):
                    carre(cord_transformer(x0, i, delta), couleur, couleur_outline, tag_interface)
            else:
                for i in range(y0, y1-1, -1):
                    carre(cord_transformer(x0, i, delta), couleur, couleur_outline, tag_interface)
        elif y0 == y1:
            if x0 < x1:
                for i in range(x0, x1+1):
                    carre(cord_transformer(i, y0, delta), couleur, couleur_outline, tag_interface)
            else:
                for i in range(x0, x1-1, -1):
                    carre(cord_transformer(i, y0, delta), couleur, couleur_outline, tag_interface)

    def creer_titre(self):
        affiche_matrice_rgb(self.titre, 2, 15, delta, "black", tag_interface)

    def creer_logo(self):
        affiche_matrice_rgb(self.logo, 60, 60, delta_min, "black", tag_interface)

    def creer_projet(self):
        affiche_matrice(self.projet, 60, 68, delta_min, "black", "white", tag_interface)

    def creer_lampe(self):
        affiche_matrice_rgb(self.lampe, 33, 2, delta, "black", tag_interface)
        Dessin.create_line(793, 44, 793, 0, fill="white", tags=tag_interface)
    
    def creer_lumiere_lampe(self):
        affiche_matrice_rgb(self.lumiere, 33, 6, delta, "black", tag_interface)

    def brickman_sante_statut(self):
        brick_counter = (brickman.sante*self.ligne_sante)//100
        for i in range(brick_counter):
            carre(cord_transformer(self.brickman_sante_position_X0+i, self.brickman_sante_position_Y, delta), "red", "black", tag_interface)
        for i in range(self.ligne_sante-brick_counter):
            carre(cord_transformer(brick_counter+i+1, self.brickman_sante_position_Y, delta), "black", "red", tag_interface)
        
    def boss_sante_statut(self):
        brick_counter = (boss.sante*self.ligne_sante*2)//200
        #print(brick_counter)
        if brick_counter < self.ligne_sante:
            #ligne 1
            for i in range(self.ligne_sante):
                carre(cord_transformer(self.boss_sante_position_X0+i, self.boss_sante_position_Y+1, delta), "black", "red", tag_interface)
            for i in range(self.ligne_sante - (brick_counter%self.ligne_sante)):
                    carre(cord_transformer((brick_counter%self.ligne_sante)+i+1, self.boss_sante_position_Y, delta), "black", "red", tag_interface)
            #ligne 0
            for i in range(brick_counter):
                carre(cord_transformer(self.boss_sante_position_X0+i, self.boss_sante_position_Y, delta), "red", "black", tag_interface)
        else:
            #ligne 0
            for i in range(self.ligne_sante):
                carre(cord_transformer(self.boss_sante_position_X0+i, self.boss_sante_position_Y, delta), "red", "black", tag_interface)
            #ligne 1
            if brick_counter == self.ligne_sante*2:
                for i in range(self.ligne_sante):
                    carre(cord_transformer(self.boss_sante_position_X0+i, self.boss_sante_position_Y+1, delta), "red", "black", tag_interface)
            else:
                for i in range(brick_counter%self.ligne_sante):
                    carre(cord_transformer(self.boss_sante_position_X0+i, self.boss_sante_position_Y+1, delta), "red", "black", tag_interface)
                
                for i in range(self.ligne_sante - (brick_counter%self.ligne_sante)):
                    carre(cord_transformer((brick_counter%self.ligne_sante)+i+1, self.boss_sante_position_Y+1, delta), "black", "red", tag_interface)
                

class Limbo():
    def __init__(self):
        self.limbo_letters = pnm.pbm_vers_matrice("./limbo/limbo.pbm")
        self.temps = 0
        self.tic = 10
        self.sortie_etat = False
        self.sortie_X = 0
        self.sortie_Y = 0
        self.affichage()
    
    def affichage(self):
        Dessin.delete(tag_limbo)
        if brickman.vie_etat == False:
            if not self.sortie_etat:
                self.sortie_X = random.randint(0, 48)
                self.sortie_Y = random.randint(10, 40)
                self.sortie_etat = True
            self.limbo()
            self.creer_sortie()
            self.reveil()
    
    def limbo(self):
        affiche_matrice(self.limbo_letters, 0, 0, delta, "white", "black", tag_limbo)
    
    def creer_sortie(self):
        carre(cord_transformer(self.sortie_X, self.sortie_Y, delta), "pink", "black", tag_limbo)
    
    def reveil(self):
        if brickman.position_X == self.sortie_X and brickman.position_Y == self.sortie_Y:
                self.sortie_etat = False
                brickman.deplacement_etat = False
                brickman.vie_etat = True
                brickman.sante = 100
                objet.kitsoin_etat = False
                if carte.niv_chargeur == 4:
                    brickman.position_X = 30
                    brickman.position_Y = 30
                Dessin.delete(tag_limbo)
                adversaire.affichage()
                etat.affichage()           

    def collision(self, x, y):
        if self.limbo_letters[y][x] == 1:
            return True
        return False

class Carte():
    def __init__(self):
        self.niveau_1 = pnm.pbm_vers_matrice("./cartes/niveau_1.pbm")
        self.niveau_2 = pnm.pbm_vers_matrice("./cartes/niveau_2.pbm")
        self.niveau_3 = pnm.pbm_vers_matrice("./cartes/niveau_3.pbm")
        self.niveau_boss = pnm.pbm_vers_matrice("./cartes/boss_carte.pbm")
        self.tuto = pnm.pbm_vers_matrice("./interface/tuto/tuto.pbm")
        self.bouger = pnm.pbm_vers_matrice("./interface/tuto/bouger.pbm")
        self.sante = pnm.pbm_vers_matrice("./interface/tuto/sante.pbm")
        self.temps = 0
        self.tic = 10
        self.niv_chargeur = -1
        self.affichage()
    
    def affichage(self):
        Dessin.delete(tag_tuto)
        Dessin.delete(tag_mure)
        if self.niv_chargeur == 0 and brickman.vie_etat == True:
            self.tutoriel()
            self.sortie_tuto()
        if self.niv_chargeur > 0 and brickman.vie_etat == True:
            self.tic = 1000
            self.labyrinthe()

    def labyrinthe(self):
        if self.niv_chargeur == 1:
            affiche_matrice(self.niveau_1, 0, 0, delta, "white", "black", tag_mure)
        if self.niv_chargeur == 2:
            affiche_matrice(self.niveau_2, 0, 0, delta, "white", "black", tag_mure)
        if self.niv_chargeur == 3:
            affiche_matrice(self.niveau_3, 0, 0, delta, "white", "black", tag_mure)
        if self.niv_chargeur == 4:
            affiche_matrice(self.niveau_boss, 0, 0, delta, "white", "black", tag_mure)
    
    def tutoriel(self):            
        carre(cord_transformer(10,20, delta), "pink", "black", tag_tuto)
        affiche_matrice(self.tuto, 0, 0, delta, "white", "black", tag_tuto)
        affiche_matrice(self.bouger, 66, 60, delta_min, "white", "black", tag_tuto)
        affiche_matrice(self.sante, 8, 58, delta_min, "white", "black", tag_tuto)
        
    def tuto_collision(self, x, y):
        if self.tuto[y][x] == 1:
            return True
        return False

    def collision(self, x, y):
        if self.niv_chargeur == 1:
            if self.niveau_1[y][x] == 1:
                return True
        elif self.niv_chargeur == 2:
            if self.niveau_2[y][x] == 1:
                return True
        elif self.niv_chargeur == 3:
            if self.niveau_3[y][x] == 1:
                return True
        elif self.niv_chargeur == 4:
            if self.niveau_boss[y][x] == 1:
                return True
        return False

    def sortie_tuto(self):
        if brickman.position_X == 10 and brickman.position_Y == 20:
            Dessin.delete(tag_tuto)
            brickman.position_X = 0
            brickman.position_Y = 1
            carte.niv_chargeur = 1
            adversaire.affichage()
            etat.affichage()  

class Brickman():
    def __init__(self):
        self.position_X = 10
        self.position_Y = 21
        self.temps = 0
        self.tic = 10
        self.sante = 100
        self.vie_etat = True
        self.deplacement_etat = False
        self.affichage()
    
    def affichage(self):
        Dessin.delete(tag_brickman)
        if carte.niv_chargeur  == 0:
            self.creer_brickman(self.position_X, self.position_Y)
        if carte.niv_chargeur >= 1:
            self.creer_brickman(self.position_X, self.position_Y)
            self.dommage()
            self.mort()

    def creer_brickman(self, x, y):
        carre(cord_transformer(x, y, delta), "yellow", "black", tag_brickman)

    def deplacer_haut(self, event):
        if brickman.vie_etat and carte.niv_chargeur == 0:
            if self.position_Y == 0:
                return
            elif carte.tuto_collision(self.position_X, self.position_Y-1):
                return 
            self.position_Y -= 1
        elif brickman.vie_etat and carte.niv_chargeur >= 1:
            if self.position_Y == 0:
                return
            elif carte.collision(self.position_X, self.position_Y-1):
                carre(cord_transformer(self.position_X, self.position_Y-1, delta), "red", "black", tag_mure)
                return 
            self.position_Y -= 1
        elif not brickman.vie_etat:
            if self.position_Y == 0:
                return
            elif limbo.collision(self.position_X, self.position_Y-1):
                return
            self.position_Y -= 1

    def deplacer_bas(self, event):
        if brickman.vie_etat and carte.niv_chargeur == 0:
            if self.position_Y == Hauteur//delta-1:
                return 
            elif carte.tuto_collision(self.position_X, self.position_Y+1):
                return 
            self.position_Y += 1
        elif brickman.vie_etat:
            if self.position_Y == Hauteur//delta-1:
                return 
            elif carte.collision(self.position_X, self.position_Y+1):
                carre(cord_transformer(self.position_X, self.position_Y+1, delta), "red", "black", tag_mure)
                return
            self.position_Y += 1
        elif not brickman.vie_etat:
            if self.position_Y == Hauteur//delta-1:
                return
            elif limbo.collision(self.position_X, self.position_Y+1):
                return
            self.position_Y += 1

    def deplacer_gauche(self, event):
        if brickman.vie_etat and carte.niv_chargeur == 0:
            if self.position_X == 0:
                return
            elif carte.tuto_collision(self.position_X-1, self.position_Y):
                return 
            self.position_X -= 1
        elif brickman.vie_etat:
            if self.position_X == 0:
                return 
            elif carte.collision(self.position_X-1, self.position_Y):
                carre(cord_transformer(self.position_X-1, self.position_Y, delta), "red", "black", tag_mure)
                return
            self.position_X -= 1
        elif not brickman.vie_etat:
            if self.position_X == 0:
                return
            elif limbo.collision(self.position_X-1, self.position_Y):
                return
            self.position_X -= 1

    def deplacer_droite(self, event):
        if brickman.vie_etat and carte.niv_chargeur == 0:
            if self.position_X == Largeur//delta-1:
                return
            elif carte.tuto_collision(self.position_X+1, self.position_Y):
                return 
            self.position_X += 1
        elif brickman.vie_etat:
            if self.position_X == Largeur//delta-1:
                return 
            elif carte.collision(self.position_X+1, self.position_Y):
                carre(cord_transformer(self.position_X+1, self.position_Y, delta), "red", "black", tag_mure)
                return
            self.position_X += 1
        elif not brickman.vie_etat:
            if self.position_X == Largeur//delta-1:
                return
            elif limbo.collision(self.position_X+1, self.position_Y):
                return
            self.position_X += 1
    
    def dommage(self):
        if self.position_X == adversaire.position_X and self.position_Y == adversaire.position_Y:
            brickman.sante -= 5
    
    def mort(self):
        if self.sante <= 0:
            Dessin.delete(tag_mure)
            Dessin.delete(tag_interface)
            Dessin.delete(tag_adversaire)
            Dessin.delete(tag_gagner)
            Dessin.delete(tag_kitsoin)
            Dessin.delete(tag_transition)
            Dessin.delete(tag_boss)
            carte.tic = 10
            self.vie_etat = False
            if not self.deplacement_etat:
                self.position_X = random.randint(0, 48)
                self.position_Y = random.randint(10, 40)
                self.deplacement_etat = True

class Adversaire():
    def __init__(self):
        self.temps = 0
        self.tic = 10
        self.position_X = 5
        self.position_Y = 3
        self.sens_etat = True
        self.affichage()
    
    def affichage(self):
        Dessin.delete(tag_adversaire)
        if carte.niv_chargeur == 4:
            self.position_X = -1
            self.position_Y = -1
        if carte.niv_chargeur >= 1 and carte.niv_chargeur < 4 and brickman.vie_etat:
            self.deplacement()
            self.creer_guerrier()
            self.tic = 500

    def creer_guerrier(self):
        carre(cord_transformer(self.position_X, self.position_Y, delta), "red", "black", tag_adversaire)
    
    def deplacement(self):
        if self.position_Y == 3:
            self.sens_etat = True

        if self.position_Y == 5:
            self.sens_etat = False

        if self.sens_etat == True:
            self.position_Y += 1

        if self.sens_etat == False:
            self.position_Y -= 1

class Etat():
    def __init__(self):
        self.temps = 0
        self.tic = 1
        self.gagner_X = 3  #49
        self.gagner_Y = 2  #37
        self.transition_X = 3
        self.transition_Y = 1
        self.transition_etat = False
        self.affichage()
        
    def affichage(self):
        Dessin.delete(tag_gagner)
        Dessin.delete(tag_transition)
        if carte.niv_chargeur > 0 and carte.niv_chargeur < 4 and brickman.vie_etat:
            self.transition()
    
    def transition(self):
        carre(cord_transformer(self.transition_X, self.transition_Y, delta), "pink", "black", tag_transition)
        if self.transition_X == brickman.position_X and self.transition_Y == brickman.position_Y and self.transition_etat == False:
            carte.niv_chargeur += 1
            Dessin.delete(tag_mure)
            Dessin.delete(tag_adversaire)
            Dessin.delete(tag_kitsoin)
            Dessin.delete(tag_brickman)
            print(f'niveau = {carte.niv_chargeur}')
            if carte.niv_chargeur == 1:
                pass
            elif carte.niv_chargeur == 2:
                pass
            elif carte.niv_chargeur == 3:
                pass
            elif carte.niv_chargeur == 4:
                brickman.position_X = 2
                brickman.position_Y = 20
            carte.affichage()
            self.transition_etat = True
        elif self.transition_X != brickman.position_X or self.transition_Y != brickman.position_Y:
            self.transition_etat = False

    def gagner(self):
        carre(cord_transformer(self.gagner_X, self.gagner_Y, delta), "green", "black", tag_gagner)
        if self.gagner_X == brickman.position_X and self.gagner_Y == brickman.position_Y:
            pass
            #print("YOU WIN!")

class Objet():
    def __init__(self):
        self.temps = 0
        self.tic = 10
        self.kitsoin_bonus = 10 
        self.kitsoin_positions = {(20, 20)}
        self.kitsoin_etat = True
        self.affichage()
    
    def affichage(self):
        Dessin.delete(tag_kitsoin)
        if carte.niv_chargeur > 0 and brickman.vie_etat:
            self.kitsoin_utilisation()
            self.position_chargeur()
            self.creer_kitsoin()

    def creer_kitsoin(self):
        for position in self.kitsoin_positions:
            carre(cord_transformer(position[0], position[1], delta), "green", "black", tag_kitsoin) 

    def position_chargeur(self):
        if self.kitsoin_etat == False:
             self.kitsoin_positions = {(0, 0)}
             self.kitsoin_etat = True
    
    def kitsoin_utilisation(self):
        if (brickman.position_X, brickman.position_Y) in self.kitsoin_positions:
            if brickman.sante + self.kitsoin_bonus > 100:
                return
            else:
                self.kitsoin_positions.remove((brickman.position_X, brickman.position_Y))
                brickman.sante += self.kitsoin_bonus

class Boss():
    def __init__(self):
        self.tic = 10
        self.temps = 10
        self.position_X = 4
        self.position_Y = 4
        self.sante = 200
        self.boss = pnm.ppm_vers_matrice("./entité/boss.ppm")
        self.longueur_boss = self.boss[0]
        self.hauteur_boss = len(self.boss) 
        self.affichage()

    def affichage(self):
        Dessin.delete(tag_boss)
        if carte.niv_chargeur == 4 and brickman.vie_etat:
            self.creer_boss()
            self.dommage()

    def creer_boss(self):
        affiche_matrice_rgb(self.boss, self.position_X, self.position_Y, delta, "black", tag_boss)


    def dommage(self):
        cords_brickman = (brickman.position_X, brickman.position_Y)
        if cords_brickman in self.cords_boss():
            brickman.sante -= 1
    
    def cords_boss(self):
        cords = []
        for i in range(6):
            for j in range(6):
                cords.append((self.position_X+i, self.position_Y+j))
        return cords

carte = Carte()
brickman = Brickman()
adversaire = Adversaire()
interface = Interface()
etat = Etat()
limbo = Limbo()
objet = Objet()
boss = Boss()

def tictac_carte():
    carte.temps = carte.temps+1
    carte.affichage()
    Dessin.after(carte.tic,tictac_carte)

def tictac_brickman():
    brickman.temps = brickman.temps+1
    brickman.affichage()
    Dessin.after(brickman.tic,tictac_brickman)

def tictac_adversaire():
    adversaire.temps = adversaire.temps+1
    adversaire.affichage()
    Dessin.after(adversaire.tic,tictac_adversaire)

def tictac_interface():
    interface.temps = interface.temps+1
    interface.affichage()
    Dessin.after(interface.tic,tictac_interface)

def tictac_etat():
    etat.temps = etat.temps+1
    etat.affichage()
    Dessin.after(etat.tic,tictac_etat)

def tictac_limbo():
    limbo.temps = limbo.temps+1
    limbo.affichage()
    Dessin.after(limbo.tic,tictac_limbo)

def tictac_objet():
    objet.temps = objet.temps+1
    objet.affichage()
    Dessin.after(objet.tic,tictac_objet)

def tictac_boss():
    boss.temps = boss.temps+1
    boss.affichage()
    Dessin.after(boss.tic,tictac_boss)

def illumine_moi():
    if not interface.lampe_lumiere_etat:
        interface.lampe_lumiere_etat = True
    if not interface.titre_etat:
        interface.titre_etat = True
    if not interface.logo_etat:
        interface.logo_etat = True
    if not interface.projet_etat:
        interface.projet_etat = True
    bouton_lumiere_1.destroy()
    interface.lumiere_etat = True

def assombris_moi():
    if interface.lumiere_etat:
        if interface.lampe_lumiere_etat:
            interface.lampe_lumiere_etat = False
        if interface.titre_etat:
            interface.titre_etat = False
        if interface.lampe_etat:
            interface.lampe_etat = False
        if interface.logo_etat:
            interface.logo_etat = False
        if interface.projet_etat:
            interface.projet_etat = False
        bouton_lumiere_2.destroy()
        carte.niv_chargeur = 0

def fermer():
    root.destroy()

bouton_lumiere_1 = tk.Button(root,text="Illumine-moi",command=illumine_moi,width=10)
bouton_lumiere_2 = tk.Button(root,text="Assombris-moi",command=assombris_moi,width=10)
button_quitter = tk.Button(root,text="Fermer",command=fermer,width=5)

bouton_lumiere_1.pack()
bouton_lumiere_2.pack()
button_quitter.pack(side='right')

root.bind('<Up>', brickman.deplacer_haut)
root.bind('<Down>', brickman.deplacer_bas)
root.bind('<Left>', brickman.deplacer_gauche)
root.bind('<Right>', brickman.deplacer_droite)

tictac_carte()
tictac_objet()
tictac_brickman()
tictac_boss()
tictac_adversaire()
tictac_interface()
tictac_etat()
tictac_limbo()



root.mainloop()