# Diseño de estrategias basadas en inteligencia artificial para jugar al juego Quarto

Para usar la interfaz gráfica y jugar contra los agentes inteligentes, se ejecuta el fichero "PartidaConInterfaz.py" y se abre el menú para seleccionar los jugadores.

1. Por defecto, los agentes MiniMax y AlphaBeta tienen una profundidad de 1 turno (2 niveles) y el evaluador tipo 1.
2. Por defecto, el agente MonteCarlo tiene una profundidaad de 1 turno (2 niveles) y un tiempo de simulación de 1 segundo.
3. Para cambiar estos valores, es necesario modificar el constructor de estos agentes en el fichero "Agentes.py".

La ejecución del fichero "SimularPartida.py" permite la siulación de partidas y el almacenamiento de los resultados en el fichero "resultados_simulacion.csv".

1. Por defecto, en el programa predefinido, el almacenamiento de los resultados en el fichero está desactivado. Para activarlo hay que cambiar el parametro "guardarResultadosEnCSV" a "True".

El fichero "resultados_simulacion.csv" contiene los resultados de los experimentos realizados en el proyecto.
