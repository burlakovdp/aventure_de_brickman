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
tag_limbo = "limbo"
tag_tuto = "tuto"
tag_kitsoin = "kitsoin"
tag_transition = "transition"
tag_boss = "boss"
tag_ecran_noir = "ecran_noir"
tag_bombe = "bombe"
tag_fin = "fin"

BOSS_SANTE = 200
BOSS_INITIAL_POSITION_X = 20
BOSS_INITIAL_POSITION_Y = 5
BRICKMAN_SANTE = 100
BRICKMAN_COULEUR = "yellow"

fin_etat = False

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

def parseur(path):
    fichier = open(path, "r", encoding="utf-8")

    niveau_donnees = [e for e in fichier]
    niveau_donnees_propres = [ligne.split(':') for ligne in niveau_donnees]

    cords_brutes = ''
    niveau_donnees_dict = {}

    for index in niveau_donnees_propres:
        if index[0] == 'kitsoin_position':
            cords_brutes = index[1].split(';')
            tmp = []
            for cords in cords_brutes:
                cord = cords.split(',')
                tmp.append((int(cord[0]), int(cord[1])))
            niveau_donnees_dict['kitsoin_position'] = tmp
        elif index[0] == 'guerrier_position':
            cords_brutes = index[1].split(';')
            tmp = []
            for cords in cords_brutes:
                cord = cords.split(',')
                print(cord)
                if len(cord) == 10:
                    tmp.append((int(cord[0]), int(cord[1]), int(cord[2]), int(cord[3]), int(cord[4]), int(cord[5]), int(cord[6]), int(cord[7]), int(cord[8]), int(cord[9])))
                elif len(cord) == 8:
                    tmp.append((int(cord[0]), int(cord[1]), int(cord[2]), int(cord[3]), int(cord[4]), int(cord[5]), int(cord[6]), int(cord[7])))
                elif len(cord) == 6:
                    tmp.append((int(cord[0]), int(cord[1]), int(cord[2]), int(cord[3]), int(cord[4]), int(cord[5])))
                else:
                    pass
            niveau_donnees_dict['guerrier_position'] = tmp
        else:
            for num in index[1]:
                if num.isdigit():
                    cords_brutes += num
            niveau_donnees_dict[index[0]] = int(cords_brutes)
        cords_brutes = ''

        fichier.close()
    return niveau_donnees_dict

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
        if fin_etat:
            Dessin.delete(tag_interface)
            return 
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
        if carte.niveau_actuel >= 0 and brickman.vie_etat:
            self.brickman_sante_statut()
            #self.sante_statut_etat = True
        if carte.niveau_actuel == 4 and brickman.vie_etat:
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
        affiche_matrice_rgb(self.logo, 60, 62, delta_min, "black", tag_interface)

    def creer_projet(self):
        affiche_matrice(self.projet, 60, 68, delta_min, "black", "white", tag_interface)

    def creer_lampe(self):
        affiche_matrice_rgb(self.lampe, 33, 2, delta, "black", tag_interface)
        Dessin.create_line(793, 44, 793, 0, fill="white", tags=tag_interface)
    
    def creer_lumiere_lampe(self):
        affiche_matrice_rgb(self.lumiere, 33, 6, delta, "black", tag_interface)

    def brickman_sante_statut(self):
        brick_counter = (brickman.sante*self.ligne_sante)//BRICKMAN_SANTE
        for i in range(brick_counter):
            carre(cord_transformer(self.brickman_sante_position_X0+i, self.brickman_sante_position_Y, delta), "red", "black", tag_interface)
        for i in range(self.ligne_sante-brick_counter):
            carre(cord_transformer(brick_counter+i+1, self.brickman_sante_position_Y, delta), "black", "red", tag_interface)
        
    def boss_sante_statut(self):
        brick_counter = (boss.sante*self.ligne_sante*2)//BOSS_SANTE
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
        if fin_etat:
            Dessin.delete(tag_limbo)
        elif brickman.vie_etat == False:
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
                etat.niv_charge_etat = False
                brickman.deplacement_etat = False
                brickman.vie_etat = True
                brickman.sante = BRICKMAN_SANTE
                if carte.niveau_actuel == 4:
                        boss.boss_start = boss.temps
                        boss.tuto_poser_bombe_etat = True
                        objet.kitsoin_positions.clear()
                        objet.kitsoin_counter = 0
                        objet.temps_dernier_creation = None
                        boss.sante = BOSS_SANTE
                        boss.position_X = BOSS_INITIAL_POSITION_X
                        boss.position_Y = BOSS_INITIAL_POSITION_Y
                        boss.etat_combat = False
                        boss.etat_deplacement = False
                        boss.etat_deplacement_X = False
                        boss.etat_deplacement_Y = False
                        boss.affichage()
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
        self.niveau_1_donnees = "./donnees/niveau_1.txt"
        self.niveau_2_donnees = "./donnees/niveau_2.txt"
        self.niveau_3_donnees = "./donnees/niveau_3.txt"
        self.niveau_4_donnees = "./donnees/niveau_4.txt"
        self.niveau_boss = pnm.pbm_vers_matrice("./cartes/boss_carte.pbm")
        self.tuto = pnm.pbm_vers_matrice("./interface/tuto/tuto.pbm")
        self.bouger = pnm.pbm_vers_matrice("./interface/tuto/bouger.pbm")
        self.sante = pnm.pbm_vers_matrice("./interface/tuto/sante.pbm")
        self.sortie = pnm.pbm_vers_matrice("./interface/tuto/sortie.pbm")
        self.soin = pnm.pbm_vers_matrice("./interface/tuto/soin.pbm")
        self.sortie_position_X = 25
        self.sortie_position_Y = 17
        self.kitsoin_position_X = 10
        self.kitsoin_position_Y = 17
        self.temps = 0
        self.tic = 10
        self.niveau_actuel = -1
        self.affichage()
    
    def affichage(self):
        Dessin.delete(tag_tuto)
        Dessin.delete(tag_mure)
        if fin_etat:
            Dessin.delete(tag_tuto)
            Dessin.delete(tag_mure)
        elif self.niveau_actuel == 0 and brickman.vie_etat == True:
            self.tutoriel()
            self.sortie_tuto()
        elif self.niveau_actuel > 0 and brickman.vie_etat == True:
            self.tic = 1000
            self.labyrinthe()

    def labyrinthe(self):
        if self.niveau_actuel == 1:
            affiche_matrice(self.niveau_1, 0, 0, delta, "white", "black", tag_mure)
        elif self.niveau_actuel == 2:
            affiche_matrice(self.niveau_2, 0, 0, delta, "white", "black", tag_mure)
        elif self.niveau_actuel == 3:
            affiche_matrice(self.niveau_3, 0, 0, delta, "white", "black", tag_mure)
        elif self.niveau_actuel == 4:
            affiche_matrice(self.niveau_boss, 0, 0, delta, "white", "black", tag_mure)
    
    def tutoriel(self):
        carre(cord_transformer(self.sortie_position_X, self.sortie_position_Y, delta), "pink", "black", tag_tuto)
        carre(cord_transformer(self.kitsoin_position_X, self.kitsoin_position_Y, delta,), "green", "black", tag_tuto)
        affiche_matrice(self.tuto, 0, 0, delta, "white", "black", tag_tuto)
        affiche_matrice(self.bouger, 65, 60, delta_min, "white", "black", tag_tuto)
        affiche_matrice(self.sante, 8, 58, delta_min, "white", "black", tag_tuto)
        affiche_matrice(self.soin, 7, 18, delta_min, "white", "black", tag_tuto)
        affiche_matrice(self.sortie, 51, 18, delta_min, "white", "black", tag_tuto)

    def tuto_collision(self, x, y):
        if self.tuto[y][x] == 1:
            return True
        return False

    def collision(self, x, y):
        if self.niveau_actuel == 1:
            if self.niveau_1[y][x] == 1:
                return True
        elif self.niveau_actuel == 2:
            if self.niveau_2[y][x] == 1:
                return True
        elif self.niveau_actuel == 3:
            if self.niveau_3[y][x] == 1:
                return True
        elif self.niveau_actuel == 4:
            if self.niveau_boss[y][x] == 1:
                return True
        return False

    def sortie_tuto(self):
        if brickman.position_X == self.sortie_position_X and brickman.position_Y == self.sortie_position_Y:
            Dessin.delete(tag_tuto)
            carte.niveau_actuel = 1
            adversaire.affichage()
            etat.affichage()  

