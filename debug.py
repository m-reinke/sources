global_debug = False

def debug_msg(s):
    global global_debug
    if global_debug:
        print(s)
        print('')
