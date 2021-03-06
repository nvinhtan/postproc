# -*- coding: utf-8 -*-
"""
@author: B. Font Garcia
@description: Module containing functions to calculate derivatives, averages, decompositions, vorticity.
@contact: b.fontgarcia@soton.ac.uk
"""
# Imports
import numpy as np


# Functions
def avg_z(u):
    """
    Return the span-wise spatial average of a three-dimensional field.
    If the passed u is spanwise periodic use trapz()/(n-1). Otherwise mean().
    :param u: The field to be spanwise-averaged.
    :return: Return the span-wise spatial average of a three-dimensional field.
    """
    if not len(u.shape)==3:
        raise ValueError("Fields must be three-dimensional")
    else:
        if np.array_equal(u[..., 0], u[..., -1]): # Periodic on last axis
            return np.trapz(u, axis=2)/(u.shape[2]-1)
        else:
            return u.mean(axis=2)

def make_periodic(u, **kwargs): # Methods t = True (add layer), t = False (substitue last layer with 1st layer)
    add = kwargs.get('add', True)
    if add:
        u_temp = np.zeros((u.shape[0], u.shape[1], u.shape[2] + 1))
        u_temp[..., :-1], u_temp[..., -1] = u, u[..., 0]
        u = u_temp
    else:
        u[..., -1] = u[..., 0]
    return u


def decomp_z(u):
    """
    :param u: field to be decomposed in z direction.
    :return: the average and the fluctuating parts of a three-dimensional field spatially averaged
    in the span-wise direction.
    """
    if not len(u.shape)==3:
        raise ValueError("Fields must be three-dimensional")
    else:
        u_avg = avg_z(u)
        u_f = u-u_avg[:, :, None]
        return u_avg, u_f


def ddx(u):
    """
    :param u: n-dimensional field.
    :return: the first-order derivative in the i direction of (n>=1 dimensional) field.
    """
    return np.gradient(u, axis=0, edge_order=2)


def ddy(u):
    """
    :param u: n-dimensional field.
    :return: the first-order derivative in the j direction of (n>=2 dimensional) field.
    """
    return np.gradient(u, axis=1, edge_order=2)


def ddz(u):
    """
    :param u: n-dimensional field.
    :return: the first-order derivative in the k direction of (n>=3 dimensional) field.
    """
    if np.array_equal(u[..., 0], u[..., -1]):  # Periodic on last axis
        u_temp = np.zeros((u.shape[0], u.shape[1], u.shape[2]+2))
        u_temp[:, :, 1:-1], u_temp[:, :, 0], u_temp[:, :, -1] = u, u[:, :, -1], u[:, :, 0]
        del u
        dudz = np.gradient(u_temp, axis=2, edge_order=2)
        del u_temp
        return dudz[:, :, 1:-1]
    else:
        return np.gradient(u, axis=2, edge_order=2)

def vortz(u, v):
    """
    :param u: x component of the velocity vector field.
    :param v: y component of the velocity vector field.
    :return: The z-vorticity of a two-dimensional velocity vector field
    """
    if not (len(u.shape)==2 and len(v.shape)==2):
        raise ValueError("Fields must be two-dimensional")
    else:
        return ddx(v)-ddy(u)

def vort(u, v, w, **kwargs):
    """
    :param u: x component of the velocity vector field.
    :param v: y component of the velocity vector field.
    :param w: z component of the velocity vector field.
    :param kwargs:
        periodic: Used to determine if the field is span-wise periodic o not.
    :return: the three components of the vorticity of a three-dimensional velocity vector field.
    """
    periodic = kwargs.get('periodic', False)

    if not (len(u.shape)==3 and len(v.shape)==3 and len(w.shape)==3):
        raise ValueError("Fields must be three-dimensional")
    else:
        return ddy(w)-ddz(v, periodic=periodic), ddz(u, periodic=periodic)-ddx(w), ddx(v)-ddy(u)
