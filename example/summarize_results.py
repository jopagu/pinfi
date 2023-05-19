import os
import sys
import filecmp
import math

#Note: This program determines if a fault injection run was benign or an SDC by comparing the output
#to a no fault "golden" run. If your program has nondeterministic output, this will not work
#This gathers results from all extant output files, so if there are some remaining from a 
#previous fault injection campaign it will mess things up. You can get around this by passing
#a number of runs to summarize as an argument
def summarize(run_count = -1):
    curr_dir = "./"
    baseline = curr_dir + "baseline"
    error = curr_dir + "error_output"
    prog = curr_dir + "prog_output"
    std = curr_dir + "std_output"

    output_file = curr_dir + "results_summary.txt"

    file_golden = baseline + "/golden_std_output"

    if (run_count == -1):
        _, _, files = os.walk(std).__next__()
        run_count = len(files)


    benign = 0
    program_crash = 0
    system_crash = 0
    hang = 0
    sdc = 0
    for f in range(run_count):
        
        file_out = std + f"/std_outputfile-{f}"

        #Get the error output if it exists
        try:
            file_err = open(error + f"/errorfile-{f}")
            err_msg = file_err.read()
            err_code = err_msg.split()[-1]
        except FileNotFoundError:
            err_msg = ""
            err_code = "0"

        #Determine result type
        if ("Program hang" in err_msg):
            hang += 1
        elif (int(err_code) < 0):
            system_crash += 1
        elif (int(err_code) > 0):
            program_crash += 1
        elif (filecmp.cmp(file_golden, file_out)):
            benign += 1
        else:
            sdc += 1

        file_err.close()

    #These are tracked seperately in case you care about the difference, but by default they're just combined
    crash = program_crash + system_crash

    run_count_s = f"{run_count} fault injections were performed."
    crash_s = f"{f'Crash count: {crash:,}':<20} | {percent(crash, run_count)}%"
    hang_s = f"{f'Hang count: {hang:,}':<20} | {percent(hang, run_count)}%"
    sdc_s = f"{f'SDC count: {sdc:,}':<20} | {percent(sdc, run_count)}%"
    benign_s = f"{f'Benign count: {benign:,}':<20} | {percent(benign, run_count)}%"   

    print(run_count_s)
    print(crash_s)
    print(hang_s)
    print(sdc_s)
    print(benign_s)

    out = open(output_file, "w")
    out.write(run_count_s + "\n")
    out.write(crash_s + "\n")
    out.write(hang_s + "\n")
    out.write(sdc_s + "\n")
    out.write(benign_s + "\n")

#return x/y as percent w/ 2 decimal places
def percent(x, y):
    x /= y
    x *= 10000
    x = math.trunc(x)
    x /= 100
    return x


if __name__ == "__main__":
    if(len(sys.argv) >= 2):
        summarize(int(sys.argv[1]))
    else:
        summarize()

