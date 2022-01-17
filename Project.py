import ciw

I = 0.001  # tmp init
Y = 0.0001  # Heure server statique
R = 10000  # taux de serveur dynamique
S = 1500  # Bande passante serveur
A = 30  # entre 10 et 40 taux arrivée réseau
C = 707  # Bande passante client
B = 16  # Taille du tampon
F = 42.2  # taille moyenne fichier
N = ciw.create_network(
    arrival_distributions=[ciw.dists.Exponential(rate=A),  # SI
                           ciw.dists.NoArrivals(),  # SR
                           ciw.dists.NoArrivals(),  # SS
                           ciw.dists.NoArrivals()],  # SC
    service_distributions=[ciw.dists.Deterministic(value=I),  # SI
                           ciw.dists.Exponential(rate=1/(Y+B/R)),  # SR
                           ciw.dists.Deterministic(value=B/S),  # SS
                           ciw.dists.Deterministic(value=B/C)],  # SC
    routing=[[0, 1, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 0, 1],
             [0, B/F, 0, 0]],
    number_of_servers=[1, 1, 1, 1]
)
