#  MiniLight Python : minimal global illumination renderer
#
#  Harrison Ainsworth / HXA7241 and Juraj Sukop : 2007-2008, 2013.
#  http://www.hxa.name/minilight


from math import pi, tan
from raytracer import RayTracer
from vector3f import Vector3f
from random import Random

import re
SEARCH = re.compile('(\(.+\))\s*(\(.+\))\s*(\S+)').search

VIEW_ANGLE_MIN =  10.0
VIEW_ANGLE_MAX = 160.0

class Camera(object):

    def __init__(self, in_stream):
        for line in in_stream:
            if not line.isspace():
                p, d, a = SEARCH(line).groups()
                self.view_position = Vector3f(p)
                self.view_direction = Vector3f(d).unitize()
                if self.view_direction.is_zero():
                    self.view_direction = Vector3f(0.0, 0.0, 1.0)
                self.view_angle = min(max(VIEW_ANGLE_MIN, float(a)),
                    VIEW_ANGLE_MAX) * (pi / 180.0)
                self.right = Vector3f(0.0, 1.0, 0.0).cross(self.view_direction
                    ).unitize()
                if self.right.is_zero():
                    self.up = Vector3f(0.0, 0.0,
                        1.0 if self.view_direction.y else -1.0)
                    self.right = self.up.cross(self.view_direction).unitize()
                else:
                    self.up = self.view_direction.cross(self.right).unitize()
                break

    def get_pixel(self, scene, random, image, x, y, sample_no):
        raytracer = RayTracer(scene)
        aspect = float(image.height) / float(image.width)
		for i in range(sample_no):
			x_coefficient = ((x + random.real64()) * 2.0 / image.width) \
				- 1.0
			y_coefficient = ((y + random.real64()) * 2.0 / image.height) \
				- 1.0
			offset = self.right * x_coefficient + \
				self.up * (y_coefficient * aspect)
			sample_direction = (self.view_direction +
				(offset * tan(self.view_angle * 0.5))).unitize()
			radiance = raytracer.get_radiance(self.view_position,
				sample_direction, random)
				
            for a in radiance:
                self.pixels[index] += a
                index += 1
				
			return radiance
				
    def get_frame(self, scene, random, image):
        raytracer = RayTracer(scene)
        aspect = float(image.height) / float(image.width)
        for y in range(image.height):
            for x in range(image.width):
                x_coefficient = ((x + random.real64()) * 2.0 / image.width) \
                    - 1.0
                y_coefficient = ((y + random.real64()) * 2.0 / image.height) \
                    - 1.0
                offset = self.right * x_coefficient + \
                    self.up * (y_coefficient * aspect)
                sample_direction = (self.view_direction +
                    (offset * tan(self.view_angle * 0.5))).unitize()
                radiance = raytracer.get_radiance(self.view_position,
                    sample_direction, random)
                image.add_to_pixel(x, y, radiance)
