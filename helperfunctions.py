#helperfunctions.py

'''
// Definition of variables in the dirpipulses ant file
antdef n 30 // Number of columns per line
// Event wide information
antdef run 1 // Run number
antdef evt 2 // Event number within
antdef tInRun 3 // Time since start of run in seconds
antdef tBetweenEvents 4 // Time since previous event in seconds
antdef nPulses 5 // Number of pulses in event summed over both channels
antdef nCh1Pulses 6 // Number of pulses in channel 1
antdef nCh2Pulses 7 // Number of pulses in channel 2
antdef RMS1 8 // RMS for channel 1
antdef RMS2 9 // RMS for channel 2
antdef Ped1 10 // Pedestal for channel 1 (subtracted before pulse finding)
antdef Ped2 11 // Pedestal for channel 2 (subtracted before pulse finding)
// The following are the sum of all pulses in different time windows.
// Region a is well before the trigger, b is before the trigger window
// Region c is after the trigger, and d is well after the trigger.
// The specific time windows will be adjusted based on run type,
// but the intent for LANL is a=preRF, b=RF, c=beam, d=post-beam
// These are not yet implimented and for now just 0
antdef Area1a 12 // Total CH1 area in waveform for time region a
antdef Area1b 13 // Total CH1 area in waveform for time region b
antdef Area1c 14 // Total CH1 area in waveform for time region c
antdef Area1d 15 // Total CH1 area in waveform for time region d
antdef Area2a 16 // Total CH2 area in waveform for time region a
antdef Area2b 17 // Total CH2 area in waveform for time region b
antdef Area2c 18 // Total CH2 area in waveform for time region c
antdef Area2d 19 // Total CH2 area in waveform for time region d
// Pulse specific information
antdef chan 20 // Channel number for pulse (1 or 2)
antdef ipulse 21 // number of pulse within waveform for this particular channel
antdef t 22 // Time of pulse (in address units)
antdef A 23 // Area of pulse (in ADCxAddress units)
antdef V 24 // Height of pulse (in ADC counts)
antdef width 25 // Width of pulse (in Address units)
antdef E 26 // Calibrated energy of pulse (in keV)
antdef dt 27 // Time to nearest other pulse in the channel (65536=none)
antdef dtOther 28 // Time to nearest pulse in other channel (65536=none)
antdef coinc 29 // Flag=1 if coincident |dtOther|<4, 0 if not
antdef qual 30 // Pulse quality flag, 0=good
// The quality flag is based on compatibility of V vs A and width vs A.
// The quality flag is not yet implimented and for now just 0.
'''
def is_int(value):
    if value is None:
        return False
    try:
        int(value)
        return True
    except:
        return False

def is_float(value):
    if value is None:
        return False
    try:
        float(value)
        return True
    except:
        return False

def openfile(name):
    f = open(name) 
    text = f.read() #read a string that seperate by " " & "\n"
    f.close() #close file
    line = text.split("\n") #split each line
    
    arr = []
    for x in line:
        arr.append(x.split(" ")) #split by each space

    for i in range(len(arr)-1,0,-1): #remove unwanted line, e.g.['']
        if arr[i] == ['']:
            arr.pop(i) #usually this occur at the very end
        
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if is_int(arr[i][j]):
                arr[i][j] = int(arr[i][j]) #convert to int
            elif is_float(arr[i][j]):
                arr[i][j] = float(arr[i][j]) #convert to float
            else:
                raise Exception("Not an int or float at arr[{i}][{j}]".format(i=i, j=j))
    return arr

#convert to pandas dataframe
import pandas as pd
import numpy as np

def to_df(run):
    df_col = ["run", "evt", "tInRun", "tBetweenEvents", "nPulses", "nCh1Pulses", "nCh2Pulses", "RMS1", "RMS2", "Ped1", "Ped2",
         "Area1a", "Area1b", "Area1c", "Area1d", "Area2a", "Area2b", "Area2c", "Area2d", "chan", "ipulse", "t",
         "A", "V", "width", "E", "dt", "dtOther", "coinc", "qual"]
    return pd.DataFrame(run, columns = df_col)
#show dataframe (df is the name)
#display(df)

#change channel number
def changeCh(df, ch_ori, ch_new):
    df.loc[df['chan'] == ch_ori, ["chan"]] = ch_new

#combine df
df = pd.concat([df_1, df_2])

#sort
df = df.sort_values(by = ["tInRun", "chan"])

#reset index if they are off order after concat
df = df.reset_index(drop=True)

#select by row and coloum
##return a dataframe
df.loc[0:4, ["tInRun"]]
##return a series
df.loc[0:4, "tInRun"]

#get number of row
df.shape[0]

#get value at specific row and col
df.at[6, "tInRun"] #[row ind, column name]

#check 4 Ch Coinc
##change coinc to 1 if hit all 4 channel, and to 0 if not
##given that by sorting run time, 4 hit of same event will be in consecutive order
##with time difference smaller than (?)
count = 0
df_1.loc[:,["coinc"]] = 0
ind = 0
err = 0.05
while ind < df_1.shape[0]-3:
    t = df_1.at[ind, "tInRun"]
    t_dif = [abs(t-df_1.at[ind+1, "tInRun"]), abs(t-df_1.at[ind+2, "tInRun"]), abs(t-df_1.at[ind+3, "tInRun"])]
    Ch_set = {df_1.at[ind, "chan"], df_1.at[ind+1, "chan"], df_1.at[ind+2, "chan"], df_1.at[ind+3, "chan"]}
    if Ch_set == {1,2,3,4} and max(t_dif) <= err:
        df_1.loc[ind:ind+3,["coinc"]] = 1
        ind += 4
    else:
        ind += 1
        count +=1
print("There are {} 4Ch coinc hit, {} hit only trigger 3 or less channel".format(df_1.shape[0]-count, count))

#Sample Plotting Histogram
plt.hist(Ch4_h, bins = 220)
plt.xlim((-10,240))
plt.ylim((0,500))
plt.xlabel("Height of pulse (in ADC counts)")
plt.ylabel("frequency")
plt.savefig("Channel 4 Pulse Height(y_cutoff).png", dpi=300)

#Sample Plotting Scatter Plot
plt.scatter(Ch1.loc[:,["V"]], Ch4.loc[:,["V"]])
plt.xlabel("Ch1 Pulse Height")
plt.ylabel("Ch4 Pulse Height")
plt.savefig("Pulse Height Ch1 vs Ch4.png", dpi=300)
