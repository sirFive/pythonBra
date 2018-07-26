class Animal(object):
    def run(self):
        print('animal run')

    def run_twice(self,s):
        s.run()
        s.run()

class Dog(Animal):
    def run(self):
        print('dog class run')

    def eat(self):
        print('eat dog')

class Tt(object):
    def run(self):
        print('tt class run')

d = Dog()
d.run()
d.run_twice(d)

t = Tt()
t.run()

a = Animal()
a.run()
a.run_twice(t)


#运行结果
# dog class run
# dog class run
# dog class run
# tt class run
# animal run
# tt class run
# tt class run