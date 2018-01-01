# parse.py 
# PowerGrid - Group 6
# CMPT 318 D2 Cyber Security
# Summer 2017

from power_sample import PowerSample
import datetime
import csv

# Get list from valid power sample csv file
def csv_to_power_samples(dir_str):
    power_samples = []
    # Get csv reader object from valid csv file
    with open(dir_str, newline='') as csv_file:
        # Get reader object and header
        csv_reader = csv.DictReader(csv_file, strict=True)
        
        # Check header validity
        if (csv_reader.fieldnames != 
                ['Date', 'Time', 'Global_active_power',
                'Global_reactive_power', 'Voltage', 'Global_intensity', 
                'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3'] ):
            # Close and exit
            return None
            
        # File is good, continue read
        for row in csv_reader:
            # Strip NA values
            for key in row.keys():
                if row[key] == 'NA':
                    row[key] = None
            
            # Convert date and time to proper types
            row['Date'] = datetime.datetime.strptime(row['Date'], "%d/%m/%Y").date()
            row['Time'] = datetime.datetime.strptime(row['Time'], "%H:%M:%S").time()
            
            # Append list with new sample
            power_samples.append(
                    PowerSample(
                        date=row['Date'],
                        time=row['Time'],
                        global_active_power=row['Global_active_power'],
                        global_reactive_power=row['Global_reactive_power'],
                        voltage=row['Voltage'],
                        global_intensity=row['Global_intensity'],
                        sub_metering_1=row['Sub_metering_1'],
                        sub_metering_2=row['Sub_metering_2'],
                        sub_metering_3=row['Sub_metering_3']
                        )
                    )
        # Close file
    return power_samples
    
# Test driver
def main(argv):
    power_samples = csv_to_power_samples(argv[1])
    print("The first ", argv[2], " power samples are: ")
    for i in range(0, int(argv[2])):
        print("Power Sample ", i, ":")
        print(power_samples[i])

if __name__ == '__main__':
    import sys
    main(sys.argv)
        
