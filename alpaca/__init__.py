import os

#lisht = os.listdir()
__all__ = []
for i in os.listdir('alpaca'): 
    if i.endswith('.py') and not i.startswith('_'):
        print(i)
        __all__.append(i.replace('.py', '', 1))
