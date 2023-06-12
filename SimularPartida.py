from Partida import SimularPartida
from Agentes import Aleatorio, ReglasSimples, ReglasComplejas, MiniMax, AlphaBeta, MonteCarlo



def aleatorioVsReglas(guardarResultadosEnCSV=True):
    SimularPartida(Aleatorio(), ReglasSimples(), 500, guardarResultadosEnCSV)
    SimularPartida(ReglasSimples(), Aleatorio(), 500, guardarResultadosEnCSV)

    SimularPartida(Aleatorio(), ReglasComplejas(), 500, guardarResultadosEnCSV)
    SimularPartida(ReglasComplejas(), Aleatorio(), 500, guardarResultadosEnCSV)

def reglasSimplesVsReglasComplejas(guardarResultadosEnCSV=True):
    SimularPartida(ReglasSimples(), ReglasComplejas(), 500, guardarResultadosEnCSV)
    SimularPartida(ReglasComplejas(), ReglasSimples(), 500, guardarResultadosEnCSV)

def reglasComplejasVsMinimax(guardarResultadosEnCSV=True):
    SimularPartida(ReglasComplejas(), MiniMax(1,1), 500, guardarResultadosEnCSV)
    SimularPartida(MiniMax(1,1), ReglasComplejas(), 500, guardarResultadosEnCSV)

    SimularPartida(ReglasComplejas(), MiniMax(1,2), 500, guardarResultadosEnCSV)
    SimularPartida(MiniMax(1,2), ReglasComplejas(), 500, guardarResultadosEnCSV)

    SimularPartida(ReglasComplejas(), MiniMax(1,3), 500, guardarResultadosEnCSV)
    SimularPartida(MiniMax(1,3), ReglasComplejas(), 500, guardarResultadosEnCSV)

def reglasComplejasVsAlphaBeta(guardarResultadosEnCSV=True):
    SimularPartida(ReglasComplejas(), AlphaBeta(1,1), 500, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,1), ReglasComplejas(), 500, guardarResultadosEnCSV)

    SimularPartida(ReglasComplejas(), AlphaBeta(1,2), 500, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,2), ReglasComplejas(), 500, guardarResultadosEnCSV)

    SimularPartida(ReglasComplejas(), AlphaBeta(1,3), 500, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,3), ReglasComplejas(), 500, guardarResultadosEnCSV)

def alphaBetaVsAlphaBetaMismaProfundidad(guardarResultadosEnCSV=True):
    SimularPartida(AlphaBeta(1,1), AlphaBeta(1,2), 500, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,2), AlphaBeta(1,1), 500, guardarResultadosEnCSV)

    SimularPartida(AlphaBeta(1,1), AlphaBeta(1,3), 500, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,3), AlphaBeta(1,1), 500, guardarResultadosEnCSV)

    SimularPartida(AlphaBeta(1,2), AlphaBeta(1,3), 500, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,3), AlphaBeta(1,2), 500, guardarResultadosEnCSV)

def alphaBetaVsAlphaBetaDistintaProfundidad(guardarResultadosEnCSV=True):
    SimularPartida(AlphaBeta(2,1), AlphaBeta(1,3), 50, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,3), AlphaBeta(2,1), 50, guardarResultadosEnCSV)

    SimularPartida(AlphaBeta(2,2), AlphaBeta(1,3), 50, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,3), AlphaBeta(2,2), 50, guardarResultadosEnCSV)

