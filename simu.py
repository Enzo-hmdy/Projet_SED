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

def plottest(data):
    x=np.array([i for i in range(10,41)])
    y=np.array(data)
    plt.plot(x,y)
    plt.show()


def getValidClients(listClients, start, stop):
    validClients = [clientt for clientt in listClients if clientt.arrival_date > start and clientt.exit_date < stop]
    return validClients

def meanStayTime(validClients):
    return sum([r.exit_date - r.arrival_date for r in validClients])/len(validClients)

def meanWaitingTime(validClients):
    return sum([r.waiting_time for r in validClients])/len(validClients)

def extractArrivalList(clients, nodeNumber, nbServers):
    clientsNode = [c for c in clients if c.node == nodeNumber]
    arrival_attente = []
    for c in clientsNode:
        nbattente = c.queue_size_at_arrival if c.queue_size_at_arrival + 1 > nbServers else 0
        arrival_attente.append(tuple([c.arrival_date, nbattente]))
    return arrival_attente

def extractDepartureList(clients, nodeNumber, nbServers):
    clientsNode = [c for c in clients if c.node == nodeNumber]
    departure_attente = []
    for c in clientsNode:
        nbattente = c.queue_size_at_departure - 1 - 1 if c.queue_size_at_departure - 1 > nbServers else 0
        departure_attente.append(tuple([c.exit_date, nbattente]))
    return departure_attente

def meanClientsPerNode(clients, nodeNumber):
    clientsNode = [c for c in clients if c.node == nodeNumber]
    return sum([1 for r in clientsNode if r.waiting_time])/len(clientsNode)
    # return sum([1 for r in clientsNode if r.waiting_time])

def firstElement(elem):
    return elem[0]

#################################### Partie 1 ####################################

#################################### Tache 1 ####################################
#• Temps moyen de séjour
#• Temps moyen d’attente
#• Nombre moyen de clients en attente sur chaque file d’attente

Ss = createSimulation(A)
newSimulation = ciw.Simulation(Ss)
newSimulation.simulate_until_max_time(rechTime+simuTime+10)
#newSimulation.simulate_until_max_time(100)
records = newSimulation.get_all_records()
print("On a : " + str(len(newSimulation.nodes) - 2) + " files d'attente")
# newSimulation.nodes => [Arrival Node, Node 1, Node 2, Node 3, Node 4, Exit Node]
# Les attributs de record: id_number, customer_class, node, arrival_date, waiting_time, service_start_date, service_time, service_end_date, time_blocked, exit_date, destination, queue_size_at_arrival, queue_size_at_departure
validClients = getValidClients(records, rechTime, stopTime)
print("Nombre de clients: " + str(len(records)))
print("Nombre de clients valides: " + str(len(validClients)))

tempsMoyenSejour = meanStayTime(validClients)
print("Temps moyen de sejour: ",tempsMoyenSejour)

tempsMoyenAttente = meanWaitingTime(validClients)
print("Temps moyen d'attente': ",tempsMoyenAttente)

# Moyenne temps reel
arrivals = []
departures = []
attentes = []
for i in range(4):
    arrivals.append(extractArrivalList(validClients,i+1,1))
    departures.append(extractDepartureList(validClients,i+1,1))
    attentes.append(arrivals[i] + departures[i])

for i in range(4):
    attentes[i].sort(key=firstElement)

temps = [attentes[3][i][0] for i in range(len(attentes[3]))]
nbattentes = [attentes[3][i][1] for i in range(len(attentes[3]))]
print(np.trapz(nbattentes,x=temps)/ (temps[-1] - temps[0]))
# sort the list suivant le temps puis séparer temps et nbre attente puis les faire passer a trapz



#################################### Tache 1 ####################################

#################################### Tache 2 ####################################

# Pour la méthode de replication on a juste a iterer dans une boucle en appelant les fonctions precedentes?
# On itere sur les valeurs de A
#On varie la valeur de A entre 10 et 40
# print("###############################")
TMS = [] #liste de temps moyen de sejour
TMA = [] #liste de temps moyen d'attente
NBMC = [[] for i in range(4)] #nbre moyen de clients par file
for i in range(10,41): 
    print("###############################")
    print("Pour A = " + str(i))
    print("Essai numero ",i-9)
    S1 = createSimulation(i)
    ns = ciw.Simulation(S1)
    ns.simulate_until_max_time(rechTime+simuTime+10)
    records1 = ns.get_all_records()
    vc = getValidClients(records1, rechTime, stopTime)
    mst = meanStayTime(vc)
    mwt = meanWaitingTime(vc)
    print("Temps moyen d'attente: ",mst)
    print("Temps moyen d'attente: ", mwt)
    TMS.append(mst)
    TMA.append(mwt)
    arrivals = []
    departures = []
    attentes = []
    for i in range(4):
        arrivals.append(extractArrivalList(vc,i+1,1))
        departures.append(extractDepartureList(vc,i+1,1))
        attentes.append(arrivals[i] + departures[i])

    for j in range(4):
        attentes[j].sort(key=firstElement)
        temps = [attentes[j][i][0] for i in range(len(attentes[j]))]
        nbattentes = [attentes[j][i][1] for i in range(len(attentes[j]))]
        n = np.trapz(nbattentes,x=temps)/ (temps[-1] - temps[0])
        print(n)
        NBMC[j].append(n)
        print("Nombre moyen de clients pour la file " + str(j+1)+ " est " + str(np.trapz(nbattentes,x=temps)/ (temps[-1] - temps[0])) )
    print("###############################")
# print(NBMC)
# print(TMA)
# print(TMS)

plottest(TMS)