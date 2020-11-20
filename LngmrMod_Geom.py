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

class Geom(object):
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
    
    def __str__(self):
        """Print out info."""
        res = f'This is a {self.dim}D geometry called {self.name},'
        if self.is_cyl:
            res += '\nwith Cylindrical symmetry'
        else:
            res += '\nwith Cartesian symmetry'
        return res
    
    def add_domain(self, domain):
        """
        Add domain to the geometry.
        
        domain: class Shape
        """
        self.domain = domain
        self.mater_set.add(domain.mater)
        self.mater_dict.update({domain.mater:0})
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


class Shape():
    """Basic geometry element."""
    
    def __init__(self, label, mater, dim):
        """
        Define the common attributes.
        
        label: str, var, label of shape
        mater: str, var, material of shape
        dim: 1 or 2, dimension of shape
        """
        self.label = label
        self.mater = mater
        self.dim = dim

class Domain2D(Shape):
    """Define 2D domain."""
    
    def __init__(self, bl=(0.0, 0.0), domain=(1.0, 1.0)):
        """
        Define the init attributes.
        
        label: 'A', label of shape
        mater: 'Plasma', material of shape
        dim: 2, dimension of shape
        bl: float, (2, ) tuple, bottom left of domain
        tr: float, (2, ) tuple, top right of domain
        domain: float, (2, ) tuple, width and height of domain
        type: str, var, type of domain
        """
        super().__init__(label='A', mater='Plasma', dim=2)
        self.bl = np.asarray(bl)
        self.domain = np.asarray(domain)
        self.tr = self.bl + self.domain
        self.width, self.height = self.domain
        self.type = 'Domain'

    def __contains__(self, posn):
        """
        Determind if a position is inside the Domain.
        
        posn: unit in m, (2, ) array, position as input
        boundaries are consindered as "Inside"
        """
        return all(self.bl <= posn) and all(posn <= self.tr)

class Domain1D(Shape):
    """Define 1D domain."""
    
    def __init__(self, domain=(0.0, 1.0)):
        """
        Define the init attributes.
        
        label: 'A', label of shape
        mater: 'Plasma', material of shape
        dim: 1, dimension of shape
        domain: float, (2, ) tuple, left and right of domain
        type: str, var, type of domain
        """
        super().__init__(label='A', mater='Plasma', dim=1)
        self.domain = np.asarray(domain)
        self.type = 'Domain'

    def __contains__(self, posn):
        """
        Determind if a position is inside the Domain.
        
        posn: unit in m, (2, ) array, position as input
        boundaries are consindered as "Inside"
        """
        return self.domain[0] <= posn <= self.domain[1]

class Rectangle(Shape):
    """Rectangle is a 2D basic shape."""
    
    def __init__(self, mater, bottom_left, top_right):
        """
        Init the Rectangle.
        
        bottom_left: unit in m, (2, ) tuple, point position
        up_right: unit in m, (2, ) tuple, point position
        type: str, var, type of Shape
        """
        super().__init__(label='A', mater=mater, dim=2)
        self.bl = np.asarray(bottom_left)
        self.tr = np.asarray(top_right)
        self.width = self.tr[0] - self.bl[0]
        self.height = self.tr[1] - self.bl[1]
        self.type = 'Rectangle'

    def __contains__(self, posn):
        """
        Determind if a position is inside the Interval.
        
        posn: unit in m, (2, ) array, position as input
        boundaries are not consindered as "Inside"
        """
        return all(self.bl <= posn) and all(posn <= self.tr)

class Interval(Shape):
    """Rectangle is a 1D basic shape."""
    
    def __init__(self, mater, lr):
        """
        Init the Interval.
        
        lr: unit in m, (2, ) tuple, defines the domain
        mater: str, var, label of Interval.
        """
        super().__init__(label='A', mater=mater, dim=1)
        self.lr = np.asarray(lr)
        self.length = self.lr[1] - self.lr[0]

    def __contains__(self, posn):
        """
        Determind if a position is inside the Interval.
        
        posn: unit in m, (2, ) array, position as input
        boundaries are consindered as "Inside"
        """
        return self.lr[0] <= posn <= self.lr[1]


