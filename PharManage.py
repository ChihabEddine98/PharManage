from tkinter import *
import tkinter.ttk as ttk
from tkinter.ttk import *
import sys
from tkinter.simpledialog import *
from tkinter.constants import *
from tkinter import *
import matplotlib.pyplot as plt

from tkinter.messagebox import *
import datetime
import time
from tkcalendar import Calendar, DateEntry


from tkinter import *
import tkinter.ttk as ttk
import sys
from tkinter.simpledialog import *
import hashlib as hash
from tkinter.messagebox import *
import datetime
import time
from tkcalendar import Calendar, DateEntry

import numpy as np
from gmplot import gmplot
import webbrowser


from urllib.request import urlopen
import json

from PyPDF2 import PdfFileReader,PdfFileWriter
import io
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
import webbrowser
import re
from tkinter.messagebox import *

from numpy import *

import hashlib as hash
import PyMySQL.pymysql as sq
from datetime import date
from math import sin, cos, sqrt, atan2, radians
import datetime

titre_global = "PharManage"

#################################################################################
###################### ConnectBDD ###############################################





class connectBdd: ## La Classe des accés a la bdd (ouverture,fermeture,Recherche,Ajout,...etc)


    def __init__(self):



        try:
            #self.conn=sq.connect("192.168.43.225", "pharmacie", password="pharmanage", db="pharmacie")
            self.conn = sq.connect("localhost", "root", password=None, db="pharmacie")
            self.cur = self.conn.cursor()
        except:
            showerror(" Erreur "," Probleme de connexion Réseau ! ")








    def authentification(self,un, pwd):  # la fonction qui confirme ou pas l"acces a un compte
        id = hash.md5(un.encode()).hexdigest()  # La méthode de hash utilisé est :  MD5
        ps = hash.md5(pwd.encode()).hexdigest()


        cur = self.cur

        cur.execute(''' SELECT * FROM comptes WHERE id=%s;''', id)

        exist = cur.fetchone()


        if exist :
            if (ps == exist[1]):

                return exist
            else:
                return 0

    def rechercheProduit(self, nmP, dosage,forme,bienEtre=0):  ## La recherche des produits selon

        cur = self.cur

        if nmP:

            if forme:
                if dosage!=0:

                    cur.execute(''' SELECT * FROM produits WHERE nomProduit=%s and forme=%s
                                    and dosage=%s;''', (nmP, forme, dosage))
                else:

                    cur.execute(''' SELECT * FROM produits WHERE nomProduit=%s 
                                    and forme=%s;''', (nmP,forme))
            else:
                if dosage!=0:

                    cur.execute(''' SELECT * FROM produits WHERE nomProduit=%s 
                                    and dosage=%s;''', (nmP, dosage))
                else:

                    cur.execute(''' SELECT * FROM produits WHERE nomProduit=%s 
                                    ;''', (nmP,))



        else:
            return []


        exist1 = cur.fetchall()

        return exist1

    #############################################################################################
    def rechercheStock1(self, idPd,cPh):

            cur = self.cur
            stock="stock"+cPh
            # cur.execute(''' SELECT * FROM produits,stock1 WHERE produits.nomProduit=%s
            #                and stock1.dateExp<=%s;''', (nmP, date))
            cur.execute(''' SELECT * FROM '''+ stock+''' WHERE idProduit=%s;''',(idPd))
            exist1 = cur.fetchall()
            return exist1

    #########################################################################################
    def rechercheEquivalent(self, categorie, bienEtre=0, dci=None):  ## La recherche des produits selon

            cur = self.cur
            if (dci != None and bienEtre == 0):
                cur.execute(''' SELECT * FROM produits WHERE dci=%s 
                                ;''', dci)
            else:
                if(categorie!= None):

                    cur.execute(''' SELECT * FROM produits WHERE categorie=%s 
                                    ;''', categorie)

            exist1 = cur.fetchall()


            return exist1

########################################################################################

    def categories(self): # une méthode qui nous retourne la liste des catégories dans notre table produits
                          # Elle sera exécuter a chaque lancement de la classe AffichProduits
        cur = self.cur

        cur.execute(''' SELECT categorie FROM produits ;''')
        exist1 = cur.fetchall()
        catego=[]
        if exist1:

            for e in exist1:
                if e[0] and e[0] not in catego:
                    catego.append(e[0])
        return catego
#############################################################################################
    def produitsDeCatego(self,catego):
        cur=self.cur
        cur.execute(''' SELECT nomProduit,dosage,forme FROM produits WHERE categorie=%s;''',catego)
        exist=cur.fetchall()
        produits=[]
        if exist:
            for e in exist:
                if e[0] and e[0] not in produits:
                    if(e[2]=="comprime"):
                        produits.append((e[0].upper().capitalize(),str(e[1])+" (mg) ",e[2].upper().capitalize()))
                    else:
                        produits.append((e[0].upper().capitalize(), "  " + str(e[1]) + " (mg/l)   ", e[2].upper().capitalize()))
        return produits

############################################################################################
####################### Partie Des statistiques ############################################
############################################################################################
    def venteRest(self,date1,date2,cPh):
        cur=self.cur


        if date1!=0 and date2!=0:
        #    date1 = datetime.datetime(year=date1, month=1, day=1)
         #   date2 = datetime.datetime(year=date2, month=12, day=30)
            if(date1<=date2):
                cur.execute(''' SELECT * FROM ventes'''+cPh+''' WHERE 
                                  dateVente>=%s
                                  AND dateVente<=%s;''', (date1,date2))
                exist1 = cur.fetchall()

                res=[]
                if exist1:
                    for e in exist1:
                        res.append((e[3],e[2],e[1]))


                return res
            else:
                return 0
        else:
            return -1
#################################################################################################
############################# Echanges entres pharmacies ########################################
#################################################################################################
    def produitDindice(self,ind):
        cur = self.cur

        if ind:
            cur.execute('''SELECT * FROM produits WHERE 
                            idProduit=%s;''',ind)
            exist1=cur.fetchone()
            if exist1:
                return exist1[3]
            else:
                return 0
        else:
            return -1
############################################################################################

    def qteDeNom(self,nomProd,p1,p2):
        cur=self.cur

        cur.execute(''' SELECT code FROM contacts WHERE pharmacie=%s;''',(p1,))
        code1=str(cur.fetchone()[0])

        cur.execute(''' SELECT code FROM contacts WHERE pharmacie=%s;''',(p2,))
        code2=str(cur.fetchone()[0])

        s=self.echangesEntrePharm(code1,code2)
        qte=0
        if s!=-1 and s!=0:
            for i in s:
                if i[0]==nomProd:
                    qte+=i[1]

        return qte




############################################################################################
    '''Cette méthode nous calcul le nombre des échanges éffectués
        entre deux pharmacies  '''
    def echangesEntrePharm(self,pharm1,pharm2):
        cur = self.cur
        s=[]

        if pharm1 and pharm2:
            cur.execute('''SELECT * FROM echanges WHERE 
                            donneur=%s AND recepteur=%s OR 
                            recepteur=%s AND donneur=%s;''',(pharm2,pharm1,pharm2,pharm1))
            exist1=cur.fetchall()
            if exist1:
                for e in exist1:
                    nomProd=self.produitDindice(e[5])
                    s.append((nomProd,e[3]))
                    ''' S=[Nom_Produit,Quantité ]'''
                return s
            else:
                return 0
        else:
            return -1







    def Recupere_contact(self,Cph):

        cur = self.cur

        cur.execute(''' SELECT * FROM Contacts WHERE contacts.code !=%s''',Cph)
        exist1 = cur.fetchall()
        return exist1

    #############################################################################################

    ############################################################################################
    def rechercheStock(self, idPd, date,cPh):

            cur = self.cur

            cur.execute(''' SELECT * FROM stock'''+cPh+''' WHERE 
                            idProduit=%s
                            AND dateExp=%s AND P=0;''', (idPd, date))
            exist1 = cur.fetchall()

            if exist1:

                return exist1

            else:
                print(" Le produit rechercher n'existe pas ")

    ############################################################################################################################
    ########################################InscripAdmin#########################################################################
    ################################################################################
    def rechProd(self, nmP, forme):  ## La recherche des produits selon

        cur = self.cur

        cur.execute(''' SELECT * FROM produits WHERE nomProduit=%s and forme=%s
                                     ;''', (nmP, forme))

        exist1 = cur.fetchall()

        return exist1

    #########################################################################################
    def Admin(self, tel, mail, adres, long, lat, Nphar, Cphar, user, mdp):
        cur = self.cur

        cur.execute(''' SELECT * FROM comptes WHERE 
                    comptes.code=%s AND comptes.typeCompte=%s  ;''', (Cphar,1))
        exist = cur.fetchall()
        if not exist:
            cur.execute(
                """INSERT INTO contacts (pharmacie,adresse,tel,email,latitude,longitude,code)
                VALUES (%s,%s,%s,%s,%s,%s,%s);""",
                (Nphar, adres,tel,mail, lat, long, Cphar))
            self.conn.commit()
            passHash = hash.md5(mdp.encode()).hexdigest()
            userNameHash = hash.md5(user.encode()).hexdigest()
            cur.execute(
                """INSERT INTO comptes (id,pass,code,typeCompte) 
                 VALUES (%s,%s,%s,1);""",
                (userNameHash, passHash,Cphar,)) # Le 1 ici correspand a l'admin 0 sinon
            self.conn.commit()

            stock=" stock"+Cphar
            stock_produit=" `fk_"+stock+"_produits_idx`"

            #### On Crée maintenant les tables stock et ventes pour cette nouvelle pharmacie
            sql=('''CREATE TABLE IF NOT EXISTS'''+stock+''' (
                      `idStock` INT NOT NULL AUTO_INCREMENT,
                      `quantiteN` INT NOT NULL,
                      `quantiteR` INT NOT NULL,
                      `dateExp` DATE NULL,
                      `idProduit` INT NOT NULL,
                      `P` INT NOT NULL,
                      `numlot` VARCHAR(45) NOT NULL,
                      PRIMARY KEY (`idStock`, `idProduit`),
                      INDEX'''+stock_produit+'''(`idProduit` ASC),
                      CONSTRAINT'''+stock_produit+'''
                      FOREIGN KEY (`idProduit`)
                      REFERENCES `pharmacie`.`produits` (`idProduit`)
                      ON DELETE NO ACTION
                      ON UPDATE NO ACTION)
                    ENGINE = InnoDB;
                    ''')
            cur.execute(sql)
            self.conn.commit()
            #################### arrivons maintenant a la table des ventes

            ventes=" ventes"+Cphar
            ventes_produit1=" `fk_"+ventes+"_produits_idx`"
            ventes_produit2 = " `fk_" + ventes + "_produits`"
            sql=('''CREATE TABLE IF NOT EXISTS'''+ventes+''' (
                  `idVente` INT NOT NULL AUTO_INCREMENT,
                  `quantiteR` INT NOT NULL,
                  `quantiteN` INT NOT NULL,
                  `dateVente` DATE NOT NULL,
                  `idProduit` INT NOT NULL,
                  PRIMARY KEY (`idVente`, `idProduit`),
                  INDEX '''+ventes_produit1+'''(`idProduit` ASC),
                  CONSTRAINT'''+ventes_produit2+'''
                  FOREIGN KEY (`idProduit`)
                  REFERENCES `pharmacie`.`produits` (`idProduit`)
                  ON DELETE NO ACTION
                  ON UPDATE NO ACTION)
                  ENGINE = InnoDB;''')
            cur.execute(sql)
            self.conn.commit()
            #################### arrivons maintenant a la table des reponses Au Commandes

            commande=" reponseCommande"+Cphar
            ventes_produit1=" `fk_"+commande+"_produits_idx`"
            ventes_produit2 = " `fk_" + commande + "_produits`"
            sql=('''CREATE TABLE IF NOT EXISTS'''+commande+''' (
                  `nCommande` INT NOT NULL AUTO_INCREMENT,
                  `code` VARCHAR(45) NOT NULL,
                  `date` DATE NOT NULL,
                   PRIMARY KEY (`nCommande`))
                   ENGINE = InnoDB;''')
            cur.execute(sql)
            self.conn.commit()


        else:
            showerror("Erreur!", "Le code pharmacie introduit est deja pris."
                                 "Veuillez changer de code pharmacie")

    ########################################InscripUser#########################################################################

    def User(self, Nphar, Cphar, user, mdp):
        cur = self.cur
        cur.execute(''' SELECT * FROM comptes WHERE 
                     comptes.code=%s AND comptes.typeCompte=%s;''', (Cphar, 1))
        exist = cur.fetchall()
        if exist:
            passHash = hash.md5(mdp.encode()).hexdigest()
            userNameHash = hash.md5(user.encode()).hexdigest()
            cur.execute(
                '''INSERT INTO comptes (id,pass,code,typeCompte)  VALUES (%s,%s,%s,0);''',
                (userNameHash, passHash, Cphar))
            self.conn.commit()
        else:
            showerror("Erreur!", "Cette pharmacie ne posséde pas de compte administrateur.")

    ############################################################################################################
    def verifMail(self, mail):
        if mail == '':
            return False
        else:
            motif = r"^[a-zA-Z0-9_\-]+(\.[a-zA-Z0-9_\-]+)*@[a-zA-Z0-9_\-]+(\.[a-zA-Z0-9_\-]+)*(\.[a-zA-Z]{2,6})$"
            return re.match(motif, mail) != None
            # Le resultat retourné est un booleen

    def quantiteProduit(self, nmP, dosage,cPh, bienEtre=0, forme=None):
            list = []
            rs = 0
            exist = self.rechercheProduit(nmP=nmP,dosage= dosage,bienEtre=0, forme=None)
            if exist:
                e = exist[0][0]
                exist1 = self.rechercheStock1(e,cPh)
                if exist1:
                    x = 0
                    rs = 0
                    for r in exist1:
                        x = x + r[1]
                        rs = rs + r[2]


                else:
                    x = 0

                t = x + rs


            else:

                x = 0
                rs = 0
                t = 0
            x = str(x)
            rs = str(rs)
            t = str(t)
            list.append(x)
            list.append(rs)
            list.append(t)

            return list

        ####################################################################
    def rupStock(self,cPh):

            #print("Les produits en rupture de stock :")
            cur = self.cur
            cur.execute(''' SELECT MAX(idProduit) FROM Produits ''')
            idmax = 0
            idmax = cur.fetchall()
            k = 0
            list1 = []

            for i in range(0, idmax[0][0], 1):

                list2 = self.rechercheStock1(i,cPh)
                if list2:
                    x = 0
                    for j in list2:
                        x = x + j[1]

                else:
                    x = 0

                if x == 0:

                    cur.execute(''' SELECT * FROM Produits WHERE Produits.idProduit=%s ;''', i)

                    var = cur.fetchall()
                    for e in var:
                        # print(e)

                        list1.append(e)

            # print(list1)
            return list1
            # if list1:

            # for e in list1:
            #  if e[1]=='M':
            #  print(k,"-" ,e[3],e[6])
            # else:
            #  print(k,"-" ,e[3])
            # k = k + 1

        # print("Nombre de produits en rupture de stock = ",k)
        ################################################################################################################


    ###############################################################################################################
    def retrait(self, nom, forme, numlot,cPh):

            exist = self.rechProd(nom, forme)
            exist1=[]
            if exist :
                if exist[0]:
                    if exist[0][0]:
                        id = exist[0][0]
                        cur = self.cur
                        stock="stock"+cPh

                        exist1=cur.execute(''' SELECT * FROM '''+ stock+''' WHERE idProduit=%s AND numlot=%s''',(id,numlot))

                        if exist1:
                            cur.execute(''' DELETE FROM '''+ stock+''' WHERE idProduit=%s AND numlot=%s''',(id,numlot))
                            self.conn.commit()

            return exist1

    def ajour_ligne(self, i,cPh):

        cur = self.cur

        cur.execute(''' UPDATE  stock'''+cPh+''' SET P=1 WHERE  idStock=%s ; ''', i)
        self.conn.commit()

    def recupere_date(self, i,cPh):

        cur = self.cur

        cur.execute(''' SELECT dateExp  FROM stock'''+cPh+''' WHERE  idStock=%s ; ''', i)
        existe = cur.fetchall()
        return existe

    def date(self):
        return date.today
    def recupere_id(self,cPh):
        cur = self.cur

        cur.execute(''' SELECT idStock  FROM stock'''+cPh)
        existe = cur.fetchall()
        return existe


    def mise_jour(self,cPh):
        past = datetime.date.today()
        k = self.recupere_id(cPh)
        i = 0
        r = len(k)
        liste = []
        while i < r:
            c = k[i][0]
            liste.append(c)
            i = i + 1

        for id in liste:
            date = self.recupere_date(id,cPh)
            if date:
                if date[0]:
                    if date[0][0]:

                        k = date[0][0]
                        if k < past:
                            self.ajour_ligne(id,cPh)


    def fermer(self):
        self.cur.close()
        self.conn.close()

#######################commande
    def commandes(self, entree, envoyeur):

        cur = self.cur
        # lentree est une liste dont les element sont comm suit :
        # 0:dosage   1: quantite    2: nomprodit  3: form  4 : bm
        sortie = []
        cur.execute("""SELECT MAX(Ncommande) FROM commandes""")
        ncommande = cur.fetchall()
        date = datetime.date.today()
        if ncommande[0][0]:

            idst = ncommande[0][0] + 1
        else:
            idst = 1
        for e in entree:  # pour chaque produit on va generer son id dans la table produit
            resultat = self.rechProd_ajout(e[2], e[0], e[4], e[3])

            if resultat:
                idProduit = resultat[0][0]

                var = (idst, idProduit, e[1], date, envoyeur)
            else:
                var = (idst, 0, date, e[1], envoyeur)
            idst = idst + 1

            sortie.append(var)

        return sortie


    def pre_commande(self, entree):
        liste = []
        cur = self.cur

        for i in entree:
            cur.execute()


    def faire_commandes(self, entree):
        # entree de type liste
        # n commande     idproduit   datetoday   quantite   codeenvoyeur

        for e in entree:
            self.cur.execute(
                '''insert into commandes (Ncommande ,IdProd,quantite,Date,CodeEnvoyeur) values (%s,%s,%s,%s,%s);''',
                (e[0], e[1], e[2], e[3], e[4]))
            k=e[4]
            self.conn.commit()
            #on ecrit dans la table notif
            # la notification
            #il faut l'envoyer pour toutes les pharmacies :
            #on récupère d'abord les codes disponibles :
            cur = self.cur
            cur.execute('SELECT code from contacts; ')
            e = cur.fetchall()
            list = []
            for i in e:
                if i[0]!= k:
                    list.append(i[0])
            notif = "Nouvelle commande recue !"
            cur.execute('SELECT MAX(idnotif) from notifications; ')
            e = cur.fetchone()
            if e:
                if e[0]:
                    id=e[0]+1
                else:
                    id = 1
            else:
                id=1
            for i in list:
                self.cur.execute('''insert into notifications (idnotif,notif,code) values (%s,%s,%s);''',(id,notif,i))
                self.conn.commit()
                id=id+1



    def selection_commande(self, entree, me):
        cur = self.cur
        liste = []
        # je recupere mes coordonnees geographiques
        var = "contacts"
        cur.execute(" SELECT * FROM " + var + " WHERE code=%s;", me)
        exist1 = cur.fetchall()

        lat1 = exist1[0][4]
        lon1 = exist1[0][5]
        # liste de codes des pharmacies
        for e in entree:
            var = []
            # on recupere les coordonnees georaphiques a  partir du code de la pharmacie
            cur.execute(''' SELECT * FROM contacts WHERE code=%s;''', e)
            exist = cur.fetchall()
            # calcul de la distance
            d = self.distance(lat1, exist[0][4], lon1, exist[0][5])
            var.append(d)
            var.append(e)
            liste.append(var)

        liste = sorted(liste)

        # on selectionne le premier :
        selection = liste[0][1]

        return selection
    def infos_transfert(self,commande,accepte, refuse):
        #on recupere les infos de la commande
        cur=self.cur
        cur.execute("SELECT * FROM commandes WHERE Ncommande=%s",commande)
        e=cur.fetchall()
        e1=e[0]# la commande
        #les infos du produit
        cur.execute("SELECT * FROM produits WHERE idProduit=%s", e1[1])
        e = cur.fetchall()
        e2=e[0]# le produit
        if e2[1]=="b":
            medoc=str(e2[3]+" - "+e2[7])
        else:
            medoc=str(e2[3]+" - "+e2[7]+" - "+str(e2[6])+" (mg ou mg/l)")
        # la pharmacie commandante:
        cur.execute("SELECT * FROM contacts WHERE code=%s",e1[4])
        e=cur.fetchall()
        pharm=e[0][0]
        qt=e1[2]

        # on informe les pharmacies du transfert
        accept = str("Votre Stock en " + medoc + " a été décrémenté de" + str(qt) + " en faveur de la pharmacie " + pharm)
        refus = str("Votre livraison de " + str(qt) + " " + medoc.upper().capitalize() + " a été refusée")
        # pour la pharmacie a laquelle on a accepté la livraison
        cur.execute('SELECT MAX(idnotif) from notifications; ')
        e = cur.fetchone()
        if e[0]:
            id = e[0] + 1
        else:
            id = 1

        self.cur.execute('''insert into notifications (idnotif,notif,code) values (%s,%s,%s);''', (id, accept, accepte))
        self.conn.commit()
        id = id + 1
        # pour mes refusees :
        for i in refuse :
            self.cur.execute('''insert into notifications (idnotif,notif,code) values (%s,%s,%s);''',
                             (id, refus, i))
            self.conn.commit()
    def refus_commandes(self,commande,refuse):
        # on recupere les infos de la commande
        cur = self.cur
        cur.execute("SELECT * FROM commandes WHERE Ncommande=%s", commande)
        e = cur.fetchall()
        e1 = e[0]  # la commande
        # les infos du
        #
        #
        #  produit
        cur.execute("SELECT * FROM produits WHERE idProduit=%s", e1[1])
        e = cur.fetchall()
        e2 = e[0]  # le produit
        if e2[1] == "b":
            medoc = str(e2[3] + " - " + e2[7])
        else:
            medoc = str(e2[3] + " - " + e2[7] + " - " + str(e2[6]) + " (mg ou mg/l)")
        # la pharmacie commandante:
        cur.execute("SELECT * FROM contacts WHERE code=%s", e1[4])
        e = cur.fetchall()
        pharm = e[0][0]
        qt = e1[2]

        cur.execute('SELECT MAX(idnotif) from notifications; ')
        e = cur.fetchone()
        if e[0]:
            id = e[0] + 1
        else:
            id = 1

        refus = str("Votre livraison de " + str(qt) + " " + medoc.upper().capitalize() + " a été refusée")
        for i in refuse:
            self.cur.execute('''insert into notifications (idnotif,notif,code) values (%s,%s,%s);''',(id, refus, i))
            self.conn.commit()






    def transfert_stock(self, me, he, numero):  # en entree le code de ma pharmacie, lenvoyeur et le numero de commande
        var1 = str("stock" + me)
        var2 = str("stock" + he)
        var3 = str("reponsecommande" + me)

        cur = self.cur
        # on recupere la commande pour avoir le produit et la quantité demandée
        cur.execute(''' SELECT * FROM commandes WHERE CodeEnvoyeur=%s and Ncommande=%s;''', (me, numero))
        exist = cur.fetchall()
        qt = exist[0][2]
        a=qt

        # on sait qu'il a plus de qt sans son stock
        cur.execute(''' SELECT * FROM '''+var2+''' WHERE idProduit=%s;''', exist[0][1])
        exist2 = cur.fetchall()
        i = 0
        e = exist2[i]

        for e in exist2:
            if qt != 0:

                if e[1] != 0:
                    if e[1] > qt:

                        cur.execute("UPDATE " + var2 + " SET quantiteN=%s  WHERE idStock=%s;", (e[1] - qt, e[0]))
                        self.conn.commit()
                        # pour l'ajout en stock :

                        # on recherche dans le stock du recepteur
                        cur.execute(''' SELECT * FROM ''' + var1 + ''''''' WHERE idProduit=%s AND dateExp=%s and P =%s;''',
                                    (exist[0][1], e[3], 0))
                        exist1 = cur.fetchall()

                        if exist1:

                            exist2 = cur.fetchall()

                            qn = exist1[0][1]
                            qr = exist1[0][2]

                            qt = int(qt)

                            qn = qn + qt

                            cur.execute('''UPDATE ''' + var1 + ''' SET quantiteN=%s  WHERE dateExp =%s;''', (qn, e[3]))
                            self.conn.commit()
                            cur.execute(''' UPDATE ''' + var1 + ''' SET quantiteR=%s WHERE dateExp = %s;''', (qr, e[3]))
                            self.conn.commit()

                        else:

                            qr = 0
                            qn = qt
                            # on doit recuperer le max de idStock
                            cur.execute("""SELECT MAX(idStock) FROM """ + var1)
                            idstock = cur.fetchall()

                            if idstock[0][0]:

                                idst = idstock[0][0] + 1
                            else:
                                idst = 1
                            cur.execute(
                                """INSERT INTO """ + var1 + """ (idStock,quantiteN,quantiteR,dateExp,idProduit,P,numlot)  VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                                (idst, qn, qr, e[3], exist[0][1], 0,e[6]))
                            self.conn.commit()
                        qt = 0
                    else:
                        qt = qt - e[1]
                        cur.execute("UPDATE " + var2 + " SET quantiteN=%s  WHERE idStock=%s;", (0, e[0]))
                        self.conn.commit()

                        # pour l'ajout en stock :
                        exist2 = self.rechStock(idP=exist[0][1], date=e[3],cPh=me)
                        if exist2:
                            exist2 = cur.fetchall()
                            qn = exist2[0][1]
                            qr = exist2[0][2]

                            e[1] = int(e[1])

                            qn = qn + e[1]

                            cur.execute('''UPDATE ''' + var1 + ''' SET quantiteN=%s  WHERE dateExp =%s;''', (qn, e[3]))
                            self.conn.commit()
                            cur.execute(''' UPDATE ''' + var1 + ''' SET quantiteR=%s WHERE dateExp = %s;''', (qr, e[3]))
                            self.conn.commit()

                        else:

                            qr = 0
                            qn = e[1]
                            # on doit recuperer le max de idStock
                            cur.execute("""SELECT MAX(idStock) FROM """ + var1)
                            idstock = cur.fetchall()

                            if idstock[0][0]:

                                idst = idstock[0][0] + 1
                            else:
                                idst = 1
                            cur.execute(
                                """INSERT INTO """ + var1 + """ (idStock,quantiteN,quantiteR,dateExp,idProduit,P,numlot)  VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                                (idst, qn, qr, e[3], exist[0][1], 0,e[6]))
                            self.conn.commit()
        # on enregistre l'echange dans la table echanges
        date = datetime.date.today()
        cur.execute("INSERT INTO echanges (donneur,recepteur,quantite,date,idProduit) VALUES (%s,%s,%s,%s,%s)",
                    (he, me, a, date, exist[0][1]))
        self.conn.commit()
        # on supprime toutes les lignes de reponses pour cette commande
        cur.execute('''DELETE from  ''' + var3 + ''' WHERE Ncommande =%s;''', numero)
        self.conn.commit()
        cur.execute('''DELETE from  commandes WHERE Ncommande =%s;''', numero)
        self.conn.commit()

    def repondre_commande(self, numero, me):
        # on recupere la commande
        cur = self.cur
        cur.execute(''' SELECT * FROM commandes WHERE  Ncommande=%s;''', numero)
        exist = cur.fetchall()
        # on recupere l'id du produit et la quantité voulue
        qt = exist[0][2]
        id = exist[0][1]
        he = exist[0][4]

        # on calcule la quantite en stock
        myqt = self.quantiteProduitId(id, me)
        var = str("reponsecommande" + he)

        if myqt:
            date = datetime.date.today()

            if myqt >= qt:

                # message de confirmation
                # on ajoute dans la table reponse de l'envoyeur
                cur.execute("INSERT INTO " + var + " (Ncommande,code,Date) VALUES (%s,%s,%s)",
                            (numero, me, date))
                self.conn.commit()
                # on note dans la table notifications
                #infos medicament
                cur.execute("SELECT * from produits where idProduit=%s",id)
                e=cur.fetchall()
                e2 = e[0]  # le produit
                if e2[1] == "b":
                    medoc = str(e2[3] + " - " + e2[7])
                else:
                    medoc = str(e2[3] + " - " + e2[7] + " - " + str(e2[6]) + " (mg ou mg/l)")
                cur.execute('SELECT MAX(idnotif) from notifications; ')
                e = cur.fetchone()
                if e[0]:
                    id = e[0] + 1
                else:
                    id = 1

                notif =str("Vous avez une nouvelle réponse à votre commande de ("+str(qt)+") "+medoc )
                cur.execute("INSERT INTO notifications (idnotif,notif,code) VALUES (%s,%s,%s)",
                            (id, notif, he))
                self.conn.commit()
            else:

                # infos medicament
                cur.execute("SELECT * from produits where idProduit=%s", id)
                e = cur.fetchall()
                e2 = e[0]  # le produit
                if e2[1] == "b":
                    medoc = str(e2[3] + " - " + e2[7])
                else:
                    medoc = str(e2[3] + " - " + e2[7] + " - " + str(e2[6]) + " (mg ou mg/l)")

                showinfo("Opération impossible ","Vous ne pouvez pas répondre a cette commande de ("+medoc+")!")
        else :
            # infos medicament
            cur.execute("SELECT * from produits where idProduit=%s", id)
            e = cur.fetchall()
            e2 = e[0]  # le produit
            if e2[1] == "b":
                medoc = str(e2[3] + " - " + e2[7])
            else:
                medoc = str(e2[3] + " - " + e2[7] + " - " + str(e2[6]) + " (mg ou mg/l)")
            showinfo("Opération impossible ", "Vous ne pouvez pas répondre a cette commande de (" + medoc + ")!")



    def distance(self, lat1, lat2, lon1, lon2):
        # approximate radius of earth in km
        R = 6373.0
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return distance


    def quantiteProduitId(self, id, m):
        var = str("stock" + m)
        cur = self.cur
        rs=0
        cur.execute("SELECT * FROM " + var + " WHERE idProduit=%s and P=%s;", (id, 0))
        exist1 = cur.fetchall()
        if exist1:
            x = 0
            rs = 0
            for r in exist1:
                x = x + r[1]
                rs = rs + r[2]
        else:
            x = 0
        return x

    def quantiteProduitIdTotale(self, id, m):
            var = str("stock" + m)
            cur = self.cur
            rs = 0
            cur.execute("SELECT * FROM " + var + " WHERE idProduit=%s and P=%s;", (id, 0))
            exist1 = cur.fetchall()
            if exist1:
                x = 0
                rs = 0
                for r in exist1:
                    x = x + r[1]
                    rs = rs + r[2]
                    x=x+rs
            else:
                 x = 0

            return x


            ########################################################"AJOUUUUUUUUUUUUUUUUT###########################################################

    def rechProd_ajout(self, nmP, dosage, bienEtre, forme):  ## La recherche des produits selon # marche bien ( testee)

        cur = self.cur



        cur.execute(''' SELECT * FROM produits WHERE nomProduit=%s and forme=%s
                                    and dosage=%s;''', (nmP, forme, dosage))



        exist1 = cur.fetchall()


        return exist1

    def rechStock(self, idP, date,cPh):
        cur = self.cur
        exist1 = cur.execute(''' SELECT * FROM stock'''+cPh+''' WHERE 
                                idProduit=%s
                                AND dateExp=%s and P=%s;''', (idP, date,0))

        return exist1

    def rechStock_sans_date(self, idP,cPh):
        cur = self.cur
        cur.execute(''' SELECT * FROM stock'''+cPh+''' WHERE 
                                        idProduit=%s and P=0;''',idP)
        exist1=cur.fetchall()


        return exist1

    def ajoutexiste(self, nmP, forme, dosage, b, rest, qte, date,cPh,lot):
        cur = self.cur

        if b == "b":
            bm = 1
        else:
            bm = 0
        exist1 = self.rechProd_ajout(nmP, dosage, bm, forme)


        if exist1:
            idprod = exist1[0][0]


            exist2 = self.rechStock(idP=idprod, date=date,cPh=cPh)
            if exist2:
                exist2 = cur.fetchall()
                qn = exist2[0][1]
                qr = exist2[0][2]


                qte = int(qte)

                if rest:
                    qr = qr + qte
                else:
                    qn = qn + qte

                cur.execute('''UPDATE stock'''+cPh+''' SET quantiteN=%s  WHERE dateExp =%s;''', (qn, date))
                self.conn.commit()
                cur.execute(''' UPDATE stock'''+cPh+''' SET quantiteR=%s WHERE dateExp = %s;''', (qr, date))
                self.conn.commit()
                cur.execute(''' UPDATE stock''' +cPh + ''' SET numlot=%s WHERE dateExp = %s;''', (lot, date))
                self.conn.commit()

            else:
                qn = 0
                qr = 0
                if rest:
                    qr = qte
                else:
                    qn = qte
                # on doit recuperer le max de idStock
                cur.execute("""SELECT MAX(idStock) FROM Stock"""+cPh)
                idstock = cur.fetchall()

                if idstock[0][0]:

                    idst = idstock[0][0] + 1
                else:
                    idst = 1
                cur.execute(
                    """INSERT INTO stock"""+cPh+""" (idStock,quantiteN,quantiteR,dateExp,idProduit,P,numlot)  VALUES (%s,%s,%s,%s,%s,%s,%s)""",(idst, qn, qr, date, idprod,0,lot))
                self.conn.commit()

        return exist1

        # self.master.show_frame(Ajou)

    def ajoutnew(self, nmP, forme, dosage, b, rest, qte, categorie, labo, prix, dci, notice, date,cPh,lot):

        cur = self.cur

        qr = 0
        qn = 0
        if rest:
            qr = qte
        else:
            qn = qte

        cur.execute("""SELECT MAX(idProduit) FROM Produits""")
        idp = cur.fetchall()
        maxp = idp[0][0] + 1

        cur.execute(
            """INSERT INTO Produits (idProduit,bm,categorie,nomProduit,labo,prix,dosage,forme,dci,notice,image,restituable) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",
            (maxp, b, categorie, nmP, labo, prix, dosage, forme, dci, notice, 1, 0))
        self.conn.commit()

        cur.execute("""SELECT MAX(idStock) FROM Stock"""+cPh)
        ids = cur.fetchall()
        if ids[0][0]:
            maxs = ids[0][0] + 1
        else :
            maxs =1

        cur.execute("""INSERT INTO Stock"""+cPh+"""(idStock,quantiteN,quantiteR,dateExp,idProduit,P,numlot)  VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                    (maxs, qn, qr, date, maxp,0,lot))

        self.conn.commit()

        ################################################################################################################################
        #                                                     POUR L'ACHAT DE PRODUITS                                                 #

    def vente_de_produits(self, entree,cPh):
        cur = self.cur
        # dans l'entree on a une liste de liste de donnees dont les champs seront :
        # 0 : idproduit, 1:quantite , 2: booleeen rest, 3: booleen commande
        # les produits existent tous dans la table " produits"
        # nous commencons d'abord par faire une recherche dans le stock de notre pharmacie de tous les produits demandés

        restVendu = 0
        newVendu = 0
        sortie = []
        for e in entree:
            if e[0] != 0:  # le produit existe ( id different de 0)

                resultat1 = self.rechStock_sans_date(e[0],cPh)


                # resultat 1 va contenir une liste de toutes les lignes de la table "stock" ou il ya ce produit
                if resultat1:  # si el produit exise en stock


                    # mais d'abord on recherche la date la plus petite

                    resultat4 = resultat1

                    k = 0  # representera le nombre de ligne de stock pour ce produit
                    for h in resultat1:
                        k = k + 1

                    w = k  # on le sauvegarde pour plus tard
                    datemin = datetime.date(1000, 12, 30)
                    quantite_initiale = e[1]
                    while e[1] != 0 and k != 0 and e[2]:  # tant qu'in reste des lignes de stock non etudiees # si le client accepte de prendre un produit restitue

                        resultat2 = self.RechPetiteDate(resultat1, datemin)

                        datemin = resultat2[3]


                        # nous allons decrementer de quantiteR
                        qr = resultat2[2]
                        if qr >= e[1]:
                            qr = qr - e[1]
                            e = (e[0], 0, e[2], e[3])
                            # le changement dans la bdd

                            cur.execute('''UPDATE stock'''+cPh+''' SET quantiteR=%s  WHERE idStock =%s;''', (qr, resultat2[0]))
                            self.conn.commit()
                        else:
                            var = e[1]
                            var = var - qr
                            e = (e[0], var, e[2], e[3])


                            if resultat2[1] != 0:
                                cur.execute('''UPDATE stock'''+cPh+''' SET quantiteR=%s  WHERE idStock =%s;''', (0, resultat2[0]))
                                self.conn.commit()
                            else:
                                cur.execute('''DELETE from stock'''+cPh+'''  WHERE idStock =%s;''', resultat2[0])
                                self.conn.commit()

                        k = k - 1
                    restVendu = quantite_initiale - e[1]

                    quantite_secondaire = e[1]

                    datemin = datetime.date(1000, 12, 30)
                    if not e[2] or (e[1] != 0):  #
                        while (e[1] != 0) and w != 0:
                            resultat2 = self.RechPetiteDate(resultat4, datemin)
                            datemin = resultat2[3]

                            qn = resultat2[1]
                            if (qn >= e[1]):
                                qn = qn - e[1]
                                e = (e[0], 0, e[2], e[3])
                                cur.execute('''UPDATE stock'''+cPh+''' SET quantiteN=%s  WHERE idStock =%s;''', (qn, resultat2[0]))
                                self.conn.commit()
                            else:
                                e = (e[0], e[1] - qn, e[2], e[3])

                                if resultat2[2] != 0:
                                    cur.execute('''UPDATE stock'''+cPh+''' SET quantiteN=%s  WHERE idStock =%s;''',
                                                (0, resultat2[0]))
                                    self.conn.commit()
                                else:
                                    cur.execute('''DELETE from stock'''+cPh+'''  WHERE idStock =%s;''', resultat2[0])
                                    self.conn.commit()

                            w = w - 1
                    newVendu = quantite_secondaire - e[1]

                sortie.append(e)

                if resultat1:
                    sortie.append(restVendu)
                    sortie.append(newVendu)
                else :
                    sortie.append(0)
                    sortie.append(0)



                #############################

        return sortie

        # pour enregistrer la sortie de produits restitués du stock sans notre table 'vente'

    def enregistreVente(self, entree,cPh):

        #entree : enregistremnt, vendu resr , vendu new
        #enregistrement :  0 : idproduit, 1:quantiterestante , 2: booleeen rest, 3: booleen commande
        cur = self.cur
        sortie = []

        # on récupere la date du jour
        date = datetime.date.today()

        k = 0
        for e in entree:
            k = k + 1
        w = 0
        while w < k:
            s=[]
            # on récupere l'id du produit:

            id = entree[w][0]
            c = entree[w][3]
            w = w + 1
            # on recupere la quantite rest sortie du stock
            qt = entree[w]
            w = w + 1
            # quantite new sortie du stock
            qt2 = entree[w]
            w = w + 1
            s.append(id)
            s.append(qt)
            s.append(qt2)
            s.append(c)

            sortie.append(s)

            if qt != 0 or qt2!=0:
                #on voit d'abord si la date existe deja POUR CE PRODUIT §

                #cur.execute('''SELECT * FROM ventes'''+cPh+''' WHERE ventes'''+cPh+'''.dateVente=%s AND idProduit=%s;''',(date,id))
                cur.execute('''SELECT * FROM ventes''' + cPh + ''' WHERE  idProduit=%s;''', ( id))
                resultat= []
                re=cur.fetchall()
                for i in re:
                    if i[3]==date:
                        resultat.append(i)

                if resultat:
                    quantite=resultat[0][1]+qt
                    quantite2=resultat[0][2]+qt2

                    cur.execute('''UPDATE ventes'''+cPh+''' SET quantiteR=%s  WHERE dateVente =%s;''',(quantite,date))
                    self.conn.commit()
                    cur.execute('''UPDATE ventes'''+cPh+''' SET  quantiteN=%s WHERE dateVente =%s;''',( quantite2, date))
                    self.conn.commit()

                else :
                    # on récupère le maxidvente:
                    cur.execute("""SELECT MAX(idVente) FROM ventes"""+cPh)
                    idvente = cur.fetchall()
                    if idvente[0][0]:
                        idv = idvente[0][0] + 1
                    else:
                        idv = 1


                    cur.execute('''INSERT INTO ventes'''+cPh+''' (idVente,quantiteR,quantiteN,idProduit,dateVente) values  (%s,%s,%s,%s,%s);''', (idv, qt,qt2, id,date))

                    self.conn.commit()


        # 0: id produit 1: qt vendue rest  2: qte new 3 : commande
        return sortie

    def listeProduits(self, entree):
        # lentree est une liste dont les element sont comm suit :
        # 0:dosage   1: quantite  2: rest  3: nomprodit  4: form  5 :commande  6 : bm
        sortie = []
        for e in entree:  # pour chaque produit on va generer son id dans la table produit

            self.cur.execute("SELECT * FROM produits where nomProduit=%s  AND forme=%s;",(e[3],e[4]))
            resultat=self.cur.fetchall()






            if resultat:
                idProduit = resultat[0][0]

                var = (idProduit, e[1], e[2], e[5])
            else:
                var = (0, e[1], e[2], e[5])

            sortie.append(var)


        return sortie

    def RechPetiteDate(self, e, petite):


        # recherche la ligne ou il y a la date d'expiration la plus proche

        re = (0, 0, 0, 0, 0)

        for i in e:

            date = datetime.date(3000, 12, 30)
            if (i[3] < date) and (i[3] > petite):
                re = i
                date = i[3]


        return re

    def facturation(self,entrees):
        sortie=[]
        inter = []
        # entree : enregistremnt, vendu resr , vendu new
        # enregistrement :  0 : idproduit, 1:quantiterestante , 2: booleeen rest, 3: booleen commande
        cur = self.cur
        k=0
        for i in entrees:
            k=k+1

        w=0
        prix=0
        for entree in entrees:

            #on recupere le prix, le nom et la forme, et le dosage
            if w==0:
                cur.execute('''SELECT * FROM produits WHERE  produits.idProduit=%s ;''', entree[0])
                resultat1 = cur.fetchall()
                if resultat1:
                    prix = resultat1[0][5]
                    nom = resultat1[0][3]
                    forme = resultat1[0][7]
                    dosage = resultat1[0][6]
                    restante = entree[1]
                    commande = entree[3]
                    inter.append(nom)
                    inter.append(forme)
                    inter.append(dosage)

            if w==1:
                donnee = entree

            if w==2:
                vendue = entree
                total = vendue * prix
                inter.append(vendue)
                inter.append(donnee)
                inter.append(restante)
                if commande:
                    inter.append('Oui')
                else:
                    inter.append('Non')
                inter.append(prix)
                inter.append(total)

                sortie.append(inter)
                inter=[]


            w=w+1
            if w==3:
                w=0
        return sortie


    def mes_commandes(self,cPh):
        cur=self.cur
        #on recupere les numeros des commandes pour lesquelles on a des reponses
        cur.execute('''SELECT nCommande FROM reponsecommande'''+cPh)
        numeros=cur.fetchall()
        num=[]
        c=[]
        if numeros :
            for i in numeros :
                num.append(i[0])
            num=sorted(num)
            #on supprime les doublants dans num:
            inter='impossible a trouver'
            n=[]
            for i in num :
                if i!=inter:
                    n.append(i)
                    inter=i
            les_commandes=[]
            #now on va récuperer toutes les commandes
            for i in n:
                les_commandes=[]
                # on recupere les infos de cette commande :
                cur.execute('''SELECT * FROM commandes WHERE nCommande=%s;''', i)
                test2 = cur.fetchall()
                maCommande=test2[0]
                # on va concatener ces infos dans une chaine de caractères
                commande1 =str("Commande N° "+str(i))
                #on recupere les infos du produit :
                cur.execute('''SELECT * FROM produits WHERE idProduit=%s;''',maCommande[1])
                res= cur.fetchall()
                res1=res[0]
                if res1[1]=="b":#produit de bien etre
                    commande2=str("Produit commandé : "+res1[3].upper().capitalize()+" - "+res1[7].upper().capitalize())
                else :
                    commande2 = str("Produit commandé : " + res1[3].upper().capitalize() + " - " + res1[7].upper().capitalize()+" - "+str(res1[6])+" (mg ou mg/l)")

                cur.execute('''SELECT * FROM reponsecommande''' + cPh+''' WHERE nCommande=%s;''',i)
                test=cur.fetchall()
                var = []
                var.append(commande1)
                var.append(commande2)
                h=[]
                for k in test:
                    h.append(k)
                pharmacies=[]

                #ici h est la liste des reponses pour cette commande , nous alons les structurer
                for w in h : # on ne doit pas afficher le code pharmacie , seuelemnt son nom
                    cur.execute('''SELECT pharmacie FROM contacts WHERE code=%s;''',w[1])
                    name=cur.fetchall()

                    namepharmacie=name[0][0]

                    infos =str("    Pharmacie: "+namepharmacie+"  , Le : "+str(w[2]))
                    pharmacies.append(infos)

                les_commandes.append(var)
                les_commandes.append(pharmacies)
                c.append(les_commandes)

            return c
        else :
            return 0

    def affichageConfimAchat(self ,entree):
        cur=self.cur
        sortie=[]
        var=[]
        # entree :#id quantite rest commande
        for e in entree :
            #on recupere le nom, la forme , le dosage et le prix du produit
            cur.execute('''SELECT * FROM produits WHERE  produits.idProduit=%s ;''', e[0])
            resultat2=cur.fetchall()
            if resultat2:
                # quantite

                resultat1=resultat2[0]
                nom=resultat1[3]
                forme =resultat1[7]
                dosage=resultat1[6]
                prix=resultat1[5]
                total=prix*e[1]
                var.append(nom)
                var.append(forme)
                var.append(dosage)
                var.append(e[1])
                var.append(e[3])
                var.append(prix)
                var.append(total)
                sortie.append(var)
                var=[]


        return sortie

    def reponses (self,n,me):
        liste=[]
        cur=self.cur
        cur.execute("SELECT code FROM reponsecommande"+me+" WHERE nCommande=%s;",n)
        res=cur.fetchall()
        for i in res :
            liste.append(i[0])

        return liste
    def supprimeCommande(self,me,n):
        cur =self.cur
        #de la table reponses
        #de ka table commndes
        var3 = str("reponsecommande" + me)
        # on recupere les reponses aux commandes
        cur.execute("SELECT code FROM "+var3+" where nCommande=%s",n)
        e=cur.fetchall()
        liste=[]
        for i in e :
            liste.append(i[0])
            # les infos du produit
        cur .execute('SELECT * from commandes where Ncommande=%s',n)
        f=cur.fetchall()
        qt=f[0][2]
        cur.execute("SELECT * FROM produits WHERE idProduit=%s", f[0][1])
        e = cur.fetchall()
        e2 = e[0]  # le produit
        if e2[1] == "b":
            medoc = str(e2[3] + " - " + e2[7])
        else:
            medoc = str(e2[3] + " - " + e2[7] + " - " + str(e2[6]) + " (mg ou mg/l)")
        #on envoie une notif de refus
        refus = str("Votre livraison de " + str(qt) + " " + medoc.upper().capitalize() + " a été refusée")
        cur.execute('SELECT MAX(idnotif) from notifications; ')
        e = cur.fetchone()
        if e[0]:
            id = e[0] + 1
        else:
            id = 1

        for i in liste:
            self.cur.execute('''insert into notifications (idnotif,notif,code) values (%s,%s,%s);''', (id, refus, i))
            self.conn.commit()
            id = id + 1

        # on supprime toutes les lignes de reponses pour cette commande
        cur.execute('''DELETE from  ''' + var3 + ''' WHERE Ncommande =%s;''', n)
        self.conn.commit()
        cur.execute('''DELETE from  commandes WHERE Ncommande =%s;''', n)
        self.conn.commit()
#####################################################notifications##################################################################################################
    def supprimeNotifs(self,cPh):
        cur=self.cur
        cur.execute(''' DELETE FROM notifications WHERE code=%s''', cPh)
        self.conn.commit()
    def recup_notifs(self,cPh):
        cur = self.cur
        cur.execute(''' SELECT * FROM notifications WHERE code=%s''', cPh)
        e=cur.fetchall()



##################################################################################################################
#  affichage reponses aux commandes

    def cmdRecu(self, Cph):
        np = []
        form = []
        dos = []
        phar = []
        sortie = []
        qt = []
        num=[]
        cur = self.cur
        cur.execute('''SELECT * FROM commandes WHERE CodeEnvoyeur != %s''', Cph)
        exist = cur.fetchall()
        for e in exist:
            num.append(e[0])
            qt.append(e[2])
            cur.execute('''SELECT * FROM produits WHERE produits.idProduit =%s''', e[1])
            exist1 = cur.fetchall()

            for i in exist1:
                np.append(i[3])
                dos.append(i[6])
                form.append(i[7])

        k = []
        cur.execute('''SELECT CodeEnvoyeur FROM commandes WHERE commandes.CodeEnvoyeur !=%s''', Cph)
        k = cur.fetchall()

        ex = []
        for s in k:
            cur.execute('''SELECT pharmacie FROM contacts WHERE contacts.code=%s''', s[0])
            ex = cur.fetchall()
            phar.append(ex[0])

        sortie.append(phar)
        sortie.append(np)
        sortie.append(dos)
        sortie.append(form)
        sortie.append(qt)
        sortie.append(num)
        return sortie

  #############################################################################################

    def rechercheStock3(self,numlot,idPd, cPh):

        cur = self.cur
        stock = "stock" + cPh

        cur.execute(''' SELECT * FROM ''' + stock + ''' WHERE idProduit=%s AND numlot=%s AND P=0;''', (idPd,numlot))
        exist1 = cur.fetchall()
        return exist1

    ###################################################################
    def quantiteLot(self,numlot, nmP,cPh, forme):
            list = []
            rs = 0
            exist = self.rechProd(nmP=nmP, forme=forme)

            if exist:
                e = exist[0][0]
                exist1 = self.rechercheStock3(numlot,e,cPh)

                if exist1:
                    x = 0
                    rs = 0
                    for r in exist1:
                        x = x + r[1]
                        rs = rs + r[2]


                else:
                    x = 0

                t = x + rs


            else:

                x = 0
                rs = 0
                t = 0
            x = str(x)
            rs = str(rs)
            t = str(t)
            list.append(x)
            list.append(rs)
            list.append(t)

            return list

        ####################################################################



    # pour les produits périmes
    def perimes(self,cPh):
        # on les recupere de la table stock correspondate a l'utilisateur
        cur=self.cur
        cur.execute("SELECT * from stock"+cPh+" where P=1")
        sortie=[]
        e=cur.fetchall()
        if e:
            for i in e :
                var=[]
                #on recupere les infos du produit

                cur.execute("SELECT * from produits where idProduit=%s",i[4])
                f=cur.fetchall()
                var.append(f[0][3].upper().capitalize())# le nom

                var.append(f[0][6])#le dosage
                var.append(f[0][7])# la forme
                var.append(i[1]+i[2])# la quantité totale
                var.append(i[3])# la date d'expiration
                var.append(i[6])# le lot
                sortie.append(var)

        return sortie
    def suppr_perim(self,code):
        cur=self.cur
        cur.execute("DELETE from stock"+code+" where P=1;")
        self.conn.commit()


#########################################################################################""
class Chargement (Frame):


    def __init__(self, parent, controller=None):
        Frame.__init__(self, parent)

        self.controller = controller



        font9 = "-family {Futura Bk BT} -size 15 -weight bold -slant "  \
            "roman -underline 0 -overstrike 0"

        font11 = "-family {Futura Bk BT} -size 16 -weight bold -slant "  \
            "roman -underline 0 -overstrike 0"




        self.hautFrame = Frame(self)
        self.hautFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.hautFrame.configure(borderwidth="2")
        self.hautFrame.configure(background="#ffffff")
        self.hautFrame.configure(highlightbackground="#ffffff")
        self.hautFrame.configure(highlightcolor="black")
        self.hautFrame.configure(width=945)

        self.titleLabel = Label(self.hautFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(activebackground="#f9f9f9")
        self.titleLabel.configure(activeforeground="black")
        self.titleLabel.configure(background="#ffffff")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(foreground="#000000")
        self.titleLabel.configure(highlightbackground="#ffffff")
        self.titleLabel.configure(highlightcolor="black")
        self._img1 = PhotoImage(file="images/vide.png")
        self.titleLabel.configure(image=self._img1)

        font12 = "-family {Futura Bk BT} -size 14 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"




        self.bodyframe = Frame(self)
        self.bodyframe.place(relx=0.0, rely=0.21, relheight=0.92, relwidth=1.0)
        self.bodyframe.configure(borderwidth="2")
        self.bodyframe.configure(background="#ffffff")
        self.bodyframe.configure(width=935)

        self.Labelbody = Label(self.bodyframe)
        self.Labelbody.place(relx=0.0, rely=0.0, height=700, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)

        self.Labelbody.configure(width=935)

        nmpLabel = Label(self.bodyframe)
        nmpLabel.place(relx=0.40, rely=0.24, height=34, width=200)
        nmpLabel.configure(anchor=W)
        nmpLabel.configure(background="#ffffff")
        nmpLabel.configure(disabledforeground="#fafafa")
        nmpLabel.configure(font=font12)
        nmpLabel.configure(foreground="#000000")
        nmpLabel.configure(text='''Chargement ....''')
        nmpLabel.configure(width=202)
        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img124 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img124)





        # barre de chargement
        self.p = ttk.Progressbar(self, mode='determinate', length=350)


        self.p.pack()
        self.p.place(relx=0.3, rely=0.57)


        self.p.start()
        self.p.after(5000, self.stop_progressbar)
    def stop_progressbar(self):
        self.p.stop()
        self.controller.show_frame(Bienvenue)







#########################################################################################################################

class Produits(Frame):
    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var=self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res :
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()



    def affichPage(self):
        self.titleLabel = Label(self.headFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")

        self.titleLabel.configure(foreground="#fafafa")
        self.titleLabel.configure(width=362)
        self._img701 = PhotoImage(file="images/prod_cat.png")
        self.titleLabel.configure(image=self._img701)
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        self.retourButt.destroy()
        self.treeView = ttk.Treeview(self.bodyFrame)
        self.treeView.place(relx=0.1, rely=0.035, relheight=0.76, relwidth=0.8)
        self.scroll = Scrollbar(self.bodyFrame, bd=1, command=self.treeView.yview)
        self.treeView.config(yscrollcommand=self.scroll.set)

        self.scroll.place(relx=0.87, rely=0.035, relheight=0.76, relwidth=0.03)
        con = connectBdd()
        catego = con.categories()
        #        self.img1 = PhotoImage(file="images/stock_2.png")
        # self.img2=PhotoImage(file="images/stat_2.png")

        i, j = 0, 0
        self.treeView.heading("#0")
        for c in catego:
            produits = con.produitsDeCatego(catego[i])

            self.treeView.insert('', i, "item" + str(i), text=c, tag="categorie")  # ,image=self.img1)

            for p in produits:
                self.treeView.insert("item" + str(i), j, "item" + str(j + len(catego)), text="{:19}".format(p[0])
                                                                                             + "{:>17}".format(
                    p[1]) + "{:>15}".format(p[2]), tag="produit")
                j += 1

            i += 1

        self.treeView.tag_configure("categorie", font=self.font14)
        self.treeView.tag_configure("produit", font=self.font12)

        self.retourButt = Button(self.bodyFrame)
        self.retourButt.place(relx=0.4, rely=0.86, height=40, width=180)
        self.retourButt.configure(activebackground="#d9d9d9")
        self.retourButt.configure(font=self.font12)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')
        self.retourButt.configure(width=100)
        self.retourButt['command'] = self.retour2


    # self.master.master.show_frame(Affichage_Des_Produits)
    def retour2(self):
        self.treeView.destroy()
        self.scroll.destroy()
        self.titleLabel = Label(self.headFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")

        self.titleLabel.configure(foreground="#fafafa")
        self.titleLabel.configure(width=362)
        self._img7 = PhotoImage(file="images/np.png")
        self.titleLabel.configure(image=self._img7)

        self.retourButt = Button(self.bodyFrame)
        self.retourButt.place(relx=0.4, rely=0.86, height=40, width=180)
        self.retourButt.configure(activebackground="#d9d9d9")
        self.retourButt.configure(font=self.font12)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')
        self.retourButt.configure(width=100)
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        self.retourButt['command'] = self.retour

    def recherchePage(self):
        self.master.master.show_frame(Recherche_Produit)

    def rechercheEqPage(self):
        self.master.master.show_frame(Recherche_Des_equivalents)

    def retour(self):
        self.master.master.show_frame(Acceuil)

    def GestionDeCompte(self):
        self.retour2()
        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()
    def notifs(self):
        if self.notif==0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])


                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                              height=1, bg='white',anchor="w",
                              font=self.font12).grid(row=r,
                                                     column=1)
                    r = r + 1
                r = 0
                self.notif=1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=818)
                self.supprnotifs.configure(activebackground="#009D78")
                self.supprnotifs.configure(activeforeground="#009D78")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command']=self.supprimenotifs
            else:
                showinfo("Pas de notifications","Vous n'avez pas de notifications !")

        else :
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif=0
    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con=connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0

    def __init__(self, parent, controller=None):
        Frame.__init__(self, parent)
        self.controller = controller
        self.font19 = "-family {Futura Bk BT} -size 15 -weight bold " \
                      "-slant roman -underline 0 -overstrike 0"
        font14 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        self.font14=font14

        font11 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        font15 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        self.font12=font12

        self.headFrame = Frame(self)
        self.headFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.headFrame.configure(borderwidth="2")
        self.headFrame.configure(background="#009D78")
        self.headFrame.configure(width=565)

        self.titleLabel = Label(self.headFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(font=font11)
        self.titleLabel.configure(foreground="#fafafa")
        self.titleLabel.configure(width=362)
        self._img7 = PhotoImage(file="images/np.png")
        self.titleLabel.configure(image=self._img7)
        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0

        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)



        self.bodyFrame = Frame(self)
        self.bodyFrame.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1)

        self.bodyFrame.configure(relief=FLAT)
        self.bodyFrame.configure(borderwidth="0")
        self.bodyFrame.configure(relief=FLAT)
        self.bodyFrame.configure(background="#ffffff")
        self.bodyFrame.configure(width=7935)

        self.Labelbody = Label(self.bodyFrame)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)

        self.affichButt = Button(self.bodyFrame)
        self.affichButt.place(relx=0.3, rely=0.13, height=70, width=357)
        self.affichButt.config(relief=RIDGE)
        self.affichButt.configure(activebackground="#d9d9d9")
        self.affichButt.configure(activeforeground="#000000")
        self.affichButt.configure(background="#ffffff")
        self.affichButt.configure(disabledforeground="#a3a3a3")
        self.affichButt.configure(foreground="#000000")
        self.affichButt.configure(highlightbackground="#ffffff")
        self.affichButt.configure(highlightcolor="black")
        self.affichButt.configure(pady="0")
        self.affichButt.configure(font=self.font19)
        # self.affichButt.configure(width=357)

        self.affichButt['command'] = self.affichPage
        self.affichButt.configure(text='''Affichage des Produits Disponibles''')

        self.rechButt = Button(self.bodyFrame)
        self.rechButt.place(relx=0.3, rely=0.36, height=70, width=357)
        self.rechButt.configure(activebackground="#d9d9d9")
        self.rechButt.configure(activeforeground="#000000")
        self.rechButt.configure(background="#ffffff")
        self.rechButt.configure(disabledforeground="#a3a3a3")
        self.rechButt.configure(foreground="#000000")
        self.rechButt.configure(highlightbackground="#ffffff")
        self.rechButt.configure(highlightcolor="black")
        self.rechButt.configure(pady="0")
        self.rechButt.config(text='''Recherche D'un Produit''')
        self.rechButt.configure(font=self.font19)
        self.rechButt.configure(relief=RIDGE)

        self.rechButt['command'] = self.recherchePage

        self.rechEqButt = Button(self.bodyFrame)
        self.rechEqButt.place(relx=0.3, rely=0.58, height=70, width=357)
        self.rechEqButt.configure(activebackground="#d9d9d9")
        self.rechEqButt.configure(activeforeground="#000000")
        self.rechEqButt.configure(background="#ffffff")
        self.rechEqButt.configure(disabledforeground="#a3a3a3")
        self.rechEqButt.configure(foreground="#000000")
        self.rechEqButt.configure(highlightbackground="#ffffff")
        self.rechEqButt.configure(highlightcolor="black")
        self.rechEqButt.configure(pady="0")
        self.rechEqButt.configure(text='''Recherche des Equivalents''')
        self.rechEqButt.configure(font=self.font19)
        self.rechEqButt.configure(relief=RIDGE)

        self.rechEqButt['command'] = self.rechercheEqPage




        self.retourButt = Button(self.bodyFrame)
        self.retourButt.place(relx=0.4, rely=0.86, height=40, width=180)
        self.retourButt.configure(activebackground="#d9d9d9")
        self.retourButt.configure(font=font12)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')
        self.retourButt.config(command = self.retour)

        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img1 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img1)





##########################################################################################
class Affichage_Des_Produits(Frame):

    def retour(self):
        self.master.master.show_frame(Produits)

    def __init__(self, parent, controller=None):
        Frame.__init__(self, parent)
        self.controller = controller

        font11 ="-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        font12 ="-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        font14 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        self.headFrame = Frame(self)
        self.headFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.headFrame.configure(borderwidth="2")
        self.headFrame.configure(background="#009D78")
        self.headFrame.configure(width=125)

        self.titleLabel = Label(self.headFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(font=font11)
        self.titleLabel.configure(foreground="#fafafa")
        self.titleLabel.configure(text='''Affichage Des Produits''')
        self.titleLabel.configure(width=382)
        self._img7 = PhotoImage(file="images/np.png")
        self.titleLabel.configure(image=self._img7)

        self.footFrame = Frame(self)
        self.footFrame.place(relx=0.0, rely=0.88, relheight=0.12, relwidth=1.0)
        self.footFrame.configure(borderwidth="2")
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(highlightbackground="#ffffff")
        self.footFrame.configure(highlightcolor="black")
        self.footFrame.configure(width=125)

        self.rightFrame = Frame(self)
        self.rightFrame.place(relx=0.9, rely=0.21, relheight=0.76, relwidth=0.1)
        self.rightFrame.configure(borderwidth="2")
        self.rightFrame.configure(background="#ffffff")
        self.rightFrame.configure(highlightbackground="#ffffff")
        self.rightFrame.configure(highlightcolor="black")
        self.rightFrame.configure(width=125)

        self.leftFrame = Frame(self)
        self.leftFrame.place(relx=0.0, rely=0.21, relheight=0.76, relwidth=0.1)
        self.leftFrame.configure(borderwidth="2")
        self.leftFrame.configure(background="#ffffff")
        self.leftFrame.configure(highlightbackground="#ffffff")
        self.leftFrame.configure(highlightcolor="black")
        self.leftFrame.configure(width=125)

        self.bodyFrame = Frame(self)
        self.bodyFrame.place(relx=0.1, rely=0.21, relheight=0.76, relwidth=0.8)
        self.bodyFrame.configure(borderwidth="2")
        self.bodyFrame.configure(background="#ffffff", relief=FLAT)
        self.bodyFrame.configure(width=125)

        self.treeView = ttk.Treeview(self.bodyFrame)
        self.treeView.place(relx=0.1, rely=0.12, relheight=0.76, relwidth=0.8)
        self.scroll = Scrollbar(self.bodyFrame, bd=1, command=self.treeView.yview)
        self.treeView.config(yscrollcommand=self.scroll.set)

        self.scroll.place(relx=0.87, rely=0.12, relheight=0.76, relwidth=0.03)
        con = connectBdd()
        catego = con.categories()
        #        self.img1 = PhotoImage(file="images/stock_2.png")
        # self.img2=PhotoImage(file="images/stat_2.png")

        i, j = 0, 0
        self.treeView.heading("#0")
        for c in catego:
            produits = con.produitsDeCatego(catego[i])

            self.treeView.insert('', i, "item" + str(i), text=c, tag="categorie")  # ,image=self.img1)

            for p in produits:
                self.treeView.insert("item" + str(i), j, "item" + str(j + len(catego)), text="{:19}".format(p[0])
                                                                                             + "{:>17}".format(
                    p[1]) + "{:>15}".format(p[2]), tag="produit")
                j += 1

            i += 1

        self.treeView.tag_configure("categorie", font=font14)
        self.treeView.tag_configure("produit", font=font12)


        self.retourButt = Button(self.bodyFrame)
        self.retourButt.place(relx=0.4, rely=0.86, height=40, width=180)
        self.retourButt.configure(activebackground="#d9d9d9")
        self.retourButt.configure(font=font12)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')
        self.retourButt.config(command = self.retour)


        con.fermer()


###############################################################################################

###############################################################################################
class Recherche_Produit(Frame):
    font11 = "-family {Futura Bk BT} -size 20 -weight bold -slant " \
             "roman -underline 0 -overstrike 0"
    font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
             "roman -underline 0 -overstrike 0"

    # ' pour les notifications'
    def GestionDeCompte(self):
        try:
            self.retour()
        except:
            pass
        try:
            self.retour2()
        except:
            pass


        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()

    def notifs(self):
        if self.notif == 0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])

                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                          height=1, bg='white', anchor="w",
                          font=self.font12).grid(row=r,
                                                 column=1)
                    r = r + 1
                r = 0
                self.notif = 1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=818)
                self.supprnotifs.configure(activebackground="#009D78")
                self.supprnotifs.configure(activeforeground="#009D78")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command'] = self.supprimenotifs
            else:
                showinfo("Pas de notifications", "Vous n'avez pas de notifications !")

        else:
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif = 0

    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con = connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0

    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var = self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res:
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()

    def updateDosage(self, *args):

        if self.bienCheckVar.get():
            self.dosageVar = self.dosageEntryVar.get()
            self.dosageEntry.config(state="readonly")
            self.dosageEntryVar.set("")
        else:
            self.dosageEntry.config(state="normal")
            self.dosageEntryVar.set(self.dosageVar)

    def retour(self):
        self.retourButt.destroy()
        try:
            self.scrollable_canvas.destroy()
        except:
            pass
        self.dosageEntryVar.set("")
        self.nmpEntryVar.set("")
        self.formeEntryVar.set("")
        self.rechButt = Button(self.bodyFrame)
        self.rechButt.place(relx=0.64, rely=0.86, height=40, width=180)

        self.rechButt.configure(activebackground="#d9d9d9")
        self.rechButt.configure(activeforeground="#000000")
        self.rechButt.configure(background="#ffffff")
        self.rechButt.configure(disabledforeground="#a3a3a3")
        self.rechButt.configure(font=self.font12)
        self.rechButt.configure(foreground="#000000")
        self.rechButt.configure(highlightbackground="#ffffff")
        self.rechButt.configure(highlightcolor="black")
        self.rechButt.configure(pady="0")
        self.rechButt.configure(relief=RIDGE)
        self.rechButt.configure(text='''Rechercher''')
        self.rechButt['command'] = self.submit

        self.retourButt = Button(self.bodyFrame)
        self.retourButt['command'] = self.retour
        self.retourButt.place(relx=0.17, rely=0.86, height=40, width=180)
        self.retourButt.configure(activebackground="#d9d9d9")
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(font=self.font12)
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')

        self.controller.show_frame(Produits)

    def submit(self):
        con = connectBdd()
        self.exist = con.rechercheProduit(nmP=self.nmpEntry.get()
                                          , dosage=self.dosageEntry.get(), forme=self.formeEntry.get()
                                          , bienEtre=self.bienCheckVar.get())

        if self.exist:
            self.affichage()
        else:
            showinfo("Produit Non Existant ", " Le Produit que vous cherchez n'existe pas ! ")
        con.fermer()

    def affichage(self):
        self.destruction()
        self.scrollable_canvas = ScrollableCanvasProduit(self)
        self.scrollable_canvas.grid(row=1, column=1)
        self.scrollable_canvas.place(relx=0.1, rely=0.23)

        self.donnees[:] = []
        self.var = ('Catégorie :', 'Nom Du Produit :', 'Forme', 'Dosage(mg ou mg/l)', 'Laboratoire :', 'Prix (DA) :'
                    , 'DCI :',)
        for variable in self.exist:
            self.donnees.append(variable)
        r = 0
        for i in self.var:
            self.label1 = Label(self.scrollable_canvas.interior, text=i, relief=FLAT, width=18, height=1,anchor="w", bg='#ffffff',
                                foreground="#009D78", font=self.font12).grid(row=r, column=1)
            r = r + 1
        self.label1 = Label(self.scrollable_canvas.interior, text="Notice :",relief=FLAT, width=18,anchor="w", height=12,
                            bg='#ffffff',
                            foreground="#009D78", font=self.font12).grid(row=r, column=1)
        r = 0


        self.label1 = Label(self.scrollable_canvas.interior, text=self.donnees[0][2], relief=FLAT, width=55, height=1,anchor="w",
                            bg='#ffffff', font=self.font12).grid(row=0, column=2)
        self.label1 = Label(self.scrollable_canvas.interior, text=self.donnees[0][3], relief=FLAT, width=55, height=1,anchor="w",
                            bg='#ffffff', font=self.font12).grid(row=1, column=2)
        self.label1 = Label(self.scrollable_canvas.interior, text=self.donnees[0][7], relief=FLAT, width=55, height=1,anchor="w",
                            bg='#ffffff', font=self.font12).grid(row=2, column=2)
        self.label1 = Label(self.scrollable_canvas.interior, text=self.donnees[0][6], relief=FLAT, width=55, height=1,anchor="w",
                            bg='#ffffff', font=self.font12).grid(row=3, column=2)
        self.label1 = Label(self.scrollable_canvas.interior, text=self.donnees[0][4], relief=FLAT, width=55, height=1,anchor="w",
                            bg='#ffffff', font=self.font12).grid(row=4, column=2)
        self.label1 = Label(self.scrollable_canvas.interior, text=self.donnees[0][5], relief=FLAT, width=55, height=1,anchor="w",
                            bg='#ffffff', font=self.font12).grid(row=5, column=2)
        self.label1 = Label(self.scrollable_canvas.interior, text=self.donnees[0][8], relief=FLAT, width=55, height=1,anchor="w",
                            bg='#ffffff', font=self.font12).grid(row=6, column=2)

        T = Text(self.scrollable_canvas.interior, height=12, width=55, relief=FLAT, font=self.font12)
        S = Scrollbar(self.scrollable_canvas.interior)

        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        T.grid(row=7, column=2)
        S.place(relx=0.967,rely=0.43,relheight=0.565,relwidth=0.033)


        T.insert(END, self.donnees[0][10])
        T.config(state=DISABLED)

        self.retourButt = Button(self.bodyFrame)
        self.retourButt['command'] = self.retour
        self.retourButt.place(relx=0.4, rely=0.86, height=40, width=180)
        self.retourButt.configure(activebackground="#d9d9d9")
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(font=self.font12)
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')

    def destruction(self):
        self.rechButt.destroy()
        self.retourButt.destroy()

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller

        font11 = "-family {Futura Bk BT} -size 20 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        self.donnees = []
        headFrame = Frame(self)
        headFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        headFrame.configure(relief=FLAT)
        headFrame.configure(borderwidth="2")
        headFrame.configure(relief=FLAT)
        headFrame.configure(background="#009D78")
        headFrame.configure(width=950)


        self.titleLabel = Label(headFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(activebackground="#336464")
        self.titleLabel.configure(activeforeground="white")
        self.titleLabel.configure(activeforeground="black")
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(font=font11)
        self.titleLabel.configure(foreground="#ffffff")
        self.titleLabel.configure(highlightbackground="#ffffff")
        self.titleLabel.configure(highlightcolor="black")
        self._img6 = PhotoImage(file="images/rech.png")
        self.titleLabel.configure(image=self._img6)

        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0

        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        footFrame = Frame(self)
        footFrame.place(relx=0.0, rely=0.9, relheight=0.09, relwidth=1.0)
        footFrame.configure(relief=FLAT)
        footFrame.configure(borderwidth="2")
        footFrame.configure(relief=FLAT)
        footFrame.configure(background="#ffffff")
        footFrame.configure(highlightbackground="#3fa693")
        footFrame.configure(highlightcolor="#3fa693")
        footFrame.configure(width=935)

        bodyFrame = Frame(self)
        bodyFrame.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1.0)

        bodyFrame.configure(relief=FLAT)
        bodyFrame.configure(borderwidth="2")
        bodyFrame.configure(relief=FLAT)
        bodyFrame.configure(background="#ffffff")
        bodyFrame.configure(width=745)
        self.bodyFrame=bodyFrame

        self.Labelbody = Label(self.bodyFrame)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)

        nmpLabel = Label(bodyFrame)
        nmpLabel.place(relx=0.22, rely=0.15, height=34, width=200)
        nmpLabel.configure(anchor=W)
        nmpLabel.configure(background="#ffffff")
        nmpLabel.configure(disabledforeground="#fafafa")
        nmpLabel.configure(font=font12)
        nmpLabel.configure(foreground="#000000")
        nmpLabel.configure(text='''Nom Du Produit :''')
        nmpLabel.configure(width=202)

        self.exist = []

        # on genere la liste des produits existants:
        self.liste_produits = []
        var = connectBdd()
        cur = var.cur
        cur.execute("""SELECT nomProduit FROM produits""")
        resultat1 = cur.fetchall()

        for inter in resultat1:
            for inter2 in inter:
                var = inter2.lower().capitalize()
                self.liste_produits.append(var)

        self.liste_produits = sorted(self.liste_produits)
        # on supprime les doublants dans cette liste:
        self.inter = ""
        self.liste_products = []
        for produit in self.liste_produits:
            if produit != self.inter:
                self.liste_products.append(produit)
                self.inter = produit

        self.nmpEntryVar = StringVar()
        self.nmpEntry = Combobox(self.bodyFrame, textvariable=self.nmpEntryVar, values=self.liste_products,
                                 state="readonly")
        self.nmpEntry.place(relx=0.45, rely=0.15, relheight=0.06, relwidth=0.38)
        self.nmpEntry.configure(background="#ffffff")




        dosageLabel = Label(bodyFrame)
        dosageLabel.place(relx=0.22, rely=0.33, height=34, width=200)
        dosageLabel.configure(activebackground="#fafafa")
        dosageLabel.configure(activeforeground="black")
        dosageLabel.configure(anchor=W)
        dosageLabel.configure(background="#ffffff")
        dosageLabel.configure(disabledforeground="#a3a3a3")
        dosageLabel.configure(font=font12)
        dosageLabel.configure(foreground="#000000")
        dosageLabel.configure(highlightbackground="#ffffff")
        dosageLabel.configure(highlightcolor="black")
        dosageLabel.configure(text='''Dosage  :''')
        dosageLabel.configure(width=112)

        self.dosageEntryVar = IntVar()
        self.dosageEntry = Entry(bodyFrame, textvariable=self.dosageEntryVar)
        self.dosageEntry.place(relx=0.45, rely=0.33, relheight=0.06
                               , relwidth=0.38)
        self.dosageEntry.configure(background="#ffffff")
        self.dosageEntry.configure(relief=RIDGE)
        self.dosageEntry.configure(disabledforeground="#a3a3a3")
        self.dosageEntry.configure(font=font12)
        self.dosageEntry.configure(foreground="#000000")
        self.dosageEntry.configure(highlightbackground="#ffffff")
        self.dosageEntry.configure(highlightcolor="black")
        self.dosageEntry.configure(borderwidth='1')
        self.dosageEntry.configure(insertbackground="black")
        self.dosageEntry.configure(selectbackground="#c4c4c4")
        self.dosageEntry.configure(selectforeground="black")

        self.formeLabel = Label(bodyFrame)
        self.formeLabel.place(relx=0.22, rely=0.56, height=34, width=200)
        self.formeLabel.configure(activebackground="#f9f9f9")
        self.formeLabel.configure(activeforeground="black")
        self.formeLabel.configure(anchor=W)
        self.formeLabel.configure(background="#ffffff")
        self.formeLabel.configure(disabledforeground="#a3a3a3")
        self.formeLabel.configure(font=font12)
        self.formeLabel.configure(foreground="#000000")
        self.formeLabel.configure(highlightbackground="#ffffff")
        self.formeLabel.configure(highlightcolor="black")
        self.formeLabel.configure(text='''Forme   :''')

        self.formeEntryVar = StringVar()

        con = connectBdd()
        con.cur.execute("SELECT forme from produits ");
        e = con.cur.fetchall()
        self.liste_formes = []
        k = []
        for m in e:
            k.append(m[0])

        k = set(k)
        for i in k:
            self.liste_formes.append(i)
        con.fermer()
        # self.liste_formes = (
        # 'Comprime', 'Suppositoire', 'Sirop', 'Solution buvable', 'Gelule', 'Solution injectable', 'ComprimeEfferv',
        # 'Poudre', 'Liquide', 'Pommade', 'Gel', 'Sachet', 'Capsule', 'Goute', 'Ampoule', '')

        self.liste_formes = sorted(self.liste_formes)
        self.formeEntry = Combobox(self.bodyFrame, textvariable=self.formeEntryVar, values=self.liste_formes,
                                  state="readonly")




        self.formeEntry.place(relx=0.45, rely=0.56, relheight=0.06
                              , relwidth=0.38)
        self.formeEntry.configure(background="#ffffff")


        self.bienCheckVar = IntVar()
        self.bienCheckVar.trace("w", self.updateDosage)
        self.bienCheck = Checkbutton(bodyFrame)
        self.bienCheck.place(relx=0.45, rely=0.42, relheight=0.06, relwidth=0.38)

        self.bienCheck.configure(activebackground="#d9d9d9")
        self.bienCheck.configure(activeforeground="#000000")
        self.bienCheck.configure(anchor=W)
        self.bienCheck.configure(background="#ffffff")
        self.bienCheck.configure(borderwidth="10")
        self.bienCheck.configure(disabledforeground="#a3a3a3")
        self.bienCheck.configure(font=font12)
        self.bienCheck.configure(foreground="#000000")
        self.bienCheck.configure(highlightbackground="#000000")
        self.bienCheck.configure(highlightcolor="black")
        self.bienCheck.configure(justify=LEFT)
        self.bienCheck.configure(text='''Bien_Etre''')
        self.bienCheck.configure(variable=self.bienCheckVar)
        self.bienCheck.configure(width=439)

        self.rechButt = Button(bodyFrame)
        self.rechButt.place(relx=0.64, rely=0.86, height=40, width=180)

        self.rechButt.configure(activebackground="#d9d9d9")
        self.rechButt.configure(activeforeground="#000000")
        self.rechButt.configure(background="#ffffff")
        self.rechButt.configure(disabledforeground="#a3a3a3")
        self.rechButt.configure(font=font12)
        self.rechButt.configure(foreground="#000000")
        self.rechButt.configure(highlightbackground="#ffffff")
        self.rechButt.configure(highlightcolor="black")
        self.rechButt.configure(pady="0")
        self.rechButt.configure(relief=RIDGE)
        self.rechButt.configure(text='''Rechercher''')
        self.rechButt['command'] = self.submit

        self.retourButt = Button(bodyFrame)
        self.retourButt['command'] = self.retour
        self.retourButt.place(relx=0.17, rely=0.86, height=40, width=180)
        self.retourButt.configure(activebackground="#d9d9d9")
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(font=font12)
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')

        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img1 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img1)


################################################################################################
class ScrollableCanvasProduit(Frame):
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        canvas = Canvas(self, background='#FFFFFF', width=700, height=400, scrollregion=(0, 0, 500, 500))

        canvas.config(width=850, height=400)

        canvas.pack(side=RIGHT, expand=True, fill=BOTH)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)

class ScrollableCanvasEquivalent(Frame):
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        canvas = Canvas(self, bg='#FFFFFF', width=700, height=400, scrollregion=(0, 0, 500, 500))

        vbar = Scrollbar(self, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=canvas.yview)
        canvas.config(width=850, height=344)
        canvas.config(yscrollcommand=vbar.set)
        canvas.pack(side=RIGHT, expand=True, fill=BOTH)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)

##111111111111111111##############################################################################################
class Recherche_Des_equivalents(Frame):

    def GestionDeCompte(self):
        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()
        try :
            self.scrollable_canvas.destroy()
            self.retourButt.destroy()
            self.title.destroy()
            self.rechButt = Button(self.bodyFrame)
            self.rechButt.config(command=self.submit)
            self.rechButt.place(relx=0.64, rely=0.86, height=40, width=180)
            self.rechButt.configure(activeforeground="#000000")
            self.rechButt.configure(background="#ffffff")
            self.rechButt.configure(disabledforeground="#a3a3a3")
            self.rechButt.configure(font=self.font12)
            self.rechButt.configure(foreground="#000000")
            self.rechButt.configure(highlightbackground="#ffffff")
            self.rechButt.configure(highlightcolor="black")
            self.rechButt.configure(pady="0")
            self.rechButt.configure(relief=RIDGE)
            self.rechButt.configure(text='''Rechercher''')
            self.rechButt.configure(width=176)

            self.retourButt = Button(self.bodyFrame)
            self.retourButt.place(relx=0.17, rely=0.86, height=40, width=180)
            self.retourButt.configure(font=self.font12)
            self.retourButt.configure(activeforeground="#000000")
            self.retourButt.configure(background="#ffffff")
            self.retourButt.configure(disabledforeground="#a3a3a3")
            self.retourButt.configure(foreground="#000000")
            self.retourButt.configure(highlightbackground="#ffffff")
            self.retourButt.configure(highlightcolor="black")
            self.retourButt.configure(pady="0")
            self.retourButt.configure(relief=RIDGE)
            self.retourButt.configure(text='''Retour''')
            self.retourButt.configure(width=100)
            self.retourButt.configure(pady="0")
            self.retourButt.config(command=self.retour)


        except :
            pass


    def notifs(self):
        if self.notif == 0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])

                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                          height=1, bg='white', anchor="w",
                          font=self.font12).grid(row=r,
                                                 column=1)
                    r = r + 1
                r = 0
                self.notif = 1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=818)
                self.supprnotifs.configure(activebackground="#009D78")
                self.supprnotifs.configure(activeforeground="#009D78")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command'] = self.supprimenotifs
            else:
                showinfo("Pas de notifications", "Vous n'avez pas de notifications !")

        else:
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif = 0

    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con = connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0

    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var = self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res:
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()

    def retour(self):
        self.dciEntryVar.set("")
        self.categoEntryVar.set("")
        try:
            self.scrollable_canvas.destroy()
            self.retourButt.destroy()
            self.title.destroy()
        except:
            pass

        self.rechButt = Button(self.bodyFrame)
        self.rechButt.config(command=self.submit)
        self.rechButt.place(relx=0.64, rely=0.86, height=40, width=180)
        self.rechButt.configure(activeforeground="#000000")
        self.rechButt.configure(background="#ffffff")
        self.rechButt.configure(disabledforeground="#a3a3a3")
        self.rechButt.configure(font=self.font12)
        self.rechButt.configure(foreground="#000000")
        self.rechButt.configure(highlightbackground="#ffffff")
        self.rechButt.configure(highlightcolor="black")
        self.rechButt.configure(pady="0")
        self.rechButt.configure(relief=RIDGE)
        self.rechButt.configure(text='''Rechercher''')
        self.rechButt.configure(width=176)


        self.retourButt = Button(self.bodyFrame)
        self.retourButt.place(relx=0.17, rely=0.86, height=40, width=180)
        self.retourButt.configure(font=self.font12)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')
        self.retourButt.configure(width=100)
        self.retourButt.configure(pady="0")
        self.retourButt.config(command=self.retour)

        self.controller.show_frame(Produits)

    def submit(self):

        con = connectBdd()
        self.exist = con.rechercheEquivalent(categorie=self.categoEntryVar.get()
                                             , bienEtre=self.bienCheckVar.get()
                                             , dci=self.dciEntryVar.get())
        exist = self.exist
        if exist and exist[0][5] != 0:
            self.affichage()
        else:
            showinfo("Equivalents Non Existants ", " Le Produit que vous Avez entrer"

                                                   " n'a pas d'équivalents ! ")
        self.dciEntryVar.set("")
        self.categoEntryVar.set("")

    def destruction(self):
        self.dciEntryVar.set("")
        self.categoEntryVar.set("")
        try:
            self.rechButt.destroy()
            self.retourButt.destroy()


        except:
            pass

    def affichage(self):
        self.destruction()
        self.scrollable_canvas = ScrollableCanvasEquivalent(self)
        self.scrollable_canvas.grid(row=1, column=1)
        self.scrollable_canvas.place(relx=0.025, rely=0.3)

        self.donnees[:] = []
        self.var = ("Nom Du Produit", "Dosage(Mg)/(Mg/l)", "Forme", "Laboratoire", "Prix (DA) ")
        self.donnees.append(self.var)
        for variable in self.exist:
            self.donnees.append(variable)
        cat = self.donnees[1][2]


        r = 0
        for b in self.donnees:

            if r == 0:
                Label(self.scrollable_canvas.interior, text=b[0].upper().capitalize(), relief=FLAT, width=22, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=1)
            else:
                Label(self.scrollable_canvas.interior, text=b[3].upper().capitalize(), relief=RIDGE, width=22, height=2, bg='white',
                      font=self.font12).grid(row=r,
                                             column=1)
            r = r + 1
        r = 0
        for c in self.donnees:
            if r == 0:
                Label(self.scrollable_canvas.interior, text=c[1], relief=FLAT, width=15, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=2)
            else:
                Label(self.scrollable_canvas.interior, text=c[6], relief=RIDGE, width=15, height=2, bg='white',
                      font=self.font12).grid(row=r,
                                             column=2)
            r = r + 1
        r = 0
        for d in self.donnees:
            if r == 0:
                Label(self.scrollable_canvas.interior, text=d[2].upper().capitalize(), relief=FLAT, width=13, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=3)
            else:
                Label(self.scrollable_canvas.interior, text=d[7].upper().capitalize(), relief=RIDGE, width=13, height=2, bg='white',
                      font=self.font12).grid(row=r,
                                             column=3)
            r = r + 1

        r = 0
        for g in self.donnees:
            if r == 0:
                Label(self.scrollable_canvas.interior, text=g[3].upper().capitalize(), relief=FLAT, width=22, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=5)
            else:
                Label(self.scrollable_canvas.interior, text=g[4].upper().capitalize(), relief=RIDGE, width=22, height=2, bg='white',
                      font=self.font12).grid(row=r,
                                             column=5)
            r = r + 1
        r = 0
        for h in self.donnees:
            if r == 0:
                Label(self.scrollable_canvas.interior, text=h[4], relief=FLAT, width=12, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=6)
            else:
                Label(self.scrollable_canvas.interior, text=h[5], relief=RIDGE, width=12, height=2, bg='white',
                      font=self.font12).grid(row=r,
                                             column=6)
            r = r + 1

        self.retourButt = Button(self.bodyFrame)
        self.retourButt['command'] = self.retour
        self.retourButt.place(relx=0.43, rely=0.86, height=40, width=180)
        self.retourButt.configure(font=self.font12)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')
        self.retourButt.configure(width=100)
        self.retourButt.configure(pady="0")
        self.retourButt.config(command=self.retour)


        self.title = Label(self.bodyFrame)
        self.title.place(relx=0.28, rely=0.035, height=40, width=382)
        self.title.configure(background="#009D78")
        self.title.configure(disabledforeground="#a3a3a3")
        self.title.configure(font=self.font12)
        self.title.configure(foreground="#fafafa")
        self.title.configure(text='''Catégorie: ''' + cat.upper().capitalize())
        self.title.configure(width=382)

    def updateDci(self, *args):

        if self.bienCheckVar.get():
            self.dciVar = self.dciEntryVar.get()
            self.dciEntry.config(state="readonly")
            self.dciEntryVar.set("")
        else:
            self.dciEntry.config(state="normal")
            self.dciEntryVar.set(self.dciVar)

    def __init__(self, parent, controller=None):
        Frame.__init__(self, parent)

        self.controller = controller
        self.exist = []

        font11 = "-family {Futura Bk BT} -size 19 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        font13 = "-family {Futura Bk BT} -size 11  -slant " \
                 "roman -underline 0 -overstrike 0"

        self.donnees = []
        self.font12 = font12
        self.font13 = font13
        self.font11 = font11

        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0



        self.headFrame = Frame(self)
        self.headFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.headFrame.configure(borderwidth="2")
        self.headFrame.configure(background="#009D78")
        self.headFrame.configure(width=125)

        self.titleLabel = Label(self.headFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(font=font11)
        self.titleLabel.configure(foreground="#fafafa")
        self._img5 = PhotoImage(file="images/recheq.png")
        self.titleLabel.configure(image=self._img5)

        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img1 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img1)

        self.bodyFrame = Frame(self)
        self.bodyFrame.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1)
        self.bodyFrame.configure(borderwidth="2")
        self.bodyFrame.configure(background="#ffffff")
        self.bodyFrame.configure(width=125)
        self.bodyFrame.config(relief=FLAT)

        self.Labelbody = Label(self.bodyFrame)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(width=935)

        self.categoLabel = Label(self.bodyFrame)
        self.categoLabel.place(relx=0.22, rely=0.25, height=34, width=190)
        self.categoLabel.configure(background="#ffffff")
        self.categoLabel.configure(disabledforeground="#a3a3a3")
        self.categoLabel.configure(font=font12)
        self.categoLabel.configure(foreground="#000000")
        self.categoLabel.configure(text='''Catégorie :''')
        self.categoLabel.configure(anchor=W)


        self.categoEntryVar = StringVar()
        self.categoEntry = Entry(self.bodyFrame, textvariable=self.categoEntryVar)
        self.categoEntry.place(relx=0.45, rely=0.25, relheight=0.06
                               , relwidth=0.38)
        self.categoEntry.configure(background="#ffffff")
        self.categoEntry.configure(disabledforeground="#a3a3a3")
        self.categoEntry.configure(font=font12)
        self.categoEntry.configure(foreground="#000000")
        self.categoEntry.configure(insertbackground="black")
        self.categoEntry.configure(width=384)

        self.dciLabel = Label(self.bodyFrame)
        self.dciLabel.place(relx=0.22, rely=0.46, height=34, width=190)
        self.dciLabel.configure(activebackground="#f9f9f9")
        self.dciLabel.configure(activeforeground="black")
        self.dciLabel.configure(background="#ffffff")
        self.dciLabel.configure(disabledforeground="#a3a3a3")
        self.dciLabel.configure(font=font12)
        self.dciLabel.configure(foreground="#000000")
        self.dciLabel.configure(highlightbackground="#ffffff")
        self.dciLabel.configure(highlightcolor="black")
        self.dciLabel.configure(text='''DCI :''')
        self.dciLabel.configure(anchor=W)

        self.dciEntryVar = StringVar()
        self.dciEntry = Entry(self.bodyFrame)
        self.dciEntry.place(relx=0.45, rely=0.46, relheight=0.06, relwidth=0.38)
        self.dciEntry.configure(background="#ffffff")
        self.dciEntry.configure(disabledforeground="#a3a3a3")
        self.dciEntry.configure(font=font12)
        self.dciEntry.configure(foreground="#000000")
        self.dciEntry.configure(highlightbackground="#ffffff")
        self.dciEntry.configure(highlightcolor="black")
        self.dciEntry.configure(insertbackground="black")
        self.dciEntry.configure(selectbackground="#c4c4c4")
        self.dciEntry.configure(selectforeground="black", textvariable=self.dciEntryVar)

        self.bienCheckVar = IntVar()
        self.bienCheckVar.trace("w", self.updateDci)

        self.bienCheck = Checkbutton(self.bodyFrame)
        self.bienCheck.place(relx=0.45, rely=0.61, relheight=0.08, relwidth=0.27)

        self.bienCheck.configure(activeforeground="#000000")
        self.bienCheck.configure(anchor=W)
        self.bienCheck.configure(background="#ffffff")
        self.bienCheck.configure(borderwidth="10")
        self.bienCheck.configure(disabledforeground="#a3a3a3")
        self.bienCheck.configure(font=font12)
        self.bienCheck.configure(foreground="#000000")
        self.bienCheck.configure(highlightbackground="#000000")
        self.bienCheck.configure(highlightcolor="black")
        self.bienCheck.configure(justify=LEFT)
        self.bienCheck.configure(text='''Bien_Etre''')
        self.bienCheck.config(variable=self.bienCheckVar)

        self.bienCheck.configure(width=190)



        self.rechButt = Button(self.bodyFrame)
        self.rechButt.config(command=self.submit)
        self.rechButt.place(relx=0.64, rely=0.86, height=40, width=180)
        self.rechButt.configure(activeforeground="#000000")
        self.rechButt.configure(background="#ffffff")
        self.rechButt.configure(disabledforeground="#a3a3a3")
        self.rechButt.configure(font=font12)
        self.rechButt.configure(foreground="#000000")
        self.rechButt.configure(highlightbackground="#ffffff")
        self.rechButt.configure(highlightcolor="black")
        self.rechButt.configure(pady="0")
        self.rechButt.configure(relief=RIDGE)
        self.rechButt.configure(text='''Rechercher''')



        self.retourButt = Button(self.bodyFrame)
        self.retourButt.place(relx=0.17, rely=0.86, height=40, width=180)
        self.retourButt.configure(font=font12)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')
        self.retourButt.configure(pady="0")
        self.retourButt.config(command=self.retour)




#####################################################################################################################
class Acceuil(Frame):

    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var=self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res :
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()


    def Nos_Produits(self):
        self.master.master.show_frame(Produits)
        self.verif_notif()



    def GestionStock(self):
        self.master.master.show_frame(gestionStock)
        self.verif_notif()

    def Statistiques(self):
        self.master.master.show_frame(Stats)
        self.verif_notif()
    def geoloc(self,nPh):
        try:

            con = connectBdd()
            cur = con.cur

            cur.execute(''' SELECT latitude,longitude,code FROM contacts ;''')
            points = cur.fetchall()
            longs, lats, pharms = [], [], []

            for i in range(len(points)):
                lats.append(points[i][0])
                longs.append(points[i][1])
                pharms.append(points[i][2])

            # Initialize the map to the first location in the list
            gmap = gmplot.GoogleMapPlotter(lats[0], longs[0], zoom=11)

            # gmap.scatter(lats, longs, 'red', size=400,marker=False)

            for i in range(len(points)):
                if (pharms[i] != nPh):
                    gmap.marker(lats[i], longs[i], '#pharm', title=pharms[i])
                else:
                    gmap.marker(lats[i], longs[i], '#rouge2', title=pharms[i])

            map = 'map.html'
            gmap.draw(map)

            webbrowser.open(map)

            con.fermer()
        except :
            showerror("Erreur","Erreur de connexion internet !")
    def retour2(self):
        try:
            self.scrollable_canvas.destroy()
            self.retourButt2.destroy()
            self.Buttgestcmp.destroy()
            self.titlLabel.destroy()
            self.map.destroy()

        except:
            pass

        self.Buttongestcmp = Button(self.titreLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titreLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

    def afficheContacts(self):
        self.titlLabel = Label(self.headFrame)

        self.titlLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titlLabel.configure(background="#009D78")
        self.titlLabel.configure(disabledforeground="#a3a3a3")
        self.titlLabel.configure(foreground="#fafafa")
        self.titlLabel.configure(text='''''')
        self.titlLabel.configure(width=592)

        self._img50 = PhotoImage(file="images/contact.png")
        self.titlLabel.configure(image=self._img50)

        self.Buttgestcmp = Button(self.titlLabel)
        self.Buttgestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttgestcmp.configure(activebackground="#d9d9d9")
        self.Buttgestcmp.configure(activeforeground="#000000")
        self.Buttgestcmp.configure(background="#009D78")
        self.Buttgestcmp.configure(borderwidth="0")
        self.Buttgestcmp.configure(disabledforeground="#a3a3a3")
        self.Buttgestcmp.configure(foreground="#808080")
        self.Buttgestcmp.configure(highlightbackground="#d9d9d9")
        self.Buttgestcmp.configure(highlightcolor="black")
        self.Buttgestcmp.configure(pady="0")
        self.Buttgestcmp.configure(text='''''')
        self.Buttgestcmp.configure(width=147)
        self.Buttgestcmp.bind("<Button-1>", self.GestionDeCompte)
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttgestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titlLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)



        # nouveau bouton retour
        self.retourButt2 = Button(self.bodyFrame)

        self.retourButt2.place(relx=0.17, rely=0.8, height=39, width=250)
        self.retourButt2.configure(activeforeground="#000000")
        self.retourButt2.configure(background="#ffffff")
        self.retourButt2.configure(disabledforeground="#a3a3a3")
        self.retourButt2.configure(font=self.font12)
        self.retourButt2.configure(foreground="#000000")
        self.retourButt2.configure(highlightbackground="#d9d9d9")
        self.retourButt2.configure(highlightcolor="black")
        self.retourButt2.configure(pady="0")
        self.retourButt2.configure(relief=RIDGE)
        self.retourButt2.configure(text='''Retour''')
        self.retourButt2.config(command=self.retour2)

        self.map = Button(self.bodyFrame)
        self.map.place(relx=0.5, rely=0.8, height=39, width=250)
        self.map.config(background='#ffffff', relief=RIDGE, font=self.font12, foreground='#000000'
                        , text=" Position Sur La Carte")



        # on recupere le code de la pharmacie courante

        acc = self.controller.getPage(Login)
        Cph = acc.nomPharm[2]
        con = connectBdd()
        self.colonnes [:]=[]
        exist = con.Recupere_contact(Cph)
        # SUpprimer ma pharma
        con.fermer()

        self.map.config(command=lambda :self.geoloc(Cph))

        a = ["Nom De Pharmacie ", "Adresse",
             "Num de Tél ", "Email "]
        self.colonnes.append(a)
        for var in exist:
            self.colonnes.append(var)

        self.scrollable_canvas = ScrollableCanvas(self)
        self.scrollable_canvas.grid(row=1, column=1)
        self.scrollable_canvas.place(relx=0.05, rely=0.26)

        r = 2
        for e in self.colonnes:
            if r == 2:
                Label(self.scrollable_canvas.interior, text=e[0], relief=FLAT, width=20, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=0)

            else:
                Label(self.scrollable_canvas.interior, text=e[0], relief=RIDGE, width=20, height=2, bg='white',
                      font=self.font12).grid(row=r,
                                             column=0)
            r = r + 1

        r = 2
        for b in self.colonnes:

            if r == 2:
                Label(self.scrollable_canvas.interior, text=b[1], relief=FLAT, width=25, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=1)
            else:
                Label(self.scrollable_canvas.interior, text=b[1], relief=RIDGE, width=25, height=2, bg='white',
                      font=self.font12).grid(row=r,
                                             column=1)
            r = r + 1
        r = 2
        for c in self.colonnes:
            if r == 2:
                Label(self.scrollable_canvas.interior, text=c[2], relief=FLAT, width=16, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=2)
            else:
                Label(self.scrollable_canvas.interior, text=c[2], relief=RIDGE, width=16, height=2, bg='white',
                      font=self.font12).grid(row=r,
                                             column=2)
            r = r + 1
        r = 2
        for d in self.colonnes:
            if r == 2:
                Label(self.scrollable_canvas.interior, text=d[3], relief=FLAT, width=20, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=3)
            else:
                Label(self.scrollable_canvas.interior, text=d[3], relief=RIDGE, width=20, height=2, bg='white',
                      font=self.font12).grid(row=r,
                                             column=3)
            r = r + 1

    def msg(self):
        self.master.master.show_frame(Messagerie)
        self.verif_notif()
    def transactions(self):
        self.master.master.show_frame(Transactions)
        self.verif_notif()

    def GestionDeCompte(self):
        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()
    def notifs(self):
        if self.notif==0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])


                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                              height=1, bg='white',anchor="w",
                              font=self.font12).grid(row=r,
                                                     column=1)
                    r = r + 1
                r = 0
                self.notif=1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=818)
                self.supprnotifs.configure(activebackground="#009D78")
                self.supprnotifs.configure(activeforeground="#009D78")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command']=self.supprimenotifs
            else:
                showinfo("Pas de notifications","Vous n'avez pas de notifications !")

        else :
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif=0
    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con=connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0


    def __init__(self, parent, controller=None):
        Frame.__init__(self, parent)

        font10 = "-family {Futura Bk BT} -size 20 -weight normal " \
                 "-slant roman -underline 0 -overstrike 0"
        font9 = "-family {Futura Bk BT} -size 14 -weight bold -slant" \
                " roman -underline 0 -overstrike 0"
        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        self.font9=font9
        self.font12=font12
        self.controller = controller
        self.notif=0
        self.notifications=[]
        self.colonnes = []

        self.Frame1 = Frame(self)
        self.Frame1.place(relx=0.0, rely=0.0, relheight=1.91, relwidth=1.94)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="0")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#ffffff")
        self.Frame1.configure(width=875)

        self.headFrame = Frame(self.Frame1)
        self.headFrame.place(relx=0.0, rely=0.0, relheight=0.12, relwidth=0.52)
        self.headFrame.configure(relief=GROOVE)
        self.headFrame.configure(borderwidth="0")
        self.headFrame.configure(relief=GROOVE)
        self.headFrame.configure(background="#ffffff")
        self.headFrame.configure(width=935)

        self.titreLabel = Label(self.headFrame)
        self.titreLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titreLabel.configure(background="#ffffff")
        self.titreLabel.configure(disabledforeground="#a3a3a3")
        self.titreLabel.configure(foreground="#808080")
        self._img11 = PhotoImage(file="images/vide.png")
        self.titreLabel.configure(image=self._img11)
        self.titreLabel.configure(text='''Label''')
        self.titreLabel.configure(width=935)
        self.titleVar = StringVar()

        self.titreLabel.configure(textvariable=self.titleVar)

        self.Buttongestcmp = Button(self.titreLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")
        self.Buttongestcmp.configure(font=font9)
        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titreLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")
        self.Buttonnotif.configure(font=font9)
        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)



        self.bodyFrame = Frame(self.Frame1)
        self.bodyFrame.place(relx=0.0, rely=0.113, relheight=0.4, relwidth=0.52)
        self.bodyFrame.configure(relief=GROOVE)
        self.bodyFrame.configure(borderwidth="0")
        self.bodyFrame.configure(relief=GROOVE)
        self.bodyFrame.configure(background="#ffffff")
        self.bodyFrame.configure(width=935)

        self.Labelbody = Label(self.bodyFrame)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)

        self.ButtonNP = Button(self.bodyFrame)
        self.ButtonNP.place(relx=0.09, rely=0.3, height=44, width=180)
        self.ButtonNP.configure(activebackground="#ffffff")
        self.ButtonNP.configure(activeforeground="#000000")
        self.ButtonNP.configure(background="#ffffff")
        self.ButtonNP.configure(borderwidth="2")
        self.ButtonNP.configure(disabledforeground="#a3a3a3")
        self.ButtonNP.configure(font=font9)
        self.ButtonNP.configure(foreground="#000000")
        self.ButtonNP.configure(highlightbackground="#ffffff")
        self.ButtonNP.configure(highlightcolor="black")
        self.ButtonNP.configure(pady="0")
        self.ButtonNP.configure(text='''Nos produits''')
        self.ButtonNP.configure(width=147)
        self.ButtonNP.configure(relief=RIDGE)

        self.ButtonNP['command'] = self.Nos_Produits

        self.ButtonGest = Button(self.bodyFrame)
        self.ButtonGest.place(relx=0.39, rely=0.3, height=44, width=210)
        self.ButtonGest.configure(activebackground="#ffffff")
        self.ButtonGest.configure(activeforeground="#000000")
        self.ButtonGest.configure(background="#ffffff")
        self.ButtonGest.configure(borderwidth="2")
        self.ButtonGest.configure(disabledforeground="#a3a3a3")
        self.ButtonGest.configure(font=font9)
        self.ButtonGest.configure(foreground="#000000")
        self.ButtonGest.configure(highlightbackground="#ffffff")
        self.ButtonGest.configure(highlightcolor="black")
        self.ButtonGest.configure(pady="0")
        self.ButtonGest.configure(text='''Gestion de stock''')
        self.ButtonGest.configure(width=210)
        self.ButtonGest.configure(relief=RIDGE)

        self.ButtonGest['command'] = self.GestionStock

        self.Buttonvente = Button(self.bodyFrame)
        self.Buttonvente.place(relx=0.72, rely=0.3, height=44, width=180)
        self.Buttonvente.configure(activebackground="#ffffff")
        self.Buttonvente.configure(activeforeground="#000000")
        self.Buttonvente.configure(background="#ffffff")
        self.Buttonvente.configure(borderwidth="2")
        self.Buttonvente.configure(disabledforeground="#a3a3a3")
        self.Buttonvente.configure(font=font9)
        self.Buttonvente.configure(foreground="#000000")
        self.Buttonvente.configure(highlightbackground="#ffffff")
        self.Buttonvente.configure(highlightcolor="black")
        self.Buttonvente.configure(pady="0")
        self.Buttonvente.configure(text='''Vente''')
        self.Buttonvente.configure(width=177)
        self.Buttonvente.configure(relief=RIDGE)

        self.Buttonvente['command'] = self.transactions

        self.BouttonMsg = Button(self.bodyFrame)
        self.BouttonMsg.place(relx=0.09, rely=0.67, height=44, width=177)
        self.BouttonMsg.configure(activebackground="#ffffff")
        self.BouttonMsg.configure(activeforeground="#000000")
        self.BouttonMsg.configure(background="#ffffff")
        self.BouttonMsg.configure(borderwidth="2")
        self.BouttonMsg.configure(disabledforeground="#a3a3a3")
        self.BouttonMsg.configure(font=font9)
        self.BouttonMsg.configure(foreground="#000000")
        self.BouttonMsg.configure(highlightbackground="#ffffff")
        self.BouttonMsg.configure(highlightcolor="black")
        self.BouttonMsg.configure(pady="0")
        self.BouttonMsg.configure(text='''Messagerie''')
        self.BouttonMsg['command'] = self.msg
        self.BouttonMsg.configure(width=177)
        self.BouttonMsg.configure(relief=RIDGE)

        self.ButtonCont = Button(self.bodyFrame)
        self.ButtonCont.place(relx=0.41, rely=0.67, height=44, width=177)
        self.ButtonCont.configure(activebackground="#ffffff")
        self.ButtonCont.configure(activeforeground="#000000")
        self.ButtonCont.configure(background="#ffffff")
        self.ButtonCont.configure(borderwidth="2")
        self.ButtonCont.configure(disabledforeground="#a3a3a3")
        self.ButtonCont.configure(font=font9)
        self.ButtonCont.configure(foreground="#000000")
        self.ButtonCont.configure(highlightbackground="#ffffff")
        self.ButtonCont.configure(highlightcolor="black")
        self.ButtonCont.configure(pady="0")
        self.ButtonCont.configure(text='''Réseau''')
        self.ButtonCont.configure(width=177)
        self.ButtonCont.configure(relief=RIDGE)

        self.ButtonCont['command'] = self.afficheContacts

        self.ButtonStat = Button(self.bodyFrame)
        self.ButtonStat.place(relx=0.72, rely=0.67, height=44, width=180)
        self.ButtonStat.configure(activebackground="#ffffff")
        self.ButtonStat.configure(activeforeground="#000000")
        self.ButtonStat.configure(background="#ffffff")
        self.ButtonStat.configure(borderwidth="2")
        self.ButtonStat.configure(disabledforeground="#a3a3a3")
        self.ButtonStat.configure(font=font9)
        self.ButtonStat.configure(foreground="#000000")
        self.ButtonStat.configure(highlightbackground="#ffffff")
        self.ButtonStat.configure(highlightcolor="black")
        self.ButtonStat.configure(pady="0")
        self.ButtonStat.configure(text='''Statistiques''')
        self.ButtonStat.configure(width=177)
        self.ButtonStat.configure(relief=RIDGE)

        self.ButtonStat['command'] = self.Statistiques

        self.LabelNP = Label(self.bodyFrame)
        self.LabelNP.place(relx=0.15, rely=0.14, height=61, width=74)
        self.LabelNP.configure(background="#ffffff")
        self.LabelNP.configure(disabledforeground="#a3a3a3")
        self.LabelNP.configure(foreground="#000000")
        self.LabelNP.configure(width=74)
        self._img5 = PhotoImage(file="images/medoc2.png")
        self.LabelNP.configure(image=self._img5)

        self.LabelMsg = Label(self.bodyFrame)
        self.LabelMsg.place(relx=0.145, rely=0.52, height=61, width=74)
        self.LabelMsg.configure(background="#ffffff")
        self.LabelMsg.configure(disabledforeground="#a3a3a3")
        self.LabelMsg.configure(foreground="#000000")
        self._img6 = PhotoImage(file="images/message.png")
        self.LabelMsg.configure(image=self._img6)

        self.LabelGS = Label(self.bodyFrame)
        self.LabelGS.place(relx=0.46, rely=0.14, height=61, width=74)
        self.LabelGS.configure(background="#ffffff")
        self.LabelGS.configure(disabledforeground="#a3a3a3")
        self.LabelGS.configure(foreground="#000000")
        self._img3 = PhotoImage(file="images/stock.png")
        self.LabelGS.configure(image=self._img3)

        self.LabelContact = Label(self.bodyFrame)
        self.LabelContact.place(relx=0.46, rely=0.52, height=61, width=74)
        self.LabelContact.configure(background="#ffffff")
        self.LabelContact.configure(disabledforeground="#a3a3a3")
        self.LabelContact.configure(foreground="#000000")
        self._img7 = PhotoImage(file="images/phone.png")
        self.LabelContact.configure(image=self._img7)

        self.LabelVente = Label(self.bodyFrame)
        self.LabelVente.place(relx=0.775, rely=0.15, height=61, width=74)
        self.LabelVente.configure(background="#ffffff")
        self.LabelVente.configure(disabledforeground="#a3a3a3")
        self.LabelVente.configure(foreground="#000000")
        self._img4 = PhotoImage(file="images/buy.png")
        self.LabelVente.configure(image=self._img4)

        self.LabelStat = Label(self.bodyFrame)
        self.LabelStat.place(relx=0.775, rely=0.52, height=61, width=74)
        self.LabelStat.configure(background="#ffffff")
        self.LabelStat.configure(disabledforeground="#a3a3a3")
        self.LabelStat.configure(foreground="#000000")
        self._img8 = PhotoImage(file="images/stat.png")
        self.LabelStat.configure(image=self._img8)

        self.footFrame = Frame(self.Frame1)
        self.footFrame.place(relx=0, rely=0.48, relheight=0.1, relwidth=0.54)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img1 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img1)


##########################################################################################
############################ Classe Bienvenue ##########################################
class Bienvenue(Frame):
    def inscrip(self):
        self.master.master.show_frame(Inscription_choix)

    def connex(self):
        self.master.master.show_frame(Login)

    def __init__(self, parent, controller=None):
        Frame.__init__(self, parent)

        self.controller = controller

        font11 = "-family {Futura Bk BT} -size 16 -weight bold " \
                 "-slant roman -underline 0 -overstrike 0"
        font9 = "-family {Futura Bk BT} -size 24 -weight bold -slant" \
                " roman -underline 0 -overstrike 0"

        self.frame1 = Frame(self)
        self.frame1.place(relx=0.0, rely=0.0, relheight=1.04, relwidth=1.0)
        self.frame1.configure(relief=GROOVE)
        self.frame1.configure(borderwidth="2")
        self.frame1.configure(relief=GROOVE)
        self.frame1.configure(background="#ffffff")
        self.frame1.configure(highlightbackground="#ffffff")
        self.frame1.configure(highlightcolor="black")
        self.frame1.configure(width=945)

        self.headFrame = Frame(self.frame1)
        self.headFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.headFrame.configure(borderwidth="2")
        self.headFrame.configure(background="#009D78")
        self.headFrame.configure(highlightbackground="#ffffff")
        self.headFrame.configure(highlightcolor="black")
        self.headFrame.configure(width=945)

        self.titleLabel = Label(self.headFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(activebackground="#f9f9f9")
        self.titleLabel.configure(activeforeground="black")
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(font=font9)
        self.titleLabel.configure(foreground="#ffffff")
        self.titleLabel.configure(highlightbackground="#ffffff")
        self.titleLabel.configure(highlightcolor="black")
        self._img1 = PhotoImage(file="images/bienv.png")

        self.titleLabel.configure(image=self._img1)

        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img900 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img900)

        self.bodyFrame = Frame(self.frame1)
        self.bodyFrame.place(relx=0.0, rely=0.20, relheight=0.72, relwidth=1)
        self.bodyFrame.configure(borderwidth="2")
        self.bodyFrame.configure(background="#ffffff")
        self.bodyFrame.configure(highlightbackground="#ffffff")
        self.bodyFrame.configure(highlightcolor="black")
        self.bodyFrame.configure(width=745)

        self.Labelbody = Label(self.bodyFrame)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)


        self.inscripButt = Button(self.bodyFrame)
        self.inscripButt.place(relx=0.31, rely=0.22, height=70, width=357)
        self.inscripButt.configure(activebackground="#ffffff")
        self.inscripButt.configure(activeforeground="#000000")
        self.inscripButt.configure(background="#ffffff")
        self.inscripButt.configure(disabledforeground="#a3a3a3")
        self.inscripButt.configure(font=font11)
        self.inscripButt.configure(foreground="#000000")
        self.inscripButt.configure(highlightbackground="#ffffff")
        self.inscripButt.configure(highlightcolor="black")
        self.inscripButt.configure(pady="0")
        self.inscripButt.configure(relief=RIDGE)
        self.inscripButt.configure(text='''S'inscrire''')

        self.inscripButt['command'] = self.inscrip




        self.connexButt = Button(self.bodyFrame)
        self.connexButt.place(relx=0.31, rely=0.51, height=70, width=357)
        self.connexButt.configure(activebackground="#ffffff")
        self.connexButt.configure(activeforeground="#000000")
        self.connexButt.configure(background="#ffffff")
        self.connexButt.configure(disabledforeground="#a3a3a3")
        self.connexButt.configure(font=font11)
        self.connexButt.configure(foreground="#000000")
        self.connexButt.configure(highlightbackground="#ffffff")
        self.connexButt.configure(highlightcolor="black")
        self.connexButt.configure(pady="0")
        self.connexButt.configure(relief=RIDGE)
        self.connexButt.configure(text='''Se connecter''')

        self.connexButt['command'] = self.connex



##############################################################################################
############################# PArtie de Stock ################################################
##############################################################################################
class gestionStock(Frame):
    def qt (self):
        self.master.master.show_frame(QuantiteLot)



    #' pour les notifications'
    def GestionDeCompte(self):
        try :
            self.retour2()
        except:
            pass
        try :
            self.retour2()
        except :
            pass
        try :
            self.retour_perime()
        except :
            pass
        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()

    def notifs(self):
        if self.notif == 0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])

                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                          height=1, bg='white', anchor="w",
                          font=self.font12).grid(row=r,
                                                 column=1)
                    r = r + 1
                r = 0
                self.notif = 1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=818)
                self.supprnotifs.configure(activebackground="#009D78")
                self.supprnotifs.configure(activeforeground="#009D78")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command'] = self.supprimenotifs
            else:
                showinfo("Pas de notifications", "Vous n'avez pas de notifications !")

        else:
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif = 0

    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con = connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0

    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var = self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res:
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()

    def retrait(self):
        # on verifie le type de l'utilisateur
        var = self.controller.getPage(Login)
        if var.nomPharm[3] == 1:
            self.master.master.show_frame(Retrait)

        else:
            showinfo("Opération impossible",
                     "Vous ne pouvez pas retirer de lot ! \nVeuillez vous connecter avec un compte admin pour pouvoir continuer ")





    def affichage(self):
        self.retourButt.destroy()
        self.titleLabel = Label(self.headFrame)

        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(font=self.font10)
        self.titleLabel.configure(foreground="#fafafa")
        self.titleLabel.configure(text='''''')
        self.titleLabel.configure(width=592)

        self._img50 = PhotoImage(file="images/rupt.png")
        self.titleLabel.configure(image=self._img50)

        self.retourButt1 = Button(self.Frame1)

        self.retourButt1.place(relx=0.17, rely=0.86, height=40, width=220)
        self.retourButt1.configure(activebackground="#d9d9d9")
        self.retourButt1.configure(activeforeground="#000000")
        self.retourButt1.configure(background="#ffffff")
        self.retourButt1.configure(disabledforeground="#a3a3a3")
        self.retourButt1.configure(font=self.font12)
        self.retourButt1.configure(foreground="#000000")
        self.retourButt1.configure(highlightbackground="#ffffff")
        self.retourButt1.configure(highlightcolor="black")
        self.retourButt1.configure(pady="0")
        self.retourButt1.configure(relief=RIDGE)
        self.retourButt1.configure(text='''Retour''')
        self.retourButt1.config(command=self.retour2)
        self.ajoutButt1 = Button(self.Frame1)

        self.ajoutButt1.place(relx=0.64, rely=0.86, height=40, width=220)
        self.ajoutButt1.configure(activebackground="#d9d9d9")
        self.ajoutButt1.configure(activeforeground="#000000")
        self.ajoutButt1.configure(background="#ffffff")
        self.ajoutButt1.configure(disabledforeground="#a3a3a3")
        self.ajoutButt1.configure(font=self.font12)
        self.ajoutButt1.configure(foreground="#000000")
        self.ajoutButt1.configure(highlightbackground="#ffffff")
        self.ajoutButt1.configure(highlightcolor="black")
        self.ajoutButt1.configure(pady="0")
        self.ajoutButt1.configure(relief=RIDGE)
        self.ajoutButt1.configure(text='''Ajouter un produit au stock''')
        self.ajoutButt1['command'] = self.ajout

        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0

        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        con = connectBdd()
        # on recupere le code de la pharmacie courante
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]

        ri = con.rupStock(cPh)

        self.donnees[:] = []
        self.scrollable_canvas = ScrollableCanvas3(self)
        self.scrollable_canvas.grid(row=1, column=1)
        self.scrollable_canvas.place(relx=0.03, rely=0.25)

        self.var = ('Nom Produit', 'Forme', 'Dosage', 'Prix')
        self.donnees.append(self.var)
        for variable in ri:
            self.donnees.append(variable)

        r = 0
        for e in self.donnees:
            if r == 0:
                Label(self.scrollable_canvas.interior, text=e[0].upper().capitalize(), relief=FLAT, width=35, height=2,
                      bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=0)

            else:
                Label(self.scrollable_canvas.interior, text=e[3].upper().capitalize(), relief=RIDGE, width=35, height=1,
                      bg='white',
                      font=self.font12).grid(row=r,
                                             column=0)
            r = r + 1

        r = 0
        for b in self.donnees:

            if r == 0:
                Label(self.scrollable_canvas.interior, text=b[1].upper().capitalize(), relief=FLAT, width=16, height=2,
                      bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=1)
            else:
                Label(self.scrollable_canvas.interior, text=b[7].upper().capitalize(), relief=RIDGE, width=16, height=1,
                      bg='white',
                      font=self.font12).grid(row=r,
                                             column=1)
            r = r + 1
        r = 0
        for c in self.donnees:
            if r == 0:
                Label(self.scrollable_canvas.interior, text=c[2], relief=FLAT, width=16, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=2)
            else:
                Label(self.scrollable_canvas.interior, text=c[6], relief=RIDGE, width=16, height=1, bg='white',
                      font=self.font12).grid(row=r,
                                             column=2)
            r = r + 1
        r = 0
        for h in self.donnees:
            if r == 0:
                Label(self.scrollable_canvas.interior, text=h[3], relief=FLAT, width=16, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=3)

            else:
                Label(self.scrollable_canvas.interior, text=h[5], relief=RIDGE, width=16, height=1, bg='white',
                      font=self.font12).grid(row=r,
                                             column=3)
            r = r + 1

    def retour(self):
        self.master.master.show_frame(Acceuil)

    def retour2(self):
        try:
            self.scrollable_canvas.destroy()
            self.ajoutButt1.destroy()
            self.retourButt1.destroy()


        except:
            pass
        try :
            self.supprButt2.destroy()
        except :
            pass

        self.titleLabel = Label(self.headFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(foreground="#fafafa")
        self.titleLabel.configure(width=382)
        self._img7 = PhotoImage(file="images/gs.png")
        self.titleLabel.configure(image=self._img7)

        self.notif = 0

        self.notifications = []



        self.retourButt = Button(self.bodyFrame)
        self.retourButt.place(relx=0.4, rely=0.86, height=40, width=180)
        self.retourButt.configure(activebackground="#d9d9d9")
        self.retourButt.configure(font=self.font9)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')

        self.retourButt['command'] = self.retour
        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

    def retour_perime(self):
        try:
            self.scrollable_canvas.destroy()
            self.retourButt2.destroy()
        except :
            pass

        self.titleLabel = Label(self.headFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(foreground="#fafafa")
        self.titleLabel.configure(width=382)
        self._img7 = PhotoImage(file="images/gs.png")
        self.titleLabel.configure(image=self._img7)
        self.supprButt2.destroy()
        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0

        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        self.retourButt = Button(self.bodyFrame)
        self.retourButt.place(relx=0.4, rely=0.86, height=40, width=180)
        self.retourButt.configure(activebackground="#d9d9d9")
        self.retourButt.configure(font=self.font9)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')

        self.retourButt['command'] = self.retour
    def suppr_perime(self):
        # on verifie le type de l'utilisateur
        var = self.controller.getPage(Login)
        if var.nomPharm[3] == 1:
            acc = self.controller.getPage(Login)
            cPh = acc.nomPharm[2]
            con = connectBdd()
            con.suppr_perim(cPh)
            con.fermer()
            self.retour_perime()
        else:
            showinfo("Opération impossible",
                     "Vous ne pouvez pas créer defféctuer cette action !\nVeuillez vous connecter avec un compte admin pour pouvoir continuer")


    def perimer(self):


        self.colonnes[:]=[]
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]

        con=connectBdd()
        con.mise_jour(cPh)


        exist = con.perimes(cPh)
        if exist:

            self.titleLabel = Label(self.headFrame)
            self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
            self.titleLabel.configure(background="#009D78")
            self.titleLabel.configure(disabledforeground="#a3a3a3")
            self.titleLabel.configure(foreground="#fafafa")
            self.titleLabel.configure(width=382)
            self._img7128 = PhotoImage(file="images/perim.png")
            self.titleLabel.configure(image=self._img7128)
            try:
                self.retourButt1.destroy()
            except :
                pass
            try:
                self.retourButt.destroy()
            except :
                pass
            # nouveau bouton retour
            self.retourButt2 = Button(self.bodyFrame)

            self.retourButt2.place(relx=0.17, rely=0.86, height=40, width=180)
            self.retourButt2.configure(activebackground="#d9d9d9")
            self.retourButt2.configure(activeforeground="#000000")
            self.retourButt2.configure(background="#ffffff")
            self.retourButt2.configure(disabledforeground="#a3a3a3")
            self.retourButt2.configure(font=self.font12)
            self.retourButt2.configure(foreground="#000000")
            self.retourButt2.configure(highlightbackground="#ffffff")
            self.retourButt2.configure(highlightcolor="black")
            self.retourButt2.configure(pady="0")
            self.retourButt2.configure(relief=RIDGE)
            self.retourButt2.configure(text='''Retour''')
            self.retourButt2.config(command=self.retour_perime)

            self.supprButt2 = Button(self.bodyFrame)

            self.supprButt2.place(relx=0.64, rely=0.86, height=40, width=180)
            self.supprButt2.configure(activebackground="#d9d9d9")
            self.supprButt2.configure(activeforeground="#000000")
            self.supprButt2.configure(background="#ffffff")
            self.supprButt2.configure(disabledforeground="#a3a3a3")
            self.supprButt2.configure(font=self.font12)
            self.supprButt2.configure(foreground="#000000")
            self.supprButt2.configure(highlightbackground="#ffffff")
            self.supprButt2.configure(highlightcolor="black")
            self.supprButt2.configure(pady="0")
            self.supprButt2.configure(relief=RIDGE)
            self.supprButt2.configure(text='''Retirer''')
            self.supprButt2.config(command=self.suppr_perime)

            font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                     "roman -underline 0 -overstrike 0"

            self.font12 = font12
            self.notif = 0

            self.notifications = []
            self.Buttongestcmp = Button(self.titleLabel)
            self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
            self.Buttongestcmp.configure(activebackground="#ffffff")
            self.Buttongestcmp.configure(activeforeground="#000000")
            self.Buttongestcmp.configure(background="#009D78")
            self.Buttongestcmp.configure(borderwidth="0")
            self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

            self.Buttongestcmp.configure(foreground="#808080")
            self.Buttongestcmp.configure(highlightbackground="#ffffff")
            self.Buttongestcmp.configure(highlightcolor="black")
            self.Buttongestcmp.configure(pady="0")
            self.Buttongestcmp.configure(text='''''')
            self.Buttongestcmp.configure(width=147)
            self.Buttongestcmp['command'] = self.GestionDeCompte
            self._img55 = PhotoImage(file="images/account.png")
            self.Buttongestcmp.configure(image=self._img55)

            self.Buttonnotif = Button(self.titleLabel)
            self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
            self.Buttonnotif.configure(activebackground="#ffffff")
            self.Buttonnotif.configure(activeforeground="#000000")
            self.Buttonnotif.configure(background="#009D78")
            self.Buttonnotif.configure(borderwidth="0")
            self.Buttonnotif.configure(disabledforeground="#a3a3a3")

            self.Buttonnotif.configure(foreground="#808080")
            self.Buttonnotif.configure(highlightbackground="#ffffff")
            self.Buttonnotif.configure(highlightcolor="black")
            self.Buttonnotif.configure(pady="0")
            self.Buttonnotif.configure(text='''''')
            self.Buttonnotif.configure(width=147)
            self.Buttonnotif['command'] = self.notifs
            self._img80 = PhotoImage(file="images/notifs.png")
            self.Buttonnotif.configure(image=self._img80)

            # on recupere le code de la pharmacie courante

            self.retourButt.destroy()

            con.fermer()

            a = ("Nom du produit ", "Dosage(mg/l-mg)", "Forme",
                 "Quantité ", "Date d'expiration","Lot")
            self.colonnes.append(a)
            for var in exist:
                self.colonnes.append(var)

            self.scrollable_canvas = ScrollableCanvas(self)
            self.scrollable_canvas.grid(row=1, column=1)
            self.scrollable_canvas.place(relx=0.02, rely=0.25)

            r = 0
            for e in self.colonnes:
                if r == 0:
                    Label(self.scrollable_canvas.interior, text=e[0], relief=FLAT, width=20, height=2, bg='#009D78',
                          foreground="#ffffff", font=self.font12).grid(row=r,
                                                                       column=0)

                else:
                    Label(self.scrollable_canvas.interior, text=e[0], relief=RIDGE, width=20, height=1, bg='white',
                          font=self.font12).grid(row=r,
                                                 column=0)
                r = r + 1

            r = 0
            for b in self.colonnes:

                if r == 0:
                    Label(self.scrollable_canvas.interior, text=b[1], relief=FLAT, width=13, height=2, bg='#009D78',
                          foreground="#ffffff", font=self.font12).grid(row=r,
                                                                       column=1)
                else:
                    Label(self.scrollable_canvas.interior, text=b[1], relief=RIDGE, width=13, height=1, bg='white',
                          font=self.font12).grid(row=r,
                                                 column=1)
                r = r + 1
            r = 0
            for c in self.colonnes:
                if r == 0:
                    Label(self.scrollable_canvas.interior, text=c[2], relief=FLAT, width=17, height=2, bg='#009D78',
                          foreground="#ffffff", font=self.font12).grid(row=r,
                                                                       column=2)
                else:
                    Label(self.scrollable_canvas.interior, text=c[2], relief=RIDGE, width=17, height=1, bg='white',
                          font=self.font12).grid(row=r,
                                                 column=2)
                r = r + 1
            r = 0
            for d in self.colonnes:
                if r == 0:
                    Label(self.scrollable_canvas.interior, text=d[3], relief=FLAT, width=12, height=2, bg='#009D78',
                          foreground="#ffffff", font=self.font12).grid(row=r,
                                                                       column=3)
                else:
                    Label(self.scrollable_canvas.interior, text=d[3], relief=RIDGE, width=12, height=1, bg='white',
                          font=self.font12).grid(row=r,
                                                 column=3)
                r = r + 1
            r = 0
            for f in self.colonnes:
                if r == 0:
                    Label(self.scrollable_canvas.interior, text=f[4], relief=FLAT, width=14, height=2, bg='#009D78',
                          foreground="#ffffff", font=self.font12).grid(row=r,
                                                                       column=4)
                else:
                    Label(self.scrollable_canvas.interior, text=f[4], relief=RIDGE, width=14, height=1, bg='white',
                          font=self.font12).grid(row=r,
                                                 column=4)
                r = r + 1
            r=0
            for f in self.colonnes:
                if r == 0:
                    Label(self.scrollable_canvas.interior, text=f[5], relief=FLAT, width=11, height=2, bg='#009D78',
                          foreground="#ffffff", font=self.font12).grid(row=r,
                                                                       column=5)
                else:
                    Label(self.scrollable_canvas.interior, text=f[5], relief=RIDGE, width=11, height=1, bg='white',
                          font=self.font12).grid(row=r,
                                                 column=5)
                r = r + 1
        else :
            showinfo("Inexistant","Il n'y a pas de produits perimés !")

    def quantite(self):
        self.master.master.show_frame(Quantite)
    def ajout(self):
        try:
            self.scrollable_canvas.destroy()
        except :
            pass
        self.master.master.show_frame(Ajout)

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller

        font10 = "-family {Futura Bk BT} -size 15 -weight bold " \
                 "-slant roman -underline 0 -overstrike 0"
        font11 = "-family {Futura Bk BT} -size 20 -weight bold " \
                 "-slant roman -underline 0 -overstrike 0"
        font9 = "-family {Futura Bk BT} -size 12 -weight bold -slant" \
                " roman -underline 0 -overstrike 0"

        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        font13 = "-family {Futura Bk BT} -size 11  -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.font13 = font13
        self.font11 = font11
        self.font10 = font10
        self.font9=font9

        #####################
        self.donnees = []
        self.donnees1 = []
        self.r = []
        self.colonnes=[]
        #################



        self.Frame1 = Frame(self)
        self.Frame1.place(relx=0.0, rely=0.0, relheight=1, relwidth=1)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="0")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#FFFFFF")
        self.Frame1.configure(highlightbackground="#ffffff")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=935)

        self.headFrame = Frame(self.Frame1)
        self.headFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.headFrame.configure(borderwidth="0")
        self.headFrame.configure(background="#009D78")
        self.headFrame.configure(highlightbackground="#ffffff")
        self.headFrame.configure(highlightcolor="black")
        self.headFrame.configure(width=935)

        self.titleLabel = Label(self.headFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(activebackground="#f9f9f9")
        self.titleLabel.configure(activeforeground="black")
        self.titleLabel.configure(background="#ffffff")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(font=font11)
        self.titleLabel.configure(foreground="#ffffff")
        self.titleLabel.configure(highlightbackground="#ffffff")
        self.titleLabel.configure(highlightcolor="black")
        self.titleLabel.configure(text='''Gestion de produits''')
        self._img88 = PhotoImage(file="images/gs.png")
        self.titleLabel.configure(image=self._img88)

        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0


        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        self.bodyFrame = Frame(self.Frame1)
        self.bodyFrame.place(relx=0.00, rely=0.21, relheight=0.72, relwidth=1)

        self.bodyFrame.configure(relief=FLAT)
        self.bodyFrame.configure(borderwidth="0")
        self.bodyFrame.configure(relief=FLAT)
        self.bodyFrame.configure(background="#FFFFFF")
        self.bodyFrame.configure(highlightbackground="#ffffff")
        self.bodyFrame.configure(highlightcolor="black")
        self.bodyFrame.configure(width=745)

        self.Labelbody = Label(self.bodyFrame)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)

        self.ajoutButt = Button(self.bodyFrame)
        self.ajoutButt.place(relx=0.07, rely=0.1, height=70, width=350)
        self.ajoutButt.configure(activebackground="#ffffff")
        self.ajoutButt.configure(activeforeground="#000000")
        self.ajoutButt.configure(background="#ffffff")
        self.ajoutButt.configure(disabledforeground="#a3a3a3")
        self.ajoutButt.configure(font=font10)
        self.ajoutButt.configure(foreground="#000000")
        self.ajoutButt.configure(highlightbackground="#ffffff")
        self.ajoutButt.configure(highlightcolor="black")
        self.ajoutButt.configure(relief=RIDGE)
        self.ajoutButt.configure(pady="0")
        self.ajoutButt.configure(text='''Ajout d'un produit au stock''')
        self.ajoutButt.config(command=self.ajout)



        self.perimButt = Button(self.bodyFrame)
        self.perimButt.place(relx=0.55, rely=0.1, height=70, width=350)
        self.perimButt.configure(activebackground="#ffffff")
        self.perimButt.configure(activeforeground="#000000")
        self.perimButt.configure(background="#ffffff")
        self.perimButt.configure(disabledforeground="#a3a3a3")
        self.perimButt.configure(font=font10)
        self.perimButt.configure(foreground="#000000")
        self.perimButt.configure(highlightbackground="#ffffff")
        self.perimButt.configure(highlightcolor="black")
        self.perimButt.configure(relief=RIDGE)
        self.perimButt.configure(pady="0")
        self.perimButt.configure(text='''Les produits périmés''')
        self.perimButt.config(command=self.perimer)


        self.ruptButt = Button(self.bodyFrame)
        self.ruptButt.place(relx=0.07, rely=0.35, height=70, width=350)
        self.ruptButt.configure(activebackground="#ffffff")
        self.ruptButt.configure(activeforeground="#000000")
        self.ruptButt.configure(background="#ffffff")
        self.ruptButt.configure(disabledforeground="#a3a3a3")
        self.ruptButt.configure(font=font10)
        self.ruptButt.configure(foreground="#000000")
        self.ruptButt.configure(highlightbackground="#ffffff")
        self.ruptButt.configure(highlightcolor="black")
        self.ruptButt.configure(pady="0")
        self.ruptButt.configure(relief=RIDGE)
        self.ruptButt.configure(text='''Les produits en rupture de stock''')

        self.ruptButt['command'] = self.affichage

        self.qtlotButt = Button(self.bodyFrame)
        self.qtlotButt.place(relx=0.55, rely=0.35, height=70, width=350)
        self.qtlotButt.configure(activebackground="#ffffff")
        self.qtlotButt.configure(activeforeground="#000000")
        self.qtlotButt.configure(background="#ffffff")
        self.qtlotButt.configure(disabledforeground="#a3a3a3")
        self.qtlotButt.configure(font=font10)
        self.qtlotButt.configure(foreground="#000000")
        self.qtlotButt.configure(highlightbackground="#ffffff")
        self.qtlotButt.configure(highlightcolor="black")
        self.qtlotButt.configure(pady="0")
        self.qtlotButt.configure(relief=RIDGE)
        self.qtlotButt.configure(text='''Quantité d'un lot''')

        self.qtlotButt['command'] = self.qt

        self.retraiButt = Button(self.bodyFrame)
        self.retraiButt.place(relx=0.55, rely=0.58, height=70, width=350)
        self.retraiButt.configure(activebackground="#ffffff")
        self.retraiButt.configure(activeforeground="#000000")
        self.retraiButt.configure(background="#ffffff")
        self.retraiButt.configure(disabledforeground="#a3a3a3")
        self.retraiButt.configure(font=font10)
        self.retraiButt.configure(foreground="#000000")
        self.retraiButt.configure(highlightbackground="#ffffff")
        self.retraiButt.configure(highlightcolor="black")
        self.retraiButt.configure(pady="0")
        self.retraiButt.configure(relief=RIDGE)
        self.retraiButt.configure(text='''Retirer un lot d'un produit''')
        self.retraiButt['command'] = self.retrait

        self.qtButt = Button(self.bodyFrame)
        self.qtButt.place(relx=0.07, rely=0.58, height=70, width=350)
        self.qtButt.configure(activebackground="#ffffff")
        self.qtButt.configure(activeforeground="#000000")
        self.qtButt.configure(background="#ffffff")
        self.qtButt.configure(disabledforeground="#a3a3a3")
        self.qtButt.configure(font=font10)
        self.qtButt.configure(foreground="#000000")
        self.qtButt.configure(highlightbackground="#ffffff")
        self.qtButt.configure(highlightcolor="black")
        self.qtButt.configure(pady="0")
        self.qtButt.configure(relief=RIDGE)
        self.qtButt.configure(text='''La quantité d'un produit''')

        self.qtButt['command'] = self.quantite

        self.retourButt = Button(self.bodyFrame)
        self.retourButt.place(relx=0.4, rely=0.86, height=40, width=180)
        self.retourButt.configure(activebackground="#d9d9d9")
        self.retourButt.configure(font=font9)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')

        self.retourButt['command'] = self.retour



        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img1 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img1)


######################################################################################
###################### QUantité ######################################################
######################################################################################
class Quantite(Frame):
    def submit(self):
        con=connectBdd()
        error=0
        #on verifie les entrees
        if (self.EntryTypeVar.get()=="" or self.EntryNmpVar.get()==""or self.newDosVar.get()=="" ):
            showerror("Erreur","Vous devez remplir tous les champs !")
            error=1
        else:
            try:
                k = int(self.newDosVar.get())
            except:
                showerror("Erreur", "Le dosage doit être un nombre !")
                error=1
        if error==0 and con.rechProd_ajout(self.EntryNmpVar.get(),self.newDosVar.get(),self.bienCheckVar.get(),self.EntryTypeVar.get()):
            con.fermer()



            self.retourButt1 = Button(self.Frame1)
            self.BtnConf.destroy()
            self.AnnulButt.destroy()

            self.retourButt1.place(relx=0.35, rely=0.76, height=40, width=250)
            self.retourButt1.configure(activebackground="#d9d9d9")
            self.retourButt1.configure(activeforeground="#000000")
            self.retourButt1.configure(background="#ffffff")
            self.retourButt1.configure(disabledforeground="#a3a3a3")
            self.retourButt1.configure(font=self.font12)
            self.retourButt1.configure(foreground="#000000")
            self.retourButt1.configure(highlightbackground="#ffffff")
            self.retourButt1.configure(highlightcolor="black")
            self.retourButt1.configure(pady="0")
            self.retourButt1.configure(relief=RIDGE)
            self.retourButt1.configure(text='''Retour''')

            self.retourButt1['command'] = self.retour
            con = connectBdd()

            # on recupere le code de la pharmacie courante
            acc = self.controller.getPage(Login)
            cPh = acc.nomPharm[2]

            ri = con.quantiteProduit(nmP=self.EntryNmpVar.get()
                                     , bienEtre=self.bienCheckVar.get()
                                     , dosage=self.newDos.get(), forme=self.EntryType.get(),cPh=cPh)
            nom = self.EntryNmpVar.get()

            dos = self.newDos.get()
            form = self.EntryType.get()
            self.LabelType.destroy()
            self.LabelDosage.destroy()
            self.LabelNmp.destroy()
            self.AnnulButt.destroy()
            self.newDos.destroy()
            self.EntryNmp.destroy()
            self.EntryType.destroy()

            self.donnees[:] = []
            self.scrollable_canvas = ScrollableCanvas4(self)
            self.scrollable_canvas.grid(row=1, column=1)
            self.scrollable_canvas.place(relx=0.08, rely=0.35)

            self.var = ('Produits neufs', 'Produits restitués', 'Total')
            for h in self.var:
                self.donnees.append(h)
            for variable in ri:
                self.donnees.append(variable)


            Label(self.scrollable_canvas.interior, text=self.donnees[0], relief=FLAT, width=25, height=5, bg='#009D78',
                  foreground="#ffffff", font=self.font12).grid(row=0,
                                                               column=0)

            Label(self.scrollable_canvas.interior, text=self.donnees[3], relief=RIDGE, width=25, height=4, bg='white',
                  font=self.font12).grid(row=1,
                                         column=0)

            Label(self.scrollable_canvas.interior, text=self.donnees[1], relief=FLAT, width=25, height=5, bg='#009D78',
                  foreground="#ffffff", font=self.font12).grid(row=0,
                                                               column=1)

            Label(self.scrollable_canvas.interior, text=self.donnees[4], relief=RIDGE, width=25, height=4, bg='white',
                  font=self.font12).grid(row=1,
                                         column=1)

            Label(self.scrollable_canvas.interior, text=self.donnees[2], relief=FLAT, width=25, height=5, bg='#009D78',
                  foreground="#ffffff", font=self.font12).grid(row=0,
                                                               column=2)

            Label(self.scrollable_canvas.interior, text=self.donnees[5], relief=RIDGE, width=25, height=4, bg='white',
                  font=self.font12).grid(row=1,
                                         column=2)



            self.ttitle = Label(self.bodyFrame)
            self.ttitle.place(relx=0.23, rely=0.02, height=70, width=500)
            self.ttitle.configure(activebackground="#336464")
            self.ttitle.configure(activeforeground="white")
            self.ttitle.configure(activeforeground="black")
            self.ttitle.configure(background="#009D78")
            self.ttitle.configure(disabledforeground="#a3a3a3")
            self.ttitle.configure(font=self.font12)
            self.ttitle.configure(foreground="#ffffff")
            self.ttitle.configure(highlightbackground="#ffffff")
            self.ttitle.configure(highlightcolor="black")
            self.ttitle.configure(text='''La quantité du produit: ''' + nom.capitalize() + " - "+dos +" - "+ form.capitalize())
        else :
            showinfo("Produit indisponible","Ce produit n'existe pas !")
        con.fermer()

    def retour(self):
        font10 = "-family {Futura Bk BT} -size 20 -weight bold " \
                 "-slant roman -underline 0 -overstrike 0"
        font11 = "-family {Futura Bk BT} -size 11 -weight bold " \
                 "-slant roman -underline 0 -overstrike 0"
        font9 = "-family {Futura Bk BT} -size 12 -weight bold -slant" \
                " roman -underline 0 -overstrike 0"

        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        font13 = "-family {Futura Bk BT} -size 11  -slant " \
                 "roman -underline 0 -overstrike 0"
        self.newDosVar.set("")
        self.EntryNmpVar.set("")
        self.EntryTypeVar.set("")
        try:
            self.scrollable_canvas.destroy()
            self.ttitle.destroy()
            self.retourButt1.destroy()
        except:
            pass

        self.LabelType = Label(self.bodyFrame)
        self.LabelType.place(relx=0.22, rely=0.57, height=35, width=174)
        self.LabelType.configure(activebackground="#f9f9f9")
        self.LabelType.configure(activeforeground="black")
        self.LabelType.configure(background="#ffffff")
        self.LabelType.configure(disabledforeground="#a3a3a3")
        self.LabelType.configure(font=font9)
        self.LabelType.configure(foreground="#000000")
        self.LabelType.configure(highlightbackground="#ffffff")
        self.LabelType.configure(highlightcolor="black")
        self.LabelType.configure(anchor=W)
        self.LabelType.configure(text='''Forme :''')

        self.LabelDosage = Label(self.bodyFrame)
        self.LabelDosage.place(relx=0.22, rely=0.4, height=35, width=174)
        self.LabelDosage.configure(activebackground="#f9f9f9")
        self.LabelDosage.configure(activeforeground="black")
        self.LabelDosage.configure(background="#ffffff")
        self.LabelDosage.configure(disabledforeground="#a3a3a3")
        self.LabelDosage.configure(font=font9)
        self.LabelDosage.configure(foreground="#000000")
        self.LabelDosage.configure(highlightbackground="#ffffff")
        self.LabelDosage.configure(highlightcolor="black")
        self.LabelDosage.configure(anchor=W)
        self.LabelDosage.configure(text='''Dosage :''')

        self.LabelNmp = Label(self.bodyFrame)
        self.LabelNmp.place(relx=0.22, rely=0.24, height=35, width=174)
        self.LabelNmp.configure(activebackground="#f9f9f9")
        self.LabelNmp.configure(activeforeground="#000000")
        self.LabelNmp.configure(background="#ffffff")
        self.LabelNmp.configure(disabledforeground="#a3a3a3")
        self.LabelNmp.configure(font=font9)
        self.LabelNmp.configure(foreground="#000000")
        self.LabelNmp.configure(highlightbackground="#ffffff")
        self.LabelNmp.configure(highlightcolor="#000000")
        self.LabelNmp.configure(anchor=W)
        self.LabelNmp.configure(text='''Nom du produit :''')

        # on genere la liste des produits existants:
        self.liste_produits = []
        var = connectBdd()
        cur = var.cur
        cur.execute("""SELECT nomProduit FROM produits""")
        resultat1 = cur.fetchall()

        for inter in resultat1:
            for inter2 in inter:
                var = inter2.lower().capitalize()
                self.liste_produits.append(var)

        self.liste_produits = sorted(self.liste_produits)
        # on supprime les doublants dans cette liste:
        self.inter = ""
        self.liste_products = []
        for produit in self.liste_produits:
            if produit != self.inter:
                self.liste_products.append(produit)
                self.inter = produit

        self.EntryNmpVar = StringVar()
        self.EntryNmp = Combobox(self.bodyFrame, textvariable=self.EntryNmpVar, values=self.liste_products,
                                      state="readonly")
        self.EntryNmp.place(relx=0.45, rely=0.24, relheight=0.06
                                 , relwidth=0.38)
        self.EntryNmp.configure(background="#ffffff")



        self.newDosVar = StringVar()
        self.newDos = Entry(self.bodyFrame, textvariable=self.newDosVar)
        self.newDos.place(relx=0.45, rely=0.39, relheight=0.06, relwidth=0.38)
        self.newDos.configure(background="#ffffff")
        self.newDos.configure(disabledforeground="#a3a3a3")
        self.newDos.configure(font="TkFixedFont")
        self.newDos.configure(foreground="#000000")
        self.newDos.configure(highlightbackground="#ffffff")
        self.newDos.configure(highlightcolor="black")
        self.newDos.configure(insertbackground="black")
        self.newDos.configure(selectbackground="#c4c4c4")
        self.newDos.configure(selectforeground="black")


        self.EntryTypeVar = StringVar()
        con = connectBdd()
        con.cur.execute("SELECT forme from produits ");
        e = con.cur.fetchall()
        self.liste_formes = []
        k = []
        for m in e:
            k.append(m[0])

        k = set(k)
        for i in k:
            self.liste_formes.append(i)
        con.fermer()
        # self.liste_formes = (
        # 'Comprime', 'Suppositoire', 'Sirop', 'Solution buvable', 'Gelule', 'Solution injectable', 'ComprimeEfferv',
        # 'Poudre', 'Liquide', 'Pommade', 'Gel', 'Sachet', 'Capsule', 'Goute', 'Ampoule', '')

        self.liste_formes = sorted(self.liste_formes)
        self.EntryType = Combobox(self.bodyFrame, textvariable=self.EntryTypeVar, values=self.liste_formes,
                                  state="readonly")

        self.EntryType.place(relx=0.45, rely=0.565, relheight=0.06, relwidth=0.38)
        self.EntryType.configure(background="#ffffff")











        self.BtnConf = Button(self.bodyFrame)
        self.BtnConf.place(relx=0.64, rely=0.86, height=40, width=180)
        self.BtnConf.configure(activebackground="#ffffff")
        self.BtnConf.configure(activeforeground="#000000")
        self.BtnConf.configure(background="#ffffff")
        self.BtnConf.configure(disabledforeground="#a3a3a3")
        self.BtnConf.configure(font=font9)
        self.BtnConf.configure(foreground="#000000")
        self.BtnConf.configure(highlightbackground="#ffffff")
        self.BtnConf.configure(highlightcolor="black")
        self.BtnConf.configure(pady="0")
        self.BtnConf.configure(relief=RIDGE)
        self.BtnConf.configure(text='''Confirmer''')

        self.BtnConf['command'] = self.submit


        self.AnnulButt = Button(self.bodyFrame)
        self.AnnulButt.place(relx=0.17, rely=0.86, height=40, width=180)
        self.AnnulButt.configure(activebackground="#d9d9d9")
        self.AnnulButt.configure(font=font9)
        self.AnnulButt.configure(activeforeground="#000000")
        self.AnnulButt.configure(background="#ffffff")
        self.AnnulButt.configure(disabledforeground="#a3a3a3")
        self.AnnulButt.configure(foreground="#000000")
        self.AnnulButt.configure(highlightbackground="#ffffff")
        self.AnnulButt.configure(highlightcolor="black")
        self.AnnulButt.configure(pady="0")
        self.AnnulButt.configure(relief=RIDGE)
        self.AnnulButt.configure(text='''Annuler''')
        self.AnnulButt.configure(pady="0")

        self.AnnulButt['command'] = self.retour


        self.master.master.show_frame(gestionStock)

    def GestionDeCompte(self):
        self.retour()
        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()

    def notifs(self):
        if self.notif == 0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])

                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                          height=1, bg='white', anchor="w",
                          font=self.font12).grid(row=r,
                                                 column=1)
                    r = r + 1
                r = 0
                self.notif = 1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=818)
                self.supprnotifs.configure(activebackground="#009D78")
                self.supprnotifs.configure(activeforeground="#009D78")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command'] = self.supprimenotifs
            else:
                showinfo("Pas de notifications", "Vous n'avez pas de notifications !")

        else:
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif = 0

    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con = connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0

    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var = self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res:
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()

    def updateDosage(self, *args):

        if self.bienCheckVar.get():
            self.dosVar = self.newDosVar.get()
            self.newDos.config(state="readonly")
            self.newDosVar.set("")
        else:
            self.newDos.config(state="normal")
            self.newDosVar.set(self.dosVar)

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller


        font10 = "-family {Futura Bk BT} -size 20 -weight bold " \
                 "-slant roman -underline 0 -overstrike 0"
        font11 = "-family {Futura Bk BT} -size 11 -weight bold " \
                 "-slant roman -underline 0 -overstrike 0"
        font9 = "-family {Futura Bk BT} -size 12 -weight bold -slant" \
                " roman -underline 0 -overstrike 0"

        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        font13 = "-family {Futura Bk BT} -size 11  -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.font13 = font13
        self.font11 = font11
        self.font10 = font10
        self.font9 = font9
        #####################
        self.donnees = []
        self.donnees1 = []
        self.r = []
        #################


        self.Frame1 = Frame(self)
        self.Frame1.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="0")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#ffffff")
        self.Frame1.configure(highlightbackground="#ffffff")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=935)

        self.FrameHaut = Frame(self.Frame1)
        self.FrameHaut.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.FrameHaut.configure(borderwidth="0")
        self.FrameHaut.configure(background="#009D78")
        self.FrameHaut.configure(highlightbackground="#ffffff")
        self.FrameHaut.configure(highlightcolor="black")
        self.FrameHaut.configure(width=935)

        self.titleLabel = Label(self.FrameHaut)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(activebackground="#336464")
        self.titleLabel.configure(activeforeground="white")
        self.titleLabel.configure(activeforeground="black")
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(font=font10)
        self.titleLabel.configure(foreground="#ffffff")
        self.titleLabel.configure(highlightbackground="#ffffff")
        self.titleLabel.configure(highlightcolor="black")
        self.titleLabel.configure(text='''Quantite d'un produit''')
        self._img5 = PhotoImage(file="images/qt1.png")
        self.titleLabel.configure(image=self._img5)

        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0


        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img1 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img1)

        self.bodyFrame = Frame(self.Frame1)
        self.bodyFrame.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1)
        self.bodyFrame.configure(relief=FLAT)
        self.bodyFrame.configure(borderwidth="0")
        self.bodyFrame.configure(relief=FLAT)
        self.bodyFrame.configure(background="#ffffff")
        self.bodyFrame.configure(highlightbackground="#ffffff")
        self.bodyFrame.configure(highlightcolor="black")
        self.bodyFrame.configure(width=935)

        self.Labelbody = Label(self.bodyFrame)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)

        self.LabelType = Label(self.bodyFrame)
        self.LabelType.place(relx=0.22, rely=0.57, height=35, width=174)
        self.LabelType.configure(activebackground="#f9f9f9")
        self.LabelType.configure(activeforeground="black")
        self.LabelType.configure(background="#ffffff")
        self.LabelType.configure(disabledforeground="#a3a3a3")
        self.LabelType.configure(font=font9)
        self.LabelType.configure(foreground="#000000")
        self.LabelType.configure(highlightbackground="#ffffff")
        self.LabelType.configure(highlightcolor="black")
        self.LabelType.configure(anchor=W)
        self.LabelType.configure(text='''Forme :''')

        self.LabelDosage = Label(self.bodyFrame)
        self.LabelDosage.place(relx=0.22, rely=0.4, height=35, width=174)
        self.LabelDosage.configure(activebackground="#f9f9f9")
        self.LabelDosage.configure(activeforeground="black")
        self.LabelDosage.configure(background="#ffffff")
        self.LabelDosage.configure(disabledforeground="#a3a3a3")
        self.LabelDosage.configure(font=font9)
        self.LabelDosage.configure(foreground="#000000")
        self.LabelDosage.configure(highlightbackground="#ffffff")
        self.LabelDosage.configure(highlightcolor="black")
        self.LabelDosage.configure(anchor=W)
        self.LabelDosage.configure(text='''Dosage :''')

        self.LabelNmp = Label(self.bodyFrame)
        self.LabelNmp.place(relx=0.22, rely=0.24, height=35, width=174)
        self.LabelNmp.configure(activebackground="#ffffff")
        self.LabelNmp.configure(activeforeground="#000000")
        self.LabelNmp.configure(background="#ffffff")
        self.LabelNmp.configure(disabledforeground="#a3a3a3")
        self.LabelNmp.configure(font=font9)
        self.LabelNmp.configure(foreground="#000000")
        self.LabelNmp.configure(highlightbackground="#ffffff")
        self.LabelNmp.configure(highlightcolor="#000000")
        self.LabelNmp.configure(anchor=W)
        self.LabelNmp.configure(text='''Nom du produit :''')

        # on genere la liste des produits existants:
        self.liste_produits = []
        var = connectBdd()
        cur = var.cur
        cur.execute("""SELECT nomProduit FROM produits""")
        resultat1 = cur.fetchall()

        for inter in resultat1:
            for inter2 in inter:
                var = inter2.lower().capitalize()
                self.liste_produits.append(var)

        self.liste_produits = sorted(self.liste_produits)
        # on supprime les doublants dans cette liste:
        self.inter = ""
        self.liste_products = []
        for produit in self.liste_produits:
            if produit != self.inter:
                self.liste_products.append(produit)
                self.inter = produit

        self.EntryNmpVar = StringVar()
        self.EntryNmp = Combobox(self.bodyFrame, textvariable=self.EntryNmpVar, values=self.liste_products,
                                      state="readonly")
        self.EntryNmp.place(relx=0.45, rely=0.24, relheight=0.06
                                 , relwidth=0.38)
        self.EntryNmp.configure(background="#ffffff")






        self.newDosVar = StringVar()
        self.newDos = Entry(self.bodyFrame, textvariable=self.newDosVar)
        self.newDos.place(relx=0.45, rely=0.39, relheight=0.06, relwidth=0.38)
        self.newDos.configure(background="#ffffff")
        self.newDos.configure(disabledforeground="#a3a3a3")
        self.newDos.configure(font="TkFixedFont")
        self.newDos.configure(foreground="#000000")
        self.newDos.configure(highlightbackground="#ffffff")
        self.newDos.configure(highlightcolor="black")
        self.newDos.configure(insertbackground="black")
        self.newDos.configure(selectbackground="#c4c4c4")
        self.newDos.configure(selectforeground="black")

        self.EntryTypeVar = StringVar()
        con = connectBdd()
        con.cur.execute("SELECT forme from produits ");
        e = con.cur.fetchall()
        self.liste_formes = []
        var = "nothing"
        k = []
        for m in e:
            k.append(m[0])

        k = set(k)
        for i in k:
            self.liste_formes.append(i)
        con.fermer()
        # self.liste_formes = (
        # 'Comprime', 'Suppositoire', 'Sirop', 'Solution buvable', 'Gelule', 'Solution injectable', 'ComprimeEfferv',
        # 'Poudre', 'Liquide', 'Pommade', 'Gel', 'Sachet', 'Capsule', 'Goute', 'Ampoule', '')

        self.liste_formes = sorted(self.liste_formes)
        self.EntryType = Combobox(self.bodyFrame, textvariable=self.EntryTypeVar, values=self.liste_formes,
                                  state="readonly")

        self.EntryType.place(relx=0.45, rely=0.565, relheight=0.06, relwidth=0.38)
        self.EntryType.configure(background="#ffffff")





        self.bienCheckVar = IntVar()
        self.bienCheckVar.trace("w", self.updateDosage)
        self.bienCheck = Checkbutton(self.bodyFrame)
        self.bienCheck.place(relx=0.45, rely=0.46, relheight=0.06, relwidth=0.17)

        self.bienCheck.configure(activebackground="#d9d9d9")
        self.bienCheck.configure(activeforeground="#000000")
        self.bienCheck.configure(anchor=W)
        self.bienCheck.configure(background="#ffffff")
        self.bienCheck.configure(borderwidth="10")
        self.bienCheck.configure(disabledforeground="#a3a3a3")
        self.bienCheck.configure(font=font11)
        self.bienCheck.configure(foreground="#000000")
        self.bienCheck.configure(highlightbackground="#000000")
        self.bienCheck.configure(highlightcolor="black")
        self.bienCheck.configure(justify=LEFT)
        self.bienCheck.configure(text='''Bien_Etre''')
        self.bienCheck.configure(variable=self.bienCheckVar)

        self.bienCheck.configure(width=439)


        self.BtnConf = Button(self.bodyFrame)
        self.BtnConf.place(relx=0.64, rely=0.86, height=40, width=180)
        self.BtnConf.configure(activebackground="#ffffff")
        self.BtnConf.configure(activeforeground="#000000")
        self.BtnConf.configure(background="#ffffff")
        self.BtnConf.configure(disabledforeground="#a3a3a3")
        self.BtnConf.configure(font=font9)
        self.BtnConf.configure(foreground="#000000")
        self.BtnConf.configure(highlightbackground="#ffffff")
        self.BtnConf.configure(highlightcolor="black")
        self.BtnConf.configure(pady="0")
        self.BtnConf.configure(relief=RIDGE)
        self.BtnConf.configure(text='''Confirmer''')

        self.BtnConf['command'] = self.submit


        self.AnnulButt = Button(self.bodyFrame)
        self.AnnulButt.place(relx=0.17, rely=0.86, height=40, width=180)
        self.AnnulButt.configure(activebackground="#d9d9d9")
        self.AnnulButt.configure(font=font9)
        self.AnnulButt.configure(activeforeground="#000000")
        self.AnnulButt.configure(background="#ffffff")
        self.AnnulButt.configure(disabledforeground="#a3a3a3")
        self.AnnulButt.configure(foreground="#000000")
        self.AnnulButt.configure(highlightbackground="#ffffff")
        self.AnnulButt.configure(highlightcolor="black")
        self.AnnulButt.configure(pady="0")
        self.AnnulButt.configure(relief=RIDGE)
        self.AnnulButt.configure(text='''Annuler''')

        self.AnnulButt['command'] = self.retour




###################################################################################################################################

#############################################################################################
############################### Statistiques ###############################################
#############################################################################################
class StatVente(Frame):

    def GestionDeCompte(self):
        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()

    def notifs(self):
        if self.notif == 0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])

                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                          height=1, bg='white', anchor="w",
                          font=self.font12).grid(row=r,
                                                 column=1)
                    r = r + 1
                r = 0
                self.notif = 1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=818)
                self.supprnotifs.configure(activebackground="#009D78")
                self.supprnotifs.configure(activeforeground="#009D78")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command'] = self.supprimenotifs
            else:
                showinfo("Pas de notifications", "Vous n'avez pas de notifications !")

        else:
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif = 0

    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con = connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0

    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var = self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res:
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()

    font11 = "-family {Futura Bk BT} -size 20 -weight bold -slant " \
             "roman -underline 0 -overstrike 0"

    font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
             "roman -underline 0 -overstrike 0"

    def retour(self):

        self.controller.show_frame(Stats)

    def submit(self):
        con = connectBdd()
        date1 = self.calDebut.get()
        date2 = self.calFin.get()
        debut = str(str(date1[6]) + str(date1[7]) + str(date1[8]) + str(date1[9]) + "/" + str(date1[3]) + str(date1[4])
                    + "/" + str(date1[0]) + str(date1[1]))
        fin = str(str(date2[6]) + str(date2[7]) + str(date2[8]) + str(date2[9]) + "/" + str(date2[3]) + str(date2[4])
                  + "/" + str(date2[0]) + str(date2[1]))
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        e2 = con.venteRest(debut, fin,cPh)
        if e2 == -1:
            showerror(" Erreur ", " Vous devez d'abord remplir les champs !")
        if e2 == 0:
            showinfo(" Information ", " La date de fin doit etre plus grande que celle du début !")
        else:

            tDate, tNew, tRest = [], [], []
            if self.bienCheckVar.get():

                for e in e2:
                    tDate.append(str(e[0]))

                for e in e2:
                    tNew.append(e[1])
                for e in e2:
                    tRest.append(e[2])

                plt.plot(tDate, tRest, label=' Restitué  ', color='r')
                plt.plot(tDate, tNew, label=' Non Restitué ', color='c')
                plt.title(" Ventes de produits ")
                plt.legend()
                plt.subplots_adjust(bottom=0.19, left=0.07, right=0.97, top=0.95)
                plt.xticks(rotation=45)
                plt.show()



            else:
                for e in e2:
                    tDate.append(e[0])
                for e in e2:
                    tRest.append(e[2])

                plt.plot(tDate, tRest, label=' Restitué  ', color='r')
                plt.title(" Ventes de produits  Restitués")
                plt.subplots_adjust(bottom=0.19, left=0.07, right=0.97, top=0.95)
                plt.xticks(rotation=45)
                plt.legend()

                plt.show()

        con.fermer()

    def __init__(self, parent, controller):
            Frame.__init__(self, parent)

            self.controller = controller

            font11 = "-family {Futura Bk BT} -size 20 -weight bold -slant " \
                     "roman -underline 0 -overstrike 0"

            font12 = "-family {Futura Bk BT} -size 12-weight bold -slant " \
                     "roman -underline 0 -overstrike 0"

            headFrame = Frame(self)
            headFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
            headFrame.configure(relief=FLAT)
            headFrame.configure(borderwidth="2")
            headFrame.configure(relief=FLAT)
            headFrame.configure(background="#009D78")
            headFrame.configure(width=950)

            self.titleLabel = Label(headFrame)
            self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
            self.titleLabel.configure(background="#009D78")
            self.titleLabel.configure(disabledforeground="#a3a3a3")
            self.titleLabel.configure(font=font11)
            self.titleLabel.configure(foreground="#ffffff")


            self.titleLabel.configure(width=462)
            self._img5 = PhotoImage(file="images/statvente.png")
            self.titleLabel.configure(image=self._img5)

            font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                     "roman -underline 0 -overstrike 0"

            self.font12 = font12
            self.notif = 0


            self.notifications = []
            self.Buttongestcmp = Button(self.titleLabel)
            self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
            self.Buttongestcmp.configure(activebackground="#ffffff")
            self.Buttongestcmp.configure(activeforeground="#000000")
            self.Buttongestcmp.configure(background="#009D78")
            self.Buttongestcmp.configure(borderwidth="0")
            self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

            self.Buttongestcmp.configure(foreground="#808080")
            self.Buttongestcmp.configure(highlightbackground="#ffffff")
            self.Buttongestcmp.configure(highlightcolor="black")
            self.Buttongestcmp.configure(pady="0")
            self.Buttongestcmp.configure(text='''''')
            self.Buttongestcmp.configure(width=147)
            self.Buttongestcmp['command'] = self.GestionDeCompte
            self._img55 = PhotoImage(file="images/account.png")
            self.Buttongestcmp.configure(image=self._img55)

            self.Buttonnotif = Button(self.titleLabel)
            self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
            self.Buttonnotif.configure(activebackground="#ffffff")
            self.Buttonnotif.configure(activeforeground="#000000")
            self.Buttonnotif.configure(background="#009D78")
            self.Buttonnotif.configure(borderwidth="0")
            self.Buttonnotif.configure(disabledforeground="#a3a3a3")

            self.Buttonnotif.configure(foreground="#808080")
            self.Buttonnotif.configure(highlightbackground="#ffffff")
            self.Buttonnotif.configure(highlightcolor="black")
            self.Buttonnotif.configure(pady="0")
            self.Buttonnotif.configure(text='''''')
            self.Buttonnotif.configure(width=147)
            self.Buttonnotif['command'] = self.notifs
            self._img80 = PhotoImage(file="images/notifs.png")
            self.Buttonnotif.configure(image=self._img80)

            self.footFrame = Frame(self)
            self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
            self.footFrame.configure(relief=GROOVE)
            self.footFrame.configure(borderwidth="1")
            self.footFrame.configure(relief=GROOVE)
            self.footFrame.configure(background="#ffffff")
            self.footFrame.configure(width=935)

            self.Labelfoot = Label(self.footFrame)
            self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
            self.Labelfoot.configure(background="#ffffff")
            self.Labelfoot.configure(disabledforeground="#a3a3a3")
            self.Labelfoot.configure(foreground="#000000")
            self.Labelfoot.configure(width=934)
            self._img1 = PhotoImage(file="images/foot.png")
            self.Labelfoot.configure(image=self._img1)

            bodyFrame = Frame(self)
            bodyFrame.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1)

            bodyFrame.configure(relief=FLAT)
            bodyFrame.configure(borderwidth="2")
            bodyFrame.configure(relief=FLAT)
            bodyFrame.configure(background="#ffffff")
            bodyFrame.configure(width=745)

            self.Labelbody = Label(bodyFrame)
            self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
            self.Labelbody.configure(background="#ffffff")
            self.Labelbody.configure(disabledforeground="#a3a3a3")
            self.Labelbody.configure(foreground="#000000")
            self._img155 = PhotoImage(file="images/accu1.png")
            self.Labelbody.configure(image=self._img155)
            self.Labelbody.configure(text='''Label''')
            self.Labelbody.configure(width=935)


            nmpLabel = Label(bodyFrame)
            nmpLabel.place(relx=0.22, rely=0.13, height=34, width=200)
            nmpLabel.configure(anchor=W)
            nmpLabel.configure(background="#ffffff")
            nmpLabel.configure(disabledforeground="#fafafa")
            nmpLabel.configure(font=font12)
            nmpLabel.configure(foreground="#000000")
            nmpLabel.configure(text='''Année De début :''')
            nmpLabel.configure(anchor=W)


            dosageLabel = Label(bodyFrame)
            dosageLabel.place(relx=0.22, rely=0.33, height=34, width=200)
            dosageLabel.configure(activebackground="#fafafa")
            dosageLabel.configure(activeforeground="black")
            dosageLabel.configure(anchor=W)
            dosageLabel.configure(background="#ffffff")
            dosageLabel.configure(disabledforeground="#a3a3a3")
            dosageLabel.configure(font=font12)
            dosageLabel.configure(foreground="#000000")
            dosageLabel.configure(highlightbackground="#ffffff")
            dosageLabel.configure(highlightcolor="black")
            dosageLabel.configure(text='''Année De fin :''')
            dosageLabel.configure(anchor=W)


            self.calDebut = DateEntry(self, width=50, background='#009D78', foreground='#ffffff', borderwidth=2)
            self.calDebut.place(relx=0.45, rely=0.31, relheight=0.05)

            self.calFin = DateEntry(self, width=50, background='#009D78',
                                   foreground='#ffffff', borderwidth=2)
            self.calFin.place(relx=0.45, rely=0.45, relheight=0.05)

            self.bienCheckVar = IntVar()
            # self.bienCheckVar.trace("w",self.updateShow)
            self.bienCheck = Checkbutton(bodyFrame)
            self.bienCheck.place(relx=0.22, rely=0.52, relheight=0.06, relwidth=0.5)

            self.bienCheck.configure(activebackground="#d9d9d9")
            self.bienCheck.configure(activeforeground="#000000")
            self.bienCheck.configure(anchor=W)
            self.bienCheck.configure(background="#ffffff")
            self.bienCheck.configure(borderwidth="10")
            self.bienCheck.configure(disabledforeground="#a3a3a3")
            self.bienCheck.configure(font=font12)
            self.bienCheck.configure(foreground="#000000")
            self.bienCheck.configure(highlightbackground="#000000")
            self.bienCheck.configure(highlightcolor="black")
            self.bienCheck.configure(justify=LEFT)
            self.bienCheck.configure(text='''Afficher Les Statistiques Des produits non restitués ''')
            self.bienCheck.configure(variable=self.bienCheckVar)
            self.bienCheck.configure(width=500)


            self.retourBtn = Button(bodyFrame)
            self.retourBtn.place(relx=0.17, rely=0.86, height=40, width=180)
            self.retourBtn.configure(activebackground="#ffffff")
            self.retourBtn.configure(activeforeground="#000000")
            self.retourBtn.configure(font=font12)
            self.retourBtn.configure(background="#ffffff")
            self.retourBtn.configure(disabledforeground="#a3a3a3")
            self.retourBtn.configure(foreground="#000000")
            self.retourBtn.configure(highlightbackground="#ffffff")
            self.retourBtn.configure(highlightcolor="black")
            self.retourBtn.configure(pady="0")
            self.retourBtn.configure(relief=RIDGE)
            self.retourBtn.configure(text='''Retour''')
            self.retourBtn.config(command=self.retour)



            self.confBtn = Button(bodyFrame)
            self.confBtn.place(relx=0.64, rely=0.86, height=40, width=180)
            self.confBtn.configure(activebackground="#ffffff")
            self.confBtn.configure(activeforeground="#000000")
            self.confBtn.configure(background="#ffffff")
            self.confBtn.configure(font=font12)
            self.confBtn.configure(disabledforeground="#a3a3a3")
            self.confBtn.configure(foreground="#000000")
            self.confBtn.configure(highlightbackground="#ffffff")
            self.confBtn.configure(highlightcolor="black")
            self.confBtn.configure(pady="0")
            self.confBtn.configure(relief=RIDGE)
            self.confBtn.configure(text='''Confimer''')
            self.confBtn.config(command=self.submit)


    ######################################################################################
    ####################################################################################################################
    ######################################################################################
class Stats(Frame):

    def GestionDeCompte(self):
        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()

    def notifs(self):
        if self.notif == 0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])

                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                          height=1, bg='white', anchor="w",
                          font=self.font12).grid(row=r,
                                                 column=1)
                    r = r + 1
                r = 0
                self.notif = 1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=818)
                self.supprnotifs.configure(activebackground="#009D78")
                self.supprnotifs.configure(activeforeground="#009D78")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command'] = self.supprimenotifs
            else:
                showinfo("Pas de notifications", "Vous n'avez pas de notifications !")

        else:
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif = 0

    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con = connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0

    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var = self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res:
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()

    def retour(self):
        self.master.master.show_frame(Acceuil)

    def statVente(self):
        self.master.master.show_frame(StatVente)
    def echangesEntrePharms(self):
        self.master.master.show_frame(EchangesEntrePharm)
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        font10 = "-family {Futura Bk BT} -size 15 -weight bold " \
                 "-slant roman -underline 0 -overstrike 0"
        font11 = "-family {Futura Bk BT} -size 20 -weight bold " \
                 "-slant roman -underline 0 -overstrike 0"
        font9 = "-family {Futura Bk BT} -size 12 -weight bold -slant" \
                " roman -underline 0 -overstrike 0"

        self.Frame1 = Frame(self)
        self.Frame1.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.Frame1.configure(relief=FLAT)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=FLAT)
        self.Frame1.configure(background="#ffffff")
        self.Frame1.configure(highlightbackground="#ffffff")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=125)

        self.headFrame = Frame(self.Frame1)
        self.headFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.headFrame.configure(borderwidth="2")
        self.headFrame.configure(background="#009D78")
        self.headFrame.configure(highlightbackground="#ffffff")
        self.headFrame.configure(highlightcolor="black")
        self.headFrame.configure(width=125)

        self.titleLabel = Label(self.headFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(activebackground="#f9f9f9")
        self.titleLabel.configure(activeforeground="black")
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(font=font11)
        self.titleLabel.configure(foreground="#ffffff")
        self.titleLabel.configure(highlightbackground="#ffffff")
        self.titleLabel.configure(highlightcolor="black")
        self.__img15 = PhotoImage(file="images/stats.png")
        self.titleLabel.configure(image=self.__img15)

        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0


        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        self.bodyFrame = Frame(self.Frame1)
        self.bodyFrame.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1)
        self.bodyFrame.configure(relief=FLAT)
        self.bodyFrame.configure(borderwidth="2")
        self.bodyFrame.configure(relief=FLAT)
        self.bodyFrame.configure(background="#ffffff")
        self.bodyFrame.configure(highlightbackground="#ffffff")
        self.bodyFrame.configure(highlightcolor="black")
        self.bodyFrame.configure(width=745)

        self.Labelbody = Label(self.bodyFrame)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)

        self.Button2 = Button(self.bodyFrame)
        self.Button2.place(relx=0.32, rely=0.22, height=70, width=357)
        self.Button2.configure(activebackground="#ffffff")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#ffffff")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(font=font10)
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#ffffff")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(relief=RIDGE)
        self.Button2.configure(text='''Echanges interpharmacies''')
        self.Button2.config(command=self.echangesEntrePharms)



        self.restButt = Button(self.bodyFrame)
        self.restButt.place(relx=0.32, rely=0.51, height=70, width=357)
        self.restButt.configure(activebackground="#ffffff")
        self.restButt.configure(activeforeground="#000000")
        self.restButt.configure(background="#ffffff")
        self.restButt.configure(disabledforeground="#a3a3a3")
        self.restButt.configure(font=font10)
        self.restButt.configure(relief=RIDGE)
        self.restButt.configure(foreground="#000000")
        self.restButt.configure(highlightbackground="#ffffff")
        self.restButt.configure(highlightcolor="black")
        self.restButt.configure(pady="0")
        self.restButt.configure(text='''Vente de produits''')

        self.restButt['command'] = self.statVente


        self.retourButt = Button(self.bodyFrame)
        self.retourButt.place(relx=0.4, rely=0.86, height=40, width=180)
        self.retourButt.configure(activebackground="#d9d9d9")
        self.retourButt.configure(font=font9)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')

        self.retourButt['command'] = self.retour

        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img1 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img1)



###########################################################################################
class Login(Frame):
    def retour(self):
        self.userEntryVar.set("")
        self.passEntryVar.set("")
        self.master.master.show_frame(Bienvenue)

    global titreGlobal

    def tick(self, time1=""):
        time2 = time.strftime(" %H: %M: %S")
        if time2 != time1:
            time1 = time2
            self.clock_frame.configure(text=time2)
        self.clock_frame.after(200, self.tick)

    def connect(self):

        un = self.userEntryVar.get()
        pwd = self.passEntryVar.get()
        r = self.restConnVar.get()
        con = connectBdd()

        if con.authentification(un, pwd):
            showinfo("Bienvenue ", "  Bienvenue  :     " + un)
            self.nomPharm = con.authentification(un, pwd)

            acc = self.controller.getPage(EchangesEntrePharm)
            cur=con.cur

            cur.execute('''SELECT pharmacie from contacts where code=%s;''',(self.nomPharm[2]))
            res=cur.fetchone()

            acc.list1Var.set(res[0])

            self.controller.show_frame(Acceuil)
            self.verif_notif()
            con.fermer()

        else:
            showerror("Erreur !", " Votre Mot de passe ou l'Identifiant est incorrect ")
    def verif_notif(self):
        # on verifie le nombre de notifications
        con=connectBdd()
        cur =con.cur
        cur.execute('''SELECT * from notifications where code=%s;''', (self.nomPharm[2]))
        res = cur.fetchall()

        k = 0
        if res:
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if self.nombrenotifs <k:
            self.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()


    def visiblePass(self,event):

        self.passEntry.config(show="")
        self.visibleMessage.config(text="")


    def invisiblePass(self,event):
        self.passEntry.config(show="\u2022")
        self.visibleMessage.config(text=" Afficher Le mot De Passe")

    def message(self,event):
        self.visibleMessage.config(text=" Afficher Le mot De Passe")
    def messageLeave(self,event):
        self.visibleMessage.config(text="")

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.nomPharm=[]
        font13 = "-family {Gill Sans Ultra Bold} -size 11 -weight " \
                 "bold -slant roman -underline 0 -overstrike 0"
        font18 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        font20 = "-family {Futura Bk BT} -size 18 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        self.nombrenotifs=0


        headerFrame = Frame(self)
        headerFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        headerFrame.configure(relief=FLAT)
        headerFrame.configure(borderwidth="2")
        headerFrame.configure(relief=FLAT)
        headerFrame.configure(background="#009D78")
        headerFrame.configure(width=955)


        self.titleLabel = Label(headerFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(activebackground="#f9f9f9")
        self.titleLabel.configure(activeforeground="black")
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(foreground="#ffffff")
        self.titleLabel.configure(highlightbackground="#ffffff")
        self.titleLabel.configure(highlightcolor="black")
        self.__img136 = PhotoImage(file="images/vide.png")
        self.titleLabel.configure(image=self.__img136)




        bodyFrame = Frame(self)
        bodyFrame.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1.0)
        bodyFrame.configure(relief=FLAT)
        bodyFrame.configure(borderwidth="2")
        bodyFrame.configure(relief=FLAT)
        bodyFrame.configure(background="#ffffff")
        bodyFrame.configure(width=745)

        self.Labelbody = Label(bodyFrame)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)





        userLabel = Label(bodyFrame)
        userLabel.place(relx=0.428, rely=0.13, height=34, width=182)
        userLabel.configure(background="#ffffff")
        userLabel.configure(disabledforeground="#a3a3a3")
        userLabel.configure(font=font18)
        userLabel.configure(anchor=W)
        userLabel.configure(foreground="#000000")
        userLabel.configure(text='''Identifiant :''')
        userLabel.configure(width=182)

        self.userEntryVar = StringVar()
        self.userEntry = Entry(bodyFrame, font=font18, textvariable=self.userEntryVar)
        self.userEntry.place(relx=0.35, rely=0.25, relheight=0.06, relwidth=0.3)

        self.userEntry.configure(width=346)
        self.userEntry.configure(background="#ffffff")
        self.userEntry.configure(takefocus="")
        self.userEntry.configure(cursor="ibeam")

        passLabel = Label(bodyFrame)
        passLabel.place(relx=0.428, rely=0.35, height=34, width=200)
        passLabel.configure(activebackground="#f9f9f9")
        passLabel.configure(activeforeground="black")
        passLabel.configure(background="#ffffff")
        passLabel.configure(disabledforeground="#a3a3a3")
        passLabel.configure(font=font18)
        passLabel.configure(foreground="#000000")
        passLabel.configure(highlightbackground="#ffffff")
        passLabel.configure(highlightcolor="black")
        passLabel.configure(text='''Mot de Passe :''')
        passLabel.configure(anchor=W)

        self.passEntryVar = StringVar()
        self.passEntry = Entry(bodyFrame, show='\u2022', font=font18, textvariable=self.passEntryVar)
        self.passEntry.place(relx=0.35, rely=0.46, relheight=0.06, relwidth=0.3)
        self.passEntry.configure(width=346)
        self.passEntry.config(background="#ffffff")
        self.passEntry.configure(takefocus="")
        self.passEntry.configure(cursor="ibeam")
        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img900 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img900)


        self.retourBtn = Button(bodyFrame)
        self.retourBtn.place(relx=0.17, rely=0.86, height=40, width=180)
        self.retourBtn.configure(activebackground="#ffffff")
        self.retourBtn.configure(activeforeground="#000000")
        self.retourBtn.configure(font=font18)
        self.retourBtn.configure(background="#ffffff")
        self.retourBtn.configure(disabledforeground="#a3a3a3")
        self.retourBtn.configure(foreground="#000000")
        self.retourBtn.configure(highlightbackground="#ffffff")
        self.retourBtn.configure(highlightcolor="black")
        self.retourBtn.configure(pady="0")
        self.retourBtn.configure(relief=RIDGE)
        self.retourBtn.configure(text='''Retour''')

        self.retourBtn['command'] = self.retour




        self.confBtn = Button(bodyFrame)
        self.confBtn['command'] = self.connect

        self.confBtn.place(relx=0.64, rely=0.86, height=40, width=180)
        self.confBtn.configure(activebackground="#ffffff")
        self.confBtn.configure(activeforeground="#000000")
        self.confBtn.configure(background="#ffffff")
        self.confBtn.configure(font=font18)
        self.confBtn.configure(disabledforeground="#a3a3a3")
        self.confBtn.configure(foreground="#000000")
        self.confBtn.configure(highlightbackground="#ffffff")
        self.confBtn.configure(highlightcolor="black")
        self.confBtn.configure(pady="0")
        self.confBtn.configure(relief=RIDGE)
        self.confBtn.configure(text='''Connexion''')



        self.visibleIcon=PhotoImage(file="images/visible2.png")


        self.visibleButt = Button(bodyFrame,image=self.visibleIcon,relief=FLAT,
                                  background='#ffffff')
        self.visibleButt.configure(activebackground="#ffffff")
        self.visibleButt.configure(overrelief="flat")

        self.visibleMessage=Label(bodyFrame,background="#ffffff",font=font18,
                                  foreground="#009D78",text="")
        self.visibleMessage.place(relx=0.55, rely=0.53)

        self.visibleButt.bind("<Button-1>",self.visiblePass)
        self.visibleButt.bind("<ButtonRelease-1>", self.invisiblePass)
        self.visibleButt.bind("<Enter>", self.message)
        self.visibleButt.bind("<Leave>", self.messageLeave)


        self.visibleButt.place(relx=0.6, rely=0.465, relheight=0.05, relwidth=0.07)




        self.restConnVar = IntVar()
        self.restConn = Checkbutton(bodyFrame, variable=self.restConnVar)
        self.restConn.place(relx=0.3, rely=0.58, relheight=0.06, relwidth=0.43)
        self.restConn.configure(activebackground="#d9d9d9")
        self.restConn.configure(activeforeground="#000000")
        self.restConn.configure(anchor=W)
        self.restConn.configure(background="#ffffff")
        self.restConn.configure(disabledforeground="#a3a3a3")
        self.restConn.configure(font=font18)
        self.restConn.configure(foreground="#000000")
        self.restConn.configure(highlightbackground="#ffffff")
        self.restConn.configure(highlightcolor="black")
        self.restConn.configure(justify=LEFT)
        self.restConn.configure(offrelief="sunken")
        self.restConn.configure(overrelief="groove")
        self.restConn.configure(text='''Restez Connecté''')
        self.restConn.configure(width=278)


#############################################################################

class Gestion_de_compte(Frame):

    def user(self):
        # on verifie le type de l'utilisateur
        var = self.controller.getPage(Login)
        if var.nomPharm[3] == 1:
            self.master.master.show_frame(Inscription_user)


        else:
            showinfo("Opération impossible",
                     "Vous ne pouvez pas créer de nouveau compte utilsateur !\nVeuillez vous connecter avec un compte admin pour pouvoir continuer")




    def GestionDeCompte(self):
        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()

    def notifs(self):
        if self.notif == 0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])

                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                          height=1, bg='white', anchor="w",
                          font=self.font12).grid(row=r,
                                                 column=1)
                    r = r + 1
                r = 0
                self.notif = 1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=818)
                self.supprnotifs.configure(activebackground="#009D78")
                self.supprnotifs.configure(activeforeground="#009D78")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command'] = self.supprimenotifs
            else:
                showinfo("Pas de notifications", "Vous n'avez pas de notifications !")

        else:
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif = 0

    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con = connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0

    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var = self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res:
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()

    def retour(self):
        self.master.master.show_frame(Acceuil)

    def deconnexion(self):

        if askyesno(" Deconnexion ", " Etes vous sur de déconnecter ? "):
            loginPage = self.controller.getPage(Login)
            rest = loginPage.restConnVar.get()
            if rest == 0:
                loginPage.userEntryVar.set("")
                loginPage.passEntryVar.set("")
            else:
                loginPage.passEntryVar.set("")

            self.controller.show_frame(Login)

    def ChangeMot(self):
        self.master.master.show_frame(ChangerMdp)

    def __init__(self, parent, controller=None):
        Frame.__init__(self, parent)
        self.controller = controller
        font10 = "-family {Futura Bk BT} -size 21 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        font11 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        font9 = "-family {Futura Bk BT} -size 15 -weight bold -slant " \
                "roman -underline 0 -overstrike 0"

        self.Frame1 = Frame(self)
        self.Frame1.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#ffffff")
        self.Frame1.configure(highlightbackground="#ffffff")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=935)

        self.headFrame = Frame(self.Frame1)
        self.headFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.headFrame.configure(borderwidth="2")
        self.headFrame.configure(background="#009D78")
        self.headFrame.configure(highlightbackground="#ffffff")
        self.headFrame.configure(highlightcolor="black")
        self.headFrame.configure(width=935)

        self.titleLabel = Label(self.headFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(activebackground="#f9f9f9")
        self.titleLabel.configure(activeforeground="black")
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(font=font10)
        self.titleLabel.configure(foreground="#ffffff")
        self.titleLabel.configure(highlightbackground="#ffffff")
        self.titleLabel.configure(highlightcolor="black")
        self.__img138 = PhotoImage(file="images/gc.png")
        self.titleLabel.configure(image=self.__img138)

        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0


        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        self.footFrame = Frame(self.Frame1)
        self.footFrame.place(relx=0.0, rely=0.88, relheight=0.12, relwidth=1.0)
        self.footFrame.configure(borderwidth="2")
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(highlightbackground="#ffffff")
        self.footFrame.configure(highlightcolor="black")
        self.footFrame.configure(width=935)


        self.bodyFrame = Frame(self.Frame1)
        self.bodyFrame.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1)
        self.bodyFrame.configure(relief=FLAT)
        self.bodyFrame.configure(borderwidth="2")
        self.bodyFrame.configure(relief=FLAT)
        self.bodyFrame.configure(background="#ffffff")
        self.bodyFrame.configure(highlightbackground="#ffffff")
        self.bodyFrame.configure(highlightcolor="black")
        self.bodyFrame.configure(width=745)

        self.Labelbody = Label(self.bodyFrame)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)



        self.decoButt = Button(self.bodyFrame)
        self.decoButt.place(relx=0.3, rely=0.13, height=70, width=357)
        self.decoButt.configure(activebackground="#ffffff")
        self.decoButt.configure(activeforeground="#000000")
        self.decoButt.configure(background="#ffffff")
        self.decoButt.configure(disabledforeground="#a3a3a3")
        self.decoButt.configure(font=font9)
        self.decoButt.configure(foreground="#000000")
        self.decoButt.configure(highlightbackground="#ffffff")
        self.decoButt.configure(highlightcolor="black")
        self.decoButt.configure(pady="0")
        self.decoButt.configure(relief=RIDGE)
        self.decoButt.configure(text='''Changer de mot passe''')

        self.decoButt['command'] = self.ChangeMot



        self.cmdpButt = Button(self.bodyFrame)
        self.cmdpButt.place(relx=0.3, rely=0.58, height=70, width=357)
        self.cmdpButt.configure(activebackground="#ffffff")
        self.cmdpButt.configure(activeforeground="#000000")
        self.cmdpButt.configure(background="#ffffff")
        self.cmdpButt.configure(disabledforeground="#a3a3a3")
        self.cmdpButt.configure(font=font9)
        self.cmdpButt.configure(foreground="#000000")
        self.cmdpButt.configure(highlightbackground="#ffffff")
        self.cmdpButt.configure(highlightcolor="black")
        self.cmdpButt.configure(pady="0")
        self.cmdpButt.configure(relief=RIDGE)
        self.cmdpButt.configure(text='''Deconnexion''')
        self.cmdpButt.config(command= self.deconnexion)

        self.uButt = Button(self.bodyFrame)
        self.uButt.place(relx=0.3, rely=0.36, height=70, width=357)
        self.uButt.configure(activebackground="#ffffff")
        self.uButt.configure(activeforeground="#000000")
        self.uButt.configure(background="#ffffff")
        self.uButt.configure(disabledforeground="#a3a3a3")
        self.uButt.configure(font=font9)
        self.uButt.configure(foreground="#000000")
        self.uButt.configure(highlightbackground="#ffffff")
        self.uButt.configure(highlightcolor="black")
        self.uButt.configure(pady="0")
        self.uButt.configure(relief=RIDGE)
        self.uButt.configure(text='''Créer un compte utilisateur ''')
        self.uButt.config(command=self.user)



        self.retourButt = Button(self.bodyFrame)
        self.retourButt.place(relx=0.4, rely=0.86, height=40, width=180)
        self.retourButt.configure(activebackground="#d9d9d9")
        self.retourButt.configure(font=font9)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')
        self.retourButt.configure(width=100)
        self.retourButt.config(command= self.retour)

        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img900 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img900)


#############################################################################################
#############################################################################################

class ChangerMdp(Frame):
    # ' pour les notifications'
    def GestionDeCompte(self):
        try:
            self.retour2()
        except:
            pass
        try:
            self.retour2()
        except:
            pass
        try:
            self.retour_perime()
        except:
            pass
        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()

    def notifs(self):
        if self.notif == 0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])

                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                          height=1, bg='white', anchor="w",
                          font=self.font12).grid(row=r,
                                                 column=1)
                    r = r + 1
                r = 0
                self.notif = 1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=750)
                self.supprnotifs.configure(activebackground="#009D78")
                self.supprnotifs.configure(activeforeground="#009D78")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command'] = self.supprimenotifs
            else:
                showinfo("Pas de notifications", "Vous n'avez pas de notifications !")

        else:
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif = 0

    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con = connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0

    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var = self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res:
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()

    def submit(self):
        ancien=self.EntryAncienVar.get()
        confirm=self.confEntryVar.get()
        new=self.newEntryVar.get()

        loginPage=self.controller.getPage(Login)
        userName=loginPage.userEntryVar.get()



        con=connectBdd()
        cur=con.cur
        if(con.authentification(userName,ancien)!=0):
            if(new==confirm):
                self.msgLabel.config(text="")
                conf=askyesno(" Confimation "," Etes vous sur de valider votre choix ? ")
                if(conf):
                    passHash=hash.md5(new.encode()).hexdigest()
                    userNameHash=hash.md5(userName.encode()).hexdigest()
                    cur.execute(''' UPDATE comptes SET pass=%s WHERE id=%s;''',(passHash,userNameHash))
                    con.conn.commit()
            else:
                self.msgLabel.config(text=" Le nouveau mot de passe ne correspand pas a sa confirmation !")
        else:
            self.msgLabel.config(text=" Le mot de passe est incorrecte !!")

        con.fermer()

    def retour(self):

        self.EntryAncienVar.set("")
        self.confEntryVar.set("")
        self.newEntryVar.set("")
        self.msgLabel.config(text="")

        self.controller.show_frame(Gestion_de_compte)


    def __init__(self,parent,controller=None):
        Frame.__init__(self, parent)

        self.controller = controller

        font10 = "-family {Futura Bk BT} -size 12 -weight bold "  \
            "-slant roman -underline 0 -overstrike 0"
        font11 = "-family {Futura Bk BT} -size 20 -weight bold "  \
            "-slant roman -underline 0 -overstrike 0"
        font9 = "-family {Futura Bk BT} -size 11 -weight bold -slant"  \
            " roman -underline 0 -overstrike 0"

        self.Frame1 = Frame(self)
        self.Frame1.place(relx=0.0, rely=0.0, relheight=1, relwidth=1)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#ffffff")
        self.Frame1.configure(highlightbackground="#ffffff")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=935)

        self.FrameHaut = Frame(self.Frame1)
        self.FrameHaut.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.FrameHaut.configure(borderwidth="2")
        self.FrameHaut.configure(background="#009D78")
        self.FrameHaut.configure(highlightbackground="#ffffff")
        self.FrameHaut.configure(highlightcolor="black")
        self.FrameHaut.configure(width=935)

        self.titleLabel = Label(self.FrameHaut)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(activebackground="#336464")
        self.titleLabel.configure(activeforeground="white")
        self.titleLabel.configure(activeforeground="black")
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(font=font11)
        self.titleLabel.configure(foreground="#ffffff")
        self.titleLabel.configure(highlightbackground="#ffffff")
        self.titleLabel.configure(highlightcolor="black")
        self._img6 = PhotoImage(file="images/changermpd.png")
        self.titleLabel.configure(image=self._img6)

        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img1 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img1)

        self.bodyFrame = Frame(self.Frame1)
        self.bodyFrame.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1)
        self.bodyFrame.configure(relief=FLAT)
        self.bodyFrame.configure(borderwidth="2")
        self.bodyFrame.configure(relief=FLAT)
        self.bodyFrame.configure(background="#ffffff")
        self.bodyFrame.configure(highlightbackground="#ffffff")
        self.bodyFrame.configure(highlightcolor="black")
        self.bodyFrame.configure(width=755)

        self.Labelbody = Label(self.bodyFrame)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)

        self.confLabel = Label(self.bodyFrame)
        self.confLabel.place(relx=0.22, rely=0.54, height=34, width=246)
        self.confLabel.configure(activebackground="#f9f9f9")
        self.confLabel.configure(activeforeground="black")
        self.confLabel.configure(background="#ffffff")
        self.confLabel.configure(disabledforeground="#a3a3a3")
        self.confLabel.configure(font=font10)
        self.confLabel.configure(foreground="#000000")
        self.confLabel.configure(highlightbackground="#ffffff")
        self.confLabel.configure(highlightcolor="black")
        self.confLabel.configure(anchor=W)
        self.confLabel.configure(text='''Confirmer Nouveau :''')

        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0

        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        self.newLabel = Label(self.bodyFrame)
        self.newLabel.place(relx=0.22, rely=0.39, height=34, width=246)
        self.newLabel.configure(activebackground="#f9f9f9")
        self.newLabel.configure(activeforeground="black")
        self.newLabel.configure(background="#ffffff")
        self.newLabel.configure(disabledforeground="#a3a3a3")
        self.newLabel.configure(font=font10)
        self.newLabel.configure(foreground="#000000")
        self.newLabel.configure(highlightbackground="#ffffff")
        self.newLabel.configure(highlightcolor="black")
        self.newLabel.configure(anchor=W)
        self.newLabel.configure(text='''Nouveau mot de passe :''')

        self.ancienLabel = Label(self.bodyFrame)
        self.ancienLabel.place(relx=0.22, rely=0.24, height=34, width=246)
        self.ancienLabel.configure(activebackground="#f9f9f9")
        self.ancienLabel.configure(activeforeground="#000000")
        self.ancienLabel.configure(background="#ffffff")
        self.ancienLabel.configure(disabledforeground="#a3a3a3")
        self.ancienLabel.configure(font=font10)
        self.ancienLabel.configure(foreground="#000000")
        self.ancienLabel.configure(highlightbackground="#ffffff")
        self.ancienLabel.configure(highlightcolor="#000000")
        self.ancienLabel.configure(text='''Ancien mot de passe :''')
        self.ancienLabel.configure(anchor=W)

        self.EntryAncienVar = StringVar()
        self.EntryAncien = Entry(self.bodyFrame, show='\u2022', textvariable=self.EntryAncienVar)
        self.EntryAncien.place(relx=0.45, rely=0.24, relheight=0.06
                               , relwidth=0.38)
        self.EntryAncien.configure(background="#ffffff")
        self.EntryAncien.configure(disabledforeground="#a3a3a3")
        self.EntryAncien.configure(font="TkFixedFont")
        self.EntryAncien.configure(foreground="#000000")
        self.EntryAncien.configure(highlightbackground="#ffffff")
        self.EntryAncien.configure(highlightcolor="black")
        self.EntryAncien.configure(insertbackground="black")
        self.EntryAncien.configure(selectbackground="#c4c4c4")
        self.EntryAncien.configure(selectforeground="black")

        self.newEntryVar = StringVar()
        self.newEntry = Entry(self.bodyFrame, show='\u2022', textvariable=self.newEntryVar)
        self.newEntry.place(relx=0.45, rely=0.39, relheight=0.06, relwidth=0.38)
        self.newEntry.configure(background="#ffffff")
        self.newEntry.configure(disabledforeground="#a3a3a3")
        self.newEntry.configure(font="TkFixedFont")
        self.newEntry.configure(foreground="#000000")
        self.newEntry.configure(highlightbackground="#ffffff")
        self.newEntry.configure(highlightcolor="black")
        self.newEntry.configure(insertbackground="black")
        self.newEntry.configure(selectbackground="#c4c4c4")
        self.newEntry.configure(selectforeground="black")

        self.confEntryVar = StringVar()
        self.confEntry = Entry(self.bodyFrame, show='\u2022', textvariable=self.confEntryVar)
        self.confEntry.place(relx=0.45, rely=0.54, relheight=0.06, relwidth=0.38)

        self.confEntry.configure(background="#ffffff")
        self.confEntry.configure(disabledforeground="#a3a3a3")
        self.confEntry.configure(font="TkFixedFont")
        self.confEntry.configure(foreground="#000000")
        self.confEntry.configure(highlightbackground="#ffffff")
        self.confEntry.configure(highlightcolor="black")
        self.confEntry.configure(insertbackground="black")
        self.confEntry.configure(selectbackground="#c4c4c4")
        self.confEntry.configure(selectforeground="black")



        self.BtnConf = Button(self.bodyFrame)
        self.BtnConf.place(relx=0.64, rely=0.86, height=40, width=180)
        self.BtnConf.configure(activeforeground="#000000")
        self.BtnConf.configure(background="#ffffff")
        self.BtnConf.configure(disabledforeground="#a3a3a3")
        self.BtnConf.configure(font=font9)
        self.BtnConf.configure(foreground="#000000")
        self.BtnConf.configure(highlightbackground="#ffffff")
        self.BtnConf.configure(highlightcolor="black")
        self.BtnConf.configure(pady="0")
        self.BtnConf.configure(relief=RIDGE)
        self.BtnConf.configure(text='''Confirmer''')
        self.BtnConf.config(command = self.submit)


        self.AnnulButt = Button(self.bodyFrame)
        self.AnnulButt.place(relx=0.17, rely=0.86, height=40, width=180)
        self.AnnulButt.configure(font=font10)
        self.AnnulButt.configure(activeforeground="#000000")
        self.AnnulButt.configure(background="#ffffff")
        self.AnnulButt.configure(disabledforeground="#a3a3a3")
        self.AnnulButt.configure(foreground="#000000")
        self.AnnulButt.configure(highlightbackground="#ffffff")
        self.AnnulButt.configure(highlightcolor="black")
        self.AnnulButt.configure(pady="0")
        self.AnnulButt.configure(relief=RIDGE)
        self.AnnulButt.configure(text='''Annuler''')
        self.AnnulButt.configure(pady="0")
        self.AnnulButt.config(command = self.retour)


       	############################### Afffiche Message #####################
        self.msgLabel = Label(self.bodyFrame)
        self.msgLabel.place(relx=0.25, rely=0.6, height=41, width=500)
        self.msgLabel.configure(font=font10)
        self.msgLabel.configure(justify=LEFT)
        self.msgLabel.config(background="#ffffff",foreground='red')






class ScrollableCanvas3(Frame):
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        canvas = Canvas(self, bg='#FFFFFF', width=700, height=400, scrollregion=(0, 0, 500, 500))

        vbar = Scrollbar(self, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=canvas.yview)
        canvas.config(width=845, height=395)
        canvas.config(yscrollcommand=vbar.set)
        canvas.pack(side=RIGHT, expand=True, fill=BOTH)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)


class ScrollableCanvas4(Frame):
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        canvas = Canvas(self, bg='#FFFFFF', width=900, height=200)

        canvas.config(width=900, height=160)

        canvas.pack(side=RIGHT, expand=True, fill=BOTH)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)



###################################################################################################################################################################

class ScrollableCanvas(Frame):
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        canvas = Canvas(self, bg='#FFFFFF', width=700, height=400, scrollregion=(0, 0, 500, 500))

        vbar = Scrollbar(self, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=canvas.yview)
        canvas.config(width=850, height=370,background='#ffffff')
        canvas.config(yscrollcommand=vbar.set)
        canvas.pack(side=RIGHT, expand=True, fill=BOTH)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)


############################################################################################################################################"
###############################################################################################

class Retrait(Frame):
    font11 = "-family {Futura Bk BT} -size 20 -weight bold -slant " \
             "roman -underline 0 -overstrike 0"
    font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
             "roman -underline 0 -overstrike 0"

    def updateDosage(self, *args):

        if self.bienCheckVar.get():
            self.dosageVar = self.dosageEntryVar.get()
            self.dosageEntry.config(state="readonly")
            self.dosageEntryVar.set("")
        else:
            self.dosageEntry.config(state="normal")
            self.dosageEntryVar.set(self.dosageVar)

    def retour(self):
        self.dosageEntryVar.set("")
        self.nmpEntryVar.set("")
        self.formeEntryVar.set("")
        self.master.master.show_frame(gestionStock)

    def submit(self):

        # on verifie d'abord si les entreees sont rempliees
        error=0
        if (self.nmpEntry.get()=="" or self.formeEntry.get()=="" or self.dosageEntry.get()=="" ):
            error=1
            showerror("Erreur", "Vous devez remplir tous les champs !")


        if error==0:
            con = connectBdd()
            # on recupere le code de la pharmacie courante
            acc = self.controller.getPage(Login)
            cPh = acc.nomPharm[2]

            exist = con.retrait(nom=self.nmpEntry.get(), forme=self.formeEntry.get()
                                , numlot=self.dosageEntry.get(),cPh=cPh)
            if exist:
                showinfo("Retrait avec succes", "Ce lot a été retiré du stock")
                self.master.master.show_frame(gestionStock)

            else:
                showinfo("Echec", "Ce lot n'est pas disponible dans le stock")

            con.fermer()
        self.dosageEntryVar.set("")
        self.nmpEntryVar.set("")
        self.formeEntryVar.set("")

    def GestionDeCompte(self):
        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()

    def notifs(self):
        if self.notif == 0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])

                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                          height=1, bg='white', anchor="w",
                          font=self.font12).grid(row=r,
                                                 column=1)
                    r = r + 1
                r = 0
                self.notif = 1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=818)
                self.supprnotifs.configure(activebackground="#009D78")
                self.supprnotifs.configure(activeforeground="#009D78")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command'] = self.supprimenotifs
            else:
                showinfo("Pas de notifications", "Vous n'avez pas de notifications !")

        else:
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif = 0

    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con = connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0

    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var = self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res:
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller

        font11 = "-family {Futura Bk BT} -size 20 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        headFrame = Frame(self)
        headFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        headFrame.configure(relief=FLAT)
        headFrame.configure(borderwidth="2")
        headFrame.configure(relief=FLAT)
        headFrame.configure(background="#009D78")
        headFrame.configure(width=950)

        titleLabel = Label(headFrame)
        titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        titleLabel.configure(background="#009D78")
        titleLabel.configure(disabledforeground="#a3a3a3")
        titleLabel.configure(font=font11)
        titleLabel.configure(foreground="#fafafa")
        titleLabel.configure(text='''Recherche D'un Produit''')
        titleLabel.configure(width=462)
        self._img88 = PhotoImage(file="images/retlot.png")
        titleLabel.configure(image=self._img88)
        self.titleLabel=titleLabel

        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0


        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img1 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img1)

        bodyFrame = Frame(self)
        bodyFrame.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1)

        bodyFrame.configure(relief=FLAT)
        bodyFrame.configure(borderwidth="0")
        bodyFrame.configure(relief=FLAT)
        bodyFrame.configure(background="#ffffff")
        bodyFrame.configure(width=7935)

        self.Labelbody = Label(bodyFrame)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)

        nmpLabel = Label(bodyFrame)
        nmpLabel.place(relx=0.22, rely=0.14, height=35, width=174)
        nmpLabel.configure(anchor=W)
        nmpLabel.configure(background="#ffffff")
        nmpLabel.configure(disabledforeground="#fafafa")
        nmpLabel.configure(font=font12)
        nmpLabel.configure(foreground="#000000")
        nmpLabel.configure(text='''Nom Du Produit :''')
        nmpLabel.configure(width=202)

        # on genere la liste des produits existants:
        self.liste_produits = []
        var = connectBdd()
        cur = var.cur
        cur.execute("""SELECT nomProduit FROM produits""")
        resultat1 = cur.fetchall()

        for inter in resultat1:
            for inter2 in inter:
                var = inter2.lower().capitalize()
                self.liste_produits.append(var)

        self.liste_produits = sorted(self.liste_produits)
        # on supprime les doublants dans cette liste:
        self.inter = ""
        self.liste_products = []
        for produit in self.liste_produits:
            if produit != self.inter:
                self.liste_products.append(produit)
                self.inter = produit

        self.bodyFrame=bodyFrame
        self.nmpEntryVar = StringVar()
        self.nmpEntry = Combobox(self.bodyFrame, textvariable=self.nmpEntryVar, values=self.liste_products,
                                 state="readonly")
        self.nmpEntry.place(relx=0.45, rely=0.15, relheight=0.06
                            , relwidth=0.38)
        self.nmpEntry.configure(background="#ffffff")


        dosageLabel = Label(bodyFrame)
        dosageLabel.place(relx=0.22, rely=0.33, height=35, width=174)
        dosageLabel.configure(activebackground="#fafafa")
        dosageLabel.configure(activeforeground="black")
        dosageLabel.configure(anchor=W)
        dosageLabel.configure(background="#ffffff")
        dosageLabel.configure(disabledforeground="#a3a3a3")
        dosageLabel.configure(font=font12)
        dosageLabel.configure(foreground="#000000")
        dosageLabel.configure(highlightbackground="#ffffff")
        dosageLabel.configure(highlightcolor="black")
        dosageLabel.configure(text='''Numéro de Lot  :''')
        dosageLabel.configure(width=112)

        self.dosageEntryVar = StringVar()
        self.dosageEntry = Entry(bodyFrame, textvariable=self.dosageEntryVar)
        self.dosageEntry.place(relx=0.45, rely=0.33, relheight=0.06
                               , relwidth=0.38)
        self.dosageEntry.configure(background="#ffffff")
        self.dosageEntry.configure(disabledforeground="#a3a3a3")
        self.dosageEntry.configure(font=font12)
        self.dosageEntry.configure(borderwidth='1')
        self.dosageEntry.configure(foreground="#000000")
        self.dosageEntry.configure(highlightbackground="#ffffff")
        self.dosageEntry.configure(highlightcolor="black")
        self.dosageEntry.configure(insertbackground="black")
        self.dosageEntry.configure(selectbackground="#c4c4c4")
        self.dosageEntry.configure(selectforeground="black")

        self.formeLabel = Label(bodyFrame)
        self.formeLabel.place(relx=0.22, rely=0.51, height=35, width=174)
        self.formeLabel.configure(activebackground="#f9f9f9")
        self.formeLabel.configure(activeforeground="black")
        self.formeLabel.configure(anchor=W)
        self.formeLabel.configure(background="#ffffff")
        self.formeLabel.configure(disabledforeground="#a3a3a3")
        self.formeLabel.configure(font=font12)
        self.formeLabel.configure(foreground="#000000")
        self.formeLabel.configure(highlightbackground="#ffffff")
        self.formeLabel.configure(highlightcolor="black")
        self.formeLabel.configure(text='''Forme   :''')

        self.formeEntryVar = StringVar()
        con = connectBdd()
        con.cur.execute("SELECT forme from produits ")
        e = con.cur.fetchall()
        self.liste_formes = []
        k = []
        for m in e:
            k.append(m[0])

        k = set(k)
        for i in k:
            self.liste_formes.append(i)

        con.fermer()
        # self.liste_formes = (
        # 'Comprime', 'Suppositoire', 'Sirop', 'Solution buvable', 'Gelule', 'Solution injectable', 'ComprimeEfferv',
        # 'Poudre', 'Liquide', 'Pommade', 'Gel', 'Sachet', 'Capsule', 'Goute', 'Ampoule', '')

        self.liste_formes = sorted(self.liste_formes)
        self.formeEntry = Combobox(self.bodyFrame, textvariable=self.formeEntryVar, values=self.liste_formes,
                                  state="readonly")

        self.formeEntry.place(relx=0.45, rely=0.51, relheight=0.06, relwidth=0.38)
        self.formeEntry.configure(background="#ffffff")






        self.rechButt = Button(self.bodyFrame)
        self.rechButt.place(relx=0.64, rely=0.86, height=40, width=180)

        self.rechButt.configure(activebackground="#d9d9d9")
        self.rechButt.configure(activeforeground="#000000")
        self.rechButt.configure(background="#ffffff")
        self.rechButt.configure(borderwidth="2")
        self.rechButt.configure(disabledforeground="#a3a3a3")
        self.rechButt.configure(font=font12)
        self.rechButt.configure(foreground="#000000")
        self.rechButt.configure(highlightbackground="#ffffff")
        self.rechButt.configure(highlightcolor="black")
        self.rechButt.configure(pady="0")
        self.rechButt.configure(relief=RIDGE)
        self.rechButt.configure(text='''Retirer''')
        self.rechButt.config(command= self.submit)



        self.retourButt = Button(self.bodyFrame)
        self.retourButt.place(relx=0.17, rely=0.86, height=40, width=180)
        self.retourButt.configure(activebackground="#d9d9d9")
        self.retourButt.configure(font=font12)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')
        self.retourButt.configure(pady="0")
        self.retourButt.config(command = self.retour)


#################################################################################################
##################################Inscription######################################################
class Inscription(Frame):
    def localisation(self):
        res=[]
        try:
            res = json.loads(urlopen('http://freegeoip.net/json').read().decode())
            self.adrEntryVarA.set(res['longitude'])
            self.latEntryVarA.set(res['latitude'])


        except:
            showerror("Erreur!","Pas de connexion internet !")
        return res
            ############################################################
    def submit(self):
        # vérifions le types des  entrees
        error=0
        tel = 0
        coord = 0
        n=0
 ####################### type du numero de telephone###############################################
        for e in self.telEntryVarA.get():
             try:
                 tel = int(e)

             except:
                 showerror("Erreur!","Le numéro de téléphone est invalide")
                 error=1
                 break
             n += 1
        if n !=10 :
            error=1
            showerror("Erreur!", "Le numéro de téléphone est invalide")
##################################type des coordonnées###############################################
        try:
            coordl=0
            coord1 = float (self.adrEntryVarA.get())

        except:
            if self.adrEntryVarA.get() == "Longitude":
                print("")
            else :
                showerror("Erreur!", "Les coordonnées introduites sont invalide !")
                self.adrEntryVarA.set(0.0)
            error = 1

######################################################################################################
        try:
            coord2 = float (self.latEntryVarA.get())

        except:
            if self.latEntryVarA.get() == "Lattitude" :

                error = 1


            else :
              showerror("Erreur!", "Les coordonnées introduites sont invalide !")
              self.latEntryVarA.set(0.0)


        # type du nom
        try:
            name = int(self.pharEntryVarA.get())
            showerror("Erreur!", "Le nom de la pharmacie doit être une chaine de caractères!")
            self.pharEntryVarA.set("")
            error =1


        except:
            pass
        # type du nom d'utilisateur
        try:
            name = int(self.userEntryVarA.get())
            showerror("Erreur!", "La nom d'utilisateur doit être une chaine de caractères!")
            self.userEntryVarA.set("")
            error =1


        except:
            pass

########################"# verification si les entrees ne sont pas vide#############################################

        if (self.userEntryVarA.get() == "" or self.pharEntryVarA.get() == "" or self.telEntryVarA.get() == 0 or
                  self.adrEntryVarA.get() == 0.0  or self.mdpEntryVarA == "" or self.confEntryVarA.get() ==""
                or  self.adrEntryVarA.get() == "Longitude" or self.latEntryVarA =="Lattitude" or self.codeEntryVarA ==""or
                self.adresEntryVarA==""):
            error =1
            showerror("Erreur!", "Vous devez remplir tous les champs du formulaire!")

#############################Verification de la validité syntaxique de l'adresse mail#######################
        con = connectBdd()
        exist = con.verifMail(self.mailEntryVarA.get())
        if exist:
            print("")
        else:
            error =1
            if self.mailEntryVarA.get() == "":
                print("")
            else:
               showerror("Attention!", "L'adresse mail introduite est non valide")
               self.mailEntryVarA.set("")
        ##############type du code de la pharmacie ##############################################"
        try:
            name = int(self.codeEntryVarA.get())
            showerror("Erreur!", "Le code de la pharmacie doit être une chaine de caractères!")
            self.codeEntryVarA.set("")
            error = 1


        except:
            pass

        ############################################################################################
        mdp = self.mdpEntryVarA.get()
        conf = self.confEntryVarA.get()
        if conf  != mdp :
            showerror("Erreur !","Le mot de passe ne correspond pas à sa confimation")
            self.confEntryVarA.set("")
            error =1



       ############################Type de l'adresse###############################################
        try:
            name = int(self.adresEntryVarA.get())
            showerror("Erreur!", "Le code de la pharmacie doit être une chaine de caractères!")
            self.adresEntryVarA.set("")
            error = 1


        except:
            pass
        ##################################Traitement#############################################################

            # l'unicite de l'identifiant :
            con = connectBdd()

            userNameHash = hash.md5(self.userEntryVarA.get().encode()).hexdigest()
            con.cur.execute("SELECT id from comptes where id=%s;", userNameHash)
            ii = con.cur.fetchall()
            if ii:
                error = 1
                showerror("Erreur", "Cet identifiant existe déja !")

        if error ==0 :
            #on fait le traiteent


            con.Admin(tel=self.telEntryVarA.get(),mail=self.mailEntryVarA.get(),adres=self.adresEntryVarA.get(),
                      long=float(self.adrEntryVarA.get()),lat=float(self.latEntryVarA.get()),
                      Nphar=self.pharEntryVarA.get(),
                      Cphar=self.codeEntryVarA.get(),user=self.userEntryVarA.get(),mdp=self.mdpEntryVarA.get())
            var = self.controller.getPage(Login)
            var.userEntryVar.set(self.userEntryVarA.get())
            var.passEntryVar.set(self.mdpEntryVarA.get())
            self.controller.show_frame(Login)
        con.fermer()


    def retour(self):
        self.telEntryVarA.set('')
        self.mailEntryVarA.set('')
        self.adresEntryVarA.set('')
        self.adrEntryVarA.set('Longitude')
        self.latEntryVarA.set('Latitude')
        self.pharEntryVarA.set('')
        self.codeEntryVarA.set('')
        self.userEntryVarA.set('')
        self.mdpEntryVarA.set('')
        self.confEntryVarA.set('')

        self.master.master.show_frame(Inscription_choix)

    def __init__(self,parent,controller=None):

        Frame.__init__(self, parent)

        self.controller = controller

        font9 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                "roman -underline 0 -overstrike 0"

        self.hautFrame = Frame(self)
        self.hautFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.hautFrame.configure(borderwidth="0")
        self.hautFrame.configure(background="#ffffff")
        self.hautFrame.configure(width=945)

        self.titleLabel = Label(self.hautFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(background="#ffffff")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(foreground="#000000")
        self._img199 = PhotoImage(file="images/vide.png")
        self.titleLabel.configure(image=self._img199)
        self.titleLabel.configure(width=934)




        self.bodyFrame = Frame(self)
        self.bodyFrame.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1)
        self.bodyFrame.configure(borderwidth="2")
        self.bodyFrame.configure(background="#ffffff")
        self.bodyFrame.configure(width=685)

        self.Labelbody = Label(self.bodyFrame)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)
        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img900 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img900)

        self.pharEntryVarA =StringVar()
        self.pharEntry = Entry(self.bodyFrame,textvariable=self.pharEntryVarA)
        self.pharEntry.place(relx=0.45, rely=0.06, relheight=0.06, relwidth=0.38)

        self.pharEntry.configure(background="white")
        self.pharEntry.configure(disabledforeground="#a3a3a3")
        self.pharEntry.configure(font="TkFixedFont")
        self.pharEntry.configure(foreground="#000000")
        self.pharEntry.configure(insertbackground="black")
        self.pharEntry.configure(width=264)

        self.adrEntryVarA = StringVar()
        self.adrEntryVarA.set("Longitude")
        self.adrEntry = Entry(self.bodyFrame,textvariable=self.adrEntryVarA)
        self.adrEntry.place(relx=0.45, rely=0.15, relheight=0.06, relwidth=0.15)
        self.adrEntry.configure(background="white")
        self.adrEntry.configure(disabledforeground="#a3a3a3")
        self.adrEntry.configure(font="TkFixedFont")
        self.adrEntry.configure(foreground="#000000")
        self.adrEntry.configure(insertbackground="black")
        self.adrEntry.configure(width=164)

        self.latEntryVarA = StringVar()
        self.latEntryVarA.set("Latitude")
        self.latEntry = Entry(self.bodyFrame, textvariable=self.latEntryVarA)
        self.latEntry.place(relx=0.62, rely=0.15, relheight=0.06, relwidth=0.15)
        self.latEntry.configure(background="white")
        self.latEntry.configure(disabledforeground="#a3a3a3")
        self.latEntry.configure(font="TkFixedFont")
        self.latEntry.configure(foreground="#000000")
        self.latEntry.configure(insertbackground="black")
        self.latEntry.configure(width=164)

        self.autoBtn = Button(self.bodyFrame)
        self.autoBtn.place(relx=0.79, rely=0.15, relheight=0.06, width=108)
        self.autoBtn.configure(activebackground="#ffffff")
        self.autoBtn.configure(activeforeground="#000000")
        self.autoBtn.configure(background="#ffffff")
        self.autoBtn.configure(font=font9)
        self.autoBtn.configure(disabledforeground="#a3a3a3")
        self.autoBtn.configure(foreground="#000000")
        self.autoBtn.configure(highlightbackground="#ffffff")
        self.autoBtn.configure(highlightcolor="black")
        self.autoBtn.configure(pady="0")
        self.autoBtn.configure(relief=RIDGE)
        self.autoBtn.configure(text='''Automatique''')
        self.autoBtn.config(command = self.localisation)

        self.telEntryVarA =StringVar()
        self.telEntry = Entry(self.bodyFrame,textvariable=self.telEntryVarA)
        self.telEntry.place(relx=0.45, rely=0.24, relheight=0.06, relwidth=0.39)
        self.telEntry.configure(background="white")
        self.telEntry.configure(disabledforeground="#a3a3a3")
        self.telEntry.configure(font="TkFixedFont")
        self.telEntry.configure(foreground="#000000")
        self.telEntry.configure(highlightbackground="#ffffff")
        self.telEntry.configure(highlightcolor="black")
        self.telEntry.configure(insertbackground="black")
        self.telEntry.configure(selectbackground="#c4c4c4")
        self.telEntry.configure(selectforeground="black")

        self.mailEntryVarA =StringVar()
        self.mailEntry = Entry(self.bodyFrame,textvariable = self.mailEntryVarA)
        self.mailEntry.place(relx=0.45, rely=0.33, relheight=0.06, relwidth=0.39)

        self.mailEntry.configure(background="white")
        self.mailEntry.configure(disabledforeground="#a3a3a3")
        self.mailEntry.configure(font="TkFixedFont")
        self.mailEntry.configure(foreground="#000000")
        self.mailEntry.configure(highlightbackground="#ffffff")
        self.mailEntry.configure(highlightcolor="black")
        self.mailEntry.configure(insertbackground="black")
        self.mailEntry.configure(selectbackground="#c4c4c4")
        self.mailEntry.configure(selectforeground="black")

        self.userEntryVarA =StringVar()
        self.userEntry = Entry(self.bodyFrame,textvariable=self.userEntryVarA)
        self.userEntry.place(relx=0.45, rely=0.42, relheight=0.06, relwidth=0.39)

        self.userEntry.configure(background="white")
        self.userEntry.configure(disabledforeground="#a3a3a3")
        self.userEntry.configure(font="TkFixedFont")
        self.userEntry.configure(foreground="#000000")
        self.userEntry.configure(highlightbackground="#ffffff")
        self.userEntry.configure(highlightcolor="black")
        self.userEntry.configure(insertbackground="black")
        self.userEntry.configure(selectbackground="#c4c4c4")
        self.userEntry.configure(selectforeground="black")

        self.mdpEntryVarA = StringVar()
        self.mdpEntry = Entry(self.bodyFrame,show ='\u2022',textvariable=self.mdpEntryVarA)
        self.mdpEntry.place(relx=0.45, rely=0.51, relheight=0.06, relwidth=0.39)
        self.mdpEntry.configure(background="white")
        self.mdpEntry.configure(disabledforeground="#a3a3a3")
        self.mdpEntry.configure(font="TkFixedFont")
        self.mdpEntry.configure(foreground="#000000")
        self.mdpEntry.configure(highlightbackground="#ffffff")
        self.mdpEntry.configure(highlightcolor="black")
        self.mdpEntry.configure(insertbackground="black")
        self.mdpEntry.configure(selectbackground="#c4c4c4")
        self.mdpEntry.configure(selectforeground="black")

        self.confEntryVarA = StringVar()
        self.confEntry = Entry(self.bodyFrame,show ='\u2022',textvariable=self.confEntryVarA)
        self.confEntry.place(relx=0.45, rely=0.6, relheight=0.06, relwidth=0.39)

        self.confEntry.configure(background="white")
        self.confEntry.configure(disabledforeground="#a3a3a3")
        self.confEntry.configure(font="TkFixedFont")
        self.confEntry.configure(foreground="#000000")
        self.confEntry.configure(highlightbackground="#ffffff")
        self.confEntry.configure(highlightcolor="black")
        self.confEntry.configure(insertbackground="black")
        self.confEntry.configure(selectbackground="#c4c4c4")
        self.confEntry.configure(selectforeground="black")

        self.nomPhar = Label(self.bodyFrame)
        self.nomPhar.place(relx=0.18, rely=0.06, height=30, width=246)
        self.nomPhar.configure(background="#ffffff")
        self.nomPhar.configure(disabledforeground="#a3a3a3")
        self.nomPhar.configure(font=font9)
        self.nomPhar.configure(foreground="#000000")
        self.nomPhar.configure(anchor=W)
        self.nomPhar.configure(text='''Nom de la pharmacie :''')

        self.adrLabel = Label(self.bodyFrame)
        self.adrLabel.place(relx=0.18, rely=0.15, height=30, width=246)
        self.adrLabel.configure(activebackground="#f9f9f9")
        self.adrLabel.configure(activeforeground="black")
        self.adrLabel.configure(background="#ffffff")
        self.adrLabel.configure(disabledforeground="#a3a3a3")
        self.adrLabel.configure(font=font9)
        self.adrLabel.configure(foreground="#000000")
        self.adrLabel.configure(highlightbackground="#ffffff")
        self.adrLabel.configure(highlightcolor="black")
        self.adrLabel.configure(anchor=W)
        self.adrLabel.configure(text='''Coordonnées géographiques :''')

        self.telLabel = Label(self.bodyFrame)
        self.telLabel.place(relx=0.18, rely=0.24, height=30, width=246)
        self.telLabel.configure(activebackground="#f9f9f9")
        self.telLabel.configure(activeforeground="black")
        self.telLabel.configure(background="#ffffff")
        self.telLabel.configure(disabledforeground="#a3a3a3")
        self.telLabel.configure(font=font9)
        self.telLabel.configure(foreground="#000000")
        self.telLabel.configure(highlightbackground="#ffffff")
        self.telLabel.configure(highlightcolor="black")
        self.telLabel.configure(text='''N°Téléphone :''')
        self.telLabel.configure(anchor=W)

        self.mailLabel = Label(self.bodyFrame)
        self.mailLabel.place(relx=0.18,rely=0.33, height=30, width=246)
        self.mailLabel.configure(activebackground="#f9f9f9")
        self.mailLabel.configure(activeforeground="black")
        self.mailLabel.configure(background="#ffffff")
        self.mailLabel.configure(disabledforeground="#a3a3a3")
        self.mailLabel.configure(font=font9)
        self.mailLabel.configure(foreground="#000000")
        self.mailLabel.configure(highlightbackground="#ffffff")
        self.mailLabel.configure(highlightcolor="black")
        self.mailLabel.configure(text='''Adresse E-mail :''')
        self.mailLabel.configure(anchor=W)

        self.userLabel = Label(self.bodyFrame)
        self.userLabel.place(relx=0.18, rely=0.42, height=30, width=246)
        self.userLabel.configure(activebackground="#f9f9f9")
        self.userLabel.configure(activeforeground="black")
        self.userLabel.configure(background="#ffffff")
        self.userLabel.configure(disabledforeground="#a3a3a3")
        self.userLabel.configure(font=font9)
        self.userLabel.configure(foreground="#000000")
        self.userLabel.configure(highlightbackground="#ffffff")
        self.userLabel.configure(highlightcolor="black")
        self.userLabel.configure(text='''Nom d'utilisateur :''')
        self.userLabel.configure(anchor=W)

        self.mdpLabel = Label(self.bodyFrame)
        self.mdpLabel.place(relx=0.18, rely=0.51, height=30, width=246)
        self.mdpLabel.configure(activebackground="#f9f9f9")
        self.mdpLabel.configure(activeforeground="black")
        self.mdpLabel.configure(background="#ffffff")
        self.mdpLabel.configure(disabledforeground="#a3a3a3")
        self.mdpLabel.configure(font=font9)
        self.mdpLabel.configure(foreground="#000000")
        self.mdpLabel.configure(highlightbackground="#ffffff")
        self.mdpLabel.configure(highlightcolor="black")
        self.mdpLabel.configure(text='''Mot de passe :''')
        self.mdpLabel.configure(anchor=W)

        self.confLabel = Label(self.bodyFrame)
        self.confLabel.place(relx=0.18, rely=0.6, height=30, width=246)
        self.confLabel.configure(activebackground="#f9f9f9")
        self.confLabel.configure(activeforeground="black")
        self.confLabel.configure(background="#ffffff")
        self.confLabel.configure(disabledforeground="#a3a3a3")
        self.confLabel.configure(font=font9)
        self.confLabel.configure(foreground="#000000")
        self.confLabel.configure(highlightbackground="#ffffff")
        self.confLabel.configure(highlightcolor="black")
        self.confLabel.configure(text='''Confirmer mot de passe :''')
        self.confLabel.configure(anchor=W)

        self.codeLabel = Label(self.bodyFrame)
        self.codeLabel.place(relx=0.18, rely=0.69, height=30, width=246)
        self.codeLabel.configure(activebackground="#f9f9f9")
        self.codeLabel.configure(activeforeground="black")
        self.codeLabel.configure(background="#ffffff")
        self.codeLabel.configure(disabledforeground="#a3a3a3")
        self.codeLabel.configure(font=font9)
        self.codeLabel.configure(foreground="#000000")
        self.codeLabel.configure(highlightbackground="#ffffff")
        self.codeLabel.configure(highlightcolor="black")
        self.codeLabel.configure(text='''Code Pharmacie :''')
        self.codeLabel.configure(anchor=W)

        self.codeEntryVarA = StringVar()
        self.codeEntry = Entry(self.bodyFrame,textvariable=self.codeEntryVarA)
        self.codeEntry.place(relx=0.45, rely=0.69, relheight=0.06, relwidth=0.39)

        self.codeEntry.configure(background="white")
        self.codeEntry.configure(disabledforeground="#a3a3a3")
        self.codeEntry.configure(font="TkFixedFont")
        self.codeEntry.configure(foreground="#000000")
        self.codeEntry.configure(highlightbackground="#ffffff")
        self.codeEntry.configure(highlightcolor="black")
        self.codeEntry.configure(insertbackground="black")
        self.codeEntry.configure(selectbackground="#c4c4c4")
        self.codeEntry.configure(selectforeground="black")

        self.adresLabel = Label(self.bodyFrame)
        self.adresLabel.place(relx=0.18, rely=0.78, height=30, width=246)
        self.adresLabel.configure(activebackground="#f9f9f9")
        self.adresLabel.configure(activeforeground="black")
        self.adresLabel.configure(background="#ffffff")
        self.adresLabel.configure(disabledforeground="#a3a3a3")
        self.adresLabel.configure(font=font9)
        self.adresLabel.configure(foreground="#000000")
        self.adresLabel.configure(highlightbackground="#ffffff")
        self.adresLabel.configure(highlightcolor="black")
        self.adresLabel.configure(text='''Adresse Pharmacie :''')
        self.adresLabel.configure(anchor=W)
        self.adresLabel.configure(width=244)

        self.adresEntryVarA = StringVar()
        self.adresEntry = Entry(self.bodyFrame, textvariable=self.adresEntryVarA)
        self.adresEntry.place(relx=0.45, rely=0.78, relheight=0.06, relwidth=0.39)

        self.adresEntry.configure(background="white")
        self.adresEntry.configure(disabledforeground="#a3a3a3")
        self.adresEntry.configure(font="TkFixedFont")
        self.adresEntry.configure(foreground="#000000")
        self.adresEntry.configure(highlightbackground="#ffffff")
        self.adresEntry.configure(highlightcolor="black")
        self.adresEntry.configure(insertbackground="black")
        self.adresEntry.configure(selectbackground="#c4c4c4")
        self.adresEntry.configure(selectforeground="black")



        self.retourBtn = Button(self.bodyFrame)
        self.retourBtn.place(relx=0.17, rely=0.86, height=40, width=180)
        self.retourBtn.configure(activebackground="#ffffff")
        self.retourBtn.configure(activeforeground="#000000")
        self.retourBtn.configure(font=font9)
        self.retourBtn.configure(background="#ffffff")
        self.retourBtn.configure(disabledforeground="#a3a3a3")
        self.retourBtn.configure(foreground="#000000")
        self.retourBtn.configure(highlightbackground="#ffffff")
        self.retourBtn.configure(highlightcolor="black")
        self.retourBtn.configure(pady="0")
        self.retourBtn.configure(relief=RIDGE)
        self.retourBtn.configure(text='''Retour''')
        self.retourBtn.config(command = self.retour)

        self.confBtn = Button(self.bodyFrame)
        self.confBtn.place(relx=0.64, rely=0.86, height=40, width=180)
        self.confBtn.configure(activebackground="#ffffff")
        self.confBtn.configure(activeforeground="#000000")
        self.confBtn.configure(background="#ffffff")
        self.confBtn.configure(font=font9)
        self.confBtn.configure(disabledforeground="#a3a3a3")
        self.confBtn.configure(foreground="#000000")
        self.confBtn.configure(highlightbackground="#ffffff")
        self.confBtn.configure(highlightcolor="black")
        self.confBtn.configure(pady="0")
        self.confBtn.configure(relief=RIDGE)
        self.confBtn.configure(text='''Confimer''')
        self.confBtn.config(command=self.submit)





###################################################################################################################
############################ChoixInscription#####################################################################
class Inscription_choix(Frame):
    def user (self):

        self.master.master.show_frame(Inscription_user)
    def retour(self):
        self.master.master.show_frame(Bienvenue)

    def admin (self):
        self.master.master.show_frame(Inscription)

    def __init__(self, parent, controller=None):
        Frame.__init__(self, parent)

        self.controller = controller



        font9 = "-family {Futura Bk BT} -size 15 -weight bold -slant "  \
            "roman -underline 0 -overstrike 0"

        font11 = "-family {Futura Bk BT} -size 16 -weight bold -slant "  \
            "roman -underline 0 -overstrike 0"




        self.hautFrame = Frame(self)
        self.hautFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.hautFrame.configure(borderwidth="2")
        self.hautFrame.configure(background="#ffffff")
        self.hautFrame.configure(highlightbackground="#ffffff")
        self.hautFrame.configure(highlightcolor="black")
        self.hautFrame.configure(width=945)

        self.titleLabel = Label(self.hautFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(activebackground="#f9f9f9")
        self.titleLabel.configure(activeforeground="black")
        self.titleLabel.configure(background="#ffffff")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(foreground="#000000")
        self.titleLabel.configure(highlightbackground="#ffffff")
        self.titleLabel.configure(highlightcolor="black")
        self._img144 = PhotoImage(file="images/vide.png")
        self.titleLabel.configure(image=self._img144)




        self.bodyframe = Frame(self)
        self.bodyframe.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1)
        self.bodyframe.configure(borderwidth="2")
        self.bodyframe.configure(background="#ffffff")
        self.bodyframe.configure(width=685)

        self.Labelbody = Label(self.bodyframe)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)
        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img900 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img900)

        self.adminBtn = Button(self.bodyframe)
        self.adminBtn.place(relx=0.12, rely=0.41, height=70, width=320)
        self.adminBtn.configure(activebackground="#ffffff")
        self.adminBtn.configure(activeforeground="#000000")
        self.adminBtn.configure(background="#ffffff")
        self.adminBtn.configure(disabledforeground="#a3a3a3")
        self.adminBtn.configure(font=font11)
        self.adminBtn.configure(foreground="#000000")
        self.adminBtn.configure(highlightbackground="#ffffff")
        self.adminBtn.configure(highlightcolor="black")
        self.adminBtn.configure(pady="0")
        self.adminBtn.configure(relief=RIDGE)
        self.adminBtn.configure(text='''Compte administrateur''')
        self.adminBtn.config(command =self.admin)



        self.userBtn = Button(self.bodyframe)
        self.userBtn.place(relx=0.53, rely=0.41, height=70, width=320)
        self.userBtn.configure(activeforeground="#000000")
        self.userBtn.configure(background="#ffffff")
        self.userBtn.configure(disabledforeground="#a3a3a3")
        self.userBtn.configure(font=font11)
        self.userBtn.configure(foreground="#000000")
        self.userBtn.configure(highlightbackground="#ffffff")
        self.userBtn.configure(highlightcolor="black")
        self.userBtn.configure(pady="0")
        self.userBtn.configure(relief=RIDGE)
        self.userBtn.configure(text='''Compte utilisateur''')
        self.userBtn.config(command= self.user)



        self.retourButt = Button(self.bodyframe)
        self.retourButt.place(relx=0.4, rely=0.86, height=40, width=180)
        self.retourButt.configure(font=font9)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')
        self.retourButt.configure(width=100)
        self.retourButt.config(command =self.retour)



#############################################################################################333############
class Inscription_user(Frame):
    def submit(self):
        error=0
        con = connectBdd()
        # vérifions le types des  entrees
        # type du nom de la pharmacie
        try:
            name = int(self.pharEntryVarU.get())
            showerror("Erreur!", "Le nom de la pharmacie doit être une chaine de caractères!")
            self.pharEntryVarU.set("")
            error=1

        except:
            pass
        # type du nom d'utilisateur
        try:
            name = int(self.userEntryVarU.get())
            showerror("Erreur!", "La nom d'utilisateur doit être une chaine de caractères!")
            self.userEntryVarU.set("")
            error=1

        except:
            pass
        # l'unicite de l'identifiant :
        con=connectBdd()

        userNameHash = hash.md5(self.userEntryVarU.get().encode()).hexdigest()
        con.cur.execute("SELECT id from comptes where id=%s;",userNameHash)
        ii=con.cur.fetchall()
        if ii:
            error=1
            showerror("Erreur","Cet identifiant existe déja !")


        con.fermer()
        # verifions si les entrees ne sont pas vide

        if (self.pharEntryVarU.get() == "" or self.mdpEntryVarU.get()== "" or self.confEntryVarU.get() =="" or self.userEntryVarU.get()==""
             or self.codeEntryVarU.get() ==""):

            showerror("Erreur!", "Vous devez remplir tous les champs!")
            error=1

        # type du code
        try:
             name = int(self.codeEntryVarU.get())
             showerror("Erreur!", "Le code de la pharmacie doit être une chaine de caractères!")
             self.codeEntryVarU.set("")
             error = 1

        except:
             pass

    ###################################################################################################################
        mdp = self.mdpEntryVarU.get()
        conf = self.confEntryVarU.get()
        if conf != mdp:
            showerror("Erreur !", "Le mot de passe ne correspond pas à sa confimation")
            self.confEntryVarU.set("")
            error = 1
        else :
            if error == 0:
                con=connectBdd()
                con.User(self.pharEntryVarU.get(), self.codeEntryVarU.get(), self.userEntryVarU.get(),
                         self.mdpEntryVarU.get())
                con.fermer()
                self.controller.show_frame(Login)


        #################################################################################################################

    def retour(self):
        self.master.master.show_frame(Inscription_choix)

    def __init__(self,parent,controller=None):

        Frame.__init__(self, parent)

        self.controller = controller

        font9 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                "roman -underline 0 -overstrike 0"

        self.hautFrame = Frame(self)
        self.hautFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.hautFrame.configure(borderwidth="2")
        self.hautFrame.configure(background="#ffffff")
        self.hautFrame.configure(width=945)

        self.titleLabel = Label(self.hautFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(background="#ffffff")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(foreground="#000000")
        self._img12 = PhotoImage(file="images/vide.png")
        self.titleLabel.configure(image=self._img12)



        self.bodyFrame = Frame(self)
        self.bodyFrame.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1)
        self.bodyFrame.configure(borderwidth="2")
        self.bodyFrame.configure(background="#ffffff")
        self.bodyFrame.configure(width=685)

        self.Labelbody = Label(self.bodyFrame)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)

        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img900 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img900)

        self.pharEntryVarU =StringVar()
        self.pharEntry = Entry(self.bodyFrame,textvariable =self.pharEntryVarU)
        self.pharEntry.place(relx=0.45, rely=0.12, relheight=0.06, relwidth=0.39)

        self.pharEntry.configure(background="white")
        self.pharEntry.configure(disabledforeground="#a3a3a3")
        self.pharEntry.configure(font="TkFixedFont")
        self.pharEntry.configure(foreground="#000000")
        self.pharEntry.configure(insertbackground="black")
        self.pharEntry.configure(width=264)

        self.userEntryVarU = StringVar()
        self.userEntry = Entry(self.bodyFrame,textvariable =self.userEntryVarU)
        self.userEntry.place(relx=0.45, rely=0.24, relheight=0.06, relwidth=0.39)

        self.userEntry.configure(background="white")
        self.userEntry.configure(disabledforeground="#a3a3a3")
        self.userEntry.configure(font="TkFixedFont")
        self.userEntry.configure(foreground="#000000")
        self.userEntry.configure(highlightbackground="#ffffff")
        self.userEntry.configure(highlightcolor="black")
        self.userEntry.configure(insertbackground="black")
        self.userEntry.configure(selectbackground="#c4c4c4")
        self.userEntry.configure(selectforeground="black")


        self.mdpEntryVarU = StringVar()
        self.mdpEntry = Entry(self.bodyFrame,show ='\u2022',textvariable= self.mdpEntryVarU)
        self.mdpEntry.place(relx=0.45, rely=0.36, relheight=0.06, relwidth=0.39)
        self.mdpEntry.configure(background="white")
        self.mdpEntry.configure(disabledforeground="#a3a3a3")
        self.mdpEntry.configure(font="TkFixedFont")
        self.mdpEntry.configure(foreground="#000000")
        self.mdpEntry.configure(highlightbackground="#ffffff")
        self.mdpEntry.configure(highlightcolor="black")
        self.mdpEntry.configure(insertbackground="black")
        self.mdpEntry.configure(selectbackground="#c4c4c4")
        self.mdpEntry.configure(selectforeground="black")


        self.confEntryVarU = StringVar()
        self.confEntry = Entry(self.bodyFrame,show ='\u2022',textvariable=self.confEntryVarU)
        self.confEntry.place(relx=0.45, rely=0.48, relheight=0.06, relwidth=0.39)

        self.confEntry.configure(background="white")
        self.confEntry.configure(disabledforeground="#a3a3a3")
        self.confEntry.configure(font="TkFixedFont")
        self.confEntry.configure(foreground="#000000")
        self.confEntry.configure(highlightbackground="#ffffff")
        self.confEntry.configure(highlightcolor="black")
        self.confEntry.configure(insertbackground="black")
        self.confEntry.configure(selectbackground="#c4c4c4")
        self.confEntry.configure(selectforeground="black")

        self.nomPhar = Label(self.bodyFrame)
        self.nomPhar.place(relx=0.2, rely=0.12, height=30, width=230)
        self.nomPhar.configure(background="#ffffff")
        self.nomPhar.configure(disabledforeground="#a3a3a3")
        self.nomPhar.configure(font=font9)
        self.nomPhar.configure(foreground="#000000")
        self.nomPhar.configure(anchor=W)
        self.nomPhar.configure(text='''Nom de la pharmacie :''')



        self.userLabel = Label(self.bodyFrame)
        self.userLabel.place(relx=0.2, rely=0.24, height=30, width=230)
        self.userLabel.configure(activebackground="#f9f9f9")
        self.userLabel.configure(activeforeground="black")
        self.userLabel.configure(background="#ffffff")
        self.userLabel.configure(disabledforeground="#a3a3a3")
        self.userLabel.configure(font=font9)
        self.userLabel.configure(foreground="#000000")
        self.userLabel.configure(highlightbackground="#ffffff")
        self.userLabel.configure(highlightcolor="black")
        self.userLabel.configure(anchor=W)
        self.userLabel.configure(text='''Nom d'utilisateur :''')

        self.mdpLabel = Label(self.bodyFrame)
        self.mdpLabel.place(relx=0.2, rely=0.36, height=30, width=230)
        self.mdpLabel.configure(activebackground="#f9f9f9")
        self.mdpLabel.configure(activeforeground="black")
        self.mdpLabel.configure(background="#ffffff")
        self.mdpLabel.configure(disabledforeground="#a3a3a3")
        self.mdpLabel.configure(font=font9)
        self.mdpLabel.configure(foreground="#000000")
        self.mdpLabel.configure(highlightbackground="#ffffff")
        self.mdpLabel.configure(highlightcolor="black")
        self.mdpLabel.configure(text='''Mot de passe :''')
        self.mdpLabel.configure(anchor=W)

        self.confLabel = Label(self.bodyFrame)
        self.confLabel.place(relx=0.2, rely=0.48, height=30, width=230)
        self.confLabel.configure(activebackground="#f9f9f9")
        self.confLabel.configure(activeforeground="black")
        self.confLabel.configure(background="#ffffff")
        self.confLabel.configure(disabledforeground="#a3a3a3")
        self.confLabel.configure(font=font9)
        self.confLabel.configure(foreground="#000000")
        self.confLabel.configure(highlightbackground="#ffffff")
        self.confLabel.configure(highlightcolor="black")
        self.confLabel.configure(text='''Confirmer mot de passe :''')
        self.confLabel.configure(anchor=W)

        self.codeLabel = Label(self.bodyFrame)
        self.codeLabel.place(relx=0.2, rely=0.6, height=30, width=230)
        self.codeLabel.configure(activebackground="#f9f9f9")
        self.codeLabel.configure(activeforeground="black")
        self.codeLabel.configure(background="#ffffff")
        self.codeLabel.configure(disabledforeground="#a3a3a3")
        self.codeLabel.configure(font=font9)
        self.codeLabel.configure(foreground="#000000")
        self.codeLabel.configure(highlightbackground="#ffffff")
        self.codeLabel.configure(highlightcolor="black")
        self.codeLabel.configure(text='''Code Pharmacie :''')
        self.codeLabel.configure(anchor=W)

        self.codeEntryVarU = StringVar()
        self.codeEntry = Entry(self.bodyFrame, textvariable=self.codeEntryVarU)
        self.codeEntry.place(relx=0.45, rely=0.6, relheight=0.06, relwidth=0.39)

        self.codeEntry.configure(background="white")
        self.codeEntry.configure(disabledforeground="#a3a3a3")
        self.codeEntry.configure(font="TkFixedFont")
        self.codeEntry.configure(foreground="#000000")
        self.codeEntry.configure(highlightbackground="#ffffff")
        self.codeEntry.configure(highlightcolor="black")
        self.codeEntry.configure(insertbackground="black")
        self.codeEntry.configure(selectbackground="#c4c4c4")
        self.codeEntry.configure(selectforeground="black")

        self.retourBtn = Button(self.bodyFrame)
        self.retourBtn.place(relx=0.17, rely=0.86, height=40, width=180)
        self.retourBtn.configure(activebackground="#ffffff")
        self.retourBtn.configure(activeforeground="#000000")
        self.retourBtn.configure(font=font9)
        self.retourBtn.configure(background="#ffffff")
        self.retourBtn.configure(disabledforeground="#a3a3a3")
        self.retourBtn.configure(foreground="#000000")
        self.retourBtn.configure(highlightbackground="#ffffff")
        self.retourBtn.configure(highlightcolor="black")
        self.retourBtn.configure(pady="0")
        self.retourBtn.configure(relief=RIDGE)
        self.retourBtn.configure(text='''Retour''')
        self.retourBtn.config(command=self.retour)


        self.confBtn = Button(self.bodyFrame)
        self.confBtn.place(relx=0.64, rely=0.86, height=40, width=180)
        self.confBtn.configure(activebackground="#ffffff")
        self.confBtn.configure(activeforeground="#000000")
        self.confBtn.configure(background="#ffffff")
        self.confBtn.configure(font=font9)
        self.confBtn.configure(disabledforeground="#a3a3a3")
        self.confBtn.configure(foreground="#000000")
        self.confBtn.configure(highlightbackground="#ffffff")
        self.confBtn.configure(highlightcolor="black")
        self.confBtn.configure(pady="0")
        self.confBtn.configure(relief=RIDGE)
        self.confBtn.configure(text='''Confimer''')
        self.confBtn.config(command =self.submit)







###################################################################################################
########################### Stats##################################################################

######################################################################################
####################### Echanges Entre Pharmacies#####################################
######################################################################################
class ListeDeroullante(Frame):
    def __init__(self,boss,item='',items=[],command='',width=75,listSize=5,coler="#ffffff"):
        Frame.__init__(self,boss)

        font12 = "-family {Futura Bk BT} -size 12 -slant "  \
            "roman -underline 0 -overstrike 0"

        self.boss =boss             # référence du widget 'maître'
        self.items =items           # items à placer dans la boîte de liste
        self.command =command       # fonction à invoquer après clic ou <enter>
        self.item =item             # item entré ou sélectionné
        self.listSize =listSize     # nombre d'items visibles dans la liste
        self.width =width           # largeur du champ d'entrée (en caract.)
        self.coler=coler



        self.entree=Entry(self,width=width-1,background=coler,relief=FLAT,font=font12)
        self.entree.insert(END,item)
        self.config(background=self.coler)

        self.bind("<Return>", self.sortieE)
        self.entree.pack(side=LEFT)

        # Bouton pour faire apparaître la liste associée :
        self.gif1 = PhotoImage(file ="images/down.png")       # ! variable persistante
        Button(self,background=self.coler ,image =self.gif1, width =30,
                    height=30,command =self.popup,relief=FLAT).pack(side=RIGHT)

    def sortieL(self,event=None):
        index = self.bListe.curselection()
        ind0=int(index[0])
        self.item=self.items[ind0]
        self.entree.delete(0,END)
        self.entree.insert(END,self.item)

        self.pop.destroy()

    def sortieE(self,event=None):
        self.command(self.entree.get())

    def get(self):
        return self.item

    def popup(self):
        font12 = "-family {Futura Bk BT} -size 12  -slant "  \
            "roman -underline 0 -overstrike 0"
        xW, yW = self.winfo_x(), self.winfo_y()

        geo = self.master.master.controller.geometry().split("+")
        xF, yF = int(geo[1]), int(geo[2])
        xP, yP = xF + xW + 10, yF + yW + 45
        self.pop = Toplevel(self)
        self.pop.geometry("+{}+{}".format(xP+120, yP+75))

        self.pop.overrideredirect(1)


        cadreLB = Frame(self.pop,relief=FLAT,background=self.coler)
        self.bListe = Listbox(cadreLB, height=self.listSize, width=self.width,relief=FLAT
                              , background=self.coler,font=font12)
        scrol = Scrollbar(cadreLB, command=self.bListe.yview)
        self.bListe.config(yscrollcommand=scrol.set)
        self.bListe.bind("<ButtonRelease-1>", self.sortieL)
        self.bListe.pack(side=LEFT)
        scrol.pack(expand=YES, fill=Y)
        cadreLB.pack()

        for it in self.items:
            self.bListe.insert(END, it)
####################################################################################
class EchangesEntrePharm(Frame):
    # ' pour les notifications'
    def GestionDeCompte(self):
        try:
            self.retour2()
        except:
            pass
        try:
            self.retour2()
        except:
            pass
        try:
            self.retour_perime()
        except:
            pass
        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()

    def notifs(self):
        if self.notif == 0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])

                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                          height=1, bg='white', anchor="w",
                          font=self.font12).grid(row=r,
                                                 column=1)
                    r = r + 1
                r = 0
                self.notif = 1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=818)
                self.supprnotifs.configure(activebackground="#009D78")
                self.supprnotifs.configure(activeforeground="#009D78")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command'] = self.supprimenotifs
            else:
                showinfo("Pas de notifications", "Vous n'avez pas de notifications !")

        else:
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif = 0

    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con = connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0

    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var = self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res:
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()

    font11 = "-family {Futura Bk BT} -size 20 -slant " \
             "roman -underline 0 -overstrike 0"

    font12 = "-family {Futura Bk BT} -size 12 -weight bold " \
             "-slant roman -underline 0 -overstrike 0"


    def retour(self):



        self.controller.show_frame(Stats)

    def submit(self):
        con=connectBdd()
        pharm1 = self.list1Var.get()
        pharm2 = self.list2.get()




        cur=con.cur
        cur.execute(''' SELECT code FROM contacts WHERE pharmacie=%s;''',(pharm1,))
        code1=str(cur.fetchone()[0])

        cur.execute(''' SELECT code FROM contacts WHERE pharmacie=%s;''',(pharm2,))
        code2=str(cur.fetchone()[0])
        e2 = con.echangesEntrePharm(code1, code2)

        if e2==-1:
            showerror(" Erreur "," Vous devez d'abord remplir les champs !")
        if e2==0:
            showinfo(" Information "," Les deux pharmacies n'ont pas effectués d'échanges ! ")
        else:
            ''' Cette Boucle a fait de récupérer la quantité totale de toutes les échanges
                effectuer ( pour avoir la proportion des produits échangée )'''
            qteTotal=0
            for e in e2:
                qteTotal+=e[1]

            tab1,tab2,tab3=[],[],[]
            i=0

            for e in e2:
                if e[0] not in tab1 :
                    tab1.append(e[0])
            for e in tab1:
                tab2.append(con.qteDeNom(e,pharm1,pharm2))

            while(i<len(tab2)):
                tab3.append(str(tab1[i])+"  "+
                            str('%.2f' % (100*tab2[i]/qteTotal))+" %")
                i+=1

            plt.pie(tab2,labels=tab3)
            plt.subplots_adjust(right=0.83)

            plt.show()

        con.fermer()
    def nomPharms(self):
        con=connectBdd()
        cur = con.cur
        s=[]
        cur.execute('''SELECT pharmacie FROM contacts  ;''')
        con.fermer()
        for e in cur.fetchall():
            s.append(e[0])
        return s









    def __init__(self,parent,controller):
        Frame.__init__(self, parent)

        self.controller = controller
        self.parent=parent

        font11 = "-family {Futura Bk BT} -size 20 -slant "  \
            "roman -underline 0 -overstrike 0"
        font12 = "-family {Futura Bk BT} -size 12 -weight bold " \
                 "-slant roman -underline 0 -overstrike 0"

        self.Frame1 = Frame(self)
        self.Frame1.place(relx=0.0, rely=0.0, relheight=1, relwidth=1)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#ffffff")
        self.Frame1.configure(highlightbackground="#ffffff")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=935)


        headFrame = Frame(self.Frame1)
        headFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        headFrame.configure(relief=FLAT)
        headFrame.configure(borderwidth="2")
        headFrame.configure(relief=FLAT)
        headFrame.configure(background="#009D78")
        headFrame.configure(width=935)

        self.titleLabel = Label(headFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(activebackground="#336464")
        self.titleLabel.configure(activeforeground="white")
        self.titleLabel.configure(activeforeground="black")
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(font=font11)
        self.titleLabel.configure(foreground="#ffffff")
        self.titleLabel.configure(highlightbackground="#ffffff")
        self.titleLabel.configure(highlightcolor="black")
        self._img6 = PhotoImage(file="images/stat_ech.png")
        self.titleLabel.configure(image=self._img6)
        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0

        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img1 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img1)
        bodyFrame = Frame(self.Frame1)
        bodyFrame.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1)

        bodyFrame.configure(relief=FLAT)
        bodyFrame.configure(borderwidth="2")
        bodyFrame.configure(relief=FLAT)
        bodyFrame.configure(background="#ffffff")
        bodyFrame.configure(width=745)

        self.Labelbody = Label(bodyFrame)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)

        self.pharms=self.nomPharms()
        self.pharms2=[]

        ######### Pharmacie 01 #########################
        self.list1Var=StringVar()
        self.list1=Label(bodyFrame,width=45,textvariable=self.list1Var,font=font12)
        self.list1.place(relx=0.45, rely=0.3, relheight=0.06, relwidth=0.38)


        ######### Pharmacie 02 #########################

        self.list2Var = StringVar()
        self.list2 = Combobox(bodyFrame, textvariable=self.list2Var, values=self.pharms)


        self.list2.place(relx=0.45, rely=0.5, relheight=0.06
                , relwidth=0.38)




        nmpLabel = Label(bodyFrame)
        nmpLabel.place(relx=0.2, rely=0.3, height=34, width=202)
        nmpLabel.configure(anchor=W)
        nmpLabel.configure(background="#ffffff")
        nmpLabel.configure(disabledforeground="#fafafa")
        nmpLabel.configure(font=font12)
        nmpLabel.configure(foreground="#000000")
        nmpLabel.configure(text='''Votre Pharmacie    :''')
        nmpLabel.configure(width=202)


        dosageLabel = Label(bodyFrame)
        dosageLabel.place(relx=0.2, rely=0.5, height=46, width=202)
        dosageLabel.configure(activebackground="#fafafa")
        dosageLabel.configure(activeforeground="black")
        dosageLabel.configure(anchor=W)
        dosageLabel.configure(background="#ffffff")
        dosageLabel.configure(disabledforeground="#a3a3a3")
        dosageLabel.configure(font=font12)
        dosageLabel.configure(foreground="#000000")
        dosageLabel.configure(highlightbackground="#ffffff")
        dosageLabel.configure(highlightcolor="black")
        dosageLabel.configure(text='''Nom de Pharmacie 02  :''')
        dosageLabel.configure(width=202)

        self.rechButt = Button(bodyFrame)
        self.rechButt.place(relx=0.64, rely=0.86, height=40, width=180)

        self.rechButt.configure(activebackground="#ffffff")
        self.rechButt.configure(activeforeground="#000000")
        self.rechButt.configure(background="#ffffff")
        self.rechButt.configure(borderwidth="2")
        self.rechButt.configure(disabledforeground="#a3a3a3")
        self.rechButt.configure(font=font12)
        self.rechButt.configure(foreground="#000000")
        self.rechButt.configure(highlightbackground="#ffffff")
        self.rechButt.configure(highlightcolor="black")
        self.rechButt.configure(pady="0")
        self.rechButt.configure(relief=RIDGE)
        self.rechButt.configure(text='''Confirmer''')
        self.rechButt.configure(width=196)
        self.rechButt['command']=self.submit

        self.retourButt = Button(bodyFrame)
        self.retourButt['command']=self.retour
        self.retourButt.place(relx=0.17, rely=0.86, height=40, width=180)
        self.retourButt.configure(activebackground="#ffffff")
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(borderwidth="2")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(font=font12)
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')


########################################################################################""
class Messagerie(Frame):

    def GestionDeCompte(self):
        try:
            self.retour3()
        except :
            pass
        try :
            self.retour2()
        except:
            pass
        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()

    def notifs(self):
        if self.notif == 0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])

                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                          height=1, bg='white', anchor="w",
                          font=self.font12).grid(row=r,
                                                 column=1)
                    r = r + 1
                r = 0
                self.notif = 1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=818)
                self.supprnotifs.configure(activebackground="#009D78")
                self.supprnotifs.configure(activeforeground="#3fa693")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command'] = self.supprimenotifs
            else:
                showinfo("Pas de notifications", "Vous n'avez pas de notifications !")

        else:
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif = 0

    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con = connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0

    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var = self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res:
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()

    def retour(self):
        self.master.master.show_frame(Acceuil)
    def mes_commandes(self):


        # on recupere la tables reponses a mes commandes ; mais tout d'abord le code de ma pharmacie
        con=connectBdd()
        var = self.controller.getPage(Login)
        cPh = var.nomPharm[2]
        #on recupere la table mes commandes :
        r=con.mes_commandes (cPh)
        if r==0 :
            showinfo( "Réponses non disponibles ","Vous n'avez aucune reponse à vos commandes !")
        else :
            self.titleLabel = Label(self.hautFrame)
            self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
            self.titleLabel.configure(activebackground="#f9f9f9")
            self.titleLabel.configure(activeforeground="black")
            self.titleLabel.configure(background="#ffffff")
            self.titleLabel.configure(disabledforeground="#a3a3a3")
            self.titleLabel.configure(foreground="#000000")
            self.titleLabel.configure(highlightbackground="#ffffff")
            self.titleLabel.configure(highlightcolor="black")
            self._img1000000 = PhotoImage(file="images/mes_cmd.png")
            self.titleLabel.configure(image=self._img1000000)
            self.notifications = []
            self.Buttongestcmp = Button(self.titleLabel)
            self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
            self.Buttongestcmp.configure(activebackground="#ffffff")
            self.Buttongestcmp.configure(activeforeground="#000000")
            self.Buttongestcmp.configure(background="#009D78")
            self.Buttongestcmp.configure(borderwidth="0")
            self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

            self.Buttongestcmp.configure(foreground="#808080")
            self.Buttongestcmp.configure(highlightbackground="#ffffff")
            self.Buttongestcmp.configure(highlightcolor="black")
            self.Buttongestcmp.configure(pady="0")
            self.Buttongestcmp.configure(text='''''')
            self.Buttongestcmp.configure(width=147)
            self.Buttongestcmp['command'] = self.GestionDeCompte
            self._img55 = PhotoImage(file="images/account.png")
            self.Buttongestcmp.configure(image=self._img55)

            self.Buttonnotif = Button(self.titleLabel)
            self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
            self.Buttonnotif.configure(activebackground="#ffffff")
            self.Buttonnotif.configure(activeforeground="#000000")
            self.Buttonnotif.configure(background="#009D78")
            self.Buttonnotif.configure(borderwidth="0")
            self.Buttonnotif.configure(disabledforeground="#a3a3a3")

            self.Buttonnotif.configure(foreground="#808080")
            self.Buttonnotif.configure(highlightbackground="#ffffff")
            self.Buttonnotif.configure(highlightcolor="black")
            self.Buttonnotif.configure(pady="0")
            self.Buttonnotif.configure(text='''''')
            self.Buttonnotif.configure(width=147)
            self.Buttonnotif['command'] = self.notifs
            self._img80 = PhotoImage(file="images/notifs.png")
            self.Buttonnotif.configure(image=self._img80)

            self.retourButt.destroy()
            self.scrollable_canvas = ScrollableCanvas(self)
            self.scrollable_canvas.grid(row=1, column=1)
            self.scrollable_canvas.place(relx=0.088, rely=0.22)
            self.donnees = r
            cocher=[]
            r = 0
            ligne=1
            for e in self.donnees:
                r=0
                for i in e :
                     if r == 0:
                         Label(self.scrollable_canvas.interior, relief=FLAT, width=73, height=1, bg='#009D78', text=i[0],anchor="w",foreground="#ffffff", font=self.font9).grid(row=ligne,
                                                                       column=0)
                         ligne = ligne + 1
                         Label(self.scrollable_canvas.interior, relief=FLAT, width=73, height=1, bg='#009D78',
                               text=i[1], anchor="w", foreground="#ffffff", font=self.font9).grid(
                             row=ligne,
                             column=0)
                         k=0

                         ligne=ligne+1

                     else:
                         k=0
                         for m in i:
                            Label(self.scrollable_canvas.interior, text=m, relief=RIDGE, width=73, height=1, bg='white',font=self.font9, anchor="w").grid(row=ligne, column=0)
                            ligne=ligne+1
                            k=k+1
                         cocher.append(k)
                     r = r + 1



        ################################################################################################
            self.boxVars = []
            self.rows = -1
            for k in cocher:
                self.rows=2+k

            for i in range(self.rows):
                self.boxVars.append(IntVar())
                self.boxVars[i].set(0)

            y = 0
            r=1
            for h in cocher:

                Checkbutton(self.scrollable_canvas.interior, width=2, height=1, bg='white', variable=self.boxVars[y],
                                command=lambda y=y: self.check(y)).grid(row=r, column=1)
                y = y + 1
                w=r+1
                r = r + 2+h
                while w!=r:
                    Label(self.scrollable_canvas.interior, text=" ", relief=FLAT, width=4, height=1, bg='#ffffff',
                          font=self.font9, anchor="w").grid(row=w, column=1)
                    w=w+1

            r = 0
            self.retourButt = Button(self.bodyframe)
            self.retourButt.place(relx=0.17, rely=0.86, height=40, width=180)
            self.retourButt.configure(font=self.font9)
            self.retourButt.configure(activeforeground="#000000")
            self.retourButt.configure(background="#ffffff")
            self.retourButt.configure(disabledforeground="#a3a3a3")
            self.retourButt.configure(foreground="#000000")
            self.retourButt.configure(highlightbackground="#ffffff")
            self.retourButt.configure(highlightcolor="black")
            self.retourButt.configure(pady="0")
            self.retourButt.configure(relief=RIDGE)
            self.retourButt.configure(text='''Retour''')
            self.retourButt.configure(width=100)
            self.retourButt.config(command=self.retour2)


            self.accepterButt = Button(self.bodyframe)
            self.accepterButt.place(relx=0.64, rely=0.86, height=40, width=180)
            self.accepterButt.configure(font=self.font9)
            self.accepterButt.configure(activeforeground="#000000")
            self.accepterButt.configure(background="#ffffff")
            self.accepterButt.configure(disabledforeground="#a3a3a3")
            self.accepterButt.configure(foreground="#000000")
            self.accepterButt.configure(highlightbackground="#ffffff")
            self.accepterButt.configure(highlightcolor="black")
            self.accepterButt.configure(pady="0")
            self.accepterButt.configure(relief=RIDGE)
            self.accepterButt.configure(text='''Accepter la sélection''')
            self.accepterButt.configure(width=100)
            self.accepterButt.config(command=self.accepter_commandes)

            self.refuserButt = Button(self.bodyframe)
            self.refuserButt.place(relx=0.405, rely=0.86, height=40, width=180)
            self.refuserButt.configure(font=self.font9)
            self.refuserButt.configure(activeforeground="#000000")
            self.refuserButt.configure(background="#ffffff")
            self.refuserButt.configure(disabledforeground="#a3a3a3")
            self.refuserButt.configure(foreground="#000000")
            self.refuserButt.configure(highlightbackground="#ffffff")
            self.refuserButt.configure(highlightcolor="black")
            self.refuserButt.configure(pady="0")
            self.refuserButt.configure(relief=RIDGE)
            self.refuserButt.configure(text='''Refuser la sélection''')
            self.refuserButt.configure(width=100)
            self.refuserButt.config(command=self.refuser_commandes)

        con.fermer()

    def retour2(self):
        try:
            self.scrollable_canvas.destroy()
            self.retourButt.destroy()
            self.accepterButt.destroy()
            self.refuserButt.destroy()

        except:
            pass
        self.titleLabel = Label(self.hautFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(activebackground="#f9f9f9")
        self.titleLabel.configure(activeforeground="black")
        self.titleLabel.configure(background="#ffffff")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(foreground="#000000")
        self.titleLabel.configure(highlightbackground="#ffffff")
        self.titleLabel.configure(highlightcolor="black")
        self._img105 = PhotoImage(file="images/messag.png")
        self.titleLabel.configure(image=self._img105)
        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img57 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img57)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)


        # on remet l'ancien bouton retour
        self.retourButt = Button(self.bodyframe)
        self.retourButt.place(relx=0.4, rely=0.86, height=40, width=180)
        self.retourButt.configure(font=self.font9)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')
        self.retourButt.configure(width=100)
        self.retourButt.config(command=self.retour)

    def check(self, i):
        if self.boxVars:

            var = self.boxVars[i]
            deselected = []
            if var.get() == 0:
                deselected.append(i)
    def accepter_commandes(self):
        selection_commandes=[]
        for i in range(self.rows):
            self.boxVars.append(IntVar())
            if (self.boxVars[i].get()==1):
                selection_commandes.append(i)
        w=0
        ma_selection=[]



        for i in self.donnees:
            if w in selection_commandes:

                ma_selection.append(i)
            w+=1


        # now ma selectiooo:
        for i in ma_selection:
            # on recupere le numero de la commande

            numCommande=i[0][0][12:len(i[0][0])]
            numCommande=int(numCommande)

            #on recupere les code des pharmacies repondantes :
            con=connectBdd()
            var = self.controller.getPage(Login)
            moi = var.nomPharm[2]
            liste=con.reponses(numCommande,moi)
            # on appelle la methode de selection d'apres la distance
            other=con.selection_commande(liste,moi)
            liste.remove(other)
            con.infos_transfert(numCommande,other,liste)
            con.transfert_stock(moi,other,numCommande)
        self.retour2()


    def refuser_commandes(self):
        var = self.controller.getPage(Login)
        moi = var.nomPharm[2]
        selection_commandes = []
        for i in range(self.rows):
            self.boxVars.append(IntVar())
            if (self.boxVars[i].get() == 1):
                selection_commandes.append(i)
        w = 0
        ma_selection = []



        for i in self.donnees:
            if w in selection_commandes:
                ma_selection.append(i)
            w += 1

        # now ma selectiooo:
        con = connectBdd()
        for i in ma_selection:
            # on recupere le numero de la commande

            numCommande = i[0][0][12:len(i[0][0])]
            numCommande = int(numCommande)

            con.supprimeCommande(moi,numCommande)
        con.fermer()
        self.retour2()
############################################################################################################################
    ###" repondre a une commande#################""
    def retour3(self):
        try:
            self.scrollable_canvas.destroy()
            self.retourButt.destroy()
            self.retourButt2.destroy()
            self.accepterButt.destroy()

        except:
            pass
        self._img188222 = PhotoImage(file="images/messag.png")
        self.titleLabel.configure(image=self._img188222)
        self.retourButt = Button(self.bodyframe)
        self.retourButt.place(relx=0.4, rely=0.86, height=40, width=180)
        self.retourButt.configure(activebackground="#ffffff")
        self.retourButt.configure(font=self.font9)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#d9d9d9")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')
        self.retourButt.configure(width=100)
        self.retourButt.config(command=self.retour)

        self.master.master.show_frame(Messagerie)

    def affichage(self):
        # on verifie le type de l'utilisateur
        var = self.controller.getPage(Login)
        if var.nomPharm[3] == 1:
            self.colonnes[:] = []
            acc = self.controller.getPage(Login)
            Cph = acc.nomPharm[2]

            con = connectBdd()

            exist = con.cmdRecu(Cph)

            self.colonnes = exist
            if exist:
                if exist[0]:
                    # nouveau bouton retour
                    self.retourButt2 = Button(self.bodyframe)
                    self._img1369 = PhotoImage(file="images/cmdr.png")
                    self.titleLabel.configure(image=self._img1369)

                    self.retourButt2.place(relx=0.17, rely=0.86, height=40, width=180)
                    self.retourButt2.configure(activeforeground="#000000")
                    self.retourButt2.configure(background="#ffffff")
                    self.retourButt2.configure(disabledforeground="#a3a3a3")
                    self.retourButt2.configure(font=self.font12)
                    self.retourButt2.configure(foreground="#000000")
                    self.retourButt2.configure(highlightbackground="#d9d9d9")
                    self.retourButt2.configure(highlightcolor="black")
                    self.retourButt2.configure(pady="0")
                    self.retourButt2.configure(relief=RIDGE)
                    self.retourButt2.configure(text='''Retour''')
                    self.retourButt2.config(command=self.retour3)

                    self.accepterButt = Button(self.bodyframe)
                    self.accepterButt.place(relx=0.64, rely=0.86, height=40, width=180)
                    self.accepterButt.configure(font=self.font9)
                    self.accepterButt.configure(activeforeground="#000000")
                    self.accepterButt.configure(background="#ffffff")
                    self.accepterButt.configure(disabledforeground="#a3a3a3")
                    self.accepterButt.configure(foreground="#000000")
                    self.accepterButt.configure(highlightbackground="#ffffff")
                    self.accepterButt.configure(highlightcolor="black")
                    self.accepterButt.configure(pady="0")
                    self.accepterButt.configure(relief=RIDGE)
                    self.accepterButt.configure(text='''Accepter la sélection''')
                    self.accepterButt.configure(width=100)
                    self.accepterButt['command'] = self.repondre

                    # on recupere le code de la pharmacie courante

                    self.retourButt.destroy()

                    a = ('Nom Pharmacie', "Nom du produit ", "Dosage(mg/l-mg)", "Forme", "Quantité")

                    self.scrollable_canvas = ScrollableCanvasReçue(self)
                    self.scrollable_canvas.grid(row=1, column=1)
                    self.scrollable_canvas.place(relx=0.09, rely=0.25)

                    Label(self.scrollable_canvas.interior, text=a[0], relief=FLAT, width=15, height=2,
                          foreground="#ffffff", bg='#009D78',
                          font=self.font12).grid(row=0,
                                                 column=0)
                    Label(self.scrollable_canvas.interior, text=a[1], relief=FLAT, width=17, height=2,
                          foreground="#ffffff", bg='#009D78',
                          font=self.font12).grid(row=0,
                                                 column=1)
                    Label(self.scrollable_canvas.interior, text=a[2], relief=FLAT, width=13, height=2,
                          foreground="#ffffff", bg='#009D78',
                          font=self.font12).grid(row=0,
                                                 column=2)
                    Label(self.scrollable_canvas.interior, text=a[3], relief=FLAT, width=17, height=2,
                          foreground="#ffffff", bg='#009D78',
                          font=self.font12).grid(row=0,
                                                 column=3)
                    Label(self.scrollable_canvas.interior, text=a[4], relief=FLAT, width=9, height=2,
                          foreground="#ffffff", bg='#009D78',
                          font=self.font12).grid(row=0,
                                                 column=4)
                    Label(self.scrollable_canvas.interior, relief=FLAT, width=4, height=2, foreground="#ffffff",
                          bg='#009D78',
                          font=self.font12).grid(row=0,
                                                 column=5)

                    r = 1

                    for e in self.colonnes[0]:
                        Label(self.scrollable_canvas.interior, text=e, relief=RIDGE, width=15, height=1, bg='white',
                              font=self.font12).grid(row=r,
                                                     column=0)
                        r = r + 1

                    r = 1
                    k = 0
                    for b in self.colonnes[1]:
                        Label(self.scrollable_canvas.interior, text=b, relief=RIDGE, width=17, height=1, bg='white',
                              font=self.font12).grid(row=r,
                                                     column=1)
                        r = r + 1

                    r = 1

                    for c in self.colonnes[2]:
                        Label(self.scrollable_canvas.interior, text=c, relief=RIDGE, width=13, height=1, bg='white',
                              font=self.font12).grid(row=r,
                                                     column=2)
                        r = r + 1

                    r = 1

                    for d in self.colonnes[3]:
                        Label(self.scrollable_canvas.interior, text=d, relief=RIDGE, width=17, height=1, bg='white',
                              font=self.font12).grid(row=r,
                                                     column=3)
                        r = r + 1

                    r = 1

                    for f in self.colonnes[4]:
                        Label(self.scrollable_canvas.interior, text=f, relief=RIDGE, width=9, height=1, bg='white',
                              font=self.font12).grid(row=r,
                                                     column=4)
                        r = r + 1

                    self.boxVars2 = []

                    self.rows2 = r - 1

                    for i in range(self.rows2):
                        self.boxVars2.append(IntVar())
                        self.boxVars2[i].set(0)
                    r = 1
                    y = 0
                    for h in range(self.rows2):


                        Checkbutton(self.scrollable_canvas.interior, width=2, height=1, bg='white',
                                    variable=self.boxVars2[y],
                                    command=lambda y=y: self.check(y)).grid(row=r, column=5)
                        y = y + 1
                        r = r + 1
                else:
                    showinfo("Pas de commandes", "Aucune commande reçue !")
            else:
                showinfo("Pas de commandes", "Aucune commande reçue !")

        else:
            showinfo("Opération impossible !",
                     "Vous ne pouvez pas visualiser ou répondre à des commandes !\nVeuillez vous connecter avec un compte admin pour pouvoir continuer ")





    def repondre(self):
        con=connectBdd()

        selection = []
        for i in range(self.rows2):
            self.boxVars.append(IntVar())
            if (self.boxVars2[i].get() == 1):
                selection.append(self.colonnes[5][i])

        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        for i in selection:
            con.repondre_commande(i,cPh)
        self.retour3()

        con.fermer()

###########################################################################################################################################
    def __init__(self, parent, controller=None):
        Frame.__init__(self, parent)

        self.controller = controller

        self.boxVars = []
        self.rows = -1
        self.colonnes=[]
        font9 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        font11 ="-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        self.boxVars2 = []
        self.rows2 = -1
        self.font19="-family {Futura Bk BT} -size 15 -weight bold " \
                 "-slant roman -underline 0 -overstrike 0"

        self.Frame1 = Frame(self)
        self.Frame1.place(relx=0.0, rely=0.0, relheight=1, relwidth=1)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#ffffff")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=935)

        self.font11=font11
        self.font9=font9
        self.donnees=[]
        self.var=[]

        self.hautFrame = Frame(self)
        self.hautFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.hautFrame.configure(borderwidth="2")
        self.hautFrame.configure(background="#ffffff")
        self.hautFrame.configure(highlightbackground="#ffffff")
        self.hautFrame.configure(highlightcolor="black")
        self.hautFrame.configure(width=945)

        self.titleLabel = Label(self.hautFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(activebackground="#f9f9f9")
        self.titleLabel.configure(activeforeground="black")
        self.titleLabel.configure(background="#ffffff")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(foreground="#000000")
        self.titleLabel.configure(highlightbackground="#ffffff")
        self.titleLabel.configure(highlightcolor="black")
        self._img1999 = PhotoImage(file="images/messag.png")
        self.titleLabel.configure(image=self._img1999)

        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0


        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img19997 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img19997)

        self.bodyframe = Frame(self)
        self.bodyframe.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1.0)
        self.bodyframe.configure(borderwidth="2")
        self.bodyframe.configure(background="#ffffff")
        self.bodyframe.configure(width=745)


        self.Labelbody = Label(self.bodyframe)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img1578 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img1578)
        self.Labelbody.configure(width=935)


        self.Button2 = Button(self.bodyframe)
        self.Button2.place(relx=0.31, rely=0.12, height=70, width=357)

        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#ffffff")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(font=self.font19)
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#ffffff")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(relief=RIDGE)
        self.Button2.configure(text=''' Réponses à Mes commandes ''')
        self.Button2['command'] = self.mes_commandes



        self.restButt = Button(self.bodyframe)
        self.restButt.place(relx=0.31, rely=0.46, height=70, width=357)

        self.restButt.configure(background="#ffffff")
        self.restButt.configure(disabledforeground="#a3a3a3")
        self.restButt.configure(font=self.font19)
        self.restButt.configure(foreground="#000000")
        self.restButt.configure(highlightbackground="#ffffff")
        self.restButt.configure(highlightcolor="black")
        self.restButt.configure(pady="0")
        self.restButt.configure(relief=RIDGE)
        self.restButt.configure(text='''Commandes reçues''')
        self.restButt['command'] = self.affichage




        self.retourButt = Button(self.bodyframe)
        self.retourButt.place(relx=0.4, rely=0.86, height=40, width=180)
        self.retourButt.configure(font=self.font9)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')
        self.retourButt.configure(width=100)
        self.retourButt.config(command =self.retour)



#########################################################################################""
class Transactions(Frame):

    def GestionDeCompte(self):

        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()

    def notifs(self):
        if self.notif == 0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])

                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                          height=1, bg='white', anchor="w",
                          font=self.font12).grid(row=r,
                                                 column=1)
                    r = r + 1
                r = 0
                self.notif = 1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=818)
                self.supprnotifs.configure(activebackground="#009D78")
                self.supprnotifs.configure(activeforeground="#3fa693")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command'] = self.supprimenotifs
            else:
                showinfo("Pas de notifications", "Vous n'avez pas de notifications !")

        else:
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif = 0

    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con = connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0

    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var = self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res:
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()

    def retour(self):
        self.master.master.show_frame(Acceuil)
    def do_commande(self):
        self.master.master.show_frame(Faire_commande)
    def do_achat(self):
        self.master.master.show_frame(Achat_prod)

    def __init__(self, parent, controller=None):
        Frame.__init__(self, parent)

        self.controller = controller



        font9 = "-family {Futura Bk BT} -size 15 -weight bold -slant "  \
            "roman -underline 0 -overstrike 0"

        font11 = "-family {Futura Bk BT} -size 16 -weight bold -slant "  \
            "roman -underline 0 -overstrike 0"




        self.hautFrame = Frame(self)
        self.hautFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.hautFrame.configure(borderwidth="2")
        self.hautFrame.configure(background="#ffffff")
        self.hautFrame.configure(highlightbackground="#ffffff")
        self.hautFrame.configure(highlightcolor="black")
        self.hautFrame.configure(width=945)

        self.titleLabel = Label(self.hautFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(activebackground="#f9f9f9")
        self.titleLabel.configure(activeforeground="black")
        self.titleLabel.configure(background="#ffffff")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(foreground="#000000")
        self.titleLabel.configure(highlightbackground="#ffffff")
        self.titleLabel.configure(highlightcolor="black")
        self._img1000 = PhotoImage(file="images/trans.png")
        self.titleLabel.configure(image=self._img1000)

        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0


        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)



        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img1 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img1)
        self.bodyframe = Frame(self)
        self.bodyframe.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1.0)
        self.bodyframe.configure(borderwidth="2")
        self.bodyframe.configure(background="#ffffff")
        self.bodyframe.configure(width=685)

        self.Labelbody = Label(self.bodyframe)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)



        self.Button2 = Button(self.bodyframe)
        self.Button2.place(relx=0.32, rely=0.13, height=70, width=357)

        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#ffffff")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(font=font11)
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#ffffff")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(relief=RIDGE)
        self.Button2.configure(text='''Vente de produits ''')
        self.Button2['command'] = self.do_achat



        self.restButt = Button(self.bodyframe)
        self.restButt.place(relx=0.32, rely=0.46, height=70, width=357)

        self.restButt.configure(background="#ffffff")
        self.restButt.configure(disabledforeground="#a3a3a3")
        self.restButt.configure(font=font11)
        self.restButt.configure(foreground="#000000")
        self.restButt.configure(highlightbackground="#ffffff")
        self.restButt.configure(highlightcolor="black")
        self.restButt.configure(pady="0")
        self.restButt.configure(relief=RIDGE)
        self.restButt.configure(text='''Effectuer une commande''')
        self.restButt['command'] = self.do_commande



        self.retourButt = Button(self.bodyframe)
        self.retourButt.place(relx=0.4, rely=0.86, height=40, width=180)
        self.retourButt.configure(font=font9)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')
        self.retourButt.configure(width=100)
        self.retourButt.config(command =self.retour)

#############################################################################################
#####commande
#################LA COMMANDE // FAIRE UNE COMMANDE #######################################################################
class Faire_commande(Frame):
    # ' pour les notifications'
    def GestionDeCompte(self):
        try:
            self.retour2()
        except:
            pass
        try:
            self.retour2()
        except:
            pass

        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()

    def notifs(self):
        if self.notif == 0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])

                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                          height=1, bg='white', anchor="w",
                          font=self.font12).grid(row=r,
                                                 column=1)
                    r = r + 1
                r = 0
                self.notif = 1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=818)
                self.supprnotifs.configure(activebackground="#009D78")
                self.supprnotifs.configure(activeforeground="#009D78")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command'] = self.supprimenotifs
            else:
                showinfo("Pas de notifications", "Vous n'avez pas de notifications !")

        else:
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif = 0

    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con = connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0

    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var = self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res:
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()

    def retour(self):
        t=askyesno("Annuler","Etez-vous sur de vouloir annuler vos commandes?")
        if (t):
            self.EntryQuantiteVar.set(0)

            self.EntryNproduitVar.set("")




            self.master.master.show_frame(Transactions)
            self.donnees=[]
            self.variable=0




    def recup_nfd(self,entree):
        nom = str()
        forme = str()
        dosage = str()
        i = 0
        fi = 0
        di = 0
        ni = 0
        while entree[i] != " ":
            ni = ni + 1
            i = i + 1
        nom = entree[0:i]
        if entree[i+1]!="-":
            wi=i+1
            i=i+1
            while entree[i] != " ":
                ni = ni + 1
                i = i + 1
            nom=str(nom+" "+str(entree[wi:i]))


        i = i + 3
        w = i

        while entree[i] != " ":

            i = i + 1
        forme = entree[w:i]

        if entree[i+1]!="-":
            wi=i+1
            i=i+1
            while entree[i] != " ":
                ni = ni + 1
                i = i + 1
            forme=str(forme+" "+str(entree[wi:i]))



        i = i + 3
        w = i
        while entree[i] != " ":
            i = i + 1
        dosage = entree[w:i]
        try:
             dosage = int(dosage)
        except :
            dosage=0

        sortie = []
        sortie.append(nom)
        sortie.append(forme)
        sortie.append(dosage)
        return sortie
    def new(self):
        # on enregistre les donnees du formualre
        if self.variable==0:
            self.donnees[:]=[]
        self.variable=1
        error=0
        #on va verifier les entrees d'abord :
        dosage=0
        quantite=0
        #verification des types :
        # type de la quantité
        try:
            quantite = int(self.EntryQuantite.get())
        except:
            showerror("Erreur!", "La quantité doit être un nombre!")
            self.EntryQuantiteVar.set(0)
            error = 1
        con=connectBdd()

        #on verifie si les entrees ne sont pas vides
        if( quantite==0 or self.EntryNproduit.get()=="" ):
            error=1
            showerror("Erreur! ","Vous devez remplir tous les champs !")

        var = []
        if error==0:
            #on recupere le nom la forme et le dosage :
            liste=self.recup_nfd(self.EntryNproduit.get())

            name = liste[0]
            forme =liste[1]
            dosage=liste[2]
            # on verifie si le produit existe deja
            con=connectBdd()

            var.append(dosage)
            var.append(quantite)

            var.append(name)
            var.append(forme)

            if dosage :
                bm="m"
            else :
                bm="b"
            var.append(bm)


            #on les ajoute a notre liste de donnees
            self.donnees.append(var)


            showinfo("Opération exectuée","Ce produit a été ajouté à votre panier !")


                #vider les entreeeeeeeeeeeeeee

            self.EntryQuantiteVar.set(0)

            self.EntryNproduitVar.set("")

            self.master.master.show_frame(Faire_commande)
            con.fermer()



    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        font10 = "-family {Futura Bk BT} -size 20 -weight normal " \
                 "-slant roman -underline 0 -overstrike 0"

        font9 = "-family {Futura Bk BT} -size 12 -weight bold -slant" \
                " roman -underline 0 -overstrike 0"

        font11 = "-family {Futura Bk BT} -size 12 -weight bold -slant" \
                " roman -underline 0 -overstrike 0"
        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        font13 = "-family {Futura Bk BT} -size 11  -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.font13 = font13
        self.font11 = font11
        self.font10=font10


        #on genere la liste des produits existants:
        self.liste_produits=[]
        var = connectBdd()
        cur = var.cur
        cur.execute("""SELECT * FROM produits""")
        resultat1=cur.fetchall()
        var =[]
        self.liste_products=[]
        for inter in resultat1:
            var=[]
            if inter[1]=="b": #c'est un produit de bien être , on ne prend pas le dosage
                var =str(inter[3].lower().capitalize()+" - "+inter[7]+"       ")
            else :
                var= str(inter[3].lower().capitalize()+" - "+inter[7]+" - "+str(inter[6])+" (mg ou mg/l)")
            self.liste_products.append(var)

        self.liste_products=sorted(self.liste_products)











        self.controller=controller
        self.variable=0





        self.Frame1 = Frame(self)
        self.Frame1.place(relx=0.0, rely=0.0, relheight=1, relwidth=1)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#ffffff")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=935)

        self.FrameTop = Frame(self.Frame1)
        self.FrameTop.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.FrameTop.configure(borderwidth="2")
        self.FrameTop.configure(background="#009D78")
        self.FrameTop.configure(highlightbackground="#d9d9d9")
        self.FrameTop.configure(highlightcolor="black")
        self.FrameTop.configure(width=935)

        self.titleLabel = Label(self.FrameTop)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(font=font11)
        self.titleLabel.configure(foreground="#fafafa")
        self.titleLabel.configure(text='''Affichage Des Produits''')
        self.titleLabel.configure(width=382)
        self._img7 = PhotoImage(file="images/cmd.png")
        self.titleLabel.configure(image=self._img7)

        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0

        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        self.Frame6 = Frame(self.Frame1)
        self.Frame6.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1.0)
        self.Frame6.configure(relief=FLAT)
        self.Frame6.configure(borderwidth="2")
        self.Frame6.configure(relief=FLAT)
        self.Frame6.configure(background="#ffffff")
        self.Frame6.configure(highlightbackground="#d9d9d9")
        self.Frame6.configure(highlightcolor="black")
        self.Frame6.configure(width=745)

        self.Labelbody = Label(self.Frame6)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)

        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img1 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img1)

        self.NpLabel = Label(self.Frame6)
        self.NpLabel.place(relx=0.22, rely=0.27, height=31, width=150)
        self.NpLabel.configure(activebackground="#f9f9f9")
        self.NpLabel.configure(activeforeground="#000000")
        self.NpLabel.configure(background="#ffffff")
        self.NpLabel.configure(disabledforeground="#a3a3a3")
        self.NpLabel.configure(font=font9)
        self.NpLabel.configure(anchor=W)
        self.NpLabel.configure(foreground="#000000")
        self.NpLabel.configure(highlightbackground="#d9d9d9")
        self.NpLabel.configure(highlightcolor="#000000")
        self.NpLabel.configure(text='''Produit :''')



        self.EntryNproduitVar= StringVar()
        self.EntryNproduit = Combobox(self.Frame6,textvariable=self.EntryNproduitVar,values=self.liste_products,
                                   state="readonly")
        self.EntryNproduit.place(relx=0.45, rely=0.27 , relheight=0.06
                                 , relwidth=0.38)
        self.EntryNproduit.configure(background="#ffffff")



        self.BtnConf1 = Button(self.Frame6)
        self.BtnConf1.place(relx=0.64, rely=0.86, height=40, width=180)
        self.BtnConf1.configure(activebackground="#d9d9d9")
        self.BtnConf1.configure(activeforeground="#000000")
        self.BtnConf1.configure(background="#ffffff")
        self.BtnConf1.configure(disabledforeground="#a3a3a3")
        self.BtnConf1.configure(font=font11)
        self.BtnConf1.configure(foreground="#000000")
        self.BtnConf1.configure(highlightbackground="#d9d9d9")
        self.BtnConf1.configure(highlightcolor="black")
        self.BtnConf1.configure(pady="0")
        self.BtnConf1.configure(relief=RIDGE)
        self.BtnConf1.configure(text='''Terminer''')

        self.BtnConf1['command'] = self.submit


        self.BtnAjout = Button(self.Frame6)
        self.BtnAjout.place(relx=0.40, rely=0.86, height=40, width=180)
        self.BtnAjout.configure(activebackground="#d9d9d9")
        self.BtnAjout.configure(activeforeground="#000000")
        self.BtnAjout.configure(background="#ffffff")
        self.BtnAjout.configure(disabledforeground="#a3a3a3")
        self.BtnAjout.configure(font=font11)
        self.BtnAjout.configure(foreground="#000000")
        self.BtnAjout.configure(highlightbackground="#d9d9d9")
        self.BtnAjout.configure(highlightcolor="black")
        self.BtnAjout.configure(pady="0")
        self.BtnAjout.configure(relief=RIDGE)
        self.BtnAjout.configure(text='''Ajouter produit''')
        self.BtnAjout['command'] = self.new


        self.EntryQuantiteVar= StringVar()
        self.EntryQuantite= Entry(self.Frame6,textvariable=self.EntryQuantiteVar)
        self.EntryQuantite.place(relx=0.45, rely=0.54, relheight=0.06
                                 , relwidth=0.38)
        self.EntryQuantite.configure(background="#ffffff")
        self.EntryQuantite.configure(disabledforeground="#a3a3a3")
        self.EntryQuantite.configure(font="TkFixedFont")
        self.EntryQuantite.configure(foreground="#000000")
        self.EntryQuantite.configure(highlightbackground="#d9d9d9")
        self.EntryQuantite.configure(highlightcolor="black")
        self.EntryQuantite.configure(insertbackground="black")
        self.EntryQuantite.configure(borderwidth='1')
        self.EntryQuantite.configure(selectbackground="#c4c4c4")
        self.EntryQuantite.configure(selectforeground="black")









        self.CategorieLabel2 = Label(self.Frame6)
        self.CategorieLabel2.place(relx=0.22, rely=0.54, height=21, width=200)
        self.CategorieLabel2.configure(activebackground="#f9f9f9")
        self.CategorieLabel2.configure(activeforeground="black")
        self.CategorieLabel2.configure(background="#ffffff")
        self.CategorieLabel2.configure(disabledforeground="#a3a3a3")
        self.CategorieLabel2.configure(font=font9)
        self.CategorieLabel2.configure(foreground="#000000")
        self.CategorieLabel2.configure(highlightbackground="#d9d9d9")
        self.CategorieLabel2.configure(highlightcolor="black")
        self.CategorieLabel2.configure(anchor=W)
        self.CategorieLabel2.configure(text='''Quantité:''')











        self.BtnAnnuler = Button(self.Frame6)
        self.BtnAnnuler.place(relx=0.17, rely=0.86, height=40, width= 180)
        self.BtnAnnuler.configure(activebackground="#d9d9d9")
        self.BtnAnnuler.configure(activeforeground="#000000")
        self.BtnAnnuler.configure(background="#ffffff")
        self.BtnAnnuler.configure(disabledforeground="#a3a3a3")
        self.BtnAnnuler.configure(font=font11)
        self.BtnAnnuler.configure(foreground="#000000")
        self.BtnAnnuler.configure(highlightbackground="#d9d9d9")
        self.BtnAnnuler.configure(highlightcolor="black")
        self.BtnAnnuler.configure(pady="0")
        self.BtnAnnuler.configure(relief=RIDGE)
        self.BtnAnnuler.configure(text='''Annuler''')

        self.BtnAnnuler['command'] = self.retour





        ################
        self.donnees=[]
        self.donnees1=[]
        self.r=[]
        self.boxVars = []
        self.rows = -1
        self.boxVars2 = []
        self.rows2 = -1


    def submit(self):

        error = 0
        if self.variable == 0:

            self.donnees[:] = []
        else:
            self.variable = 0


        # on va verifier les entrees d'abord :
        dosage = 0
        quantite = 0
        # verification des types :

        # type de la quantité
        try:
            quantite = int(self.EntryQuantite.get())
        except:
            showerror("Erreur!", "La quantité doit être un nombre!")
            self.EntryQuantiteVar.set(0)
            error = 1

        # on verifie si les entrees ne sont pas vides
        if (quantite == 0 or self.EntryNproduit.get() == ""):
            error = 1
            showerror("Erreur! ", "Vous devez remplir tous les champs !")
            if self.donnees:
                a = askyesno("", "Voulez-vous terminer la vente et ignorer ce produit?")
                if a:
                    con = connectBdd()

                    r = con.listeProduits(self.donnees)

                    self.r = r

                else:
                    self.variable = 1
        # on enregistre les donnees du dernier formualaire
        if error == 0:

            con = connectBdd()

            var = []
            var[:] = []

            liste = self.recup_nfd(self.EntryNproduit.get())


            name = liste[0]
            forme = liste[1]
            dosage = liste[2]

            var.append(dosage)
            if dosage:
                bm = "m"
            else:
                bm = "b"




            var.append(int(self.EntryQuantiteVar.get()))

            var.append(name)
            var.append(forme)
            var.append(bm)


            # on les ajoute a notre liste de donnees
            self.donnees.append(var)

            showinfo("Opération exécutée", "Ce produit a été ajouté!")

            sortie_commandes=[]
            #on doit recuperer le code de notre pharmacie
        #                 var=self.controller.getPage(Login)
            var=self.controller.getPage(Login)
            moi=var.nomPharm[2]

            sortie_commandes=con.commandes(self.donnees,moi)

            #on enregistre les commandes
            con.faire_commandes(sortie_commandes)
            showinfo("Opération exécutée", "Vos commandes ont été lancées!\n Vous pourrez consulter les reponses à vos commandes dans l'onglet Messagerie")



            # vider les entreeeeeeeeeeeeeee
            self.EntryQuantiteVar.set(0)

            self.EntryNproduitVar.set("")




            self.master.master.show_frame(Transactions)
            con.fermer()

        ###################autre page ##########################"""




###################"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Ajout(Frame):
    # ' pour les notifications'
    def GestionDeCompte(self):
        try:
            self.retour2()
        except:
            pass
        try:
            self.retour2()
        except:
            pass
        try:
            self.retour_perime()
        except:
            pass
        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()

    def notifs(self):
        if self.notif == 0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])

                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                          height=1, bg='white', anchor="w",
                          font=self.font12).grid(row=r,
                                                 column=1)
                    r = r + 1
                r = 0
                self.notif = 1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=818)
                self.supprnotifs.configure(activebackground="#009D78")
                self.supprnotifs.configure(activeforeground="#009D78")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command'] = self.supprimenotifs
            else:
                showinfo("Pas de notifications", "Vous n'avez pas de notifications !")

        else:
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif = 0

    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con = connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0

    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var = self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res:
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()

    def retour(self):

        self.EntryFormeVar.set("")

        self.EntryDosVar.set(0)
        self.EntryNmpVar.set("")
        self.EntryQtVar.set(0)
        self.CheckbuttbmVar.set(0)
        self.restCheckVar.set(0)
        self.master.master.show_frame(gestionStock)

    def videForm(self):
        self.EntryFormeVar.set("")

        self.EntryDosVar.set(0)
        self.EntryNmpVar.set("")
        self.EntryQtVar.set(0)
        self.CheckbuttbmVar.set(0)
        self.restCheckVar.set(0)





    def updateDosage(self, *args):

        if self.CheckbuttbmVar.get():
            self.dosageVar = self.EntryDosVar.get()
            self.EntryDos.config(state="readonly")
            self.EntryDosVar.set("")
        else:
            self.EntryDos.config(state="normal")





    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        font10 = "-family {Futura Bk BT} -size 12 -weight bold "  \
            "-slant roman -underline 0 -overstrike 0"
        font11 = "-family {Futura Bk BT} -size 20 -weight normal "  \
            "-slant roman -underline 0 -overstrike 0"
        font9 = "-family {Futura Bk BT} -size 11 -weight normal -slant"  \
            " roman -underline 0 -overstrike 0"
        self.controller = controller

        self.dosageVar= IntVar()
        # on genere la liste des produits existants:
        self.liste_produits = []
        var = connectBdd()
        cur = var.cur
        cur.execute("""SELECT nomProduit FROM produits""")
        resultat1 = cur.fetchall()

        for inter in resultat1:
            for inter2 in inter:
                self.liste_produits.append(inter2.upper().capitalize())

        self.liste_produits = sorted(self.liste_produits)
        # on supprime les doublants dans cette liste:
        self.inter = ""
        self.liste_products = []
        for produit in self.liste_produits:
            if produit != self.inter:
                self.liste_products.append(produit)
                self.inter = produit


        #######################################################

        self.verification_neuf = 0
        self.verification_date=0

        self.Frame1 = Frame(self)
        self.Frame1.place(relx=0.0, rely=0.0, relheight=1, relwidth=1.0)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#ffffff")
        self.Frame1.configure(highlightbackground="#ffffff")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=935)

        self.FrameHaut = Frame(self.Frame1)
        self.FrameHaut.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.FrameHaut.configure(borderwidth="2")
        self.FrameHaut.configure(background="#009D78")
        self.FrameHaut.configure(highlightbackground="#ffffff")
        self.FrameHaut.configure(highlightcolor="black")
        self.FrameHaut.configure(width=945)


        self.titleLabel = Label(self.FrameHaut)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(font=font11)
        self.titleLabel.configure(foreground="#fafafa")
        self.titleLabel.configure(text='''Affichage Des Produits''')
        self.titleLabel.configure(width=382)
        self._img7 = PhotoImage(file="images/ajout.png")
        self.titleLabel.configure(image=self._img7)

        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0

        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img1 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img1)



        self.Framebody = Frame(self.Frame1)
        self.Framebody.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1)

        self.Framebody.configure(relief=FLAT)
        self.Framebody.configure(borderwidth="2")
        self.Framebody.configure(relief=FLAT)
        self.Framebody.configure(background="#ffffff")
        self.Framebody.configure(highlightbackground="#ffffff")
        self.Framebody.configure(highlightcolor="black")
        self.Framebody.configure(width=745)

        self.Labelbody = Label(self.Framebody)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)

        self.QuantiteLabel = Label(self.Framebody)


        self.QuantiteLabel.place(relx=0.22, rely=0.51, height=34, width=104)
        self.QuantiteLabel.configure(activebackground="#f9f9f9")
        self.QuantiteLabel.configure(activeforeground="black")
        self.QuantiteLabel.configure(background="#ffffff")
        self.QuantiteLabel.configure(disabledforeground="#a3a3a3")
        self.QuantiteLabel.configure(font=font10)
        self.QuantiteLabel.configure(foreground="#000000")
        self.QuantiteLabel.configure(highlightbackground="#ffffff")
        self.QuantiteLabel.configure(highlightcolor="black")
        self.QuantiteLabel.configure(anchor=W)
        self.QuantiteLabel.configure(text='''Quantité: ''')

        self.NmpLabel = Label(self.Framebody)
        self.NmpLabel.place(relx=0.22, rely=0.06, height=34, width=200)
        self.NmpLabel.configure(activebackground="#f9f9f9")
        self.NmpLabel.configure(activeforeground="black")
        self.NmpLabel.configure(background="#ffffff")
        self.NmpLabel.configure(disabledforeground="#a3a3a3")
        self.NmpLabel.configure(font=font10)
        self.NmpLabel.configure(foreground="#000000")
        self.NmpLabel.configure(highlightbackground="#ffffff")
        self.NmpLabel.configure(highlightcolor="black")
        self.NmpLabel.configure(anchor=W)
        self.NmpLabel.configure(text='''Nom du produit:''')

        self.CheckbuttbmVar = IntVar()
        self.Checkbuttbm = Checkbutton(self.Framebody, variable=self.CheckbuttbmVar)
        self.CheckbuttbmVar.trace("w", self.updateDosage)
        self.Checkbuttbm.pack()
        self.Checkbuttbm.place(relx=0.45, rely=0.24, relheight=0.05, relwidth=0.02)
        self.Checkbuttbm.configure(activebackground="#ffffff")
        self.Checkbuttbm.configure(activeforeground="#ffffff")
        self.Checkbuttbm.configure(background="#ffffff")
        self.Checkbuttbm.configure(disabledforeground="#a3a3a3")
        self.Checkbuttbm.configure(foreground="#000000")
        self.Checkbuttbm.configure(highlightbackground="#ffffff")
        self.Checkbuttbm.configure(highlightcolor="black")
        self.Checkbuttbm.configure(anchor=W)
        self.Checkbuttbm.configure(variable=self.CheckbuttbmVar)
        self.Checkbuttbm.configure(text='''''')

        self.PdRestitueLabel = Label(self.Framebody)
        self.PdRestitueLabel.place(relx=0.22, rely=0.24, height=34, width=104)
        self.PdRestitueLabel.configure(activebackground="#f9f9f9")
        self.PdRestitueLabel.configure(activeforeground="black")
        self.PdRestitueLabel.configure(background="#ffffff")
        self.PdRestitueLabel.configure(disabledforeground="#a3a3a3")
        self.PdRestitueLabel.configure(font=font10)
        self.PdRestitueLabel.configure(foreground="#000000")
        self.PdRestitueLabel.configure(highlightbackground="#ffffff")
        self.PdRestitueLabel.configure(highlightcolor="black")
        self.PdRestitueLabel.configure(anchor=W)
        self.PdRestitueLabel.configure(text='''Bien etre''')


        self.EntryNmpVar = StringVar()
        self.EntryNmp = Combobox(self.Framebody,textvariable=  self.EntryNmpVar,values=self.liste_products )
        self.EntryNmp.place(relx=0.45, rely=0.06, relheight=0.06, relwidth=0.38)
        self.EntryNmp.configure(background="#ffffff")


        self.EntryQtVar = StringVar()
        self.EntryQt = Entry(self.Framebody,textvariable=  self.EntryQtVar )
        self.EntryQt.place(relx = 0.45, rely = 0.51, relheight = 0.06, relwidth = 0.38)
        self.EntryQt.configure(background="#ffffff")
        self.EntryQt.configure(disabledforeground="#a3a3a3")
        self.EntryQt.configure(font="TkFixedFont")
        self.EntryQt.configure(foreground="#000000")
        self.EntryQt.configure(highlightbackground="#ffffff")
        self.EntryQt.configure(highlightcolor="black")
        self.EntryQt.configure(insertbackground="black")
        self.EntryQt.configure(selectbackground="#c4c4c4")
        self.EntryQt.configure(borderwidth='1')
        self.EntryQt.configure(selectforeground="black")

        self.BtnConf1 = Button(self.Framebody)
        self.BtnConf1.place(relx=0.64, rely=0.86, height=40, width=180)
        self.BtnConf1.configure(activebackground="#ffffff")
        self.BtnConf1.configure(activeforeground="#000000")
        self.BtnConf1.configure(background="#ffffff")
        self.BtnConf1.configure(disabledforeground="#a3a3a3")
        self.BtnConf1.configure(font=font10)
        self.BtnConf1.configure(foreground="#000000")
        self.BtnConf1.configure(highlightbackground="#ffffff")
        self.BtnConf1.configure(highlightcolor="black")
        self.BtnConf1.configure(pady="0")
        self.BtnConf1.configure(relief=RIDGE)
        self.BtnConf1.configure(text='''Confirmer''')

        self.BtnConf1['command'] = self.submit

        self.DosageLabel = Label(self.Framebody)
        self.DosageLabel.place(relx=0.22, rely=0.15, height=34, width=200)
        self.DosageLabel.configure(activebackground="#f9f9f9")
        self.DosageLabel.configure(activeforeground="black")
        self.DosageLabel.configure(background="#ffffff")
        self.DosageLabel.configure(disabledforeground="#a3a3a3")
        self.DosageLabel.configure(font=font10)
        self.DosageLabel.configure(foreground="#000000")
        self.DosageLabel.configure(highlightbackground="#ffffff")
        self.DosageLabel.configure(highlightcolor="black")
        self.DosageLabel.configure(anchor=W)
        self.DosageLabel.configure(text='''Dosage:''')

        self.FormeLabel = Label(self.Framebody)
        self.FormeLabel.place(relx=0.22, rely=0.33, height=30, width=104)
        self.FormeLabel.configure(activebackground="#f9f9f9")
        self.FormeLabel.configure(activeforeground="black")
        self.FormeLabel.configure(background="#ffffff")
        self.FormeLabel.configure(disabledforeground="#a3a3a3")
        self.FormeLabel.configure(font=font10)
        self.FormeLabel.configure(foreground="#000000")
        self.FormeLabel.configure(highlightbackground="#ffffff")
        self.FormeLabel.configure(highlightcolor="black")
        self.FormeLabel.configure(anchor=W)
        self.FormeLabel.configure(text='''Forme:''')

        self.DateExpirationLabel = Label(self.Framebody)
        self.DateExpirationLabel.place(relx=0.22, rely=0.42, height=34, width=200)
        self.DateExpirationLabel.configure(activebackground="#f9f9f9")
        self.DateExpirationLabel.configure(activeforeground="black")
        self.DateExpirationLabel.configure(background="#ffffff")
        self.DateExpirationLabel.configure(disabledforeground="#a3a3a3")
        self.DateExpirationLabel.configure(font=font10)
        self.DateExpirationLabel.configure(foreground="#000000")
        self.DateExpirationLabel.configure(highlightbackground="#ffffff")
        self.DateExpirationLabel.configure(highlightcolor="black")
        self.DateExpirationLabel.configure(anchor=W)
        self.DateExpirationLabel.configure(text='''Date d'expiration:''')

        self.PdRestitueLabel = Label(self.Framebody)
        self.PdRestitueLabel.place(relx=0.22, rely=0.6, height=34, width=200)
        self.PdRestitueLabel.configure(activebackground="#f9f9f9")
        self.PdRestitueLabel.configure(activeforeground="black")
        self.PdRestitueLabel.configure(background="#ffffff")
        self.PdRestitueLabel.configure(disabledforeground="#a3a3a3")
        self.PdRestitueLabel.configure(font=font10)
        self.PdRestitueLabel.configure(foreground="#000000")
        self.PdRestitueLabel.configure(highlightbackground="#ffffff")
        self.PdRestitueLabel.configure(highlightcolor="black")
        self.PdRestitueLabel.configure(anchor=W)
        self.PdRestitueLabel.configure(text='''Le produit est restitué:''')

        self.EntryDosVar = StringVar()
        self.EntryDos = Entry(self.Framebody,textvariable= self.EntryDosVar )
        self.EntryDos.place(relx=0.45, rely=0.15, relheight=0.06, relwidth=0.38)
        self.EntryDos.configure(background="#ffffff")
        self.EntryDos.configure(disabledforeground="#a3a3a3")
        self.EntryDos.configure(font="TkFixedFont")
        self.EntryDos.configure(foreground="#000000")
        self.EntryDos.configure(highlightbackground="#ffffff")
        self.EntryDos.configure(highlightcolor="black")
        self.EntryDos.configure(insertbackground="black")
        self.EntryDos.configure(selectbackground="#c4c4c4")
        self.EntryDos.configure(borderwidth='1')
        self.EntryDos.configure(selectforeground="black")

        self.EntryLotVar = StringVar()
        self.EntryLot = Entry(self.Framebody, textvariable=self.EntryLotVar)
        self.EntryLot.place(relx=0.45, rely=0.69, relheight=0.06, relwidth=0.38)
        self.EntryLot.configure(background="#ffffff")
        self.EntryLot.configure(disabledforeground="#a3a3a3")
        self.EntryLot.configure(font="TkFixedFont")
        self.EntryLot.configure(foreground="#000000")
        self.EntryLot.configure(highlightbackground="#ffffff")
        self.EntryLot.configure(highlightcolor="black")
        self.EntryLot.configure(borderwidth='1')
        self.EntryLot.configure(insertbackground="black")
        self.EntryLot.configure(selectbackground="#c4c4c4")
        self.EntryLot.configure(selectforeground="black")



        self.EntryFormeVar = StringVar()
        # la liste des formes existentes :
        con = connectBdd()
        con.cur.execute("SELECT forme from produits ");
        e = con.cur.fetchall()
        self.liste_formes = []
        k = []
        for m in e:
            k.append(m[0])

        k = set(k)
        for i in k:
            self.liste_formes.append(i)
        con.fermer()
        # self.liste_formes = (
        # 'Comprime', 'Suppositoire', 'Sirop', 'Solution buvable', 'Gelule', 'Solution injectable', 'ComprimeEfferv',
        # 'Poudre', 'Liquide', 'Pommade', 'Gel', 'Sachet', 'Capsule', 'Goute', 'Ampoule', '')
        #self.liste_formes = ( 'Comprime', 'Suppositoire', 'Sirop', 'Solution buvable', 'Gelule', 'Solution injectable', 'ComprimeEfferv', 'Poudre', 'Liquide', 'Pommade', 'Gel', 'Sachet', 'Capsule', 'Goute', 'Ampoule', '')
        self.liste_formes = sorted(self.liste_formes)
        self.EntryForme = Combobox(self.Framebody, textvariable=self.EntryFormeVar, values=self.liste_formes,
                                   state="readonly")


        self.EntryForme.place(relx=0.45, rely=0.33, relheight=0.06, relwidth=0.38)
        self.EntryForme.configure(background="#ffffff")

        self.DateExp = DateEntry(self, width=30, background='#009D78',
                                foreground='#ffffff', borderwidth=2)
        self.DateExp.place(relx=0.45, rely=0.51, relheight=0.05, relwidth=0.38)



        self.restCheckVar = IntVar()
        self.Checkbutt = Checkbutton(self.Framebody,variable=self.restCheckVar)
        self.Checkbutt.pack()
        self.Checkbutt.place(relx=0.45, rely=0.6, relheight=0.05, relwidth=0.02)

        self.Checkbutt.configure(activebackground="#ffffff")
        self.Checkbutt.configure(activeforeground="#000000")
        self.Checkbutt.configure(background="#ffffff")
        self.Checkbutt.configure(disabledforeground="#a3a3a3")
        self.Checkbutt.configure(foreground="#000000")
        self.Checkbutt.configure(highlightbackground="#ffffff")
        self.Checkbutt.configure(highlightcolor="black")
        self.Checkbutt.configure(anchor=W)
        self.Checkbutt.configure(variable=self.restCheckVar)
        self.Checkbutt.configure(text='''''')


        self.BtnAnnul1 = Button(self.Framebody)
        self.BtnAnnul1.place(relx=0.17, rely=0.86, height=40, width=180)
        self.BtnAnnul1.configure(activebackground="#ffffff")
        self.BtnAnnul1.configure(activeforeground="#000000")
        self.BtnAnnul1.configure(background="#ffffff")
        self.BtnAnnul1.configure(disabledforeground="#a3a3a3")
        self.BtnAnnul1.configure(font=font10)
        self.BtnAnnul1.configure(foreground="#000000")
        self.BtnAnnul1.configure(highlightbackground="#ffffff")
        self.BtnAnnul1.configure(highlightcolor="black")
        self.BtnAnnul1.configure(pady="0")
        self.BtnAnnul1.configure(relief=RIDGE)
        self.BtnAnnul1.configure(text='''Annuler''')

        self.BtnAnnul1['command'] = self.retour








        self.VideformBtn = Button(self.Framebody)
        self.VideformBtn.place(relx=0.40, rely=0.86, height=40, width=180)
        self.VideformBtn.configure(activebackground="#ffffff")
        self.VideformBtn.configure(activeforeground="#000000")
        self.VideformBtn.configure(background="#ffffff")
        self.VideformBtn.configure(disabledforeground="#a3a3a3")
        self.VideformBtn.configure(font=font10)
        self.VideformBtn.configure(foreground="#000000")
        self.VideformBtn.configure(highlightbackground="#ffffff")
        self.VideformBtn.configure(highlightcolor="black")
        self.VideformBtn.configure(pady="0")
        self.VideformBtn.configure(relief=RIDGE)
        self.VideformBtn.configure(text='''Vider le formulaire''')

        self.VideformBtn['command'] = self.videForm

        self.LotLabel = Label(self.Framebody)
        self.LotLabel.place(relx=0.22, rely=0.69, height=30, width=140)
        self.LotLabel.configure(activebackground="#f9f9f9")
        self.LotLabel.configure(activeforeground="black")
        self.LotLabel.configure(background="#ffffff")
        self.LotLabel.configure(disabledforeground="#a3a3a3")
        self.LotLabel.configure(font=font10)
        self.LotLabel.configure(foreground="#000000")
        self.LotLabel.configure(highlightbackground="#ffffff")
        self.LotLabel.configure(highlightcolor="black")
        self.LotLabel.configure(anchor=W)
        self.LotLabel.configure(text='''Numéro de lot : ''')

    def submit(self):
        con = connectBdd()
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]

        if self.CheckbuttbmVar.get():
            bm = "b"
        else:
            bm = "m"
        if self.restCheckVar.get():
            r = 1
        else:
            r = 0
        #######################################################################################################"
        #on va vérifier les entrees:
        error=0
        #verification des types
        dosage=0
        forme=0
        #type du dosage

        if bm=="m":
            try:
                dosage=int(self.EntryDosVar.get())

            except:
                showerror("Erreur!","Le dosage doit être un nombre!")
                self.EntryDosVar.set(0)
                error=1
         # type de la quantite
        try:

            quantite = int(self.EntryQtVar.get())
        except:
            showerror("Erreur!", "La quantité doit être un nombre!")
            self.EntryQtVar.set(0)
            error = 1
        #type du nom
        try:
            name=int(self.EntryNmp.get())
            showerror("Erreur!","Le nom du produit doit être une chaine de caractères!")
            self.EntryNmpVar.set("")
            error=1
        except:
            pass
        #type de la forme
        try:
            name = int(self.EntryForme.get())
            showerror("Erreur!","La forme doit être une chaine de caractères!")
            self.EntryNmpVar.set("")
            error = 1
        except:
            pass
        #verification si la date de peromption est acceptable
        today = datetime.date.today( )
        #calcul de differences entre les dates
        if error==0:
            #var=(self.EntryDateVar.get())
            date1= self.DateExp.get()
            var=datetime.date(int(date1[6])*1000 + int(date1[7])*100 + int(date1[8])*10 + int(date1[9]),int(date1[3])*10 + int(date1[4]),int(date1[0])*10+ int(date1[1]))
           # var = str(str(date1[6]) + str(date1[7]) + str(date1[8]) + str(date1[9]) + "-" + str(date1[3]) + str(date1[4]) + "-" + str(date1[0]) + str(date1[1]))




            if(var>today):
                difference = (var.year - today.year)*12
                difference += (var.month- today.month)
                if difference < 1 and self.verification_date==0:
                    showinfo("Attention !", "La date d'expiration de ce produit est proche ! Veuillez reconfirmer son ajout en stock! ")
                    self.verification_date=1
                    error=1

            else :
                showerror("Erreur!", "Ce produit est périmé!")
                error=1




        #verification si les entrees ne sont pas vide
        if (self.EntryForme.get()=="" or self.EntryNmp.get()=="" or self.EntryQtVar.get()==0 or (dosage==0 and bm=="b") or self.EntryLotVar.get()=="" ):
            error=1
            showerror("Erreur!","Vous devez remplir tous les champs!")
        lot =self.EntryLotVar.get()

        verif_forme=["Gel","Gouttes","Liquide","Pommade","Solution buvable","Solution injectable","Sirop"]
        if error==0:
            if r and (self.EntryForme.get()in verif_forme) and self.verification_neuf==0:
                showinfo("Attention!", "Vérifiez que le produit entré est neuf! ")
                self.verification_neuf=1
                error=1
        if error==0:
            if bm =="b":
                d=0
            else :
                d=dosage
            e = con.ajoutexiste(nmP=self.EntryNmp.get(), forme=self.EntryForme.get(), dosage=int(d), b=bm, rest=r,
                                qte=quantite, date=var,cPh=cPh,lot=lot)
            self.verifiction_neuf=0
            if e:
                showinfo("Opération terminée!", "L'ajout en stock a été exécuté avec succès! ")
                self.controller.show_frame(gestionStock)

            if (not e):
                #on verifie le type de l'utilisateur
                var=self.controller.getPage(Login)
                if var.nomPharm[3]==1:
                     showinfo("Informations manquantes",
                         "Le produit que vous voulez ajouter n'existe pas! Veuillez entrer ses informations ")
                     self.AjoutNew()
                else :
                    showinfo("Informations manquantes",
                             "Le produit que vous voulez ajouter n'existe pas! Veuillez vous connecter avec un compte admin pour pouvoir les entrer ")
                    self.videForm()
                    self.controller.show_frame(gestionStock)








    def AjoutNew(self):
        ajout_new=self.controller.getPage(Ajout_dun_nouveau_produit)
        ajout_new.noProdVar.set(self.EntryNmp.get())
        ajout_new.formProd.set(self.EntryForme.get())
        if (self.EntryDos.get()!=""):
             ajout_new.dosageProd.set(int(self.EntryDos.get()))
        else:
            ajout_new.dosageProd.set(0)

        if(self.CheckbuttbmVar.get()==0):
           r = "m"
        else :
            r="b"
        ajout_new.bmProd.set(r)
        ajout_new.qteProd.set(int(self.EntryQt.get()))
        ajout_new.restProd.set(self.restCheckVar.get())
        ajout_new.lot.set(self.EntryLotVar.get())
        date1 = self.DateExp.get()
        var = datetime.date(int(date1[6]) * 1000 + int(date1[7]) * 100 + int(date1[8]) * 10 + int(date1[9]),int(date1[3]) * 10 + int(date1[4]), int(date1[0]) * 10 + int(date1[1]))

        ajout_new.dateProd.set(var)
        self.controller.show_frame(Ajout_dun_nouveau_produit)


#"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#'''''''''''''''''''''''''''''''''''         AJOUT NOUVEAU PRODUIT         '''''''''''''''''''''''''''''''''''''''''''''

class Ajout_dun_nouveau_produit(Frame):
    # ' pour les notifications'
    def GestionDeCompte(self):
        try:
            self.retour2()
        except:
            pass
        try:
            self.retour2()
        except:
            pass
        try:
            self.retour_perime()
        except:
            pass
        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()

    def notifs(self):
        if self.notif == 0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])

                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                          height=1, bg='white', anchor="w",
                          font=self.font12).grid(row=r,
                                                 column=1)
                    r = r + 1
                r = 0
                self.notif = 1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=818)
                self.supprnotifs.configure(activebackground="#009D78")
                self.supprnotifs.configure(activeforeground="#009D78")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command'] = self.supprimenotifs
            else:
                showinfo("Pas de notifications", "Vous n'avez pas de notifications !")

        else:
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif = 0

    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con = connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0

    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var = self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res:
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()

    def retour(self):
        self.master.master.show_frame(gestionStock)

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        font10 = "-family {Futura Bk BT} -size 20 -weight normal " \
                 "-slant roman -underline 0 -overstrike 0"
        font11 = "-family {Futura Bk BT} -size 12 -weight bold " \
                 "-slant roman -underline 0 -overstrike 0"
        font9 = "-family {Futura Bk BT} -size 12 -weight bold -slant" \
                " roman -underline 0 -overstrike 0"


        self.controller = controller

        ######################################     attributs    ##############################
        self.noProdVar=StringVar()
        self.formProd=StringVar()
        self.dosageProd=IntVar()
        self.bmProd=StringVar()
        self.qteProd=IntVar()
        self.dateProd=StringVar()
        self.restProd=IntVar()
        self.lot=StringVar()



        ######################################################################################



        self.Frame1 = Frame(self)
        self.Frame1.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#ffffff")
        self.Frame1.configure(highlightbackground="#ffffff")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=125)

        self.headFrame = Frame(self.Frame1)
        self.headFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.headFrame.configure(borderwidth="2")
        self.headFrame.configure(background="#009D78")
        self.headFrame.configure(highlightbackground="#ffffff")
        self.headFrame.configure(highlightcolor="black")
        self.headFrame.configure(width=935)
        self.headFrame.configure(relief=FLAT)


        self.titleLabel = Label(self.headFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(font=font11)
        self.titleLabel.configure(foreground="#fafafa")
        self.titleLabel.configure(text='''Affichage Des Produits''')
        self.titleLabel.configure(width=382)
        self._img7 = PhotoImage(file="images/ajout.png")
        self.titleLabel.configure(image=self._img7)
        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0

        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        self.bodyFrame = Frame(self.Frame1)
        self.bodyFrame.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1.0)
        self.bodyFrame.configure(relief=FLAT)
        self.bodyFrame.configure(borderwidth="2")
        self.bodyFrame.configure(relief=FLAT)
        self.bodyFrame.configure(background="#ffffff")
        self.bodyFrame.configure(highlightbackground="#ffffff")
        self.bodyFrame.configure(highlightcolor="black")
        self.bodyFrame.configure(width=745)

        self.Labelbody = Label(self.bodyFrame)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)

        self.categorieLabel = Label(self.bodyFrame)
        self.categorieLabel.place(relx=0.22, rely=0.06, height=25, width=200)
        self.categorieLabel.configure(activebackground="#f9f9f9")
        self.categorieLabel.configure(activeforeground="black")
        self.categorieLabel.configure(background="#ffffff")
        self.categorieLabel.configure(disabledforeground="#a3a3a3")
        self.categorieLabel.configure(font=font9)
        self.categorieLabel.configure(foreground="#000000")
        self.categorieLabel.configure(highlightbackground="#ffffff")
        self.categorieLabel.configure(highlightcolor="black")
        self.categorieLabel.configure(anchor=W)
        self.categorieLabel.configure(text='''Catégorie :''')

        self.laboratoireLabel = Label(self.bodyFrame)
        self.laboratoireLabel.place(relx=0.22, rely=0.15, height=34, width=200)
        self.laboratoireLabel.configure(activebackground="#f9f9f9")
        self.laboratoireLabel.configure(activeforeground="black")
        self.laboratoireLabel.configure(background="#ffffff")
        self.laboratoireLabel.configure(disabledforeground="#a3a3a3")
        self.laboratoireLabel.configure(font=font9)
        self.laboratoireLabel.configure(foreground="#000000")
        self.laboratoireLabel.configure(highlightbackground="#ffffff")
        self.laboratoireLabel.configure(highlightcolor="black")
        self.laboratoireLabel.configure(anchor=W)
        self.laboratoireLabel.configure(text='''Laboratoire :''')

        self.dciLabel = Label(self.bodyFrame)
        self.dciLabel.place(relx=0.22, rely=0.24, height=25, width=100)
        self.dciLabel.configure(activebackground="#f9f9f9")
        self.dciLabel.configure(activeforeground="black")
        self.dciLabel.configure(background="#ffffff")
        self.dciLabel.configure(disabledforeground="#a3a3a3")
        self.dciLabel.configure(font=font9)
        self.dciLabel.configure(foreground="#000000")
        self.dciLabel.configure(highlightbackground="#ffffff")
        self.dciLabel.configure(highlightcolor="black")
        self.dciLabel.configure(anchor=W)
        self.dciLabel.configure(text='''DCI :''')

        self.prixLabel = Label(self.bodyFrame)
        self.prixLabel.place(relx=0.22, rely=0.33, height=25, width=150)
        self.prixLabel.configure(activebackground="#f9f9f9")
        self.prixLabel.configure(activeforeground="black")
        self.prixLabel.configure(background="#ffffff")
        self.prixLabel.configure(disabledforeground="#a3a3a3")
        self.prixLabel.configure(font=font9)
        self.prixLabel.configure(foreground="#000000")
        self.prixLabel.configure(highlightbackground="#ffffff")
        self.prixLabel.configure(highlightcolor="black")
        self.prixLabel.configure(anchor=W)
        self.prixLabel.configure(text='''Prix :''')

        self.noticeLabel = Label(self.bodyFrame)
        self.noticeLabel.place(relx=0.22, rely=0.42, height=25, width=200)
        self.noticeLabel.configure(activebackground="#f9f9f9")
        self.noticeLabel.configure(activeforeground="black")
        self.noticeLabel.configure(background="#ffffff")
        self.noticeLabel.configure(disabledforeground="#a3a3a3")
        self.noticeLabel.configure(font=font9)
        self.noticeLabel.configure(foreground="#000000")
        self.noticeLabel.configure(highlightbackground="#ffffff")
        self.noticeLabel.configure(highlightcolor="black")
        self.noticeLabel.configure(anchor=W)
        self.noticeLabel.configure(text='''Notice :''')

        self.categorieEntryVar = StringVar()
        self.categorieEntry = Entry(self.bodyFrame,textvariable =self.categorieEntryVar )
        self.categorieEntry.place(relx=0.45, rely=0.06, relheight=0.06
                , relwidth=0.38)
        self.categorieEntry.configure(background="#ffffff")
        self.categorieEntry.configure(disabledforeground="#a3a3a3")
        self.categorieEntry.configure(font="TkFixedFont")
        self.categorieEntry.configure(foreground="#000000")
        self.categorieEntry.configure(highlightbackground="#ffffff")
        self.categorieEntry.configure(highlightcolor="black")
        self.categorieEntry.configure(borderwidth='1')
        self.categorieEntry.configure(insertbackground="black")

        self.categorieEntry.configure(selectbackground="#c4c4c4")
        self.categorieEntry.configure(selectforeground="black")

        self.laboratoireEntryVar = StringVar()
        self.laboratoireEntry = Entry(self.bodyFrame,textvariable=self.laboratoireEntryVar)
        self.laboratoireEntry.place(relx=0.45, rely=0.15, relheight=0.06
                , relwidth=0.38)
        self.laboratoireEntry.configure(background="#ffffff")
        self.laboratoireEntry.configure(disabledforeground="#a3a3a3")
        self.laboratoireEntry.configure(font="TkFixedFont")
        self.laboratoireEntry.configure(foreground="#000000")
        self.laboratoireEntry.configure(highlightbackground="#ffffff")
        self.laboratoireEntry.configure(highlightcolor="black")
        self.laboratoireEntry.configure(borderwidth='1')
        self.laboratoireEntry.configure(insertbackground="black")

        self.laboratoireEntry.configure(selectbackground="#c4c4c4")
        self.laboratoireEntry.configure(selectforeground="black")

        self.dciEntryVar = StringVar()
        self.dciEntry = Entry(self.bodyFrame, textvariable=self.dciEntryVar )
        self.dciEntry.place(relx=0.45, rely=0.24, relheight=0.06, relwidth=0.38)
        self.dciEntry.configure(background="#ffffff")
        self.dciEntry.configure(disabledforeground="#a3a3a3")
        self.dciEntry.configure(font="TkFixedFont")
        self.dciEntry.configure(foreground="#000000")
        self.dciEntry.configure(highlightbackground="#ffffff")
        self.dciEntry.configure(highlightcolor="black")
        self.dciEntry.configure(borderwidth='1')
        self.dciEntry.configure(insertbackground="black")

        self.dciEntry.configure(selectbackground="#c4c4c4")
        self.dciEntry.configure(selectforeground="black")

        self.prixEntryVar = DoubleVar()
        self.prixEntry = Entry(self.bodyFrame,textvariable=self.prixEntryVar)
        self.prixEntry.place(relx=0.45, rely=0.33, relheight=0.06, relwidth=0.38)
        self.prixEntry.configure(background="#ffffff")
        self.prixEntry.configure(disabledforeground="#a3a3a3")
        self.prixEntry.configure(font="TkFixedFont")
        self.prixEntry.configure(foreground="#000000")
        self.prixEntry.configure(highlightbackground="#ffffff")
        self.prixEntry.configure(highlightcolor="black")
        self.prixEntry.configure(borderwidth='1')
        self.prixEntry.configure(insertbackground="black")

        self.prixEntry.configure(selectbackground="#c4c4c4")
        self.prixEntry.configure(selectforeground="black")

        self.noticeEntryVar = StringVar()

        self.noticeEntry = Text(self.bodyFrame)
        self.noticeEntryVar.set(self.noticeEntry.get("1.0", END))

        self.noticeEntry.place(relx=0.45, rely=0.42, relheight=0.41
                , relwidth=0.38)
        self.noticeEntry.configure(background="#ffffff")
#        self.noticeEntry.configure(disabledforeground="#a3a3a3")
        self.noticeEntry.configure(font="TkFixedFont")
        self.noticeEntry.configure(foreground="#000000")
        self.noticeEntry.configure(highlightbackground="#ffffff")
        self.noticeEntry.configure(highlightcolor="black")
        self.noticeEntry.configure(borderwidth='1')

        self.noticeEntry.configure(insertbackground="black")

        self.noticeEntry.configure(selectbackground="#c4c4c4")
        self.noticeEntry.configure(selectforeground="black")
        self.noticeEntry.configure(wrap=WORD)



        self.annulerButton = Button(self.bodyFrame)
        self.annulerButton.place(relx=0.17, rely=0.86, height=40, width=180)
        self.annulerButton.configure(activebackground="#ffffff")
        self.annulerButton.configure(activeforeground="#000000")
        self.annulerButton.configure(background="#ffffff")
        self.annulerButton.configure(disabledforeground="#a3a3a3")
        self.annulerButton.configure(font=font11)
        self.annulerButton.configure(foreground="#000000")
        self.annulerButton.configure(highlightbackground="#ffffff")
        self.annulerButton.configure(highlightcolor="black")
        self.annulerButton.configure(relief=RIDGE)
        self.annulerButton.configure(pady="0")
        self.annulerButton.configure(text='''Annuler''')

        self.annulerButton['command'] = self.retour






        self.enregistrerButton = Button(self.bodyFrame)
        self.enregistrerButton.place(relx=0.64, rely=0.86, height=40, width=180)
        self.enregistrerButton.configure(activebackground="#ffffff")
        self.enregistrerButton.configure(activeforeground="#000000")
        self.enregistrerButton.configure(background="#ffffff")
        self.enregistrerButton.configure(disabledforeground="#a3a3a3")
        self.enregistrerButton.configure(font=font11)
        self.enregistrerButton.configure(foreground="#000000")
        self.enregistrerButton.configure(highlightbackground="#ffffff")
        self.enregistrerButton.configure(highlightcolor="black")
        self.enregistrerButton.configure(relief=RIDGE)
        self.enregistrerButton.configure(pady="0")
        self.enregistrerButton.configure(text='''Enregistrer''')

        self.enregistrerButton['command'] = self.submit

        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img1 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img1)



    def submit( self):

        con = connectBdd()
        error=0
        #vérification des types
        # le prix
        try:
            dosage=float(self.prixEntry.get())
        except:
            showerror("Erreur!","Le champs prix doit être un nombre!")
            self.prixEntryVar.set(0)
            error=1
        #la catégorie
        try:
            name=int(self.categorieEntry.get())
            showerror("Erreur!","Le champs catégorie doit être une chaine de caractères!")
            self.categorieEntryVar.set("")
            error=1
        except:
            pass
        # le laboratoire
        try:
            name = int(self.laboratoireEntry.get())
            showerror("Erreur!", "Le champs laboratoire doit être une chaine de caractères!")
            self.laboratoireEntryVar.set("")
            error = 1
        except:
            pass

        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        #la notice
        try:
            name = int(self.noticeEntry.get(1.0,'end-1c'))

            showerror("Erreur!", "Le champs notice doit être un texte!")
            self.noticeEntryVar.set("")
            error = 1

        except:
            pass
        # verification des champs vides
        if (self.categorieEntryVar.get()=="" or self.laboratoireEntryVar.get()==""or self.prixEntryVar.get==0 or self.dciEntryVar.get()==""):
            error=1
            showerror("Erreur!", "Les champs Catégorie, Laboratoire, Prix et Dci sont obligatoires!")


        if error==0:

           con.ajoutnew(nmP=self.noProdVar.get(), forme=self.formProd.get(), dosage=self.dosageProd.get(),b=self.bmProd.get(), rest=self.restProd.get(), qte=self.qteProd.get(),date=self.dateProd.get(), categorie=self.categorieEntryVar.get(), labo=self.laboratoireEntryVar.get(), prix=self.prixEntryVar.get(), dci=self.dciEntryVar.get(), notice=self.noticeEntry.get(1.0,'end-1c'),cPh=cPh,lot=self.lot.get())
           showinfo("Opération terminée!", "L'ajout en stock et l'enregistrement du produit ontété exécutés avec succès! ")
           self.controller.show_frame(gestionStock)

########################################################################################################################################
###############VENTE DE PRODUITS ##############################################################################################
#########################################################LA CLASSE ACHAT_Prod / VENTE #############################################################

class Achat_prod(Frame):
    # creation de facture
    def genereFacturePdf(self,prod, prixU, qte, qteG, infosPharm):
        packet = io.BytesIO()

        ttFich = "images/futuraMD.ttf"
        pdfmetrics.registerFont(TTFont("maFont", ttFich))

        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("maFont", 12)
        text = can.beginText(380, 802)
        text.textLine("Pharmacie   : ")
        text.textLine("Adresse     : ")
        text.textLine("Num de tél  : ")
        can.drawText(text)

        text = can.beginText(460, 802)
        i = 0
        j = 0

        while (j in range(len(infosPharm))):
            text.textLine(str(infosPharm[j]))
            j += 1

        can.drawText(text)
        can.setFont("maFont", 13)

        text = can.beginText(45, 450)

        i = 0
        j = 0

        while (j in range(len(prod))):
            text.textLine(str(prod[j]))
            text.textLine("")
            j += 1

        can.drawText(text)

        text = can.beginText(250, 450)

        j = 0
        while (j in range(len(prod))):
            text.textLine(str(prixU[j]))
            text.textLine("")
            j += 1

        can.drawText(text)

        text = can.beginText(350, 450)

        j = 0
        while (j in range(len(prod))):
            text.textLine(str(qte[j]))
            text.textLine("")
            j += 1

        can.drawText(text)

        text = can.beginText(430, 450)

        j = 0
        while (j in range(len(prod))):
            text.textLine(str(qteG[j]))
            text.textLine("")
            j += 1

        can.drawText(text)

        totals = [prixU[i] * qte[i] for i in range(len(prixU))]

        text = can.beginText(500, 450)

        j = 0
        while (j in range(len(prod))):
            text.textLine(str(totals[j]))
            text.textLine("")
            j += 1

        can.drawText(text)

        can.setFont("maFont", 20)
        if len(prod) == 1 or len(prod)==2:
            can.line(35, 450 - 40 * len(prod), 570, 450 - 40 * len(prod))
            can.line(35, 450 - 80 * len(prod), 570, 450 - 80 * len(prod))

            total = 0

            for t in totals:
                total += t

            can.drawString(320, 450 - 60 * len(prod), " Total à Payer :" + "    " + str(total))
        else:
            can.line(35, 450 - 35 * len(prod), 570, 450 - 35 * len(prod))
            can.line(35, 450 - 45 * len(prod), 570, 450 - 45 * len(prod))

            total = 0

            for t in totals:
                total += t

            can.drawString(320, 450 - 40 * len(prod), " Total à Payer :" + "    " + str(total))

        # can.drawImage("buy.png",inch,h-2*inch)
        can.save()

        packet.seek(0)
        newPdf = PdfFileReader(packet)
        oldPdf = PdfFileReader(open("images/facture.pdf", "rb"))
        output = PdfFileWriter()
        page = oldPdf.getPage(0)
        page.mergePage(newPdf.getPage(0))
        output.addPage(page)
        error=1
        while error==1:
            try:
                sortie = open("sortie.pdf", "wb")
                output.write(sortie)

                webbrowser.open("sortie.pdf")
                sortie.close()
                error =0
            except :
                showerror("Erreur ","Veuillez fermer l'ancienne facture")


    def retour(self):
        t=askyesno("Annuler","Etez-vous surs de vouloir annuler vos achats?")
        if (t):
            self.EntryQuantiteVar.set(0)
            self.CheckPrestitueVar.set(0)
            self.EntryNproduitVar.set("")


            self.CheckPrestitue1Var.set(0)

            self.master.master.show_frame(Transactions)
            self.donnees=[]
            self.variable=0





    def recup_nfd(self,entree):
        nom = str()
        forme = str()
        dosage = str()
        i = 0
        fi = 0
        di = 0
        ni = 0
        while entree[i] != " ":
            ni = ni + 1
            i = i + 1
        nom = entree[0:i]
        if entree[i+1]!="-":
            wi=i+1
            i=i+1
            while entree[i] != " ":
                ni = ni + 1
                i = i + 1
            nom=str(nom+" "+str(entree[wi:i]))


        i = i + 3
        w = i

        while entree[i] != " ":

            i = i + 1
        forme = entree[w:i]

        if entree[i+1]!="-":
            wi=i+1
            i=i+1
            while entree[i] != " ":
                ni = ni + 1
                i = i + 1
            forme=str(forme+" "+str(entree[wi:i]))


        i = i + 3
        w = i
        while entree[i] != " ":
            i = i + 1
        dosage = entree[w:i]
        try:
             dosage = int(dosage)
        except :
            dosage=0

        sortie = []
        sortie.append(nom)
        sortie.append(forme)
        sortie.append(dosage)
        return sortie

    def new(self):
        # on enregistre les donnees du formualre
        if self.variable==0:
            self.donnees[:]=[]
        self.variable=1
        error=0
        #on va verifier les entrees d'abord :
        dosage=0
        quantite=0
        #verification des types :
        # type de la quantité
        try:
            quantite = int(self.EntryQuantite.get())
        except:
            showerror("Erreur!", "La quantité doit être un nombre!")
            self.EntryQuantiteVar.set(0)
            error = 1
        con=connectBdd()

        #on verifie si les entrees ne sont pas vides
        if( quantite==0 or self.EntryNproduit.get()=="" ):
            error=1
            showerror("Erreur! ","Vous devez remplir tous les champs !")

        var = []
        if error==0:
            #on recupere le nom la forme et le dosage :
            liste=self.recup_nfd(self.EntryNproduit.get())

            name = liste[0]
            forme =liste[1]
            dosage=liste[2]
            # on verifie si le produit existe deja
            con=connectBdd()

            var.append(dosage)
            var.append(quantite)
            var.append(self.CheckPrestitueVar.get())
            var.append(name)
            var.append(forme)
            var.append(self.CheckPrestitue1Var.get())
            if dosage :
                bm="m"
            else :
                bm="b"
            var.append(bm)


            #on les ajoute a notre liste de donnees
            self.donnees.append(var)
            showinfo("Opération exectuée","Ce produit a été ajouté à votre panier !")


                #vider les entreeeeeeeeeeeeeee

            self.EntryQuantiteVar.set(0)
            self.CheckPrestitueVar.set(0)
            self.EntryNproduitVar.set("")
            self.CheckPrestitue1Var.set(0)
            self.master.master.show_frame(Achat_prod)
            con.fermer()
    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var=self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res :
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()






    def GestionDeCompte(self):

        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()

    def notifs(self):
        if self.notif == 0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])

                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                          height=1, bg='white', anchor="w",
                          font=self.font12).grid(row=r,
                                                 column=1)
                    r = r + 1
                r = 0
                self.notif = 1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=818)
                self.supprnotifs.configure(activebackground="#009D78")
                self.supprnotifs.configure(activeforeground="#3fa693")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command'] = self.supprimenotifs
            else:
                showinfo("Pas de notifications", "Vous n'avez pas de notifications !")

        else:
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif = 0

    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con = connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0


    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        font10 = "-family {Futura Bk BT} -size 20 -weight normal " \
                 "-slant roman -underline 0 -overstrike 0"

        font9 = "-family {Futura Bk BT} -size 12 -weight bold -slant" \
                " roman -underline 0 -overstrike 0"

        font11 = "-family {Futura Bk BT} -size 12 -weight bold -slant" \
                " roman -underline 0 -overstrike 0"
        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        font13 = "-family {Futura Bk BT} -size 11  -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.font13 = font13
        self.font11 = font11
        self.font10=font10


        #on genere la liste des produits existants:
        self.liste_produits=[]
        var = connectBdd()
        cur = var.cur
        cur.execute("""SELECT * FROM produits""")
        resultat1=cur.fetchall()
        var =[]
        self.liste_products=[]
        for inter in resultat1:
            var=[]
            if inter[1]=="b": #c'est un produit de bien être , on ne prend pas le dosage
                var =str(inter[3].lower().capitalize()+" - "+inter[7]+"       ")
            else :
                var= str(inter[3].lower().capitalize()+" - "+inter[7]+" - "+str(inter[6])+" (mg ou mg/l)")
            self.liste_products.append(var)

        self.liste_products=sorted(self.liste_products)











        self.controller=controller
        self.variable=0





        self.Frame1 = Frame(self)
        self.Frame1.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#ffffff")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=935)

        self.FrameTop = Frame(self.Frame1)
        self.FrameTop.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.FrameTop.configure(background="#009D78")
        self.FrameTop.configure(highlightbackground="#d9d9d9")
        self.FrameTop.configure(highlightcolor="black")
        self.FrameTop.configure(width=935)

        self.titleLabel = Label(self.FrameTop)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(foreground="#fafafa")
        self.titleLabel.configure(width=382)
        self._img7 = PhotoImage(file="images/vente_prod.png")
        self.titleLabel.configure(image=self._img7)
        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)
        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img1 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img1)





        self.Frame6 = Frame(self.Frame1)
        self.Frame6.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1.0)
        self.Frame6.configure(relief=FLAT)
        self.Frame6.configure(borderwidth="2")
        self.Frame6.configure(relief=FLAT)
        self.Frame6.configure(background="#ffffff")
        self.Frame6.configure(highlightbackground="#d9d9d9")
        self.Frame6.configure(highlightcolor="black")
        self.Frame6.configure(width=745)

        self.Labelbody = Label(self.Frame6)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)

        self.NpLabel = Label(self.Frame6)
        self.NpLabel.place(relx=0.22, rely=0.2, height=31, width=150)
        self.NpLabel.configure(activebackground="#f9f9f9")
        self.NpLabel.configure(activeforeground="#000000")
        self.NpLabel.configure(background="#ffffff")
        self.NpLabel.configure(disabledforeground="#a3a3a3")
        self.NpLabel.configure(font=font9)
        self.NpLabel.configure(anchor=W)
        self.NpLabel.configure(foreground="#000000")
        self.NpLabel.configure(highlightbackground="#d9d9d9")
        self.NpLabel.configure(highlightcolor="#000000")
        self.NpLabel.configure(text='''Produit :''')

        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0

        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        self.EntryNproduitVar= StringVar()
        self.EntryNproduit = Combobox(self.Frame6,textvariable=self.EntryNproduitVar,values=self.liste_products,
                                   state="readonly")
        self.EntryNproduit.place(relx=0.45, rely=0.2 , relheight=0.06
                                 , relwidth=0.38)
        self.EntryNproduit.configure(background="#FFFFFF")


        self.BtnConf1 = Button(self.Frame6)
        self.BtnConf1.place(relx=0.64, rely=0.86, height=40, width=180)
        self.BtnConf1.configure(activebackground="#d9d9d9")
        self.BtnConf1.configure(activeforeground="#000000")
        self.BtnConf1.configure(background="#ffffff")
        self.BtnConf1.configure(disabledforeground="#a3a3a3")
        self.BtnConf1.configure(font=font11)
        self.BtnConf1.configure(foreground="#000000")
        self.BtnConf1.configure(highlightbackground="#d9d9d9")
        self.BtnConf1.configure(highlightcolor="black")
        self.BtnConf1.configure(pady="0")
        self.BtnConf1.configure(relief=RIDGE)
        self.BtnConf1.configure(text='''Terminer''')

        self.BtnConf1['command'] = self.submit


        self.BtnAjout = Button(self.Frame6)
        self.BtnAjout.place(relx=0.40, rely=0.86, height=40, width=180)
        self.BtnAjout.configure(activebackground="#d9d9d9")
        self.BtnAjout.configure(activeforeground="#000000")
        self.BtnAjout.configure(background="#ffffff")
        self.BtnAjout.configure(disabledforeground="#a3a3a3")
        self.BtnAjout.configure(font=font11)
        self.BtnAjout.configure(foreground="#000000")
        self.BtnAjout.configure(highlightbackground="#d9d9d9")
        self.BtnAjout.configure(highlightcolor="black")
        self.BtnAjout.configure(pady="0")
        self.BtnAjout.configure(relief=RIDGE)
        self.BtnAjout.configure(text='''Ajouter produit''')
        self.BtnAjout['command'] = self.new


        self.EntryQuantiteVar= StringVar()
        self.EntryQuantite= Entry(self.Frame6,textvariable=self.EntryQuantiteVar)
        self.EntryQuantite.place(relx=0.45, rely=0.35, relheight=0.06
                                 , relwidth=0.38)
        self.EntryQuantite.configure(background="#FFFFFF")
        self.EntryQuantite.configure(disabledforeground="#a3a3a3")
        self.EntryQuantite.configure(font="TkFixedFont")
        self.EntryQuantite.configure(foreground="#000000")
        self.EntryQuantite.configure(highlightbackground="#d9d9d9")
        self.EntryQuantite.configure(highlightcolor="black")
        self.EntryQuantite.configure(insertbackground="black")
        self.EntryQuantite.configure(borderwidth='1')
        self.EntryQuantite.configure(selectbackground="#c4c4c4")
        self.EntryQuantite.configure(selectforeground="black")

        self.PprestitueLabel = Label(self.Frame6)
        self.PprestitueLabel.place(relx=0.22, rely=0.5, height=34, width=250)
        self.PprestitueLabel.configure(activebackground="#f9f9f9")
        self.PprestitueLabel.configure(activeforeground="black")
        self.PprestitueLabel.configure(background="#ffffff")
        self.PprestitueLabel.configure(disabledforeground="#a3a3a3")
        self.PprestitueLabel.configure(font=font9)
        self.PprestitueLabel.configure(foreground="#000000")
        self.PprestitueLabel.configure(highlightbackground="#d9d9d9")
        self.PprestitueLabel.configure(highlightcolor="black")
        self.PprestitueLabel.configure(justify=LEFT)
        self.PprestitueLabel.configure(anchor=W)
        self.PprestitueLabel.configure(text='''Prendre un produit réstitué :''')
        self.PprestitueLabel.configure(width=304)


        self.CheckPrestitueVar= IntVar()
        self.CheckPrestitue = Checkbutton(self.Frame6,variable=self.CheckPrestitueVar)
        self.CheckPrestitue.pack()
        self.CheckPrestitue.place(relx=0.5, rely=0.508, relheight=0.05
                                  , relwidth=0.02)
        self.CheckPrestitue.configure(activebackground="#d9d9d9")
        self.CheckPrestitue.configure(activeforeground="#000000")
        self.CheckPrestitue.configure(background="#ffffff")
        self.CheckPrestitue.configure(disabledforeground="#a3a3a3")
        self.CheckPrestitue.configure(foreground="#000000")
        self.CheckPrestitue.configure(highlightbackground="#ffffff")
        self.CheckPrestitue.configure(highlightcolor="black")
        self.CheckPrestitue.configure(justify=LEFT)
        self.CheckPrestitue.configure(width=91)




        self.CategorieLabel2 = Label(self.Frame6)
        self.CategorieLabel2.place(relx=0.22, rely=0.35, height=21, width=200)
        self.CategorieLabel2.configure(activebackground="#f9f9f9")
        self.CategorieLabel2.configure(activeforeground="black")
        self.CategorieLabel2.configure(background="#ffffff")
        self.CategorieLabel2.configure(disabledforeground="#a3a3a3")
        self.CategorieLabel2.configure(font=font9)
        self.CategorieLabel2.configure(foreground="#000000")
        self.CategorieLabel2.configure(highlightbackground="#d9d9d9")
        self.CategorieLabel2.configure(highlightcolor="black")
        self.CategorieLabel2.configure(anchor=W)
        self.CategorieLabel2.configure(text='''Quantité:''')






        self.PprestitueLabel1 = Label(self.Frame6)
        self.PprestitueLabel1.place(relx=0.22, rely=0.65, height=34, width=380)
        self.PprestitueLabel1.configure(activebackground="#f9f9f9")
        self.PprestitueLabel1.configure(activeforeground="black")
        self.PprestitueLabel1.configure(background="#ffffff")
        self.PprestitueLabel1.configure(disabledforeground="#a3a3a3")
        self.PprestitueLabel1.configure(font=font9)
        self.PprestitueLabel1.configure(foreground="#000000")
        self.PprestitueLabel1.configure(highlightbackground="#d9d9d9")
        self.PprestitueLabel1.configure(highlightcolor="black")
        self.PprestitueLabel1.configure(anchor=W)
        self.PprestitueLabel1.configure(text='''Faire une commande d'une autre pharamcie:''')
        self.PprestitueLabel1.configure(width=374)



        self.CheckPrestitue1Var= IntVar()
        self.CheckPrestitue1 = Checkbutton(self.Frame6,variable=self.CheckPrestitue1Var)
        self.CheckPrestitue1.pack()
        self.CheckPrestitue1.place(relx=0.65, rely=0.658, relheight=0.05
                                   , relwidth=0.02)
        self.CheckPrestitue1.configure(activebackground="#d9d9d9")
        self.CheckPrestitue1.configure(activeforeground="#000000")
        self.CheckPrestitue1.configure(background="#ffffff")
        self.CheckPrestitue1.configure(disabledforeground="#a3a3a3")
        self.CheckPrestitue1.configure(foreground="#000000")
        self.CheckPrestitue1.configure(highlightbackground="#ffffff")
        self.CheckPrestitue1.configure(highlightcolor="black")
        self.CheckPrestitue1.configure(justify=LEFT)
        self.CheckPrestitue1.configure(width=101)

        self.BtnAnnuler = Button(self.Frame6)
        self.BtnAnnuler.place(relx=0.17, rely=0.86, height=40, width= 180)
        self.BtnAnnuler.configure(activebackground="#d9d9d9")
        self.BtnAnnuler.configure(activeforeground="#000000")
        self.BtnAnnuler.configure(background="#ffffff")
        self.BtnAnnuler.configure(disabledforeground="#a3a3a3")
        self.BtnAnnuler.configure(font=font11)
        self.BtnAnnuler.configure(foreground="#000000")
        self.BtnAnnuler.configure(highlightbackground="#d9d9d9")
        self.BtnAnnuler.configure(highlightcolor="black")
        self.BtnAnnuler.configure(pady="0")
        self.BtnAnnuler.configure(relief=RIDGE)
        self.BtnAnnuler.configure(text='''Annuler''')

        self.BtnAnnuler['command'] = self.retour




        ################
        self.donnees=[]
        self.donnees1=[]
        self.r=[]
        self.boxVars = []
        self.rows = -1
        self.boxVars2 = []
        self.rows2 = -1

    def submit(self):

        error = 0
        if self.variable == 0:
            self.donnees[:] = []
        else:
            self.variable = 0

        # on va verifier les entrees d'abord :
        dosage = 0
        quantite = 0
        # verification des types :

        # type de la quantité
        try:
            quantite = int(self.EntryQuantite.get())
        except:
            showerror("Erreur!", "La quantité doit être un nombre!")
            self.EntryQuantiteVar.set(0)
            error = 1

        # on verifie si les entrees ne sont pas vides
        if (quantite == 0 or self.EntryNproduit.get() == ""):
            error = 1
            showerror("Erreur! ", "Vous devez remplir tous les champs !")
            if self.donnees:
                a=askyesno("","Voulez-vous terminer la vente et ignorer ce produit?")
                if a :
                    con = connectBdd()

                    r = con.listeProduits(self.donnees)

                    self.r = r
                    self.destruction1()
                    self.affichage1()
                else :
                    self.variable=1
        # on enregistre les donnees du dernier formualaire
        if error==0:
            acc = self.controller.getPage(Login)

            cPh = acc.nomPharm[2]

            con = connectBdd()
            con.mise_jour(cPh)


            var = []
            var[:]=[]

            liste = self.recup_nfd(self.EntryNproduit.get())

            name = liste[0]
            forme = liste[1]
            dosage = liste[2]

            var.append(dosage)
            if dosage :
                bm="m"
            else :
                bm="b"

            var.append(int(self.EntryQuantiteVar.get()))
            var.append(self.CheckPrestitueVar.get())
            var.append(name)
            var.append(forme)

            var.append(self.CheckPrestitue1Var.get())
            var.append(bm)
            self.EntryQuantiteVar.set(0)
            self.CheckPrestitueVar.set(0)
            self.EntryNproduitVar.set("")

            self.CheckPrestitue1Var.set(0)


            # on les ajoute a notre liste de donnees
            self.donnees.append(var)

            showinfo("Opération exécutée","Ce produit a été ajoué à votre panier !")
            con = connectBdd()

            r=con.listeProduits(self.donnees)

            self.r=r
            self.destruction1()
            self.affichage1()

            con.fermer()



        ###################autre page ##########################"""
    def destruction1(self):
        self.BtnAnnuler.destroy()
        self.BtnConf1.destroy()
        self.BtnAjout.destroy()
        try:
            self.Label6.destroy()
        except :
            pass

    def affichage1(self):


        self.rechButt = Button(self.Frame6)

        self.rechButt.place(relx=0.64, rely=0.86, height=40, width=200)
        self.rechButt.configure(activebackground="#FFFFFF")
        self.rechButt.configure(activeforeground="#000000")
        self.rechButt.configure(background="#ffffff")
        self.rechButt.configure(disabledforeground="#a3a3a3")
        self.rechButt.configure(font=self.font12)
        self.rechButt.configure(foreground="#000000")
        self.rechButt.configure(highlightbackground="#d9d9d9")
        self.rechButt.configure(highlightcolor="black")
        self.rechButt.configure(pady="0")
        self.rechButt.configure(relief=RIDGE)
        self.rechButt.configure(text='''Confirmer les d'achats''')
        self.rechButt['command'] = self.submit1

        self.retourButt = Button(self.Frame6)
        self.retourButt['command'] = self.retour2
        self.retourButt.place(relx=0.17, rely=0.86, height=40, width=180)

        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#FFFFFF")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(font=self.font12)
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#d9d9d9")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')

        con = connectBdd()


        ri = con.affichageConfimAchat(self.r)




        self.donnees[:] = []
        self.scrollable_canvas = ScrollableCanvas(self)
        self.scrollable_canvas.grid(row=1, column=1)
        self.scrollable_canvas.place(relx=0.03, rely=0.22)

        self.var = ('Nom Produit', 'Forme', 'Dosage', 'Quantité ', 'Commande', 'Prix Unité', 'Prix Total')
        self.donnees.append(self.var)
        for variable in ri:
            self.donnees.append(variable)

        r = 0
        for e in self.donnees:
            if r == 0:
                Label(self.scrollable_canvas.interior, text=e[0], relief=FLAT, width=16, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=0)

            else:
                Label(self.scrollable_canvas.interior, text=e[0], relief=RIDGE, width=16, height=1, bg='white',
                      font=self.font12).grid(row=r, column=0)
            r = r + 1

        r = 0
        for b in self.donnees:

            if r == 0:
                Label(self.scrollable_canvas.interior, text=b[1], relief=FLAT, width=14, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=1)
            else:
                Label(self.scrollable_canvas.interior, text=b[1], relief=RIDGE, width=14, height=1, bg='white',
                      font=self.font12).grid(row=r,
                                             column=1)
            r = r + 1
        r = 0
        for c in self.donnees:
            if r == 0:
                Label(self.scrollable_canvas.interior, text=c[2], relief=FLAT, width=8, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=2)
            else:
                Label(self.scrollable_canvas.interior, text=c[2], relief=RIDGE, width=8, height=1, bg='white',
                      font=self.font12).grid(row=r,
                                             column=2)
            r = r + 1
        r = 0
        for d in self.donnees:
            if r == 0:
                Label(self.scrollable_canvas.interior, text=d[3], relief=FLAT, width=12, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=3)
            else:
                Label(self.scrollable_canvas.interior, text=d[3], relief=RIDGE, width=12, height=1, bg='white',
                      font=self.font12).grid(row=r,
                                             column=3)
            r = r + 1
        r = 0
        for f in self.donnees:
            if r == 0:
                Label(self.scrollable_canvas.interior, text=f[4], relief=FLAT, width=10, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=4)
            else:
                if f[4]:
                    l = "oui"
                else:
                    l = "non"
                Label(self.scrollable_canvas.interior, text=l, relief=RIDGE, width=10, height=1, bg='white',
                      font=self.font12).grid(row=r,
                                             column=4)
            r = r + 1
        r = 0
        for g in self.donnees:
            if r == 0:
                Label(self.scrollable_canvas.interior, text=g[5], relief=FLAT, width=10, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=5)
            else:
                Label(self.scrollable_canvas.interior, text=g[5], relief=RIDGE, width=10, height=1, bg='white',
                      font=self.font12).grid(row=r,
                                             column=5)
            r = r + 1
        r = 0
        w=-1
        for h in self.donnees:
            if r == 0:
                Label(self.scrollable_canvas.interior, text=h[6], relief=FLAT, width=10, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=6)
            else:
                Label(self.scrollable_canvas.interior, text=h[6], relief=RIDGE, width=10, height=1, bg='white',
                      font=self.font12, command=self.check(w)).grid(row=r,
                                             column=6)
            r = r + 1
            w=w+1
        r = 0

        ################################################################################################
        self.boxVars = []
        self.rows = -1
        for k in self.donnees:
            self.rows += 1
        for i in range(self.rows):
            self.boxVars.append(IntVar())
            self.boxVars[i].set(1)
        y=0
        for h in self.donnees:
            if r == 0:
                Label(self.scrollable_canvas.interior, text='', relief=FLAT, width=4, height=2, bg='#009D78',
                      foreground="#ffffff", font=self.font12).grid(row=r,
                                                                   column=7)
            else:
                Checkbutton(self.scrollable_canvas.interior, width=2, height=1, bg='white',variable=self.boxVars[y],command=lambda y = y: self.check(y)).grid(row=r,column=7)
                y=y+1
            r = r + 1
        r = 0




    def check(self,i):
        if self.boxVars :

            var = self.boxVars[i]
            deselected = []
            if var.get() == 0:
                deselected.append(i)


    def retour1(self):
        a = askyesno("Quitter", "Etez-vous surs de vouloir quitter ?")
        if a :
            self.destruction2()

            self.BtnAnnuler = Button(self.Frame6)
            self.BtnAnnuler.place(relx=0.17, rely=0.86, height=40, width=180)
            self.BtnAnnuler.configure(activebackground="#d9d9d9")
            self.BtnAnnuler.configure(activeforeground="#000000")
            self.BtnAnnuler.configure(background="#ffffff")
            self.BtnAnnuler.configure(disabledforeground="#a3a3a3")
            self.BtnAnnuler.configure(font=self.font11)
            self.BtnAnnuler.configure(foreground="#000000")
            self.BtnAnnuler.configure(highlightbackground="#d9d9d9")
            self.BtnAnnuler.configure(highlightcolor="black")
            self.BtnAnnuler.configure(pady="0")
            self.BtnAnnuler.configure(relief=RIDGE)
            self.BtnAnnuler.configure(text='''Annuler''')
            self.BtnAnnuler['command'] = self.retour

            self.BtnConf1 = Button(self.Frame6)
            self.BtnConf1.place(relx=0.64, rely=0.86, height=40, width=180)
            self.BtnConf1.configure(activebackground="#d9d9d9")
            self.BtnConf1.configure(activeforeground="#000000")
            self.BtnConf1.configure(background="#ffffff")
            self.BtnConf1.configure(disabledforeground="#a3a3a3")
            self.BtnConf1.configure(font=self.font11)
            self.BtnConf1.configure(foreground="#000000")
            self.BtnConf1.configure(highlightbackground="#d9d9d9")
            self.BtnConf1.configure(highlightcolor="black")
            self.BtnConf1.configure(pady="0")
            self.BtnConf1.configure(relief=RIDGE)
            self.BtnConf1.configure(text='''Terminer''')

            self.BtnConf1['command'] = self.submit

            self.BtnAjout = Button(self.Frame6)
            self.BtnAjout.place(relx=0.40, rely=0.86, height=40, width=180)
            self.BtnAjout.configure(activebackground="#d9d9d9")
            self.BtnAjout.configure(activeforeground="#000000")
            self.BtnAjout.configure(background="#ffffff")
            self.BtnAjout.configure(disabledforeground="#a3a3a3")
            self.BtnAjout.configure(font=self.font11)
            self.BtnAjout.configure(foreground="#000000")
            self.BtnAjout.configure(highlightbackground="#d9d9d9")
            self.BtnAjout.configure(highlightcolor="black")
            self.BtnAjout.configure(pady="0")
            self.BtnAjout.configure(relief=RIDGE)
            self.BtnAjout.configure(text='''Ajouter produit''')
            self.BtnAjout['command'] = self.new


            self.controller.show_frame(Transactions)


    def retour5(self):
        a = askyesno("Quitter", "Etez-vous surs de vouloir quitter ?")
        if a :
            self.destruction2()
            self.titleLabel = Label(self.FrameTop)
            self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
            self.titleLabel.configure(background="#009D78")
            self.titleLabel.configure(disabledforeground="#a3a3a3")
            self.titleLabel.configure(foreground="#fafafa")
            self.titleLabel.configure(width=382)
            self._img7 = PhotoImage(file="images/vente_prod.png")
            self.titleLabel.configure(image=self._img7)
            font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                     "roman -underline 0 -overstrike 0"

            self.font12 = font12
            self.notif = 0

            self.notifications = []
            self.Buttongestcmp = Button(self.titleLabel)
            self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
            self.Buttongestcmp.configure(activebackground="#ffffff")
            self.Buttongestcmp.configure(activeforeground="#000000")
            self.Buttongestcmp.configure(background="#009D78")
            self.Buttongestcmp.configure(borderwidth="0")
            self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

            self.Buttongestcmp.configure(foreground="#808080")
            self.Buttongestcmp.configure(highlightbackground="#ffffff")
            self.Buttongestcmp.configure(highlightcolor="black")
            self.Buttongestcmp.configure(pady="0")
            self.Buttongestcmp.configure(text='''''')
            self.Buttongestcmp.configure(width=147)
            self.Buttongestcmp['command'] = self.GestionDeCompte
            self._img55 = PhotoImage(file="images/account.png")
            self.Buttongestcmp.configure(image=self._img55)

            self.Buttonnotif = Button(self.titleLabel)
            self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
            self.Buttonnotif.configure(activebackground="#ffffff")
            self.Buttonnotif.configure(activeforeground="#000000")
            self.Buttonnotif.configure(background="#009D78")
            self.Buttonnotif.configure(borderwidth="0")
            self.Buttonnotif.configure(disabledforeground="#a3a3a3")

            self.Buttonnotif.configure(foreground="#808080")
            self.Buttonnotif.configure(highlightbackground="#ffffff")
            self.Buttonnotif.configure(highlightcolor="black")
            self.Buttonnotif.configure(pady="0")
            self.Buttonnotif.configure(text='''''')
            self.Buttonnotif.configure(width=147)
            self.Buttonnotif['command'] = self.notifs
            self._img80 = PhotoImage(file="images/notifs.png")
            self.Buttonnotif.configure(image=self._img80)

            self.BtnAnnuler = Button(self.Frame6)
            self.BtnAnnuler.place(relx=0.17, rely=0.86, height=40, width=180)
            self.BtnAnnuler.configure(activebackground="#d9d9d9")
            self.BtnAnnuler.configure(activeforeground="#000000")
            self.BtnAnnuler.configure(background="#ffffff")
            self.BtnAnnuler.configure(disabledforeground="#a3a3a3")
            self.BtnAnnuler.configure(font=self.font11)
            self.BtnAnnuler.configure(foreground="#000000")
            self.BtnAnnuler.configure(highlightbackground="#d9d9d9")
            self.BtnAnnuler.configure(highlightcolor="black")
            self.BtnAnnuler.configure(pady="0")
            self.BtnAnnuler.configure(relief=RIDGE)
            self.BtnAnnuler.configure(text='''Annuler''')
            self.BtnAnnuler['command'] = self.retour

            self.BtnConf1 = Button(self.Frame6)
            self.BtnConf1.place(relx=0.64, rely=0.86, height=40, width=180)
            self.BtnConf1.configure(activebackground="#d9d9d9")
            self.BtnConf1.configure(activeforeground="#000000")
            self.BtnConf1.configure(background="#ffffff")
            self.BtnConf1.configure(disabledforeground="#a3a3a3")
            self.BtnConf1.configure(font=self.font11)
            self.BtnConf1.configure(foreground="#000000")
            self.BtnConf1.configure(highlightbackground="#d9d9d9")
            self.BtnConf1.configure(highlightcolor="black")
            self.BtnConf1.configure(pady="0")
            self.BtnConf1.configure(relief=RIDGE)
            self.BtnConf1.configure(text='''Terminer''')

            self.BtnConf1['command'] = self.submit

            self.BtnAjout = Button(self.Frame6)
            self.BtnAjout.place(relx=0.40, rely=0.86, height=40, width=180)
            self.BtnAjout.configure(activebackground="#d9d9d9")
            self.BtnAjout.configure(activeforeground="#000000")
            self.BtnAjout.configure(background="#ffffff")
            self.BtnAjout.configure(disabledforeground="#a3a3a3")
            self.BtnAjout.configure(font=self.font11)
            self.BtnAjout.configure(foreground="#000000")
            self.BtnAjout.configure(highlightbackground="#d9d9d9")
            self.BtnAjout.configure(highlightcolor="black")
            self.BtnAjout.configure(pady="0")
            self.BtnAjout.configure(relief=RIDGE)
            self.BtnAjout.configure(text='''Ajouter produit''')
            self.BtnAjout['command'] = self.new


            self.controller.show_frame(Transactions)





    def retour3(self):

         self.destruction2()
         self.BtnAnnuler = Button(self.Frame6)
         self.BtnAnnuler.place(relx=0.17, rely=0.86, height=40, width=180)
         self.BtnAnnuler.configure(activebackground="#d9d9d9")
         self.BtnAnnuler.configure(activeforeground="#000000")
         self.BtnAnnuler.configure(background="#ffffff")
         self.BtnAnnuler.configure(disabledforeground="#a3a3a3")
         self.BtnAnnuler.configure(font=self.font11)
         self.BtnAnnuler.configure(foreground="#000000")
         self.BtnAnnuler.configure(highlightbackground="#d9d9d9")
         self.BtnAnnuler.configure(highlightcolor="black")
         self.BtnAnnuler.configure(pady="0")
         self.BtnAnnuler.configure(relief=RIDGE)
         self.BtnAnnuler.configure(text='''Annuler''')
         self.BtnAnnuler['command'] = self.retour

         self.BtnConf1 = Button(self.Frame6)
         self.BtnConf1.place(relx=0.64, rely=0.86, height=40, width=180)
         self.BtnConf1.configure(activebackground="#d9d9d9")
         self.BtnConf1.configure(activeforeground="#000000")
         self.BtnConf1.configure(background="#ffffff")
         self.BtnConf1.configure(disabledforeground="#a3a3a3")
         self.BtnConf1.configure(font=self.font11)
         self.BtnConf1.configure(foreground="#000000")
         self.BtnConf1.configure(highlightbackground="#d9d9d9")
         self.BtnConf1.configure(highlightcolor="black")
         self.BtnConf1.configure(pady="0")
         self.BtnConf1.configure(relief=RIDGE)
         self.BtnConf1.configure(text='''Terminer''')

         self.BtnConf1['command'] = self.submit

         self.BtnAjout = Button(self.Frame6)
         self.BtnAjout.place(relx=0.40, rely=0.86, height=40, width=180)
         self.BtnAjout.configure(activebackground="#d9d9d9")
         self.BtnAjout.configure(activeforeground="#000000")
         self.BtnAjout.configure(background="#ffffff")
         self.BtnAjout.configure(disabledforeground="#a3a3a3")
         self.BtnAjout.configure(font=self.font11)
         self.BtnAjout.configure(foreground="#000000")
         self.BtnAjout.configure(highlightbackground="#d9d9d9")
         self.BtnAjout.configure(highlightcolor="black")
         self.BtnAjout.configure(pady="0")
         self.BtnAjout.configure(relief=RIDGE)
         self.BtnAjout.configure(text='''Ajouter produit''')
         self.BtnAjout['command'] = self.new




         self.controller.show_frame(Transactions)




    def retour2(self):
        a =askyesno("Annulation d'achats","Etez-vous surs de vouloir annuler vos achats ?")
        if a:
            self.destruction2()
            self.BtnAnnuler = Button(self.Frame6)
            self.BtnAnnuler.place(relx=0.17, rely=0.86, height=40, width=180)
            self.BtnAnnuler.configure(activebackground="#d9d9d9")
            self.BtnAnnuler.configure(activeforeground="#000000")
            self.BtnAnnuler.configure(background="#ffffff")
            self.BtnAnnuler.configure(disabledforeground="#a3a3a3")
            self.BtnAnnuler.configure(font=self.font11)
            self.BtnAnnuler.configure(foreground="#000000")
            self.BtnAnnuler.configure(highlightbackground="#d9d9d9")
            self.BtnAnnuler.configure(highlightcolor="black")
            self.BtnAnnuler.configure(pady="0")
            self.BtnAnnuler.configure(relief=RIDGE)
            self.BtnAnnuler.configure(text='''Annuler''')
            self.BtnAnnuler['command'] = self.retour

            self.BtnConf1 = Button(self.Frame6)
            self.BtnConf1.place(relx=0.64, rely=0.86, height=40, width=180)
            self.BtnConf1.configure(activebackground="#d9d9d9")
            self.BtnConf1.configure(activeforeground="#000000")
            self.BtnConf1.configure(background="#ffffff")
            self.BtnConf1.configure(disabledforeground="#a3a3a3")
            self.BtnConf1.configure(font=self.font11)
            self.BtnConf1.configure(foreground="#000000")
            self.BtnConf1.configure(highlightbackground="#d9d9d9")
            self.BtnConf1.configure(highlightcolor="black")
            self.BtnConf1.configure(pady="0")
            self.BtnConf1.configure(relief=RIDGE)
            self.BtnConf1.configure(text='''Terminer''')

            self.BtnConf1['command'] = self.submit

            self.BtnAjout = Button(self.Frame6)
            self.BtnAjout.place(relx=0.40, rely=0.86, height=40, width=180)
            self.BtnAjout.configure(activebackground="#d9d9d9")
            self.BtnAjout.configure(activeforeground="#000000")
            self.BtnAjout.configure(background="#ffffff")
            self.BtnAjout.configure(disabledforeground="#a3a3a3")
            self.BtnAjout.configure(font=self.font11)
            self.BtnAjout.configure(foreground="#000000")
            self.BtnAjout.configure(highlightbackground="#d9d9d9")
            self.BtnAjout.configure(highlightcolor="black")
            self.BtnAjout.configure(pady="0")
            self.BtnAjout.configure(relief=RIDGE)
            self.BtnAjout.configure(text='''Ajouter produit''')
            self.BtnAjout['command'] = self.new


            self.controller.show_frame(Transactions)


    def submit1(self):
        selection_medicaments=[]
        for i in range(self.rows):
            self.boxVars.append(IntVar())
            if (self.boxVars[i].get()==1):
                selection_medicaments.append(i)


        r6=[]
        r7=0
        for r8 in self.r :
            if r7 in selection_medicaments:
                r6.append(r8)
            r7+=1

        con = connectBdd()


        # on recupere le code de la pharmacie courante
        acc = self.controller.getPage(Login)

        cPh = acc.nomPharm[2]


        r2 = con.vente_de_produits(entree=r6,cPh=cPh)


        r3 = con.enregistreVente(entree=r2,cPh=cPh)


        r4 = con.facturation(r2)

        self.r=[]

        # verification si il y eu des achats
        for k in r4:
            if k[3]+k[4]>0:
                self.r.append(k)
        if self.r:

            pdf=self.prefacture(r4)

            showinfo("Opération terminée", "Opération Vente terminée avec succès, les produits non figurant dans la facture ne sont pas disponibles en stock!")
            self.genereFacturePdf(pdf[0], pdf[1], pdf[2], pdf[3], pdf[4])
        else :
            showinfo("opération terminée",'Produits non disponibles en stock')



        self.r=r4

            ########################################################appel creation facture direct #################################
        self.affichage2()
    def prefacture(self,entree):
        sortie=[]
        produits=[]
        prix=[]
        qte=[]
        qtr=[]
        pharmacie=[]
        for e in entree :
            if e[2]==0:
                infos=str(e[0]+" "+e[1])
            else :
                infos = str(e[0] + " " + e[1]+" "+str(e[2]))
            produits.append(infos)
            prix.append(e[7])
            qte.append(e[3])
            qtr.append(e[4])
        # les infos de la pharmacie
        var = self.controller.getPage(Login)
        moi = var.nomPharm[2]
        con=connectBdd()
        cur=con.cur
        cur.execute("SELECT * FROM contacts where code=%s",moi)
        e=cur.fetchall()
        pharmacie.append(e[0][0])
        pharmacie.append(e[0][1])
        pharmacie.append(e[0][2])
        sortie.append(produits)
        sortie.append(prix)
        sortie.append(qte)
        sortie.append(qtr)
        sortie.append(pharmacie)
        con.fermer()
        return sortie
    def destruction2(self):
        self.scrollable_canvas.destroy()

        self.rechButt.destroy()
        self.retourButt.destroy()
    def commande (self):
        font11=self.font11
        selection_medicaments = []
        for i in range(self.rows2):
            self.boxVars2.append(IntVar())
            if (self.boxVars2[i].get() == 1):
                selection_medicaments.append(i)


        k=0
        new=[]

        for i in self.r:
            if k  in selection_medicaments:
                if i[6] == "Oui" and i[7] > 0:
                    new.append(i)
            k=k+1

        #################on va effectuer les commandes
        con =connectBdd()
        #on recupere le code pharmacie

        var = self.controller.getPage(Login)
        moi = var.nomPharm[2]
        # on arrange la liste new pour faire les commandes
        mes_commandes=[]
        for i in new:
            if i[2]==0:
                bm="b"
            else:
                bm="m"
            var=[]
            var.append(i[2])
            var.append(i[5])
            var.append(i[0])
            var.append(i[1])
            var.append(bm)
            mes_commandes.append(var)

        sortie_commandes = con.commandes(mes_commandes, moi)

        # on enregistre les commandes
        con.faire_commandes(sortie_commandes)
        showinfo("Opération terminée","Vos commandes ont été executés avec succès !")
        self.destruction2()
        self.BtnAnnuler = Button(self.Frame6)
        self.BtnAnnuler.place(relx=0.17, rely=0.86, height=40, width=180)
        self.BtnAnnuler.configure(activebackground="#d9d9d9")
        self.BtnAnnuler.configure(activeforeground="#000000")
        self.BtnAnnuler.configure(background="#ffffff")
        self.BtnAnnuler.configure(disabledforeground="#a3a3a3")
        self.BtnAnnuler.configure(font=font11)
        self.BtnAnnuler.configure(foreground="#000000")
        self.BtnAnnuler.configure(highlightbackground="#d9d9d9")
        self.BtnAnnuler.configure(highlightcolor="black")
        self.BtnAnnuler.configure(pady="0")
        self.BtnAnnuler.configure(relief=RIDGE)
        self.BtnAnnuler.configure(text='''Annuler''')

        self.BtnAnnuler['command'] = self.retour

        self.BtnAjout = Button(self.Frame6)

        self.BtnAjout.place(relx=0.40, rely=0.86, height=40, width=180)
        self.BtnAjout.configure(activebackground="#d9d9d9")
        self.BtnAjout.configure(activeforeground="#000000")
        self.BtnAjout.configure(background="#ffffff")
        self.BtnAjout.configure(disabledforeground="#a3a3a3")
        self.BtnAjout.configure(font=font11)
        self.BtnAjout.configure(foreground="#000000")
        self.BtnAjout.configure(highlightbackground="#d9d9d9")
        self.BtnAjout.configure(highlightcolor="black")
        self.BtnAjout.configure(pady="0")
        self.BtnAjout.configure(relief=RIDGE)
        self.BtnAjout.configure(text='''Ajouter produit''')
        self.BtnAjout['command'] = self.new

        self.BtnConf1 = Button(self.Frame6)


        self.BtnConf1.place(relx=0.64, rely=0.86, height=40, width=180)
        self.BtnConf1.configure(activebackground="#d9d9d9")
        self.BtnConf1.configure(activeforeground="#000000")
        self.BtnConf1.configure(background="#ffffff")
        self.BtnConf1.configure(disabledforeground="#a3a3a3")
        self.BtnConf1.configure(font=font11)
        self.BtnConf1.configure(foreground="#000000")
        self.BtnConf1.configure(highlightbackground="#d9d9d9")
        self.BtnConf1.configure(highlightcolor="black")
        self.BtnConf1.configure(pady="0")
        self.BtnConf1.configure(relief=RIDGE)
        self.BtnConf1.configure(text='''Terminer''')

        self.BtnConf1['command'] = self.submit
        self.titleLabel = Label(self.FrameTop)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(foreground="#fafafa")
        self.titleLabel.configure(width=382)
        self._img7 = PhotoImage(file="images/vente_prod.png")
        self.titleLabel.configure(image=self._img7)

        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)


        self.controller.show_frame(Transactions)


    def affichage2(self):
        t=0
        d = []


        for i in self.r:

            if i[6]=="Oui" and i[5]!=0 :
                d.append(i)
                t=1

        if (t):
            self.destruction2()
            self.titlLabel = Label(self.FrameTop)
            self.titlLabel.place(relx=0.0, rely=0.0, height=150, width=935)
            self.titlLabel.configure(background="#009D78")
            self.titlLabel.configure(disabledforeground="#a3a3a3")
            self.titlLabel.configure(foreground="#fafafa")
            self.titlLabel.configure(text='''Recherche D'un Produit''')
            self.titlLabel.configure(width=462)
            self._img89 = PhotoImage(file="images/cmd.png")
            self.titlLabel.configure(image=self._img89)

            self.rechButt = Button(self.Frame6)
            self.notifications = []
            self.Buttongestcmp = Button(self.titleLabel)
            self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
            self.Buttongestcmp.configure(activebackground="#ffffff")
            self.Buttongestcmp.configure(activeforeground="#000000")
            self.Buttongestcmp.configure(background="#009D78")
            self.Buttongestcmp.configure(borderwidth="0")
            self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

            self.Buttongestcmp.configure(foreground="#808080")
            self.Buttongestcmp.configure(highlightbackground="#ffffff")
            self.Buttongestcmp.configure(highlightcolor="black")
            self.Buttongestcmp.configure(pady="0")
            self.Buttongestcmp.configure(text='''''')
            self.Buttongestcmp.configure(width=147)
            self.Buttongestcmp['command'] = self.GestionDeCompte
            self._img55 = PhotoImage(file="images/account.png")
            self.Buttongestcmp.configure(image=self._img55)


            #self.rechButt.bind("<Button-1>", self.submit)
            self.rechButt.place(relx=0.64, rely=0.86, height=40, width=180)

            self.rechButt.configure(activeforeground="#000000")
            self.rechButt.configure(background="#FFFFFF")
            self.rechButt.configure(disabledforeground="#a3a3a3")
            self.rechButt.configure(font=self.font12)
            self.rechButt.configure(foreground="#000000")
            self.rechButt.configure(highlightbackground="#d9d9d9")
            self.rechButt.configure(highlightcolor="black")
            self.rechButt.configure(pady="0")
            self.rechButt.configure(relief=RIDGE)
            self.rechButt.configure(text='''Confirmer''')
            self.rechButt.configure(width=176)
            self.rechButt['command'] = self.commande

            self.retourButt = Button(self.Frame6)
            self.retourButt['command'] = self.retour5

            self.retourButt.place(relx=0.17, rely=0.86, height=40, width=180)

            self.retourButt.configure(activeforeground="#000000")
            self.retourButt.configure(background="#FFFFFF")
            self.retourButt.configure(disabledforeground="#a3a3a3")
            self.retourButt.configure(font=self.font12)
            self.retourButt.configure(foreground="#000000")
            self.retourButt.configure(highlightbackground="#d9d9d9")
            self.retourButt.configure(highlightcolor="black")
            self.retourButt.configure(pady="0")
            self.retourButt.configure(relief=RIDGE)
            self.retourButt.configure(text='''Retour''')

            self.scrollable_canvas = ScrollableCanvas(self)
            self.scrollable_canvas.grid(row=1, column=1)
            self.scrollable_canvas.place(relx=0.06, rely=0.22)



            self.donnees[:] = []
            self.var = ('Nom Produit', 'Forme', 'Dosage', 'Quantité')
            self.donnees.append(self.var)
            for variable in d:
                self.donnees.append(variable)

            r = 0
            for e in self.donnees:
                if r == 0:
                    Label(self.scrollable_canvas.interior, text=e[0], relief=FLAT, width=27, height=2, bg='#009D78',
                          foreground="#ffffff", font=self.font12).grid(row=r,
                                                                       column=0)
                else:
                    Label(self.scrollable_canvas.interior, text=e[0], relief=RIDGE, width=27, height=1, bg='white',
                          font=self.font12).grid(row=r,
                                                 column=0)
                r = r + 1

            r = 0
            for b in self.donnees:

                if r == 0:
                    Label(self.scrollable_canvas.interior, text=b[1], relief=FLAT, width=15, height=2, bg='#009D78',
                          foreground="#ffffff", font=self.font12).grid(row=r,
                                                                       column=1)
                else:
                    Label(self.scrollable_canvas.interior, text=b[1], relief=RIDGE, width=15, height=1, bg='white',
                          font=self.font12).grid(row=r,
                                                 column=1)
                r = r + 1
            r = 0
            for c in self.donnees:
                if r == 0:
                    Label(self.scrollable_canvas.interior, text=c[2], relief=FLAT, width=15, height=2, bg='#009D78',
                          foreground="#ffffff", font=self.font12).grid(row=r,
                                                                       column=2)
                else:
                    Label(self.scrollable_canvas.interior, text=c[2], relief=RIDGE, width=15, height=1, bg='white',
                          font=self.font12).grid(row=r,
                                                 column=2)
                r = r + 1
            r = 0


            for g in self.donnees:
                if r == 0:
                    Label(self.scrollable_canvas.interior, text=g[3], relief=FLAT, width=15, height=2, bg='#009D78',
                          foreground="#ffffff", font=self.font12).grid(row=r,
                                                                       column=3)
                else:
                    Label(self.scrollable_canvas.interior, text=g[5], relief=RIDGE, width=15, height=1, bg='white',
                          font=self.font12).grid(row=r,
                                                 column=3)
                r = r + 1



            self.boxVars2 = []
            self.rows2 = -1
            for k in self.donnees:
                self.rows2 += 1
            for i in range(self.rows2):
                self.boxVars2.append(IntVar())
                self.boxVars2[i].set(1)
            r=0
            y = 0
            for h in self.donnees:
                if r == 0:
                    Label(self.scrollable_canvas.interior, text='', relief=FLAT, width=4, height=2, bg='#009D78',
                          foreground="#ffffff", font=self.font12).grid(row=r,
                                                                       column=4)
                else:
                    Checkbutton(self.scrollable_canvas.interior, width=2, height=1, bg='white', variable=self.boxVars2[y],
                                command=lambda y=y: self.check(y)).grid(row=r, column=4)
                    y = y + 1
                r = r + 1
            r = 0
        else :

            self.destruction2()
            self.retour3()



    def check(self, i):
        if self.boxVars2:

            var = self.boxVars2[i]
            deselected = []
            if var.get() == 0:

                deselected.append(i)

################################################################################################
class ScrollableCanvasNotifs(Frame):
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        canvas = Canvas(self, bg='#FFFFFF', width=700, height=220, scrollregion=(0, 0, 500, 500))

        vbar = Scrollbar(self, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=canvas.yview)
        canvas.config(width=845, height=210)
        canvas.config(yscrollcommand=vbar.set)
        canvas.pack(side=RIGHT, expand=True, fill=BOTH)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)

#######################################################################################################################################
class ScrollableCanvasReçue(Frame):
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        canvas = Canvas(self, bg='#FFFFFF', width=700, height=400, scrollregion=(0, 0, 500, 500))

        vbar = Scrollbar(self, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=canvas.yview)
        canvas.config(width=945, height=340)
        canvas.config(yscrollcommand=vbar.set)
        canvas.pack(side=RIGHT, expand=True, fill=BOTH)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)

###############################################################################################################
##################################################################################################################################""
class QuantiteLot(Frame):
    font11 = "-family {Futura Bk BT} -size 20 -weight bold -slant " \
             "roman -underline 0 -overstrike 0"
    font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
             "roman -underline 0 -overstrike 0"
    def retour(self):

        self.dosageEntryVar.set("")
        self.nmpEntryVar.set("")
        self.formeEntryVar.set("")
        self.master.master.show_frame(gestionStock)



    def retour2(self):
        font10 = "-family {Futura Bk BT} -size 20 -weight bold " \
                 "-slant roman -underline 0 -overstrike 0"
        font11 = "-family {Futura Bk BT} -size 11 -weight bold " \
                 "-slant roman -underline 0 -overstrike 0"
        font9 = "-family {Futura Bk BT} -size 12 -weight bold -slant" \
                " roman -underline 0 -overstrike 0"

        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        font13 = "-family {Futura Bk BT} -size 11  -slant " \
                 "roman -underline 0 -overstrike 0"
        self.dosageEntryVar.set("")
        self.nmpEntryVar.set("")
        self.formeEntryVar.set("")

        try:
            self.scrollable_canvas.destroy()
            self.ttitle1.destroy()
            self.retourButt1.destroy()
        except:
            pass

        self.nmpLabel = Label(self.bodyFrame)
        self.nmpLabel.place(relx=0.22, rely=0.15, height=35, width=174)
        self.nmpLabel.configure(anchor=W)
        self.nmpLabel.configure(background="#ffffff")
        self.nmpLabel.configure(disabledforeground="#fafafa")
        self.nmpLabel.configure(font=font12)
        self.nmpLabel.configure(foreground="#000000")
        self.nmpLabel.configure(text='''Nom Du Produit :''')
        self.nmpLabel.configure(width=202)

        # on genere la liste des produits existants:
        self.liste_produits = []
        var = connectBdd()
        cur = var.cur
        cur.execute("""SELECT nomProduit FROM produits""")
        resultat1 = cur.fetchall()

        for inter in resultat1:
            for inter2 in inter:
                var = inter2.lower().capitalize()
                self.liste_produits.append(var)

        self.liste_produits = sorted(self.liste_produits)
        # on supprime les doublants dans cette liste:
        self.inter = ""
        self.liste_products = []
        for produit in self.liste_produits:
            if produit != self.inter:
                self.liste_products.append(produit)
                self.inter = produit

        self.bodyFrame = self.bodyFrame
        self.nmpEntryVar = StringVar()
        self.nmpEntry = Combobox(self.bodyFrame, textvariable=self.nmpEntryVar, values=self.liste_products,
                                 state="readonly")
        self.nmpEntry.place(relx=0.45, rely=0.15, relheight=0.06
                            , relwidth=0.38)
        self.nmpEntry.configure(background="#ffffff")

        self.dosageLabel = Label(self.bodyFrame)
        self.dosageLabel.place(relx=0.22, rely=0.33, height=35, width=174)
        self.dosageLabel.configure(activebackground="#fafafa")
        self.dosageLabel.configure(activeforeground="black")
        self.dosageLabel.configure(anchor=W)
        self.dosageLabel.configure(background="#ffffff")
        self.dosageLabel.configure(disabledforeground="#a3a3a3")
        self.dosageLabel.configure(font=font12)
        self.dosageLabel.configure(foreground="#000000")
        self.dosageLabel.configure(highlightbackground="#ffffff")
        self.dosageLabel.configure(highlightcolor="black")
        self.dosageLabel.configure(text='''Numéro de Lot  :''')
        self.dosageLabel.configure(width=112)

        self.dosageEntryVar = StringVar()
        self.dosageEntry = Entry(self.bodyFrame, textvariable=self.dosageEntryVar)
        self.dosageEntry.place(relx=0.45, rely=0.33, relheight=0.06
                               , relwidth=0.38)
        self.dosageEntry.configure(background="#ffffff")
        self.dosageEntry.configure(disabledforeground="#a3a3a3")
        self.dosageEntry.configure(font=font12)
        self.dosageEntry.configure(foreground="#000000")
        self.dosageEntry.configure(highlightbackground="#ffffff")
        self.dosageEntry.configure(highlightcolor="black")
        self.dosageEntry.configure(insertbackground="black")
        self.dosageEntry.configure(selectbackground="#c4c4c4")
        self.dosageEntry.configure(selectforeground="black")

        self.formeLabel = Label(self.bodyFrame)
        self.formeLabel.place(relx=0.22, rely=0.51, height=35, width=174)
        self.formeLabel.configure(activebackground="#f9f9f9")
        self.formeLabel.configure(activeforeground="black")
        self.formeLabel.configure(anchor=W)
        self.formeLabel.configure(background="#ffffff")
        self.formeLabel.configure(disabledforeground="#a3a3a3")
        self.formeLabel.configure(font=font12)
        self.formeLabel.configure(foreground="#000000")
        self.formeLabel.configure(highlightbackground="#ffffff")
        self.formeLabel.configure(highlightcolor="black")
        self.formeLabel.configure(text='''Forme   :''')

        self.formeEntryVar = StringVar()
        con = connectBdd()
        con.cur.execute("SELECT forme from produits ")
        e = con.cur.fetchall()
        self.liste_formes = []
        k = []
        for m in e:
            k.append(m[0])

        k = set(k)
        for i in k:
            self.liste_formes.append(i)
        con.fermer()
        # self.liste_formes = (
        # 'Comprime', 'Suppositoire', 'Sirop', 'Solution buvable', 'Gelule', 'Solution injectable', 'ComprimeEfferv',
        # 'Poudre', 'Liquide', 'Pommade', 'Gel', 'Sachet', 'Capsule', 'Goute', 'Ampoule', '')

        self.liste_formes = sorted(self.liste_formes)
        self.formeEntry = Combobox(self.bodyFrame, textvariable=self.formeEntryVar, values=self.liste_formes,
                                   state="readonly")

        self.formeEntry.place(relx=0.45, rely=0.51, relheight=0.06, relwidth=0.38)
        self.formeEntry.configure(background="#ffffff")


        self.rechButt = Button(self.bodyFrame)
        self.rechButt.place(relx=0.64, rely=0.86, height=40, width=180)

        self.rechButt.configure(activebackground="#d9d9d9")
        self.rechButt.configure(activeforeground="#000000")
        self.rechButt.configure(background="#ffffff")
        self.rechButt.configure(borderwidth="2")
        self.rechButt.configure(disabledforeground="#a3a3a3")
        self.rechButt.configure(font=font12)
        self.rechButt.configure(foreground="#000000")
        self.rechButt.configure(highlightbackground="#ffffff")
        self.rechButt.configure(highlightcolor="black")
        self.rechButt.configure(pady="0")
        self.rechButt.configure(relief=RIDGE)
        self.rechButt.configure(text='''Confirmer''')
        self.rechButt.config(command=self.submit)


        self.retourButt = Button(self.bodyFrame)
        self.retourButt.place(relx=0.17, rely=0.86, height=40, width=180)
        self.retourButt.configure(activebackground="#d9d9d9")
        self.retourButt.configure(font=font12)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')
        self.retourButt.configure(pady="0")
        self.retourButt.config(command=self.retour)
        self.controller.show_frame(gestionStock)


    def submit(self):

        con=connectBdd()
        acc=self.controller.getPage(Login)
        cPh=acc.nomPharm[2]
        error=0
        #on verifie les entrees

        if (self.formeEntryVar.get()=="" or self.nmpEntryVar.get()==""or self.dosageEntryVar.get()=="" ):
            showerror("Erreur","Vous devez remplir tous les champs !")
            error=1
        else:
            pass
        if error==0 and con.quantiteLot(self.dosageEntryVar.get(),self.nmpEntryVar.get(),cPh,self.formeEntryVar.get()):
            con.fermer()


            self.retourButt1 = Button(self.bodyFrame)

            self.retourButt1.place(relx=0.4, rely=0.86, height=40, width=180)
            self.retourButt1.configure(activebackground="#d9d9d9")
            self.retourButt1.configure(activeforeground="#000000")
            self.retourButt1.configure(background="#ffffff")
            self.retourButt1.configure(disabledforeground="#a3a3a3")
            self.retourButt1.configure(font=self.font12)
            self.retourButt1.configure(foreground="#000000")
            self.retourButt1.configure(highlightbackground="#ffffff")
            self.retourButt1.configure(highlightcolor="black")
            self.retourButt1.configure(pady="0")
            self.retourButt1.configure(relief=RIDGE)
            self.retourButt1.configure(text='''Retour''')

            self.titlLabel = Label(self.headFrame)
            self.titlLabel.place(relx=0.0, rely=0.0, height=150, width=935)
            self.titlLabel.configure(background="#009D78")
            self.titlLabel.configure(disabledforeground="#a3a3a3")
            self.titlLabel.configure(foreground="#fafafa")
            self.titlLabel.configure(text='''Recherche D'un Produit''')
            self.titlLabel.configure(width=462)
            self._img89 = PhotoImage(file="images/lotqt.png")
            self.titlLabel.configure(image=self._img89)

            self.retourButt1['command'] = self.retour2
            con = connectBdd()

            # on recupere le code de la pharmacie courante
            acc = self.controller.getPage(Login)
            cPh = acc.nomPharm[2]

            ri = con.quantiteLot(nmP=self.nmpEntry.get(), forme=self.formeEntry.get()
                                , numlot=self.dosageEntry.get(),cPh=cPh)
            lot=self.dosageEntryVar.get()
            nom=self.nmpEntryVar.get()
            forme= self.formeEntryVar.get()
            self.dosageEntry.destroy()
            self.retourButt.destroy()
            self.nmpEntry.destroy()
            self.rechButt.destroy()
            self.formeEntry.destroy()
            self.titleLabel.destroy()
            self.dosageLabel.destroy()
            self.formeLabel.destroy()
            self.nmpLabel.destroy()

            self.donnees[:] = []
            self.scrollable_canvas = ScrollableCanvas4(self)
            self.scrollable_canvas.grid(row=1, column=1)
            self.scrollable_canvas.place(relx=0.08, rely=0.4)

            self.var = ('Produits neufs', 'Produits restitués', 'Total')
            for h in self.var:
                self.donnees.append(h)
            for variable in ri:
                self.donnees.append(variable)


            Label(self.scrollable_canvas.interior, text=self.donnees[0], relief=FLAT, width=25, height=4, bg='#009D78',
                  foreground="#ffffff", font=self.font12).grid(row=0,
                                                               column=0)

            Label(self.scrollable_canvas.interior, text=self.donnees[3], relief=RIDGE, width=25, height=4, bg='white',
                  font=self.font12).grid(row=1,
                                         column=0)

            Label(self.scrollable_canvas.interior, text=self.donnees[1], relief=FLAT, width=25, height=4, bg='#009D78',
                  foreground="#ffffff", font=self.font12).grid(row=0,
                                                               column=1)

            Label(self.scrollable_canvas.interior, text=self.donnees[4], relief=RIDGE, width=25, height=4, bg='white',
                  font=self.font12).grid(row=1,
                                         column=1)

            Label(self.scrollable_canvas.interior, text=self.donnees[2], relief=FLAT, width=25, height=4, bg='#009D78',
                  foreground="#ffffff", font=self.font12).grid(row=0,
                                                               column=2)

            Label(self.scrollable_canvas.interior, text=self.donnees[5], relief=RIDGE, width=25, height=4, bg='white',
                  font=self.font12).grid(row=1,
                                         column=2)

            self.ttitle1 = Label(self.bodyFrame)
            self.ttitle1.place(relx=0.25, rely=0.02, height=70, width=500)
            self.ttitle1.configure(activebackground="#336464")
            self.ttitle1.configure(activeforeground="white")
            self.ttitle1.configure(activeforeground="black")
            self.ttitle1.configure(background="#009D78")
            self.ttitle1.configure(disabledforeground="#a3a3a3")
            self.ttitle1.configure(font=self.font12)
            self.ttitle1.configure(foreground="#ffffff")
            self.ttitle1.configure(highlightbackground="#ffffff")
            self.ttitle1.configure(highlightcolor="black")
            self.ttitle1.configure(text='''La quantité du lot ''' +lot+''' du produit ''' +nom.upper().capitalize()  + forme.upper().capitalize())
        else :
            showinfo("Produit indisponible","Ce produit n'existe pas !")

    def GestionDeCompte(self):
        self.master.master.show_frame(Gestion_de_compte)
        self.verif_notif()

    def notifs(self):
        if self.notif == 0:
            # on verifie le nombre de notifications
            con = connectBdd()
            cur = con.cur
            var = self.controller.getPage(Login)
            cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
            res = cur.fetchall()
            if res:

                self.scrollable_canvasn = ScrollableCanvasNotifs(self)
                self.scrollable_canvasn.grid(row=1, column=1)
                self.scrollable_canvasn.place(relx=0.10, rely=0.22)

                self.notifications[:] = []

                for variable in res:
                    self.notifications.append(variable[1])

                r = 0
                for b in self.notifications:
                    Label(self.scrollable_canvasn.interior, text=b.upper().capitalize(), relief=FLAT, width=81,
                          height=1, bg='white', anchor="w",
                          font=self.font12).grid(row=r,
                                                 column=1)
                    r = r + 1
                r = 0
                self.notif = 1
                # un bouron pour supprimer les notifications
                self.supprnotifs = Button(self)
                self.supprnotifs.place(relx=0.1, rely=0.52, height=31, width=818)
                self.supprnotifs.configure(activebackground="#3fa693")
                self.supprnotifs.configure(activeforeground="#009D78")
                self.supprnotifs.configure(background="#009D78")
                self.supprnotifs.configure(borderwidth="1")
                self.supprnotifs.configure(disabledforeground="#a3a3a3")
                self.supprnotifs.configure(font=self.font12)
                self.supprnotifs.configure(foreground="#000000")
                self.supprnotifs.configure(highlightbackground="#ffffff")
                self.supprnotifs.configure(highlightcolor="black")
                self.supprnotifs.configure(pady="0")
                self.supprnotifs.configure(text='''Supprimer les notifications''')
                self.supprnotifs.configure(width=147)
                self.supprnotifs.configure(relief=RIDGE)
                self.supprnotifs['command'] = self.supprimenotifs
            else:
                showinfo("Pas de notifications", "Vous n'avez pas de notifications !")

        else:
            self.scrollable_canvasn.destroy()
            self.supprnotifs.destroy()
            self.notif = 0

    def supprimenotifs(self):
        acc = self.controller.getPage(Login)
        cPh = acc.nomPharm[2]
        con = connectBdd()
        con.supprimeNotifs(cPh)
        con.fermer()
        self.scrollable_canvasn.destroy()
        self.supprnotifs.destroy()
        self.notif = 0

    def verif_notif(self):
        # on verifie le nombre de notifications
        con = connectBdd()
        cur = con.cur
        var = self.controller.getPage(Login)
        cur.execute('''SELECT * from notifications where code=%s;''', (var.nomPharm[2]))
        res = cur.fetchall()
        k = 0
        if res:
            if res[0]:
                if res[0][0]:
                    for i in res:
                        k += 1

        if var.nombrenotifs < k:
            var.nombrenotifs = k
            showinfo("Notifcations", "Vous avez de nouvelles notifications !")
        con.fermer()

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller

        font11 = "-family {Futura Bk BT} -size 20 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"
        #####################
        self.donnees = []
        self.donnees1 = []
        self.r = []
        #################
        self.headFrame = Frame(self)
        self.headFrame.place(relx=0.0, rely=0.0, relheight=0.28, relwidth=1.0)
        self.headFrame.configure(relief=FLAT)
        self.headFrame.configure(borderwidth="2")
        self.headFrame.configure(relief=FLAT)
        self.headFrame.configure(background="#009D78")
        self.headFrame.configure(width=950)

        self.titleLabel = Label(self.headFrame)
        self.titleLabel.place(relx=0.0, rely=0.0, height=150, width=935)
        self.titleLabel.configure(background="#009D78")
        self.titleLabel.configure(disabledforeground="#a3a3a3")
        self.titleLabel.configure(font=font11)
        self.titleLabel.configure(foreground="#fafafa")
        self.titleLabel.configure(text='''Recherche D'un Produit''')
        self.titleLabel.configure(width=462)
        self._img88 = PhotoImage(file="images/lotqt.png")
        self.titleLabel.configure(image=self._img88)


        font12 = "-family {Futura Bk BT} -size 12 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        self.font12 = font12
        self.notif = 0


        self.notifications = []
        self.Buttongestcmp = Button(self.titleLabel)
        self.Buttongestcmp.place(relx=0.93, rely=0.6, height=50, width=50)
        self.Buttongestcmp.configure(activebackground="#ffffff")
        self.Buttongestcmp.configure(activeforeground="#000000")
        self.Buttongestcmp.configure(background="#009D78")
        self.Buttongestcmp.configure(borderwidth="0")
        self.Buttongestcmp.configure(disabledforeground="#a3a3a3")

        self.Buttongestcmp.configure(foreground="#808080")
        self.Buttongestcmp.configure(highlightbackground="#ffffff")
        self.Buttongestcmp.configure(highlightcolor="black")
        self.Buttongestcmp.configure(pady="0")
        self.Buttongestcmp.configure(text='''''')
        self.Buttongestcmp.configure(width=147)
        self.Buttongestcmp['command'] = self.GestionDeCompte
        self._img55 = PhotoImage(file="images/account.png")
        self.Buttongestcmp.configure(image=self._img55)

        self.Buttonnotif = Button(self.titleLabel)
        self.Buttonnotif.place(relx=0.87, rely=0.6, height=50, width=50)
        self.Buttonnotif.configure(activebackground="#ffffff")
        self.Buttonnotif.configure(activeforeground="#000000")
        self.Buttonnotif.configure(background="#009D78")
        self.Buttonnotif.configure(borderwidth="0")
        self.Buttonnotif.configure(disabledforeground="#a3a3a3")

        self.Buttonnotif.configure(foreground="#808080")
        self.Buttonnotif.configure(highlightbackground="#ffffff")
        self.Buttonnotif.configure(highlightcolor="black")
        self.Buttonnotif.configure(pady="0")
        self.Buttonnotif.configure(text='''''')
        self.Buttonnotif.configure(width=147)
        self.Buttonnotif['command'] = self.notifs
        self._img80 = PhotoImage(file="images/notifs.png")
        self.Buttonnotif.configure(image=self._img80)

        self.footFrame = Frame(self)
        self.footFrame.place(relx=0, rely=0.92, relheight=0.1, relwidth=1)
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(borderwidth="1")
        self.footFrame.configure(relief=GROOVE)
        self.footFrame.configure(background="#ffffff")
        self.footFrame.configure(width=935)

        self.Labelfoot = Label(self.footFrame)
        self.Labelfoot.place(relx=0.0, rely=0.0, height=61, width=934)
        self.Labelfoot.configure(background="#ffffff")
        self.Labelfoot.configure(disabledforeground="#a3a3a3")
        self.Labelfoot.configure(foreground="#000000")
        self.Labelfoot.configure(width=934)
        self._img1 = PhotoImage(file="images/foot.png")
        self.Labelfoot.configure(image=self._img1)
        self.bodyFrame = Frame(self)
        self.bodyFrame.place(relx=0.0, rely=0.21, relheight=0.72, relwidth=1)

        self.bodyFrame.configure(relief=FLAT)
        self.bodyFrame.configure(borderwidth="0")
        self.bodyFrame.configure(relief=FLAT)
        self.bodyFrame.configure(background="#ffffff")
        self.bodyFrame.configure(width=745)

        self.Labelbody = Label(self.bodyFrame)
        self.Labelbody.place(relx=0.0, rely=0.0, height=600, width=935)
        self.Labelbody.configure(background="#ffffff")
        self.Labelbody.configure(disabledforeground="#a3a3a3")
        self.Labelbody.configure(foreground="#000000")
        self._img155 = PhotoImage(file="images/accu1.png")
        self.Labelbody.configure(image=self._img155)
        self.Labelbody.configure(text='''Label''')
        self.Labelbody.configure(width=935)

        self.nmpLabel = Label(self.bodyFrame)
        self.nmpLabel.place(relx=0.22, rely=0.15, height=35, width=174)
        self.nmpLabel.configure(anchor=W)
        self.nmpLabel.configure(background="#ffffff")
        self.nmpLabel.configure(disabledforeground="#fafafa")
        self.nmpLabel.configure(font=font12)
        self.nmpLabel.configure(foreground="#000000")
        self.nmpLabel.configure(text='''Nom Du Produit :''')
        self.nmpLabel.configure(width=202)

        # on genere la liste des produits existants:
        self.liste_produits = []
        var = connectBdd()
        cur = var.cur
        cur.execute("""SELECT nomProduit FROM produits""")
        resultat1 = cur.fetchall()

        for inter in resultat1:
            for inter2 in inter:
                var = inter2.lower().capitalize()
                self.liste_produits.append(var)

        self.liste_produits = sorted(self.liste_produits)
        # on supprime les doublants dans cette liste:
        self.inter = ""
        self.liste_products = []
        for produit in self.liste_produits:
            if produit != self.inter:
                self.liste_products.append(produit)
                self.inter = produit


        self.nmpEntryVar = StringVar()
        self.nmpEntry = Combobox(self.bodyFrame, textvariable=self.nmpEntryVar, values=self.liste_products,
                                 state="readonly")
        self.nmpEntry.place(relx=0.45, rely=0.15, relheight=0.06
                            , relwidth=0.38)
        self.nmpEntry.configure(background="#ffffff")

        self.dosageLabel = Label(self.bodyFrame)
        self.dosageLabel.place(relx=0.22, rely=0.33, height=35, width=174)
        self.dosageLabel.configure(activebackground="#fafafa")
        self.dosageLabel.configure(activeforeground="black")
        self.dosageLabel.configure(anchor=W)
        self.dosageLabel.configure(background="#ffffff")
        self.dosageLabel.configure(disabledforeground="#a3a3a3")
        self.dosageLabel.configure(font=font12)
        self.dosageLabel.configure(foreground="#000000")
        self.dosageLabel.configure(highlightbackground="#ffffff")
        self.dosageLabel.configure(highlightcolor="black")
        self.dosageLabel.configure(text='''Numéro de Lot  :''')
        self.dosageLabel.configure(width=112)

        self.dosageEntryVar = StringVar()
        self.dosageEntry = Entry(self.bodyFrame, textvariable=self.dosageEntryVar)
        self.dosageEntry.place(relx=0.45, rely=0.33, relheight=0.06
                               , relwidth=0.38)
        self.dosageEntry.configure(background="#ffffff")
        self.dosageEntry.configure(disabledforeground="#a3a3a3")
        self.dosageEntry.configure(font=font12)
        self.dosageEntry.configure(foreground="#000000")
        self.dosageEntry.configure(highlightbackground="#ffffff")
        self.dosageEntry.configure(highlightcolor="black")
        self.dosageEntry.configure(insertbackground="black")
        self.dosageEntry.configure(selectbackground="#c4c4c4")
        self.dosageEntry.configure(selectforeground="black")

        self.formeLabel = Label(self.bodyFrame)
        self.formeLabel.place(relx=0.22, rely=0.51, height=35, width=174)
        self.formeLabel.configure(activebackground="#f9f9f9")
        self.formeLabel.configure(activeforeground="black")
        self.formeLabel.configure(anchor=W)
        self.formeLabel.configure(background="#ffffff")
        self.formeLabel.configure(disabledforeground="#a3a3a3")
        self.formeLabel.configure(font=font12)
        self.formeLabel.configure(foreground="#000000")
        self.formeLabel.configure(highlightbackground="#ffffff")
        self.formeLabel.configure(highlightcolor="black")
        self.formeLabel.configure(text='''Forme   :''')

        self.formeEntryVar = StringVar()
        con= connectBdd()
        con.cur.execute("SELECT forme from produits ");
        e=con.cur.fetchall()





        self.liste_formes=[]

        k = []
        for m in e:
            k.append(m[0])

        k = set(k)
        for i in k:
            self.liste_formes.append(i)



        con.fermer()
        #self.liste_formes = (
           # 'Comprime', 'Suppositoire', 'Sirop', 'Solution buvable', 'Gelule', 'Solution injectable', 'ComprimeEfferv',
            #'Poudre', 'Liquide', 'Pommade', 'Gel', 'Sachet', 'Capsule', 'Goute', 'Ampoule', '')
        self.liste_formes = sorted(self.liste_formes)
        self.formeEntry = Combobox(self.bodyFrame, textvariable=self.formeEntryVar, values=self.liste_formes,
                                  state="readonly")

        self.formeEntry.place(relx=0.45, rely=0.51, relheight=0.06, relwidth=0.38)
        self.formeEntry.configure(background="#ffffff")





        self.rechButt = Button(self.bodyFrame)
        self.rechButt.place(relx=0.64, rely=0.86, height=40, width=180)

        self.rechButt.configure(activebackground="#d9d9d9")
        self.rechButt.configure(activeforeground="#000000")
        self.rechButt.configure(background="#ffffff")
        self.rechButt.configure(borderwidth="2")
        self.rechButt.configure(disabledforeground="#a3a3a3")
        self.rechButt.configure(font=font12)
        self.rechButt.configure(foreground="#000000")
        self.rechButt.configure(highlightbackground="#ffffff")
        self.rechButt.configure(highlightcolor="black")
        self.rechButt.configure(pady="0")
        self.rechButt.configure(relief=RIDGE)
        self.rechButt.configure(text='''Confirmer''')
        self.rechButt.config(command= self.submit)


        self.retourButt = Button(self.bodyFrame)
        self.retourButt.place(relx=0.17, rely=0.86, height=40, width=180)
        self.retourButt.configure(activebackground="#d9d9d9")
        self.retourButt.configure(font=font12)
        self.retourButt.configure(activeforeground="#000000")
        self.retourButt.configure(background="#ffffff")
        self.retourButt.configure(disabledforeground="#a3a3a3")
        self.retourButt.configure(foreground="#000000")
        self.retourButt.configure(highlightbackground="#ffffff")
        self.retourButt.configure(highlightcolor="black")
        self.retourButt.configure(pady="0")
        self.retourButt.configure(relief=RIDGE)
        self.retourButt.configure(text='''Retour''')
        self.retourButt.configure(pady="0")
        self.retourButt.config(command = self.retour)


#################################################################################################
#################################################################################################


#################################################################################################
################ L'Application #################################################################
class application(Tk):

    def getPage(self, pageClass):
        return self.frames[pageClass]

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.iconbitmap(r'images/icon.ico')
        self.resizable(width=False, height=False)
        self.title("PharManage")
        self.geometry("935x695+300+50")
        container = Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        fenetres = (Bienvenue, Login, Recherche_Produit, Produits
                    , Affichage_Des_Produits, Recherche_Des_equivalents, Acceuil, Gestion_de_compte,
                    ChangerMdp, gestionStock, Quantite, Stats, StatVente,Retrait,Inscription_choix,Inscription,Inscription_user
                    ,EchangesEntrePharm,Messagerie,Transactions,Faire_commande,Ajout,Ajout_dun_nouveau_produit,Achat_prod,QuantiteLot,Chargement
                    )
        self.frames = {}

        for F in fenetres:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Chargement)

    def show_frame(self, cont: object) -> object:
        frame = self.frames[cont]
        frame.tkraise()


app = application()

app.mainloop()



