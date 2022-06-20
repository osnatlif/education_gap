# entry point for the dynamic model estimation
from time import perf_counter
import cohorts
import getopt
import sys


def usage(proc):
    print("usage: " + proc +
          "\n\t-s --static: do not calculate emax" +
          "\n\t-m --moments: display moments" +
          "\n\t-c --cohort: cohort. e.g. 1970white" +
          "\n\t-v --verbose")
    exit(0)

def main():
    options = "hsvmc"
    long_options = ["help", "static", "verbose", "moments", "cohort"]
    display_moments = False
    verbose = False
    static_model = False
    try:
        args, values = getopt.getopt(sys.argv[1:], options, long_options)
        for arg, val in args:
            if arg in ("-h", "--Help"):
                usage(sys.argv[0])
            elif arg in ("-m", "--moments"):
                display_moments = True
            elif arg in ("-v", "--verbose"):
                verbose = True
            elif arg in ("-s", "--static"):
                static_model = True
            elif arg in ("-c", "--cohort"):
                if len(values) == 0:
                    print("'cohort' is a mandatory parameter")
                    usage(sys.argv[0])
                cohorts.cohort = values[0]
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
        usage(sys.argv[0])

    if cohorts.cohort is None:
        print("'cohort' is a mandatory parameter")
        usage(sys.argv[0])

    import calculate_emax as ce
    import forward_simulation as fs

    w_emax = ce.create_married_emax()
    h_emax = ce.create_married_emax()
    w_s_emax = ce.create_single_w_emax()
    h_s_emax = ce.create_single_h_emax()
    if not static_model:
        tic = perf_counter()
        iter_count = ce.calculate_emax(w_emax, h_emax, w_s_emax, h_s_emax, verbose)
        toc = perf_counter()
        print("calculate emax with %d iterations took: %.4f (sec)" % (iter_count, (toc - tic)))
    else:
        print("static model, emax not calculated")

    value = fs.forward_simulation(w_emax, h_emax, w_s_emax, h_s_emax, verbose, display_moments)
    print(value)


if __name__ == "__main__":
    main()