class RctMod2D(Geom):
    """Define the geometry for 2D Reactor Model."""
    
    def __str__(self):
        """Print out info."""
        res = '\nThis is a geometry for 2D Reactor Model'
        res += f'\nwith domain {self.domain.width} m'
        res += f' x {self.domain.height} m'
        return super().__str__() + res
    
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
        temp_col = color_dict[self.mater_dict[self.domain.mater]]
        ax.add_patch(
            patch.Rectangle(self.domain.bl, self.domain.width, self.domain.height,
                            facecolor='w'))
        for shape in self.sequence:
            
                
            if shape.type == 'Rectangle':
                
                temp_col = color_dict[self.mater_dict[shape.mater]]
                ax.add_patch(
                    patch.Rectangle(shape.bl, shape.width, shape.height,
                                    facecolor=temp_col))
                
        ax = axes[1]
        ax.add_patch(
            patch.Rectangle(self.domain.bl, self.domain.width, self.domain.height,
                            facecolor='purple'))
        for shape in self.sequence:
            if shape.type == 'Rectangle':
                ax.add_patch(
                    patch.Rectangle(shape.bl, shape.width, shape.height,
                                    facecolor='w', edgecolor='w'))
        for ax in axes:
            ax.set_xlim(self.domain.bl[0], self.domain.tr[0])
            ax.set_ylim(self.domain.bl[1], self.domain.tr[1])
        fig.savefig(self.name, dpi=dpi)
        plt.close()

class FeatMod2D(RctMod2D):
    """Define the geometry for 2D Feature Model."""
    
    pass


class RctMod1D(Geom):
    """Define the geometry for 1D Reactor Model."""
    
    def __init__(self, name='Base', is_cyl=False):
        """Reinit attributes only for self.dim=1."""
        super().__init__(name=name, is_cyl=is_cyl)
        self.dim = 1
    
    def __str__(self):
        """Print out info."""
        res = '\nThis is a geometry for 1D Reactor Model'
        res += f'\nwith domain {self.domain.domain} m'
        return super().__str__() + res
    
    def plot(self, figsize=(8, 8), dpi=300):
        """
        Plot the 1D geometry.
        
        figsize: unit in inch, (2, ) tuple, determine the fig/canvas size
        dpi: dimless, int, Dots Per Inch
        """
        fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi,
                               constrained_layout=True)
        ax.plot(self.domain.domain, (0.0, 0.0), 'o-',
                linewidth=5, color='purple', markersize=16)
        for segment in self.sequence:
            temp_col = color_dict[self.mater_dict[segment.mater]]
            ax.plot(segment.lr, (0.0, 0.0), 'o-',
                linewidth=5, color=temp_col, markersize=16)
        fig.savefig(self.name, dpi=dpi)
        plt.close()


if __name__ == '__main__':
    import os
    import glob
    for i in glob.glob("*.png"):
        os.remove(i)

    # build the geometry
    ICP2d = RctMod2D(name='ICP2D', is_cyl=False)
    #               (left, bottom), (width, height)
    domain2d = Domain2D((-0.25, 0.0),    (0.5, 0.4))
    ICP2d.add_domain(domain2d)
    
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
    
    
    """Test 1D Geometry."""
    ICP1d = RctMod1D(name='ICP1D', is_cyl=False)
    domain1d = Domain1D(domain=(-10.0, 10.0))
    ICP1d.add_domain(domain1d)
    seg1 = Interval('M', (-10.0, -8.0))
    ICP1d.add_shape(seg1)
    seg2 = Interval('M', (5.0, 10.0))
    ICP1d.add_shape(seg2)
    seg3 = Interval('D', (-6.0, 0.0))
    ICP1d.add_shape(seg3)
    ICP1d.plot()
    print(ICP1d)