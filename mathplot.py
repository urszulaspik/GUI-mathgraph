"""
Module to create application for drawing graphs of functions
"""

import os

os.environ["KIVY_NO_ARGS"] = "1"

from kivy.app import App
from kivy.uix.widget import Widget
import sys
import matplotlib.pyplot as plt
from sympy import parse_expr, lambdify, Symbol
import numpy as np
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.core.window import Window


class MathPlot(Widget):
    '''
    Class with layout methods of application.
    '''

    @staticmethod
    def quit():
        """Exit the window with application"""
        sys.exit()

    def formula_add(self, f: str):
        '''
        Add string in cursor place to formula entry
        :param f: (str) string to add
        '''
        self.ids.formula.insert_text(f)

    def formula_list(self):
        '''
        Create list of string formulas
        :return: (list) list with string formulas
        '''
        return self.ids.formula.text.split("; ")

    def formula_parse(self):
        '''
        Create list of parsed formulas
        :return: (list) list of formulas to plot
        '''
        formulas = []
        for index, i in enumerate(self.formula_list()):
            try:
                i = i.replace("^", "**").replace("e", "E").replace(",", ".")
                formulas.append(parse_expr(i))
            except:
                self.ids.errors.text = f"Wrong formula: {self.formula_list()[index]}. Remember to separate the formulas by \"; \""
                formulas = []
        return formulas

    @staticmethod
    def float_number(number: float):
        '''
        Check if number is float number
        :param number: (float) number to check
        :return: (bool) True - yes, False - no
        '''
        try:
            float(number)
        except:
            return False
        return True

    def errors(self):
        '''
        Check if value of data to plot is correctly
        :return: (bool) True - yes, False - no
        '''
        self.ids.errors.text = ""
        if not self.float_number(self.ids.limx_min.text):
            self.ids.errors.text = "Wrong specified the minimum limit of X axis"
            return False
        elif not self.float_number(self.ids.limx_max.text):
            self.ids.errors.text = "Wrong specified the maximum limit of X axis"
            return False
        elif not self.float_number(self.ids.limy_min.text):
            self.ids.errors.text = "Wrong specified the minimum limit of Y axis"
            return False
        elif not self.float_number(self.ids.limy_max.text):
            self.ids.errors.text = "Wrong specified the maximum limit of Y axis"
            return False
        elif float(self.ids.limx_min.text) >= float(self.ids.limx_max.text):
            self.ids.errors.text = "Minimum limit of the X axis is greater than or equal to the maximum limit"
            return False
        elif float(self.ids.limy_min.text) >= float(self.ids.limy_max.text):
            self.ids.errors.text = "Minimum limit of the Y axis is greater than or equal to the maximum limit"
            return False
        return True

    @staticmethod
    def function_value(func, value):
        '''
        Count value of function for list of arguments
        :param func: function to count
        :param value: (list) list of arguments
        '''
        x = Symbol("x")
        lamb = lambdify(x, func, modules=['numpy'])
        if func.is_constant():
            return np.full_like(value, lamb(value))
        else:
            return lamb(value)

    def plot_graph(self):
        '''
        Plot formulas on graph with specified title,
        x-axis title, y-axis title and legend
        '''
        if self.errors():
            self.ids.layout.clear_widgets()
            plt.clf()
            x_value = np.linspace(float(self.ids.limx_min.text), float(self.ids.limx_max.text), 1000)
            for index, i in enumerate(self.formula_parse()):
                try:
                    y_value = self.function_value(i, x_value)
                    plt.plot(x_value, y_value, label=self.formula_list()[index])
                except:
                    self.ids.errors.text = f"Wrong typed formula {index + 1}: {self.formula_list()[index]}"
            plt.xlim(float(self.ids.limx_min.text), float(self.ids.limx_max.text))
            plt.ylim(float(self.ids.limy_min.text), float(self.ids.limy_max.text))
            plt.xlabel(self.ids.x_title.text)
            plt.ylabel(self.ids.y_title.text)
            plt.title(self.ids.title.text)
            plt.grid(True)
            if self.ids.legend.active:
                plt.legend(loc=1)
            self.ids.layout.add_widget(FigureCanvasKivyAgg(plt.gcf()))


class MathPlotApp(App):
    '''
    Class to bild up application.
    '''

    def build(self):
        '''
        Build application
        '''
        Window.size = (1000, 600)
        return MathPlot()


if __name__ == '__main__':
    MathPlotApp().run()
