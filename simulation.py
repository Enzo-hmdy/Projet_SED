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


def createSimulation(AA):
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

        number_of_servers=[1, 1, 1, 1] #Chaque file d'attente contient un serveur

    )
    return N



#---------- Partie 1 ----------#
#---------- Tache 1  ----------#

jspcquecest = createSimulation(A)

simulation = ciw.Simulation(jspcquecest)

simulation.simulate_until_max_time(rechTime+simuTime+10)

records = simulation.get_all_records()

print("On a : " + str(len(simulation.nodes) - 2) + " files d'attente")

meanStayTime = sum([r.exit_date - r.arrival_date for r in records]) / len(records)

meanWaitingTima = sum([r.waiting_time for r in records]) / len(records)

#---------- Partie 2 ----------#

mst_array = []
mwt_array = []


for trial in range(1, 40):
    # print("*------ trial " + str(trial) + " ------*")
    ss = createSimulation(trial)
    S_ = ciw.Simulation(ss)
    S_.simulate_until_max_time(rechTime + simuTime + 10)
    rec = S_.get_all_records()
    mst = sum([r.exit_date - r.arrival_date for r in rec]) / len(rec)
    mwt = sum([r.waiting_time for r in rec]) / len(rec)
    # print("Mean stay time: " + str(mst))
    # print("Mean Waiting time: " + str(mwt))
    mst_array.append(mst)
    mwt_array.append(mwt)

def plottest(data):
    x=np.array([i for i in range(1, 40)])
    y=np.array(data)
    plt.plot(x,y)
    plt.show()


fig, axs = plt.subplots(2)
axs[0].plot(np.arange(1, 40, 1), np.array(mst_array), color='blue', linestyle='solid', label='stay time')
axs[1].plot(np.arange(1, 40, 1), np.array(mwt_array), color='green', linestyle='solid', label='waiting time')

axs[0].set_title("Mean stay time")
axs[1].set_title("Mean waiting time")
plt.show()