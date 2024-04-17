# realise par:
# ABDI Tafsout 


problematique=0
problematique=int(input("Tapez 1 si votre problème s'agit d'un problème de maximisation\n""Tapez 2 si votre problème s'agit d'un problème de minimisation\n"))
nbrvar=int(input("Le nombre de variables de décision : "))
nbrcont=int(input("Le nombre de contraintes :"))
# sauvegarder les données dans un tableau  
print("La fonction objectif :\n ")
matriceprincipale=[]
nouvelleligne=[]
for i in range(nbrvar):
    nouvelleligne.append(int(input("Coefficient de x"+str(i+1)+":")))
matriceprincipale.append(nouvelleligne)
print("les contraintes :\n")
for i in range(nbrcont):
    print("contrainte ",i+1,"\n")
    nouvelleligne=[]
    for j in range(nbrvar):
        nouvelleligne.append(float(input("Coefficient de x"+str(j+1)+":")))
    nouvelleligne.append(str(input("l'operateur ( <= | >= | = ): ")))
    nouvelleligne.append(float(input("b"+str(i+1)+"= ")))
#si b<0 on multiplie la matrice *(-1) pour avoir que des valeurs positives dans b
    if nouvelleligne[nbrvar+1]<0:
        #changer les valeurs 
        for k in range(nbrvar):
            nouvelleligne[k]=nouvelleligne[k]*(-1)
        nouvelleligne[nbrvar+1]=nouvelleligne[nbrvar+1]*-1
        #changer les opérateurs (les inversés)
        if nouvelleligne[nbrvar]=="<=" :
            nouvelleligne[nbrvar]=">="
        elif nouvelleligne[nbrvar]==">=":
            nouvelleligne[nbrvar]="<="
    matriceprincipale.append(nouvelleligne)

# matriceM1: la premiere matrice de bigM
matriceM1=[]
for i in range(nbrcont+2):
    nouvelleligne=[]
    for j in range(nbrvar+nbrcont*2+2):
        nouvelleligne.append(0)
    matriceM1.append(nouvelleligne)
#chaque equation aura deux valeurs supplémentaires l'une d'elle est une variable d'écart ou d'excedent ei
# l'autre c'est la variable artificielle ti (les variables au plus seront supprimées par la suite)
e=nbrvar
t=nbrvar+nbrcont
for i in range(1,nbrcont+1):
    if matriceprincipale[i][nbrvar]=="<=":
        matriceM1[i][e]=1
        e+=1 #on rajoute une variable d'écart ei 

    elif matriceprincipale[i][nbrvar]=="=":
        matriceM1[i][t]=1
        t+=1 #on rajoute une variable artificielle ti

    elif matriceprincipale[i][nbrvar]==">=":
        matriceM1[i][e]=-1
        matriceM1[i][t]=1
        t+=1 #on rajoute une variable artificielle ti 
        e+=1 #on rajoute une variable d'excedent ei

for i in range(1,nbrcont+1):
    for j in range(nbrvar):
        matriceM1[i][j]=matriceprincipale[i][j]
#stocker les noms des variables dans un vecteur puis l'ajouté a matriceM1
vect=[]
for i in range (nbrvar):
    vect.append(str("x"+str(i+1)))
for i in range (nbrcont):
    vect.append(str("e"+str(i+1)))
for i in range(nbrcont):
    vect.append(str("t"+str(i+1)))
vect.append("bi")
vect.append("bi/cp")
for j in range(nbrvar+nbrcont*2+2):
    matriceM1[0][j]=vect[j]
for i in range(1,nbrcont+1):
    matriceM1[i][nbrvar+nbrcont*2]=matriceprincipale[i][nbrvar+1]
#un vecteur qui va contenir les variable de bases
base=[]
base.append("base")
for i in range(1,nbrcont+1):
    for j in range(nbrvar,nbrvar+nbrcont*2):
        if matriceM1[i][j]==1:
            base.append(vect[j])
base.append("-z")
bigM=[]
for j in range(nbrvar+nbrcont,nbrvar+nbrcont*2+1):
    for i in range(1,nbrcont+1):
        if matriceM1[i][j]==1:
            for p in range(nbrvar+nbrcont):
                matriceM1[nbrcont+1][p]=matriceM1[nbrcont+1][p]+matriceM1[i][p]
            matriceM1[nbrcont+ 1][nbrvar+nbrcont*2] = matriceM1[nbrcont+ 1][nbrvar+nbrcont*2] + matriceM1[i][nbrvar+nbrcont*2]
#garder les coefficients de M pour les utiliser dans le choix de la variable entrante
if problematique==2:
    for j in range(len(matriceM1[0])):
        bigM.append(matriceM1[nbrcont+ 1][j])
if problematique==1:

    for j in range(len(matriceM1[0])):
        bigM.append(-1*matriceM1[nbrcont+ 1][j])
for j in range(len(matriceM1[0])):
    if not matriceM1[nbrcont+1][j]==0:
        matriceM1[nbrcont+1][j]=str(bigM[j])+"m"
for j in range(nbrvar):
    matriceM1[nbrcont+1][j] = matriceM1[nbrcont+1][j]+"+("+str(matriceprincipale[0][j])+")"
col=0
#prendre le maximum dans bigM
if problematique==1: #maximisation
    for i in range(nbrvar+nbrcont+1):
        if bigM[i]==min(bigM) and min(bigM)<0 :
            col=i
            break

if problematique==2: #minimisation
    for i in range(nbrvar+nbrcont+1):
        if bigM[i]==max(bigM) and max(bigM)>0 :
            col=i
            break

#bi/cp
for i in range(1,nbrcont+1):
    if not matriceM1[i][col]==0:
        matriceM1[i][nbrvar+nbrcont*2+1]=matriceM1[i][nbrvar+nbrcont*2]/matriceM1[i][col]
    else :
        matriceM1[i][nbrcont* 2 + nbrvar + 1] ="-"
matriceM1[nbrcont+1][nbrcont*2+nbrvar+1]="*"
#supprimer les colonnes avec des valeurs nulles
for j in range(nbrvar,nbrvar+nbrcont*2):
    count = 0
    for i in range(1, nbrcont+1):
        if matriceM1[i][j]==0:
            count+=1
    if count>=nbrcont:
        for i in range (nbrcont+2):
            matriceM1[i].pop(j)
#l'affichage du tableau
mat=[]
scp=-1
for j in range(len(matriceM1[i])):
    scp=-1
    for i in range(nbrcont+ 2):
        if len(str(matriceM1[i][j]))>scp:
            scp=len(str(matriceM1[i][j]))
    mat.append(scp)

#choix de la variable entrante
#affichage

print("-" * int((sum(mat) + 2 + 3 * (nbrcont* 2 + nbrvar + 1))/2-5)," affichage ","-"* int((sum(mat) + 7 + 1 + 3 * (nbrcont* 2 + nbrvar + 1))/2-6),
      "\n"," "* int((sum(mat) + 2 + 3 * (nbrcont* 2 + nbrvar + 1))/2-10)," Premier tableau bigM ")
print("-" * (sum(mat) + 7 + 1 + 3 * (nbrcont* 2 + nbrvar + 1)))  
print()
for i in range (nbrcont*2):
    print(" ",base[i],end=" "*(4-len(str(base[i])))+" | ")
    for j in range(len(matriceM1[i])):
        print(matriceM1[i][j],end=" "*(mat[j]-len(str(matriceM1[i][j])))+" | ")
    print()
    print("-"*(sum(mat)+2+3*(nbrcont*2+nbrvar+2)))
    print()