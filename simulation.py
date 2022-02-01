import math
import statistics
from turtle import color
import ciw 
import numpy as np
import scipy.integrate
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np

#Course example 

I=0.0001
Y=0.0001
R=10000
S=1500
A=30 #entre 10 et 40 
C=707
B=16 
F=42.2
#40 100     +40
rechTime= 10 #Le temps de réchauffement
simuTime= 10 #Le temps de simulation (en ne prenant pas en compte le rechTime)
stopTime= rechTime + simuTime + 10 #Le temps d'arret


def createSimulation(AA, SR = 1):
    N=ciw.create_network(
        arrival_distributions=[ciw.dists.Exponential(rate=AA),
        ciw.dists.NoArrivals(),#SR 
        ciw.dists.NoArrivals(),#SS 
        ciw.dists.NoArrivals()],#SC

        service_distributions=[ciw.dists.Deterministic(value=I),#SI 
        ciw.dists.Exponential(rate=1/(Y+B/R)),#SR
        ciw.dists.Deterministic(value=B/S),#SS
        ciw.dists.Deterministic(value=B/C)],#SC
        
        routing=[[0, 1, 0, 0],
                 [0, 0, 1, 0], 
                 [0, 0, 0, 1], 
                 [0,1 - B/F, 0, 0]], #Cette matrice modelise les liens entre SI, SR, SS et SC

        number_of_servers=[1, SR, 1, 1] #Chaque file d'attente contient un serveur

    )
    return N

############################################################################################################
#                                            Partie 1                                                      # 
############################################################################################################
#---------- Tache 1  ----------#

jspcquecest = createSimulation(A)

simulation = ciw.Simulation(jspcquecest)

simulation.simulate_until_max_time(rechTime+simuTime+10)

records = simulation.get_all_records()

print("On a : " + str(len(simulation.nodes) - 2) + " files d'attente")

meanStayTime = sum([r.exit_date - r.arrival_date for r in records]) / len(records)

meanWaitingTima = sum([r.waiting_time for r in records]) / len(records)

############################################################################################################
#                                            Partie 2                                                      # 
############################################################################################################

############################################################################################################
#               Calcul avec le système de base

mst_array_init = []
mwt_array_init = []

mst_confiance_up_init = []
mst_confiance_down_init = []

mwt_confiance_up_init = []
mwt_confiance_down_init = []

for trial in range(1, 40):
    # print("*------ trial " + str(trial) + " ------*")
    ss = createSimulation(trial)
    S_ = ciw.Simulation(ss)
    S_.simulate_until_max_time(rechTime + simuTime + 10)
    rec = S_.get_all_records()

    mst = sum([r.exit_date - r.arrival_date for r in rec]) / len(rec)
    mwt = sum([r.waiting_time for r in rec]) / len(rec)

    variance = sum([(r.exit_date - r.arrival_date)**2 for r in rec]) / len(rec) - mst**2

    # print("Mean stay time: " + str(mst))
    # print("Mean Waiting time: " + str(mwt))

    mst_confiance_up_init.append(mst + 1.96*(variance / math.sqrt(40)))
    mst_confiance_down_init.append(mst - 1.96*(variance / math.sqrt(40)))

    mwt_confiance_up_init.append(mwt + 1.96*(variance / math.sqrt(40)))
    mwt_confiance_down_init.append(mwt - 1.96*(variance / math.sqrt(40)))

    mst_array_init.append(mst)
    mwt_array_init.append(mwt)

############################################################################################################
#               Calcul avec R fois 2
R *= 2


mst_array_R = []
mwt_array_R = []

mst_confiance_up_R = []
mst_confiance_down_R = []

mwt_confiance_up_R = []
mwt_confiance_down_R = []

for trial in range(1, 40):
    # print("*------ trial " + str(trial) + " ------*")
    ss = createSimulation(trial)
    S_ = ciw.Simulation(ss)
    S_.simulate_until_max_time(rechTime + simuTime + 10)
    rec = S_.get_all_records()

    mst = sum([r.exit_date - r.arrival_date for r in rec]) / len(rec)
    mwt = sum([r.waiting_time for r in rec]) / len(rec)

    variance = sum([(r.exit_date - r.arrival_date)**2 for r in rec]) / len(rec) - mst**2

    # print("Mean stay time: " + str(mst))
    # print("Mean Waiting time: " + str(mwt))

    mst_confiance_up_R.append(mst + 1.96*(variance / math.sqrt(40)))
    mst_confiance_down_R.append(mst - 1.96*(variance / math.sqrt(40)))

    mwt_confiance_up_R.append(mwt + 1.96*(variance / math.sqrt(40)))
    mwt_confiance_down_R.append(mwt - 1.96*(variance / math.sqrt(40)))

    mst_array_R.append(mst)
    mwt_array_R.append(mwt)

