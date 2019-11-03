from termcolor import colored

def colorBoolean(boolean):
    if boolean:
        return colored(boolean, "green")
    else:
        return colored(boolean, "red")

def colorTuple(target,colors):
    if callable(colors):
        return colorTupleWithCallback(target,colors)
    elif type(colors) is str:
        return colorTupleWithCallback(target,lambda x: colored(x, colors))
    elif iter(colors):
        return colorTupleWithIterable(target, colors)
    else:
        raise ValueError("colors must be either callable, iterable, or string")

def colorTupleWithCallback(target, callback):
    items = []
    for item in target:
        items.append(callback(item))
    return "(" + ", ".join(items) + ")" 

def colorTupleWithIterable(target, iterable, wrapAround=True):
    items = [] # list(target)
    colorLen = len(iterable)
    for i in range(len(target)):
        item = target[i]
        color = iterable[i % colorLen]
        if i > colorLen and not wrapAround:
            # force it to be str else it may throw an exception
            items.append(str(item))
            continue
        else:
            if type(color) is str:
                items.append(colored(item, color))
            elif callable(color):
                items.append(color(item))
            else:
                raise ValueError("color must be either callable or string")


    return "(" + ", ".join(items) + ")"