class Brickman():
    def __init__(self):
        self.position_X = 10
        self.position_Y = 21
        self.temps = 0
        self.tic = 10
        self.sante = BRICKMAN_SANTE
        self.vie_etat = True
        self.deplacement_etat = False
        self.couleur = BRICKMAN_COULEUR
        self.affichage()
    
    def affichage(self):
        Dessin.delete(tag_brickman)
        if fin_etat:
            Dessin.delete(tag_brickman)
            return 
        elif carte.niveau_actuel  == 0:
            self.creer_brickman(self.position_X, self.position_Y)
        elif carte.niveau_actuel >= 1:
            self.creer_brickman(self.position_X, self.position_Y)
            self.mort()

    def creer_brickman(self, x, y):
        carre(cord_transformer(x, y, delta), self.couleur, "black", tag_brickman)

    def deplacer_haut(self, event):
        if brickman.vie_etat and carte.niveau_actuel == 4:
            return 
        elif brickman.vie_etat and carte.niveau_actuel == 0:
            if self.position_Y == 0:
                return
            elif carte.tuto_collision(self.position_X, self.position_Y-1):
                return 
            self.position_Y -= 1
        elif brickman.vie_etat and carte.niveau_actuel >= 1:
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
        if brickman.vie_etat and carte.niveau_actuel == 4:
            return 
        elif brickman.vie_etat and carte.niveau_actuel == 0:
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
        if brickman.vie_etat and carte.niveau_actuel == 0:
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
        if brickman.vie_etat and carte.niveau_actuel == 0:
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
    
    def mort(self):
        if self.sante <= 0:
            if not self.deplacement_etat: 
                Dessin.delete(tag_brickman)
            Dessin.delete(tag_bombe)
            Dessin.delete(tag_mure)
            Dessin.delete(tag_transition)
            Dessin.delete(tag_kitsoin)
            Dessin.delete(tag_interface)
            Dessin.delete(tag_adversaire)
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
        self.guerrier_dommage = 1
        self.affichage()
    
    def affichage(self):
        Dessin.delete(tag_adversaire)
        if carte.niveau_actuel == 4:
            self.position_X = -1
            self.position_Y = -1
        if carte.niveau_actuel >= 1 and carte.niveau_actuel < 4 and brickman.vie_etat and etat.niv_charge_etat:
            self.dommage()
            self.capitaine()
            self.tic = 250

    def creer_guerrier(self, x, y):
        carre(cord_transformer(x, y, delta), "red", "black", tag_adversaire)
    
    def capitaine(self):
        for i in range(len(etat.niveau_donnees_dict['guerrier_position'])):
            if len(etat.niveau_donnees_dict['guerrier_position'][i]) == 10:
                if etat.niveau_donnees_dict['guerrier_position'][i][8] == 0 and etat.niveau_donnees_dict['guerrier_position'][i][9] == 0:
                    etat.niveau_donnees_dict['guerrier_position'][i] = (
                        etat.niveau_donnees_dict['guerrier_position'][i][0],
                        etat.niveau_donnees_dict['guerrier_position'][i][1],
                        etat.niveau_donnees_dict['guerrier_position'][i][2],
                        etat.niveau_donnees_dict['guerrier_position'][i][3],
                        etat.niveau_donnees_dict['guerrier_position'][i][4],
                        etat.niveau_donnees_dict['guerrier_position'][i][5],
                        etat.niveau_donnees_dict['guerrier_position'][i][6],
                        etat.niveau_donnees_dict['guerrier_position'][i][7],
                        etat.niveau_donnees_dict['guerrier_position'][i][0],
                        etat.niveau_donnees_dict['guerrier_position'][i][1]
                    )
                self.creer_guerrier(etat.niveau_donnees_dict['guerrier_position'][i][8], etat.niveau_donnees_dict['guerrier_position'][i][9])
                etat.niveau_donnees_dict['guerrier_position'][i] = self.deplacement_carre(etat.niveau_donnees_dict['guerrier_position'][i][0],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][1],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][2],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][3],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][4],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][5],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][6],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][7],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][8],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][9]                                                                                                                                          
                                                                                       )
            if len(etat.niveau_donnees_dict['guerrier_position'][i]) == 8:
                if etat.niveau_donnees_dict['guerrier_position'][i][6] == 0 and etat.niveau_donnees_dict['guerrier_position'][i][7] == 0:
                    etat.niveau_donnees_dict['guerrier_position'][i] = (
                        etat.niveau_donnees_dict['guerrier_position'][i][0],
                        etat.niveau_donnees_dict['guerrier_position'][i][1],
                        etat.niveau_donnees_dict['guerrier_position'][i][2],
                        etat.niveau_donnees_dict['guerrier_position'][i][3],
                        etat.niveau_donnees_dict['guerrier_position'][i][4],
                        etat.niveau_donnees_dict['guerrier_position'][i][5],
                        etat.niveau_donnees_dict['guerrier_position'][i][0],
                        etat.niveau_donnees_dict['guerrier_position'][i][1] 
                    )
                self.creer_guerrier(etat.niveau_donnees_dict['guerrier_position'][i][6], etat.niveau_donnees_dict['guerrier_position'][i][7])
                etat.niveau_donnees_dict['guerrier_position'][i] = self.deplacement_ia(etat.niveau_donnees_dict['guerrier_position'][i][0],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][1],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][2],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][3],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][4],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][5],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][6],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][7]                                                                                 
                                                                                       )
            if len(etat.niveau_donnees_dict['guerrier_position'][i]) == 6:
                if etat.niveau_donnees_dict['guerrier_position'][i][4] == 0 and etat.niveau_donnees_dict['guerrier_position'][i][5] == 0:
                    etat.niveau_donnees_dict['guerrier_position'][i] = (
                        etat.niveau_donnees_dict['guerrier_position'][i][0],
                        etat.niveau_donnees_dict['guerrier_position'][i][1],
                        etat.niveau_donnees_dict['guerrier_position'][i][2],
                        etat.niveau_donnees_dict['guerrier_position'][i][3],
                        etat.niveau_donnees_dict['guerrier_position'][i][0],
                        etat.niveau_donnees_dict['guerrier_position'][i][1],
                    )
                self.creer_guerrier(etat.niveau_donnees_dict['guerrier_position'][i][4], etat.niveau_donnees_dict['guerrier_position'][i][5])
                etat.niveau_donnees_dict['guerrier_position'][i] = self.deplacement_ligne(etat.niveau_donnees_dict['guerrier_position'][i][0],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][1],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][2],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][3],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][4],
                                                                                       etat.niveau_donnees_dict['guerrier_position'][i][5],                                                                                 
                                                                                       )

    def deplacement_ia(self, x_initial, y_initial, x0_borne, y0_borne, x1_borne, y1_borne, x_actuel, y_actuel):    
        zone_guerrier = set()
        for y in range(y0_borne, y1_borne+1):
            for x in range(x0_borne, x1_borne+1):
                zone_guerrier.add((x, y))

        if (brickman.position_X, brickman.position_Y) in zone_guerrier:
            if x_actuel != brickman.position_X and y_actuel != brickman.position_Y:
                if y_actuel < brickman.position_Y:
                    y_actuel += 1
                else:
                    y_actuel -= 1
                if x_actuel < brickman.position_X:
                    x_actuel += 1
                else:
                    x_actuel -= 1
            elif x_actuel == brickman.position_X and y_actuel != brickman.position_Y:
                if y_actuel < brickman.position_Y:
                    y_actuel += 1
                else:
                    y_actuel -= 1
            elif x_actuel != brickman.position_X and y_actuel == brickman.position_Y:
                if x_actuel < brickman.position_X:
                    x_actuel += 1
                else:
                    x_actuel -= 1
            return((x_initial, y_initial, x0_borne, y0_borne, x1_borne, y1_borne, x_actuel, y_actuel))  
         
        elif (brickman.position_X, brickman.position_Y) not in zone_guerrier:
            if x_actuel == x_initial and y_actuel == y_initial:
                return((x_initial, y_initial, x0_borne, y0_borne, x1_borne, y1_borne, x_actuel, y_actuel))
            elif x_actuel != x_initial and y_actuel != y_initial:
                if y_actuel < y_initial:
                    y_actuel += 1
                else:
                    y_actuel -= 1
                if x_actuel < x_initial:
                    x_actuel += 1
                else:
                    x_actuel -= 1
            elif x_actuel == x_initial and y_actuel != y_initial:
                if y_actuel < y_initial:
                    y_actuel += 1
                else:
                    y_actuel -= 1
            elif x_actuel != x_initial and y_actuel == y_initial:
                if x_actuel < x_initial:
                    x_actuel += 1
                else:
                    x_actuel -= 1
            return((x_initial, y_initial, x0_borne, y0_borne, x1_borne, y1_borne, x_actuel, y_actuel))
    
    def deplacement_ligne(self, x_initial, y_initial, x_destination, y_destination, x_actuel, y_actuel):
        if x_actuel == x_destination and y_actuel == y_destination:
            return ((x_destination, y_destination, x_initial, y_initial, x_actuel, y_actuel))
        elif x_initial == x_destination:
            if y_actuel < y_destination:
                y_actuel += 1
            else:
                y_actuel -= 1
            return ((x_initial, y_initial, x_destination, y_destination, x_actuel, y_actuel))
        elif y_initial == y_destination:
            if x_actuel < x_destination:
                x_actuel += 1
            else:
                x_actuel -= 1
            return ((x_initial, y_initial, x_destination, y_destination, x_actuel, y_actuel))

    def deplacement_carre(self, x_initial, y_initial, x1, y1, x2, y2, x3, y3, x_actuel, y_actuel):
        if y_actuel == y1 and x_actuel != x1:
            if x_actuel < x1:
                x_actuel +=1
            return ((x_initial, y_initial, x1, y1, x2, y2, x3, y3, x_actuel, y_actuel))
        elif y_actuel != y2 and x_actuel == x1:
            if y_actuel < y2:
                y_actuel += 1
            return ((x_initial, y_initial, x1, y1, x2, y2, x3, y3, x_actuel, y_actuel))
        elif y_actuel == y2 and x_actuel != x3:
            if x_actuel > x3:
                x_actuel -= 1
            return ((x_initial, y_initial, x1, y1, x2, y2, x3, y3, x_actuel, y_actuel))
        elif x_actuel == x3 and y_actuel != y_initial:
            if y_actuel > y_initial:
                y_actuel -= 1
            return ((x_initial, y_initial, x1, y1, x2, y2, x3, y3, x_actuel, y_actuel))
        #guerrier_position:(x_initial,y_initial, x1, y1, x2, y2, x3, y3, curr_x, curr_y)
    def dommage(self):
        for cord in etat.niveau_donnees_dict['guerrier_position']:
            if (brickman.position_X, brickman.position_Y) == (cord[len(cord)-2], cord[len(cord)-1]):
                brickman.sante -= self.guerrier_dommage

