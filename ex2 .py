import unittest
import itertools



#Question 1

def memoize(func):
    cache = {}
    def f(*args):
        if args not in cache:
            v = func(*args)
            cache[args] = v
        else:
            v = cache[args]
        return v
    return f

@memoize
def sum2(x, y):
    print('calling sum2')
    return x + y


#Question 2

class Rational:
    max = None
    
    @staticmethod
    def gcd(x,y):
        while y!=0:
            (x,y) = (y,x%y)
        return x
    
    def __init__(self, numerator, denominator=1):
        if (denominator<0):
            self.numerator = numerator*-1
            self.denominator = denominator*-1
        else:
            self.numerator = numerator
            self.denominator = denominator
        if Rational.max is None or self > Rational.max:
            Rational.max=self
            

              
    def __add__(self, other):
        mult1 = other.denominator
        mult2 = self.denominator
        num1 = self.numerator*mult1
        num2 = other.numerator*mult2
        return Rational(num1+num2,mult1*mult2)
    
    def __sub__(self,other):
        return self+Rational(other.numerator*-1,other.denominator)
    
    def __mul__(self,other):
        return Rational(self.numerator*other.numerator,self.denominator*other.denominator)
    
    def __truediv__(self,other):
        return self*Rational(other.denominator,other.numerator)

    def __gt__(self,other):
        temp1 = self.numerator * other.denominator
        temp2 = self.denominator * other.numerator
        return temp1 > temp2
    
    def __ge__(self,other):  
        temp1 = self.numerator * other.denominator
        temp2 = self.denominator * other.numerator
        return temp1 >= temp2
    
    def __lt__(self,other):
        return other > self

    
    def __le__(self,other):
        return other >= self

    
    def __eq__(self,other):
        return self.numerator*other.denominator == self.denominator*other.numerator

    
    def __ne__(self,other):
        return self.numerator*other.denominator!=self.denominator*other.numerator

    def __str__(self):
        gcd = Rational.gcd(self.numerator,self.denominator)
        newNum = self.numerator//gcd
        newDen = self.denominator//gcd
        return "%s/%s" % (newNum,newDen)
    
    def __repr__(self):
        gcd = Rational.gcd(self.numerator,self.denominator)
        newNum = self.numerator//gcd
        newDen = self.denominator//gcd
        return "Rational(%r,%r)" % (newNum,newDen)

    
#Question 3
    
def myZip(iterable1, iterable2, fill=None):
    it1 = iter(iterable1)
    it2 = iter(iterable2)
    elem1 = next(it1,fill)
    elem2 = next(it2,fill)
    while elem1 is not fill or elem2 is not fill:
        result = []
        if elem1 is not None and elem2 is not None:
             result.append(elem1)
             result.append(elem2)
             yield tuple(result)   
        elem1 = next(it1,fill)
        elem2 = next(it2,fill)
             

#Question 4
        
class MyZip:

    def __init__(self, iterable1,iterable2,fill=None):
        self.iterable1=iterable1
        self.iterable2=iterable2
        self.fill=fill

    def __iter__(self):
        
        class Iterator:
            
            def __init__(self,iterable1,iterable2,fill):
                self.it1 = iter(iterable1)
                self.it2 = iter(iterable2)
                self.fill=fill
                
            def __iter__(self):
                return self
            
            def __next__(self):
                elem1 = next(self.it1,self.fill)
                elem2 = next(self.it2,self.fill)
                result = [] 
                if  elem1 is not self.fill or elem2 is not self.fill:
                     if elem1 is not None and elem2 is not None:
                         result.append(elem1)
                         result.append(elem2)
                         return tuple(result)
                     else:
                         raise StopIteration

                else:
                    raise StopIteration
                                               
        return Iterator(self.iterable1,self.iterable2,self.fill)

    
#Question 5
    
def anagram(word):
        list = []
        fin = open('words.txt')
        permutations_of_word = [''.join(permutation) for permutation in itertools.permutations(word)]
        for line in fin:
            line = line.strip()
            if line in permutations_of_word:
                list.append(line)
        fin.close()
        return sorted(list)          

#Question 6                
class VariableDescriptor:


    def __set__(self,instance,value):
        instance._value=value
        instance._history.append(value)
        instance.wCount +=1

    def __get__(self,instance,owner):
        instance.rCount+= 1
        return instance._value

class Variable:

    def __init__(self,value):
        self.wCount=0
        self.rCount=0
        self._history = []
        self.value=value

    def readCounter(self):
        return self.rCount

    def writeCounter(self):
        return self.wCount

    def history(self):
        return self._history

    value = VariableDescriptor()

#  TESTS

class TestExercise2(unittest.TestCase):

    def test_decorator(self):
        print(sum2(1,3))
        print(sum2(1,3))
        print(sum2(1,4))

    def test_rational(self):
        half = Rational(5,10)
        third = Rational(1,3)
        self.assertEqual(repr(half),"Rational(1,2)")
        self.assertEqual(str(half),"1/2")
        self.assertEqual(half < third, False)
        self.assertEqual(half <= third, False)
        self.assertEqual(half > third, True)
        self.assertEqual(half >= third, True)
        self.assertEqual(half != third, True)
        self.assertEqual(half == third, False)
        half2 = Rational(10,20)
        self.assertEqual(half == half2, True)
        self.assertEqual(half+third, Rational(5,6))
        self.assertEqual(half-third, Rational(1,6))
        self.assertEqual(half*third, Rational(1,6))
        self.assertEqual(half/third, Rational(3,2))


    def test_myZip(self):
        g = (3*i for i in range(5))
        mzip = myZip(g, ["a", "b", "c"], fill="bye")
        self.assertEqual(mzip.__next__(), (0, 'a'))
        self.assertEqual(mzip.__next__(), (3, 'b'))


    def test_MyZip(self):
        try1 = MyZip([1,2],["a","b","c"],"bye")
        it1 = iter(try1)
        self.assertEqual(it1.__next__(),(1,"a"))
        self.assertEqual(it1.__next__(),(2,"b"))
        self.assertEqual(it1.__next__(),("bye","c"))
        try2 = MyZip([1,2],["a","b","c"])
        it2 = iter(try2)
        self.assertEqual(it2.__next__(),(1,"a"))
        self.assertEqual(it2.__next__(),(2,"b"))        


    def test_descriptor(self):
        v = Variable(8)
        self.assertEqual(v.history(),[8])
        v.value=3
        self.assertEqual(v.writeCounter(),2)
        self.assertEqual(v.readCounter(),0)
        self.assertEqual(v.value,3)
        self.assertEqual(v.readCounter(),1)

    def test_anagram(self):
        self.assertEqual(anagram('restful'),['fluster', 'fluters', 'restful'])
        self.assertEqual(anagram('rrao'),['orra', 'roar'])
        
        

        
        
        


unittest.main()   
    
                    
                
                
                
                
                
            

