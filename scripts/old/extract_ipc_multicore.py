import os
import re
import csv
from openpyxl import Workbook

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
                        match = re.search(r"CPU (\d+) cumulative IPC: (\d+\.\d+)",line );
                        if match:
                            #print("matched")
                            cpu_number = int(match.group(1))
                            ipc_value = float(match.group(2))
                            cpu_ipc[cpu_number] = float(ipc_value)
                            #print(f"cpu_number ",cpu_number)
                data[filename] = cpu_ipc
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

        writer.writerow(["Filename"] + list(data.keys()))

        # Write data
        for cpu_num in range(max(len(cpu_data) for cpu_data in data.values())):
            cpu_row = [f'CPU {cpu_num} IPC']
            for filename, cpu_data in data.items():
                cpu_row.append(cpu_data.get(cpu_num, float('NaN')))
            writer.writerow(cpu_row)

def main():
    base_directory = input("Enter the base directory: ")
    isdir = os.path.isdir(base_directory)
    if not isdir:
        print("Invalid base directory provided")
        return

    #output_filename = base_directory.rstrip("/") + "_results.xlsx"
    output_filename = os.path.join(base_directory,"results.xlsx")
    output_csv = os.path.join(base_directory,"results.csv")

    parsed_data = parse_files(base_directory)
    write_to_excel(parsed_data, output_filename)
    write_to_csv(parsed_data, output_csv)
    print(f"Excel file '{output_filename}' has been created with the parsed data.")
    print(f"CSV file '{output_csv}' has been created with the parsed data.")

if __name__ == "__main__":
    main()