class Etat():
    def __init__(self):
        self.temps = 0
        self.tic = 1
        self.transition_X = None
        self.transition_Y = None
        self.transition_etat = False
        self.niv_charge_etat = False
        self.niveau_donnees_dict = None
        self.fin_position_X = 5
        self.fin_position_Y = 37
        self.ecran_noir_path = pnm.pbm_vers_matrice("./interface/techniques/ecran_noir.pbm")
        self.cellardoor = pnm.pbm_vers_matrice("./interface/techniques/cellardoor.pbm")
        self.par = pnm.pbm_vers_matrice("./interface/techniques/par.pbm")
        self.coeur = pnm.ppm_vers_matrice("./interface/techniques/coeur.ppm")
        self.code_avec = pnm.pbm_vers_matrice('./interface/techniques/code_avec.pbm')
        self.affichage()
        
    def affichage(self):
        Dessin.delete(tag_transition)
        if fin_etat:
            Dessin.delete(tag_fin)
            affiche_matrice(etat.code_avec, 7, 1, delta, "white", "black", tag_fin)
            affiche_matrice_rgb(etat.coeur, 17, 15, delta, "black", tag_fin)
            affiche_matrice(etat.par, 2, 59, delta_min, "white", "black", tag_fin)
            affiche_matrice(etat.cellardoor, 5, 33, delta, "white", "black", tag_fin)
            return
        if carte.niveau_actuel > 0 and brickman.vie_etat:
            self.niveau_chargeur()
            self.transition()
        if brickman.vie_etat == False and brickman.deplacement_etat == False:
            self.ecran_noir()
        if carte.niveau_actuel == 4 and brickman.vie_etat and boss.sante > 0:
            self.dommage_boss()
        if carte.niveau_actuel == 4 and brickman.vie_etat and boss.mort_etat == True:
            self.afficher_fin()
    
    def ecran_noir(self):
        affiche_matrice(self.ecran_noir_path, 0, 0, delta, "black", "black", tag_ecran_noir)

    def transition(self):
        if carte.niveau_actuel < 4 and carte.niveau_actuel > 0 and brickman.vie_etat:
            carre(cord_transformer(self.transition_X, self.transition_Y, delta), "pink", "black", tag_transition)
        if self.transition_X == brickman.position_X and self.transition_Y == brickman.position_Y and self.transition_etat == False:
            if carte.niveau_actuel < 4:
                carte.niveau_actuel += 1
            self.niv_charge_etat = False
            Dessin.delete(tag_mure)
            Dessin.delete(tag_adversaire)
            Dessin.delete(tag_kitsoin)
            Dessin.delete(tag_brickman)
            #(f'niveau = {carte.niveau_actuel}')
            self.affichage()
            carte.affichage()
            adversaire.affichage()
            if carte.niveau_actuel == 4:
                boss.boss_start = boss.temps
                boss.affichage()
            self.transition_etat = True
        elif self.transition_X != brickman.position_X or self.transition_Y != brickman.position_Y:
            self.transition_etat = False

    def dommage_boss(self):
        cords_brickman = (brickman.position_X, brickman.position_Y)

        if cords_brickman in boss.cords_boss():
            brickman.sante -= boss.dommage

        bombe_utilise = []
        for cord in bombe.cords_bombes:
            if (cord[0], cord[1]) in boss.cords_boss():
                if boss.sante == 0:
                    pass
                elif boss.sante - bombe.dommage < 0:
                    bombe_utilise.append(cord)
                    boss.sante = 0
                else:
                    bombe_utilise.append(cord)
                    boss.sante -= bombe.dommage

        for piece in bombe_utilise:
            bombe.cords_bombes.remove(piece)

    def niveau_chargeur(self):
        if not self.niv_charge_etat:
            if carte.niveau_actuel == 1:
                self.niveau_donnees_dict = parseur(carte.niveau_1_donnees)
                print(self.niveau_donnees_dict)
            elif carte.niveau_actuel == 2:
                self.niveau_donnees_dict = parseur(carte.niveau_2_donnees)
            elif carte.niveau_actuel == 3:
                self.niveau_donnees_dict = parseur(carte.niveau_3_donnees)
            elif carte.niveau_actuel == 4:
                objet.kitsoin_positions.clear()
                self.niveau_donnees_dict = parseur(carte.niveau_4_donnees) 
            brickman.position_X = self.niveau_donnees_dict['brickman_pos_X']
            brickman.position_Y = self.niveau_donnees_dict['brickman_pos_Y']
            self.transition_X = self.niveau_donnees_dict['transition_pos_X']
            self.transition_Y = self.niveau_donnees_dict['transition_pos_Y']
            objet.position_chargeur()
            self.transition()
            #print(self.niveau_donnees_dict)
            self.niv_charge_etat = True

    def afficher_fin(self):
        global fin_etat 
        carre(cord_transformer(self.fin_position_X, self.fin_position_Y, delta), "pink", "black", tag_transition)
        if brickman.position_X == 5 and brickman.position_Y == 37:
            self.ecran_noir()
            fin_etat = True
            Dessin.delete(tag_adversaire)
            Dessin.delete(tag_bombe)
            Dessin.delete(tag_boss)
            Dessin.delete(tag_brickman)
            Dessin.delete(tag_mure)
            Dessin.delete(tag_interface)
            Dessin.delete(tag_kitsoin)
            Dessin.delete(tag_transition)        

