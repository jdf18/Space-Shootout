from math import sqrt, atan, degrees, floor, ceil, trunc

class Vector2:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def magnitude(self):
		return sqrt(self.x*self.x + self.y*self.y)
	def magnitude2(self):
		return self.x*self.x + self.y*self.yself.x, self.y, self.z
	def angle(self):
		return (degrees(atan(self.y/self.x)) % 180) + (180 if self.y < 0 else 0)

	def __pos__(self): return self
	def __neg__(self): return Vector2(-self.x, -self.y)
	def __abs__(self): return Vector2(abs(self.x), abs(self.y))
	def __invert__(self): pass
	def __round__(self, n): return Vector2(round(self.x, n), round(self.y, n))
	def __floor__(self): return Vector2(floor(self.x), floor(self.y))
	def __ceil__(self): return Vector2(ceil(self.x), ceil(self.y))
	def __trunc__(self): return Vector2(trunc(self.x), trunc(self.y))
	# Augmented Assignment
	def __iadd__(self, other):
		if type(other) == Vector2: self.x, self.y = self.x+other.x, self.y+other.y
		elif type(other) == complex: self.x, self.y = self.x+other.real, self.y+other.imag
		elif type(other) in (int, float): self.x, self.y = self.x+other, self.y+other
		else: raise NotImplemented()
	def __isub__(self, other):
		if type(other) == Vector2: self.x, self.y = self.x-other.x, self.y-other.y
		elif type(other) == complex: self.x, self.y = self.x-other.real, self.y-other.imag
		elif type(other) in (int, float): self.x, self.y = self.x-other, self.y-other
		else: raise NotImplemented()
	def __imul__(self, other):
		if type(other) == Vector2: self.x, self.y = self.x*other.x, self.y*other.y
		elif type(other) == complex: self.x, self.y = self.x*other.real, self.y*other.imag
		elif type(other) in (int, float): self.x, self.y = self.x*other, self.y*other
		else: raise NotImplemented()
	def __ifloordiv__(self, other):
		if type(other) == Vector2: self.x, self.y = self.x//other.x, self.y//other.y
		elif type(other) == complex: self.x, self.y = self.x//other.real, self.y//other.imag
		elif type(other) in (int, float): self.x, self.y = self.x//other, self.y//other
		else: raise NotImplemented()
	def __idiv__(self, other):
		if type(other) == Vector2: self.x, self.y = self.x/other.x, self.y/other.y
		elif type(other) == complex: self.x, self.y = self.x/other.real, self.y/other.imag
		elif type(other) in (int, float): self.x, self.y = self.x/other, self.y/other
		else: raise NotImplemented()
	def __itruediv__(self, other):
		if type(other) == Vector2: self.x, self.y = self.x/other.x, self.y/other.y
		elif type(other) == complex: self.x, self.y = self.x/other.real, self.y/other.imag
		elif type(other) in (int, float): self.x, self.y = self.x/other, self.y/other
		else: raise NotImplemented()
	def __imod__(self, other):
		if type(other) == Vector2: self.x, self.y = self.x%other.x, self.y%other.y
		elif type(other) == complex: self.x, self.y = self.x%other.real, self.y%other.imag
		elif type(other) in (int, float): self.x, self.y = self.x%other, self.y%other
		else: raise NotImplemented()
	def __ipow__(self, other):
		if type(other) == Vector2: self.x, self.y = self.x**other.x, self.y**other.y
		elif type(other) == complex: self.x, self.y = self.x**other.real, self.y**other.imag
		elif type(other) in (int, float): self.x, self.y = self.x**other, self.y**other
		else: raise NotImplemented()
	def __ilshift__(self): pass
	def __irshift__(self): pass
	def __iand__(self): pass
	def __ior__(self): pass
	def __ixor__(self): pass
	# Type conversion
	def __int__(self): return round(self.magnitude2())
	def __float__(self): return self.magnitude()
	def __complex__(self): return complex(self.x, self.y)
	# String methods
	def __str__(self): return "(%s,%s)" % (self.x, self.y)
	def __repr__(self): return "(%s,%s)" % (self.x, self.y)
	def __unicode__(self): pass
	def __format__(self, __format): return __format.format(x=self.x, y=self.y)
	def __nonzero__(self): return (self.x != 0) or (self.y != 0)
	# Operator methods
	def __add__(self, other):
		if type(other) == Vector2: return Vector2(self.x+other.x, self.y+other.y)
		elif type(other) == complex: return Vector2(self.x+other.real, self.y+other.imag)
		elif type(other) in (int, float): return Vector2(self.x+other, self.y+other)
		else: raise NotImplemented()
	def __sub__(self, other):
		if type(other) == Vector2: return Vector2(self.x-other.x, self.y-other.y)
		elif type(other) == complex: return Vector2(self.x-other.real, self.y-other.imag)
		elif type(other) in (int, float): return Vector2(self.x-other, self.y-other)
		else: raise NotImplemented()
	def __mul__(self, other):
		if type(other) == Vector2: return Vector2(self.x*other.x, self.y*other.y)
		elif type(other) == complex: return Vector2(self.x*other.real, self.y*other.imag)
		elif type(other) in (int, float): return Vector2(self.x*other, self.y*other)
		else: raise NotImplemented()
	def __floordiv__(self, other):
		if type(other) == Vector2: return Vector2(self.x//other.x, self.y//other.y)
		elif type(other) == complex: return Vector2(self.x//other.real, self.y//other.imag)
		elif type(other) in (int, float): return Vector2(self.x//other, self.y//other)
		else: raise NotImplemented()
	def __div__(self, other):
		if type(other) == Vector2: return Vector2(self.x/other.x, self.y/other.y)
		elif type(other) == complex: return Vector2(self.x/other.real, self.y/other.imag)
		elif type(other) in (int, float): return Vector2(self.x/other, self.y/other)
		else: raise NotImplemented()
	def __truediv__(self, other):
		if type(other) == Vector2: return Vector2(self.x/other.x, self.y/other.y)
		elif type(other) == complex: return Vector2(self.x/other.real, self.y/other.imag)
		elif type(other) in (int, float): return Vector2(self.x/other, self.y/other)
		else: raise NotImplemented()
	def __mod__(self, other):
		if type(other) == Vector2: return Vector2(self.x%other.x, self.y%other.y)
		elif type(other) == complex: return Vector2(self.x%other.real, self.y%other.imag)
		elif type(other) in (int, float): return Vector2(self.x%other, self.y%other)
		else: raise NotImplemented()
	def __pow__(self, other):
		if type(other) == Vector2: return Vector2(self.x**other.x, self.y**other.y)
		elif type(other) == complex: return Vector2(self.x**other.real, self.y**other.imag)
		elif type(other) in (int, float): return Vector2(self.x**other, self.y**other)
		else: raise NotImplemented()
	def __eq__(self, other):
		if type(other) == Vector2: return (self.x==other.x) and (self.y==other.y)
		elif type(other) == complex: return (self.x==other.real) and (self.y==other.imag)
		elif type(other) in (int, float): return self.magnitude() == other
		else: raise NotImplemented()
	def __ne__(self, other):
		if type(other) == Vector2: return not ((self.x==other.x) and (self.y==other.y))
		elif type(other) == complex: return not ((self.x==other.real) and (self.y==other.imag))
		elif type(other) in (int, float): self.magnitude() != other
		else: raise NotImplemented()
	def __lt__(self, other):
		if type(other) == Vector2: return not ((self.x<other.x) and (self.y<other.y))
		elif type(other) == complex: return not ((self.x<other.real) and (self.y<other.imag))
		elif type(other) in (int, float): self.magnitude() < other
		else: raise NotImplemented()
	def __le__(self, other):
		if type(other) == Vector2: return not ((self.x<=other.x) and (self.y<=other.y))
		elif type(other) == complex: return not ((self.x<=other.real) and (self.y<=other.imag))
		elif type(other) in (int, float): self.magnitude() <= other
		else: raise NotImplemented()
	def __gt__(self, other):
		if type(other) == Vector2: return not ((self.x>other.x) and (self.y>other.y))
		elif type(other) == complex: return not ((self.x>other.real) and (self.y>other.imag))
		elif type(other) in (int, float): self.magnitude() > other
		else: raise NotImplemented()
	def __ge__(self, other):
		if type(other) == Vector2: return not ((self.x>=other.x) and (self.y>=other.y))
		elif type(other) == complex: return not ((self.x>=other.real) and (self.y>=other.imag))
		elif type(other) in (int, float): self.magnitude() >= other
		else: raise NotImplemented()

class Vector3:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
	def magnitude(self):
		return sqrt((self.x*self.x) + (self.y*self.y) + (self.z*self.z))
	def magnitude2(self):
		return (self.x*self.x) + (self.y*self.y) + (self.z*self.z)
		
	def __pos__(self): return self
	def __neg__(self): return Vector3(-self.x, -self.y, -self.z)
	def __abs__(self): return Vector3(abs(self.x), abs(self.y), abs(self.z))
	def __invert__(self): pass
	def __round__(self, n): return Vector3(round(self.x, n), round(self.y, n), round(self.z, n))
	def __floor__(self): return Vector3(floor(self.x), floor(self.y), floor(self.z))
	def __ceil__(self): return Vector3(ceil(self.x), ceil(self.y), ceil(self.z))
	def __trunc__(self): return Vector3(trunc(self.x), trunc(self.y), trunc(self.z))
	# Augmented Assignment
	def __iadd__(self, other):
		if type(other) == Vector3: self.x, self.y, self.z = self.x+other.x, self.y+other.y, self.z+other.z
		elif type(other) in (int, float): self.x, self.y, self.z = self.x+other, self.y+other, self.z+other
		else: raise NotImplemented()
	def __isub__(self, other):
		if type(other) == Vector3: self.x, self.y, self.z = self.x-other.x, self.y-other.y, self.z-other.z
		elif type(other) in (int, float): self.x, self.y, self.z = self.x-other, self.y-other, self.z-other
		else: raise NotImplemented()
	def __imul__(self, other):
		if type(other) == Vector3: self.x, self.y, self.z = self.x*other.x, self.y*other.y, self.z*other.z
		elif type(other) in (int, float): self.x, self.y, self.z = self.x*other, self.y*other, self.z*other
		else: raise NotImplemented()
	def __ifloordiv__(self, other):
		if type(other) == Vector3: self.x, self.y, self.z = self.x//other.x, self.y//other.y, self.z//other.z
		elif type(other) in (int, float): self.x, self.y, self.z = self.x//other, self.y//other, self.z//other
		else: raise NotImplemented()
	def __idiv__(self, other):
		if type(other) == Vector3: self.x, self.y, self.z = self.x/other.x, self.y/other.y, self.z/other.z
		elif type(other) in (int, float): self.x, self.y, self.z = self.x/other, self.y/other, self.z/other
		else: raise NotImplemented()
	def __itruediv__(self, other):
		if type(other) == Vector3: self.x, self.y, self.z = self.x/other.x, self.y/other.y, self.z/other.z
		elif type(other) in (int, float): self.x, self.y, self.z = self.x/other, self.y/other, self.z/other
		else: raise NotImplemented()
	def __imod__(self, other):
		if type(other) == Vector3: self.x, self.y, self.z = self.x%other.x, self.y%other.y, self.z&other.z
		elif type(other) in (int, float): self.x, self.y, self.z = self.x%other, self.y%other, self.z%other
		else: raise NotImplemented()
	def __ipow__(self, other):
		if type(other) == Vector3: self.x, self.y, self.z = self.x**other.x, self.y**other.y, self.z**other.z
		elif type(other) in (int, float): self.x, self.y, self.z = self.x**other, self.y**other, self.z**other
		else: raise NotImplemented()
	def __ilshift__(self): pass
	def __irshift__(self): pass
	def __iand__(self): pass
	def __ior__(self): pass
	def __ixor__(self): pass
	# Type conversion
	def __int__(self): return round(self.magnitude2())
	def __float__(self): return self.magnitude()
	def __complex__(self): return complex(self.x, self.y, self.z)
	# String methods
	def __str__(self): return "(%s,%s,%s)" % (self.x, self.y, self.z)
	def __repr__(self): return "(%s,%s,%s)" % (self.x, self.y, self.z)
	def __unicode__(self): pass
	def __format__(self, __format): return __format.format(x=self.x, y=self.y, z=self.z)
	def __nonzero__(self): return (self.x != 0) or (self.y != 0) or (self.z != 0)
	# Operator methods
	def __add__(self, other):
		if type(other) == Vector3: return Vector3(self.x+other.x, self.y+other.y, self.z+other.z)
		elif type(other) in (int, float): return Vector3(self.x+other, self.y+other, self.z+other)
		else: raise NotImplemented()
	def __sub__(self, other):
		if type(other) == Vector3: return Vector3(self.x-other.x, self.y-other.y, self.z-other.z)
		elif type(other) in (int, float): return Vector3(self.x-other, self.y-other, self.z-other)
		else: raise NotImplemented()
	def __mul__(self, other):
		if type(other) == Vector3: return Vector3(self.x*other.x, self.y*other.y, self.z*other.z)
		elif type(other) in (int, float): return Vector3(self.x*other, self.y*other, self.z*other)
		else: raise NotImplemented()
	def __floordiv__(self, other):
		if type(other) == Vector3: return Vector3(self.x//other.x, self.y//other.y, self.z//other.z)
		elif type(other) in (int, float): return Vector3(self.x//other, self.y//other, self.z//other)
		else: raise NotImplemented()
	def __div__(self, other):
		if type(other) == Vector3: return Vector3(self.x/other.x, self.y/other.y, self.z/other.z)
		elif type(other) in (int, float): return Vector3(self.x/other, self.y/other, self.z/other)
		else: raise NotImplemented()
	def __truediv__(self, other):
		if type(other) == Vector3: return Vector3(self.x/other.x, self.y/other.y, self.z/other.z)
		elif type(other) in (int, float): return Vector3(self.x/other, self.y/other, self.z/other)
		else: raise NotImplemented()
	def __mod__(self, other):
		if type(other) == Vector3: return Vector3(self.x%other.x, self.y%other.y, self.z%other.z)
		elif type(other) in (int, float): return Vector3(self.x%other, self.y%other, self.z%other)
		else: raise NotImplemented()
	def __pow__(self, other):
		if type(other) == Vector3: return Vector3(self.x**other.x, self.y**other.y, self.z**other.z)
		elif type(other) in (int, float): return Vector3(self.x**other, self.y**other, self.z**other)
		else: raise NotImplemented()
	def __eq__(self, other):
		if type(other) == Vector3: return (self.x==other.x) and (self.y==other.y) and (self.z==other.z)
		elif type(other) in (int, float): return self.magnitude() == other
		else: raise NotImplemented()
	def __ne__(self, other):
		if type(other) == Vector3: return not ((self.x==other.x) and (self.y==other.y) and (self.z==other.z))
		elif type(other) in (int, float): self.magnitude() != other
		else: raise NotImplemented()
	def __lt__(self, other):
		if type(other) == Vector3: return ((self.x<other.x) and (self.y<other.y) and (self.z<other.z))
		elif type(other) in (int, float): self.magnitude() < other
		else: raise NotImplemented()
	def __le__(self, other):
		if type(other) == Vector3: return ((self.x<=other.x) and (self.y<=other.y) and (self.z<=other.z))
		elif type(other) in (int, float): self.magnitude() <= other
		else: raise NotImplemented()
	def __gt__(self, other):
		if type(other) == Vector3: return ((self.x>other.x) and (self.y>other.y) and (self.z>other.z))
		elif type(other) in (int, float): self.magnitude() > other
		else: raise NotImplemented()
	def __ge__(self, other):
		if type(other) == Vector3: return ((self.x>=other.x) and (self.y>=other.y) and (self.z>=other.z))
		elif type(other) in (int, float): self.magnitude() >= other
		else: raise NotImplemented()