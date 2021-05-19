import multiprocessing as mp
import matplotlib.pyplot as plt


class Plotter:
    def __init__(self):
        self.steps = []
        self.costs = []
        self.episodes = []
        self.done = False

    def readPipe(self):
        if not self.done:
            while self.pipe.poll():
                data = self.pipe.recv()

                if data["done"]:
                    self.done = True

                self.steps.append(data["step"])
                self.costs.append(data["cost"])
                self.episodes.append(data["episode"])
            self.stepsGraph.plot(self.episodes, self.steps, "r-")
            self.costsGraph.plot(self.episodes, self.costs, "r-")
            self.fig.canvas.draw()
        return True

    def __call__(self, pipe):
        print("starting plotter...")

        self.pipe = pipe
        self.fig, (self.stepsGraph, self.costsGraph) = plt.subplots(2, 1, sharex=True)
        self.fig.subplots_adjust(hspace=0.5)

        self.stepsGraph.set_xlabel("episodes")
        self.stepsGraph.set_ylabel("steps")

        self.costsGraph.set_xlabel("episodes")
        self.costsGraph.set_ylabel("costs")

        timer = self.fig.canvas.new_timer(interval=1000)
        timer.add_callback(self.readPipe)
        timer.start()

        print("...done")
        plt.show()


class PlotterController:
    def __init__(self):
        self.plot_pipe, plotter_pipe = mp.Pipe()
        self.plotter = Plotter()
        self.plot_process = mp.Process(target=self.plotter, args=(plotter_pipe,), daemon=True)
        self.plot_process.start()

    def sendData(self, data):
        send = self.plot_pipe.send

        send(data)