class Objet():
    def __init__(self):
        self.temps = 0
        self.temps_dernier_creation = None
        self.tic = 10
        self.kitsoin_bonus = 10 
        self.kitsoin_positions = set()
        self.kitsoin_etat = False
        self.kitsoin_counter = 0
        self.affichage()
    
    def affichage(self):
        Dessin.delete(tag_kitsoin)
        if fin_etat:
            Dessin.delete(tag_kitsoin)
            return 
        if carte.niveau_actuel > 0 and brickman.vie_etat:
            self.kitsoin_utilisation()
            self.creer_kitsoin()
        if carte.niveau_actuel == 4:
            self.position_chargeur()

    def creer_kitsoin(self):
        for position in self.kitsoin_positions:
            carre(cord_transformer(position[0], position[1], delta), "green", "black", tag_kitsoin) 

    def position_chargeur(self):
        if carte.niveau_actuel == 4:
            if boss.sante <= 0:
                self.kitsoin_positions.clear()
            elif self.temps_dernier_creation == None:
                self.kitsoin_positions.clear()
                self.kitsoin_positions.add((random.randint(1, 47), 37))
                self.kitsoin_counter += 1
                self.temps_dernier_creation = self.temps
            elif self.temps - self.temps_dernier_creation > 500 and self.kitsoin_counter < 4:
                self.kitsoin_positions.add((random.randint(1, 47), 37))
                self.temps_dernier_creation = self.temps
                self.kitsoin_counter += 1
            elif self.kitsoin_counter == 4:
                self.temps_dernier_creation = self.temps
        else:
            self.kitsoin_positions.clear()
            for cords in etat.niveau_donnees_dict['kitsoin_position']:
                self.kitsoin_positions.add(cords)
    
    def kitsoin_utilisation(self):
        if brickman.vie_etat and carte.niveau_actuel == 4:
            for cords in boss.cords_boss():
                if cords in self.kitsoin_positions:
                    self.kitsoin_positions.remove((cords[0], cords[1]))
                    self.kitsoin_counter -= 1

        if (brickman.position_X, brickman.position_Y) in self.kitsoin_positions:
            #print(f'brickman sante avant -> {brickman.sante}')
            if brickman.sante == 100:
                return
            else:
                self.kitsoin_positions.remove((brickman.position_X, brickman.position_Y))
                if brickman.sante + self.kitsoin_bonus > 100:
                    brickman.sante = 100
                else:
                    brickman.sante += self.kitsoin_bonus
                #print(f'brickman sante apres -> {brickman.sante}')
                if carte.niveau_actuel == 4:
                    #print(self.kitsoin_counter)
                    self.kitsoin_counter -= 1

