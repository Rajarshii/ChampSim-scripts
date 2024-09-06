import os
import re
import csv
from openpyxl import Workbook
import sys
import argparse

def parse_files(directory):
    data = {}
    for filename in os.listdir(directory):
        if filename.endswith(".out"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                content = file.readlines()
                cpu_ipc = {}
                ROI = False
                for line in content:
                    if "Region of Interest Statistics" in line:
                        ROI = True
                        #print("ROI Found")
                    if ROI and "cumulative IPC:" in line:
                        #print("cpu found")
                        match = re.search(r"CPU (\d+) cumulative IPC: (\d+\.\d+)",line)
                        if match:
                            #print("matched")
                            cpu_number = int(match.group(1))
                            ipc_value = float(match.group(2))
                            cpu_ipc[cpu_number] = float(ipc_value)
                            #print(f"cpu_number ",cpu_number)
                data[filename] = cpu_ipc
    #print(data)
    return data

def write_to_excel(data, output_filename):
    wb = Workbook()
    ws = wb.active

    # Write headers
    ws.append(['Filename'] + list(data.keys()))

    # Write data
    for cpu_num in range(max(len(cpu_data) for cpu_data in data.values())):
        cpu_row = [f'CPU {cpu_num} IPC']
        for filename, cpu_data in data.items():
            cpu_row.append(cpu_data.get(cpu_num, float('NaN')))
        ws.append(cpu_row)

    wb.save(output_filename)

def write_to_csv(data, output_filename):
    with open (output_filename,'w',newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the first row
        writer.writerow(["Benchmark"]+[f"cpu_{cpu_num}" for cpu_num in range(max(len(cpu_data) for cpu_data in data.values()))])

        # Write IPC Data per CPU Core
        for filename, cpu_data in data.items():
            row = [filename]
            if not cpu_data:
                writer.writerow(row+[float('NaN')]*len(data.keys()))
                continue

            # Assumption: the CPU indices are whole numbers - starting at 0
            max_num_cpu = max(cpu_data.keys())
            for cpu_num in range(max_num_cpu + 1):
                row.append(cpu_data.get(cpu_num, float('NaN')))
            writer.writerow(row)

def main():
    base_directory = input("Enter the base directory: ")
    isdir = os.path.isdir(base_directory)
    if not isdir:
        print("Invalid base directory provided")
        sys.exit(1)


    parser = argparse.ArgumentParser(description="Output File Names", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--csv",default="result_csv.csv",help="CSV File name")
    parser.add_argument("--xlsx",default="result_xl.xlsx",help="XLSX File name")

    args = vars(parser.parse_args())

    csv_name = args["csv"]
    xl_name = args["xlsx"]

    output_xlsx = os.path.join(base_directory,xl_name)
    output_csv = os.path.join(base_directory,csv_name)

    parsed_data = parse_files(base_directory)
    write_to_excel(parsed_data, output_xlsx)
    write_to_csv(parsed_data, output_csv)
    
    print(f"Excel file '{output_xlsx}' has been created with the parsed data.")
    print(f"CSV file '{output_csv}' has been created with the parsed data.")

if __name__ == "__main__":
    main()
