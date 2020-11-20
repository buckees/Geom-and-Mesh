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
                self.mater_dict.update({shape.mater:(len(self.mater_set)-1)})
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
                
                temp_col = color_dict[self.mater_dict[shape.mater]]
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
    # build the geometry
    ICP2d = RctMod2D(name='ICP2D', is_cyl=False)
    #               (left, bottom), (width, height)
    ICP2d.create_domain((-0.25, 0.0),    (0.5, 0.4))
    
    # Add metal wall to all boundaries
    # In Metal, vector potential A = 0
    #                        (left, bottom), (right, top)
    top = Rectangle('Metal', (-0.25, 0.38), (0.25, 0.4))
    ICP2d.add_shape(top)
    bott = Rectangle('Metal', (-0.25, 0.0), (0.25, 0.02))
    ICP2d.add_shape(bott)
    # use -0.231 instead of -0.23 for mesh asymmetry
    left = Rectangle('Metal', (-0.25, 0.0), (-0.231, 0.4)) 
    ICP2d.add_shape(left)
    right = Rectangle('Metal', (0.23, 0.0), (0.25, 4.0))
    ICP2d.add_shape(right)
    ped = Rectangle('Metal', (-0.20, 0.0), (0.20, 0.1))
    ICP2d.add_shape(ped)
    
    
    # Add quartz to separate coil area and plasma area
    # Quartz conductivity = 1e-5 S/m
    quartz = Rectangle('Quartz', (-0.23, 0.3), (0.23, 0.32))
    ICP2d.add_shape(quartz)
    
    # Add air to occupy the top coil area to make it non-plasma
    # Air concudctivity = 0.0 S/m
    air = Rectangle('Air', (-0.23, 0.32), (0.23, 0.38))
    ICP2d.add_shape(air)
    
    # Add coil within air and overwirte air
    # coil 1, 2, 3: J = -J0*exp(iwt)
    # coil 4, 5, 6: J = +J0*exp(iwt)
    coil1 = Rectangle('Coil', (-0.20, 0.34), (-0.18, 0.36))
    ICP2d.add_shape(coil1)
    coil2 = Rectangle('Coil', (-0.14, 0.34), (-0.12, 0.36))
    ICP2d.add_shape(coil2)
    coil3 = Rectangle('Coil', (-0.08, 0.34), (-0.06, 0.36))
    ICP2d.add_shape(coil3)
    coil4 = Rectangle('Coil', (0.18, 0.34), (0.20, 0.36))
    ICP2d.add_shape(coil4)
    coil5 = Rectangle('Coil', (0.12, 0.34), (0.14, 0.36))
    ICP2d.add_shape(coil5)
    # use 0.081 instead of 0.08 for mesh asymmetry
    coil6 = Rectangle('Coil', (0.06, 0.34), (0.081, 0.36))
    ICP2d.add_shape(coil6)
    
    
    
    ICP2d.plot(figsize=(10, 4), ihoriz=1)
    print(ICP2d)