############################################################################################################
#                    Calcul avec S fois 2
R /= 2
S *= 2


mst_array_S = []
mwt_array_S = []

mst_confiance_up_S = []
mst_confiance_down_S = []

mwt_confiance_up_S = []
mwt_confiance_down_S = []

for trial in range(1, 40):
    # print("*------ trial " + str(trial) + " ------*")
    ss = createSimulation(trial)
    S_ = ciw.Simulation(ss)
    S_.simulate_until_max_time(rechTime + simuTime + 10)
    rec = S_.get_all_records()

    mst = sum([r.exit_date - r.arrival_date for r in rec]) / len(rec)
    mwt = sum([r.waiting_time for r in rec]) / len(rec)

    variance = sum([(r.exit_date - r.arrival_date)**2 for r in rec]) / len(rec) - mst**2

    # print("Mean stay time: " + str(mst))
    # print("Mean Waiting time: " + str(mwt))

    mst_confiance_up_S.append(mst + 1.96*(variance / math.sqrt(40)))
    mst_confiance_down_S.append(mst - 1.96*(variance / math.sqrt(40)))

    mwt_confiance_up_S.append(mwt + 1.96*(variance / math.sqrt(40)))
    mwt_confiance_down_S.append(mwt - 1.96*(variance / math.sqrt(40)))

    mst_array_S.append(mst)
    mwt_array_S.append(mwt)

############################################################################################################
#                   Calcul avec deux serveurs SR
S /= 2

mst_array_SR = []
mwt_array_SR = []

mst_confiance_up_SR = []
mst_confiance_down_SR = []

mwt_confiance_up_SR = []
mwt_confiance_down_SR = []

for trial in range(1, 40):
    # print("*------ trial " + str(trial) + " ------*")
    ss = createSimulation(trial)
    S_ = ciw.Simulation(ss)
    S_.simulate_until_max_time(rechTime + simuTime + 10)
    rec = S_.get_all_records()

    mst = sum([r.exit_date - r.arrival_date for r in rec]) / len(rec)
    mwt = sum([r.waiting_time for r in rec]) / len(rec)

    variance = sum([(r.exit_date - r.arrival_date)**2 for r in rec]) / len(rec) - mst**2

    # print("Mean stay time: " + str(mst))
    # print("Mean Waiting time: " + str(mwt))

    mst_confiance_up_SR.append(mst + 1.96*(variance / math.sqrt(40)))
    mst_confiance_down_SR.append(mst - 1.96*(variance / math.sqrt(40)))

    mwt_confiance_up_SR.append(mwt + 1.96*(variance / math.sqrt(40)))
    mwt_confiance_down_SR.append(mwt - 1.96*(variance / math.sqrt(40)))

    mst_array_SR.append(mst)
    mwt_array_SR.append(mwt)


############################################################################################################
#                                            Partie 1                                                      # 
############################################################################################################
#                    Calcul des différences systèmes avec le système de base

#------------       Cas 1

mst_dif_R = [mst_array_init[i] - mst_array_R[i] for i in range(39)]

#------------       Cas 2

mst_dif_S = [mst_array_init[i] - mst_array_S[i] for i in range(39)]

#------------       Cas 3

mst_dif_SR = [mst_array_init[i] - mst_array_SR[i] for i in range(39)]

############################################################################################################
#                    Calcul des différences entre les différents systèmes systèmes 

#------------       différence entre S et R

mst_dif_S_R = [mst_array_S[i] - mst_array_R[i] for i in range(39)]

#------------       différence entre S et SR

mst_dif_S_SR = [mst_array_S[i] - mst_array_SR[i] for i in range(39)]

#------------       différence entre R et SR

mst_dif_R_SR = [mst_array_R[i] - mst_array_SR[i] for i in range(39)]

############################################################################################################
#                                              Affichage des graphs

############################################################################################################
#                                              Pour la partie 2 

# fig, axs = plt.subplots(2)

# axs[0].plot(np.arange(1, 40, 1), np.array(mst_array_init), color = "blue")
# axs[0].plot(np.arange(1, 40, 1), np.array(mst_confiance_up_init), color = "red")
# axs[0].plot(np.arange(1, 40, 1), np.array(mst_confiance_down_init), color = "red")