def reglasComplejasVsMonteCarlo(guardarResultadosEnCSV=True):
    SimularPartida(MonteCarlo(1,0.5), ReglasComplejas(), 25, guardarResultadosEnCSV)
    SimularPartida(ReglasComplejas(), MonteCarlo(1,0.5), 25, guardarResultadosEnCSV)

    SimularPartida(MonteCarlo(1,1), ReglasComplejas(), 25, guardarResultadosEnCSV)
    SimularPartida(ReglasComplejas(), MonteCarlo(1,1), 25, guardarResultadosEnCSV)

    SimularPartida(MonteCarlo(1,1), ReglasComplejas(), 25, guardarResultadosEnCSV)
    SimularPartida(ReglasComplejas(), MonteCarlo(1,1), 25, guardarResultadosEnCSV)

    SimularPartida(MonteCarlo(1,1), ReglasComplejas(), 25, guardarResultadosEnCSV)
    SimularPartida(ReglasComplejas(), MonteCarlo(1,1), 25, guardarResultadosEnCSV)

def alphaBetaVsMonteCarloMismaProfundidad(guardarResultadosEnCSV=True):
    #Evaluador 1
    SimularPartida(MonteCarlo(1,0.5), AlphaBeta(1,1), 25, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,1), MonteCarlo(1,0.5), 25, guardarResultadosEnCSV)

    SimularPartida(MonteCarlo(1,1), AlphaBeta(1,1), 25, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,1), MonteCarlo(1,1), 25, guardarResultadosEnCSV)

    SimularPartida(MonteCarlo(1,1), AlphaBeta(1,1), 25, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,1), MonteCarlo(1,1), 25, guardarResultadosEnCSV)

    SimularPartida(MonteCarlo(1,1), AlphaBeta(1,1), 25, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,1), MonteCarlo(1,1), 25, guardarResultadosEnCSV)

    #Evaluador 2
    SimularPartida(MonteCarlo(1,0.5), AlphaBeta(1,2), 25, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,2), MonteCarlo(1,0.5), 25, guardarResultadosEnCSV)

    SimularPartida(MonteCarlo(1,1), AlphaBeta(1,2), 25, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,2), MonteCarlo(1,1), 25, guardarResultadosEnCSV)

    SimularPartida(MonteCarlo(1,1), AlphaBeta(1,2), 25, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,2), MonteCarlo(1,1), 25, guardarResultadosEnCSV)

    SimularPartida(MonteCarlo(1,1), AlphaBeta(1,2), 25, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,2), MonteCarlo(1,1), 25, guardarResultadosEnCSV)

    #Evaluador 3
    SimularPartida(MonteCarlo(1,0.5), AlphaBeta(1,3), 25, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,3), MonteCarlo(1,0.5), 25, guardarResultadosEnCSV)

    SimularPartida(MonteCarlo(1,1), AlphaBeta(1,3), 25, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,3), MonteCarlo(1,1), 25, guardarResultadosEnCSV)

    SimularPartida(MonteCarlo(1,1), AlphaBeta(1,3), 25, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,3), MonteCarlo(1,1), 25, guardarResultadosEnCSV)

    SimularPartida(MonteCarlo(1,1), AlphaBeta(1,3), 25, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,3), MonteCarlo(1,1), 25, guardarResultadosEnCSV)


def alphaBetaVsMonteCarloDistintaProfundidad(guardarResultadosEnCSV=True):
    #Evaluador 1
    SimularPartida(MonteCarlo(2,0.5), AlphaBeta(1,1), 25, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,1), MonteCarlo(2,0.5), 25, guardarResultadosEnCSV)

    SimularPartida(MonteCarlo(2,1), AlphaBeta(1,1), 25, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,1), MonteCarlo(2,1), 25, guardarResultadosEnCSV)

    SimularPartida(MonteCarlo(2,1), AlphaBeta(1,1), 25, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,1), MonteCarlo(2,1), 25, guardarResultadosEnCSV)

    SimularPartida(MonteCarlo(2,1), AlphaBeta(1,1), 25, guardarResultadosEnCSV)
    SimularPartida(AlphaBeta(1,1), MonteCarlo(2,1), 25, guardarResultadosEnCSV)

def main():
    aleatorioVsReglas(False)
    reglasComplejasVsAlphaBeta(False)
    





if __name__ == '__main__':
    main()