class Boss():
    def __init__(self):
        self.tic = 50
        self.temps = 0
        self.poser_bombe = pnm.pbm_vers_matrice("./interface/techniques/poser_bombe.pbm")
        self.espace = pnm.pbm_vers_matrice("./interface/techniques/espace.pbm")
        self.tuto_poser_bombe_etat = True
        self.mort_etat = False
        self.position_X = BOSS_INITIAL_POSITION_X
        self.position_Y = BOSS_INITIAL_POSITION_Y
        self.initial_Y = 5
        self.dommage = 50
        self.sante = BOSS_SANTE
        self.etat_combat = False
        self.etat_deplacement = False
        self.etat_deplacement_X = False
        self.etat_deplacement_Y = False
        self.deplacement_cords = None
        self.descente_etat = False
        self.montee_etat = False
        self.temps_deplacement_X = None
        self.mort_cords = None
        self.boss_start = None
        self.affichage()

    def affichage(self):
        Dessin.delete(tag_boss)
        if fin_etat:
            Dessin.delete(tag_boss)
            return 
        if carte.niveau_actuel == 4 and brickman.vie_etat and boss.sante > 0:
            if self.tuto_poser_bombe_etat:
                affiche_matrice(self.poser_bombe, 3, 14, delta, "white", "black", tag_boss)
                affiche_matrice(self.espace, 3, 21, delta, "white", "black", tag_boss)
            self.boss_controle()
            self.creer_boss()
        elif carte.niveau_actuel == 4 and brickman.vie_etat and self.sante <= 0:
            if self.mort_cords == None:
                self.tic = 100
                self.mort_cords = set()
                for cords in self.cords_boss():
                    self.mort_cords.add(cords)
            self.mort()

    def creer_boss(self):
        for cords in self.cords_boss():
            carre(cord_transformer(cords[0], cords[1], delta), "red", "black", tag_boss) 
    
    def boss_controle(self):
        if self.temps - self.boss_start > 100 and self.etat_combat == False:
            self.tuto_poser_bombe_etat = False
            self.etat_combat = True
        elif self.etat_combat and self.etat_deplacement == False:
            self.cords = self.choix_deplacement()
            self.etat_deplacement = True
        elif self.etat_combat and self.etat_deplacement:
            self.deplacement(self.cords)

    def cords_boss(self):
        cords = [((self.position_X+i, self.position_Y+j)) for i in range(6) for j in range(6)] #6 - boss longueur and hauteur (cube)
        return cords

    def choix_deplacement(self):
        return ((random.randint(1, 42), 32))

    def deplacement(self, cords):
        if self.etat_deplacement_X and self.etat_deplacement_Y:
            self.etat_deplacement = False
            self.etat_deplacement_X = False
            self.etat_deplacement_Y = False
        elif self.etat_deplacement_X == False and self.etat_deplacement_Y == False:
            if self.position_X < cords[0]:
                self.position_X += 1
            elif self.position_X > cords[0]:
                self.position_X -= 1
            elif self.position_X == cords[0]:
                self.etat_deplacement_X = True
                self.temps_deplacement_X = self.temps
                self.tic = 25
        elif self.etat_deplacement_Y == False and self.etat_deplacement_X and self.temps - self.temps_deplacement_X > 10:
            if self.position_Y == self.initial_Y and self.montee_etat and self.descente_etat:
                self.etat_deplacement_Y = True
                self.descente_etat = False
                self.montee_etat = False
            elif self.descente_etat == True and self.montee_etat == False and self.position_Y > self.initial_Y:
                self.position_Y -= 1
            elif self.descente_etat == True and self.montee_etat == False and self.position_Y == self.initial_Y:
                self.montee_etat = True
            elif self.descente_etat == False and self.position_Y < cords[1]:
                self.position_Y += 1
            elif self.position_Y == cords[1]:
                self.descente_etat = True
                self.tic = 50

    def mort(self):
        global fin_etat 
        if boss.sante <= 0 and self.mort_cords != None and len(self.mort_cords) == 0:
            boss.mort_etat = True
        for cords in self.mort_cords:
            carre(cord_transformer(cords[0], cords[1], delta), "red", "black", tag_boss)
        if len(self.mort_cords) != 0:
            self.mort_cords.pop()

