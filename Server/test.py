import numpy as np

x = np.linspace(1,1,201)
y = np.random.random(201)

header = "FAN DATA\n"
header += "PWM x15,  TACHO x15"
with open('FAN_data.dat', 'wb') as f: #w-writing mode, b- binary mode
    np.savetxt(f, [], header=header)
    for i in range(201):
        data = np.column_stack((x[i],y[i]))
        np.savetxt(f, data)
        f.flush()
#sleep(0.1)        