# axs[1].plot(np.arange(1, 40, 1), np.array(mwt_array_init), color = "blue")
# axs[1].plot(np.arange(1, 40, 1), np.array(mwt_confiance_up_init), color = "red")
# axs[1].plot(np.arange(1, 40, 1), np.array(mwt_confiance_down_init), color = "red")

# axs[0].set_title("Mean stay time")
# axs[1].set_title("Mean waiting time")

############################################################################################################
#                                              Pour la partie 3 tache 1
############################################################################################################
#---------------------------- Cas 1

# fig, axs = plt.subplots(2)

# axs[0].plot(np.arange(1, 40, 1), np.array(mst_array_R), color = "blue")
# axs[0].plot(np.arange(1, 40, 1), np.array(mst_confiance_up_R), color = "red")
# axs[0].plot(np.arange(1, 40, 1), np.array(mst_confiance_down_R), color = "red")

# axs[1].plot(np.arange(1, 40, 1), np.array(mwt_array_R), color = "blue")
# axs[1].plot(np.arange(1, 40, 1), np.array(mwt_confiance_up_R), color = "red")
# axs[1].plot(np.arange(1, 40, 1), np.array(mwt_confiance_down_R), color = "red")

# axs[0].set_title("Mean stay time ")
# axs[1].set_title("Mean waiting time")

############################################################################################################
# #---------------------------- Cas 2

# fig, axs = plt.subplots(2)

# axs[0].plot(np.arange(1, 40, 1), np.array(mst_array_S), color = "blue")
# axs[0].plot(np.arange(1, 40, 1), np.array(mst_confiance_up_S), color = "red")
# axs[0].plot(np.arange(1, 40, 1), np.array(mst_confiance_down_S), color = "red")

# axs[1].plot(np.arange(1, 40, 1), np.array(mwt_array_S), color = "blue")
# axs[1].plot(np.arange(1, 40, 1), np.array(mwt_confiance_up_S), color = "red")
# axs[1].plot(np.arange(1, 40, 1), np.array(mwt_confiance_down_S), color = "red")

# axs[0].set_title("Mean stay time ")
# axs[1].set_title("Mean waiting time")

############################################################################################################
# #---------------------------- Cas 3

# fig, axs = plt.subplots(2)

# axs[0].plot(np.arange(1, 40, 1), np.array(mst_array_SR), color = "blue")
# axs[0].plot(np.arange(1, 40, 1), np.array(mst_confiance_up_SR), color = "red")
# axs[0].plot(np.arange(1, 40, 1), np.array(mst_confiance_down_SR), color = "red")

# axs[1].plot(np.arange(1, 40, 1), np.array(mwt_array_SR), color = "blue")
# axs[1].plot(np.arange(1, 40, 1), np.array(mwt_confiance_up_SR), color = "red")
# axs[1].plot(np.arange(1, 40, 1), np.array(mwt_confiance_down_SR), color = "red")

# axs[0].set_title("Mean stay time ")
# axs[1].set_title("Mean waiting time")

############################################################################################################
#                                              Pour la partie 3 tache 2

# fig, axs = plt.subplots(3)

# axs[0].plot(np.arange(1, 40, 1), np.array(mst_dif_R), color = "black")
# axs[1].plot(np.arange(1, 40, 1), np.array(mst_dif_S), color = "black")
# axs[2].plot(np.arange(1, 40, 1), np.array(mst_dif_SR), color = "black")

# axs[0].set_ylim([-1, 1])
# axs[1].set_ylim([-1, 1])
# axs[2].set_ylim([-1, 1])

# axs[0].set_title("Diff. init - R*2")
# axs[1].set_title("Diff. init - S*2")
# axs[2].set_title("Diff. init - SR*2")

############################################################################################################
#                                              Pour la partie 3 tache 3

# fig, axs = plt.subplots(3)

# axs[0].plot(np.arange(1, 40, 1), np.array(mst_dif_S_R), color = "black")
# axs[1].plot(np.arange(1, 40, 1), np.array(mst_dif_S_SR), color = "black")
# axs[2].plot(np.arange(1, 40, 1), np.array(mst_dif_R_SR), color = "black")

# axs[0].set_ylim([-1, 1])
# axs[1].set_ylim([-1, 1])
# axs[2].set_ylim([-1, 1])

# axs[0].set_title("Diff. S - R")
# axs[1].set_title("Diff. S - SR")
# axs[2].set_title("Diff. R - SR")


plt.show()