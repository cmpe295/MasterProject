from Gen import Gen

#2GB data, 20GB address range
myGen = Gen({
        'range': (1,2*1024*1024*1024//512),
        'count': 2*1024*1024*1024//4096,
        'write_percent': 1.0,
        'write_ran_percent': 1.0,
        'read_ran_percent': 1.0
    })
myGen.gen()


