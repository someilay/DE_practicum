import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MplCanvas(FigureCanvas):
    def __init__(self, parent, width: int, height: int, dpi: int = 100):
        """
        Init MplCanvas

        :param parent: parent component
        :param width: width of canvas
        :param height: height of canvas
        :param dpi: pixels per inch
        """
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        self.ax.grid()
        super().__init__(self.fig)
        self.setParent(parent)

    def plot(self, title: str = None, xlabel: str = None, ylabel: str = None, **kwargs):
        """
        Plot graphs

        :param title: title of plot
        :param xlabel: x axis name
        :param ylabel: y axis name
        :param kwargs: decodes graph info: ["x": values, "y": values, "color": color of graph, "label": name of graph]
        :return:
        """
        plt.cla()

        self.ax.grid()
        self.ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
        for label, graph_info in kwargs.items():
            self.ax.plot(
                graph_info["x"],
                graph_info["y"],
                color=graph_info.get("color", None),
                label=graph_info.get("label", None)
            )

        plt.legend()
        self.draw()
