"""
Geometry module for Langmuir Model.

This module supports
Langmuir Feature Model 2D
Langmuir Reactor Model 1D and 2D
"""

from Constants import color_dict

import matplotlib.pyplot as plt
import matplotlib.patches as patch
import numpy as np

class Base(object):
    """Define all shared basic properties."""
    
    def __init__(self, name='Base', is_cyl=False):
        """
        Init the Base.
        
        name: str, var, name of geom.
        dim: int, var, dim of the geometry
        is_cyl: bool, var, whether cylindrical symmetry
        sequency: list of shapes
        idomain: bool, var, whether domain is created
        mater_set: str, set of str, set of materials
        mater_dict: dict, map material to number
        """
        self.name = name
        self.dim = 2
        self.is_cyl = is_cyl
        self.sequence = list()
        self.has_domain = False
        self.mater_set = set()
        self.mater_dict = dict()
    
    def create_domain(self, bl=(0.0, 0.0), domain=(1.0, 1.0),
                      default_mater='Plasma'):
        """
        Create the Domain.
        
        bl: unit in m, (2, ) tuple
        domain: unit in m, (2, ) tuple, width and height
        mater: str, var, Domain mater is fixed to 'Plasma'
        """
        self.bl = np.asarray(bl)
        self.domain = np.asarray(domain)
        self.mater = default_mater
        self.mater_set.add(self.mater)
        self.mater_dict.update({self.mater:0})
        self.has_domain = True

    def add_shape(self, shape):
        """
        Add shape to the geometry.
        
        shape: class, Rectangle()
        """
        if self.has_domain:
            self.sequence.append(shape)
            if shape.mater in self.mater_set:
                pass
            else:
                self.mater_set.add(shape.mater)
                self.mater_dict.update({shape.mater:(len(self.mater)-1)})
        else:
            res = 'Error: Domian is not created yet.'
            res += '\nRun self.create_domain() before self.add_shape()'
            return res

    def get_mater(self, posn):
        """
        Return the mater of a position.
        
        posn: unit in m, var or (2, ) array, position as input
        mater: str, var, material name
        """
        mater = 'Plasma'
        # To add domain check here
        for shape in self.sequence:
            if posn in shape:
                mater = shape.mater
        return mater

    def plot(self, figsize=(8, 8), dpi=300, ihoriz=1):
        """
        Plot the geometry.
        
        figsize: unit in inch, (2, ) tuple, determine the fig/canvas size
        dpi: dimless, int, Dots Per Inch
        """ 
        if ihoriz:
            fig, axes = plt.subplots(1, 2, figsize=figsize, dpi=dpi,
                                     constrained_layout=True)
        else:
            fig, axes = plt.subplots(2, 1, figsize=figsize, dpi=dpi,
                                     constrained_layout=True)
        ax = axes[0]
        
        for shape in self.sequence:
            if shape.type == 'Rectangle':
                
                temp_col = color_dict[self.mater[shape.mater]]
                ax.add_patch(
                    patch.Rectangle(shape.bl, shape.width, shape.height,
                                    facecolor=temp_col))
        ax = axes[1]
        ax.add_patch(
            patch.Rectangle(self.bl, self.domain[0], self.domain[1], 
                            facecolor='purple'))
        for shape in self.sequence:
            if shape.type == 'Rectangle':
                ax.add_patch(
                    patch.Rectangle(shape.bl, shape.width, shape.height,
                                    facecolor='w', edgecolor='w'))
        for ax in axes:
            ax.set_xlim(self.bl[0], self.bl[0] + self.domain[0])
            ax.set_ylim(self.bl[1], self.bl[1] + self.domain[1])
        fig.savefig(self.name, dpi=dpi)
        plt.close()

class FeatMod2D(Base):
    """Define the geometry for 2D Feature Model."""
    
    pass

class RctMod2D(Base):
    """Define the geometry for 2D Reactor Model."""
    
    pass

class RctMod1D(Base):
    """Define the geometry for 1D Reactor Model."""
    
    pass


class Rectangle():
    """Rectangle is a 2D basic shape."""
    
    def __init__(self, mater, bottom_left, up_right):
        """
        Init the Rectangle.
        
        bottom_left: unit in m, (2, ) tuple, point position
        up_right: unit in m, (2, ) tuple, point position
        type: str, var, type of Shape
        """
        self.mater = mater
        self.bl = np.asarray(bottom_left)
        self.ur = np.asarray(up_right)
        self.width = self.ur[0] - self.bl[0]
        self.height = self.ur[1] - self.bl[1]
        self.type = 'Rectangle'

    def __str__(self):
        """Print Rectangle info."""
        res = 'Rectangle:'
        res += f'\nbottom left = {self.bl} m'
        res += f'\nup right = {self.ur} m'
        return res

    def __contains__(self, posn):
        """
        Determind if a position is inside the Interval.
        
        posn: unit in m, (2, ) array, position as input
        boundaries are not consindered as "Inside"
        """
        return all(self.bl <= posn) and all(posn <= self.ur)

if __name__ == '__main__':
    geom2d = Geom2d(name='Geom2D_Test', is_cyl=False)
    domain = Domain((-1.0, 0.0), (2.0, 4.0))
    geom2d.add_domain(domain)
    top = Rectangle('Metal', (-1.0, 3.5), (1.0, 4.0))
    geom2d.add_shape(top)
    bott = Rectangle('Metal', (-0.8, 0.0), (0.8, 0.2))
    geom2d.add_shape(bott)
    left = Rectangle('Metal', (-1.0, 0.0), (-0.9, 4.0))
    geom2d.add_shape(left)
    right = Rectangle('Metal', (0.9, 0.0), (1.0, 4.0))
    geom2d.add_shape(right)
    quartz = Rectangle('Quartz', (-0.9, 3.3), (0.9, 3.5))
    geom2d.add_shape(quartz)
    geom2d.plot(fname='geom2d.png')
    print(geom2d)
    print(geom2d.get_label(np.array([0., 0.])))
