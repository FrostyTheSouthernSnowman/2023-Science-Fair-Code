with open("output.csv", 'r') as output:
    output.readline()
    write_buffer = ""
    for voltage in [7.4, 9, 110, 220]:
        print(f"Now doing {voltage}V")
        f = open(str(voltage) + "V_output.csv", "w+")
        f.write(
                "Current (Amps),Coil Diameter (Millimeters),Wire Diameter,Distance (Millimeters),Turns,Voltage,Force (Newtons)\n"
        )
        f.write(write_buffer)

        i = 0
        while True:
            if i % 10_000_000 == 1:
                print(f"10 Million lines done, now at {i} lines total")

            line = output.readline()
            data = line.split(",")
            if data[5] == str(voltage):
                f.write(line)
            
            else:
                write_buffer = line
                break

            i += 1
        
        f.close()