class Bombe():
    def __init__(self):
        self.temps = 0
        self.tic = 10
        self.cords_bombes = set()
        self.dommage = 50
        self.temps_dernier_creation = None
        self.affichage()
    
    def affichage(self):
        Dessin.delete(tag_bombe)
        if fin_etat:
            Dessin.delete(tag_bombe)
            return 
        if carte.niveau_actuel == 4 and brickman.vie_etat and boss.sante <= 0:
            self.cords_bombes.clear()
            Dessin.delete(tag_bombe)
        elif carte.niveau_actuel == 4 and brickman.vie_etat and boss.sante > 0: 
            Dessin.delete(tag_bombe)
            self.creer_bombes()
            #print(self.cords_bombes)
            self.bombe_destructeur()
    
    def creer_bombes(self):
        for cords in self.cords_bombes:
            carre(cord_transformer(cords[0], cords[1], delta), "grey", "white", tag_bombe)

    def ajouter_bombe(self, event):
        if carte.niveau_actuel == 4 and brickman.vie_etat and boss.sante > 0:
            for cords in self.cords_bombes:
                if cords[0] == brickman.position_X and cords[1] == brickman.position_Y:
                    return 
            self.cords_bombes.add((brickman.position_X, brickman.position_Y, self.temps))

    def bombe_destructeur(self):
        bombes_expirees = [bomb for bomb in self.cords_bombes if self.temps - bomb[2] > 200]
        for bomb in bombes_expirees:
            self.cords_bombes.remove(bomb)
        bombes_expirees = []


