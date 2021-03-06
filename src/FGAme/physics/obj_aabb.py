# -*- coding: utf8 -*-

from FGAme.physics.obj_all import LinearRigidBody
from FGAme.mathutils import aabb_bbox, AABB

__all__ = ['AABB']


class AABB(LinearRigidBody):

    '''Define um objeto físico que responde a colisões como uma caixa de
    contorno alinhada aos eixos.

    Deve ser inicializada ou por uma tupla com os valores (xmin, xmax, ymin,
    ymax) ou por definido shape=(lado x, lado y).


    Example
    -------

    Os objetos tipo AABB podem ser iniciados de 4 maneiras diferentes.
    A primeira é fornecendo um formato e opcionalmente a posição do centro::

        >>> A = AABB(shape=(100, 200))
        >>> A.bbox  # (xmin, xmax, ymin, ymax)
        (-50.0, 50.0, -100.0, 100.0)

    A segunda opção é indicar o uma tupla com a posição do vértice inferior
    esquerdo e a forma::

        >>> B = AABB(rect=(0, 0, 100, 200))
        >>> B.bbox
        (0.0, 100.0, 0.0, 200.0)

    A outra maneira é fornecer a caixa de contorno como uma lista::

        >>> C = AABB(bbox=(0, 100, 0, 200))

    E, finalmente, podemos fornecer os valores de xmin, xmax, ymin, ymax
    individualmente::

        >>> D = AABB(0, 100, 0, 200)
        >>> E = AABB(xmin=0, xmax=100, ymin=0, ymax=200)

    Em todos os casos, a massa já é calculada automaticamente a partir da área
    assumindo-se uma densidade de 1.0. O momento de inércia é infinito pois
    trata-se de um objeto sem dinâmica angular::

        >>> A.mass, A.inertia  # 20.000 == 200 x 100
        (20000.0, inf)

    '''

    def __init__(self, xmin=None, xmax=None, ymin=None, ymax=None,
                 pos=None, vel=(0, 0), mass=None, density=None,
                 bbox=None, shape=None, rect=None):

        # Define as propriedades das caixas de contorno
        xmin, xmax, ymin, ymax = aabb_bbox(bbox=bbox, rect=rect,
                                           shape=shape, pos=pos,
                                           xmin=xmin, xmax=xmax,
                                           ymin=ymin, ymax=ymax)

        pos = ((xmin + xmax) / 2., (ymin + ymax) / 2.)
        super(AABB, self).__init__(xmin, xmax, ymin, ymax,
                                   pos, vel,
                                   mass=mass, density=density)

    def __repr__(self):
        tname = type(self).__name__
        vel = ', '.join('%.1f' % x for x in self.vel)
        data = ', '.join('%.1f' % x for x in self.bbox())
        return '%s(bbox=[%s], vel=(%s))' % (tname, data, vel)

    # Torna as os limites da AABB modificáveis ################################
    @property
    def xmin(self):
        return self._xmin

    @xmin.setter
    def xmin(self, value):
        self._xmin = float(value)
        self._pos.x = (self._xmax - self._xmin) / 2

    @property
    def xmax(self):
        return self._xmax

    @xmax.setter
    def xmax(self, value):
        self._xmax = float(value)
        self._pos.x = (self._xmax - self._xmin) / 2

    @property
    def ymin(self):
        return self._ymin

    @ymin.setter
    def ymin(self, value):
        self._ymin = float(value)
        self._pos.y = (self._ymax - self._ymin) / 2

    @property
    def ymax(self):
        return self._ymax

    @ymax.setter
    def ymax(self, value):
        self._ymax = float(value)
        self._pos.y = (self._ymax - self._ymin) / 2

    # Propriedades geométricas ################################################
    def area(self):
        return (self._xmax - self._xmin) * (self._ymax - self._ymin)

    def ROG_sqr(self):
        a = (self._xmax - self._xmin)
        b = (self._ymax - self._ymin)
        return (a ** 2 + b ** 2) / 12

    def primitive(self):
        return AABB(bbox=self.bbox)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
