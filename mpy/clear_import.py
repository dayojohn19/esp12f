def clearImport():
    import sys
    ignore_modules = {'sys', '__main__', 'builtins'}
    for module in list(sys.modules.keys()):
        if module not in ignore_modules:
            del sys.modules[module]  # Remove the module from the cache
    for module in list(globals().keys()):
        if module not in ignore_modules:
            del globals()[module]

if __name__ == "__main__":
    clearImport()