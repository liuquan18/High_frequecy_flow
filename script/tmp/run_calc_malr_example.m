% filepath: /work/mh0033/m300883/High_frequecy_flow/script/tmp/run_calc_malr_example.m
p_example   = [100000, 90000, 80000, 70000, 60000];
temp_example = [290, 285, 280, 275, 270];

result = calc_malr(p_example, temp_example);
disp(result);