carte = Carte()
brickman = Brickman()
adversaire = Adversaire()
interface = Interface()
etat = Etat()
limbo = Limbo()
objet = Objet()
boss = Boss()
bombe = Bombe()


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

def tictac_boss():
    boss.temps = boss.temps+1
    boss.affichage()
    Dessin.after(boss.tic,tictac_boss)

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

def tictac_bombe():
    bombe.temps = bombe.temps+1
    bombe.affichage()
    Dessin.after(bombe.tic,tictac_bombe)


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
        carte.niveau_actuel = 0

def fermer():
    root.destroy()

bouton_lumiere_1 = tk.Button(root,text="Illumine-moi",command=illumine_moi,width=10)
bouton_lumiere_2 = tk.Button(root,text="Assombris-moi",command=assombris_moi,width=10)
button_quitter = tk.Button(root,text="Fermer",command=fermer,width=5)

bouton_lumiere_1.pack()
bouton_lumiere_2.pack()
button_quitter.pack(side='right')

if fin_etat == False:
    root.bind('<Up>', brickman.deplacer_haut)
    root.bind('<Down>', brickman.deplacer_bas)
    root.bind('<Left>', brickman.deplacer_gauche)
    root.bind('<Right>', brickman.deplacer_droite)
    root.bind('<space>', bombe.ajouter_bombe)

tictac_carte()
tictac_objet()
tictac_brickman()
tictac_bombe()
tictac_boss()
tictac_adversaire()
tictac_interface()
tictac_etat()
tictac_limbo()

root.mainloop()