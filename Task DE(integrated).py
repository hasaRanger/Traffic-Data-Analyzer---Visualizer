#Author:K.K.N. Hasaranga
#Date:2024/11/18 - ...
#Student ID:20240675/w21200762

import tkinter as tk

# Task A: Input Validation

def validate_date_input():
    """
    Prompts the user to enter day, month, and year separately.
    Validates each input immediately and does not proceed until the current input is valid.
    """
    days_per_month = { #month:day as key:value pairs
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,  
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }

    #Prompt for day
    while True:
        try:
            day_input = input("\nEnter the date in DD format: ")
            if not day_input.isdigit():
                raise ValueError("Integer required.")
            day = int(day_input)
            if day<1 or day>31:
                raise ValueError("Out of range. Day should be between 1 and 31.")
            break
        except ValueError as e:
            print(e)

    #Prompt for month
    while True:
        try:
            month_input = input("\nEnter the month in MM format: ")
            if not month_input.isdigit():
                raise ValueError("Integer required.")
            month = int(month_input)
            if month<1 or month>12:
                raise ValueError("Out of range. month should be between 1 and 12.")
            if day > days_per_month[month] and month != 2: #leaving Februray out of the logic avoiding prejudgements of range of days since the program has not prompted for 'year' yet
                raise ValueError(f"Day {day} is invalid for this month {month}.")
            break
        except ValueError as e:
            print(e)

    #Prompt for year
    while True:
        try:
            year_input = input("\nEnter the year in YYYY format: ")
            if not year_input.isdigit():
                raise ValueError("Integer required.")
            year = int(year_input)
            if year<2000 or year>2024:
                raise ValueError("Out of range. Year should be between 2000 and 2024.")

            #Check for the leap year and update days in February
            if (year%4 == 0 and year%100 != 0) or (year%400 == 0):  
                days_per_month[2] = 29
            if month == 2 and day > days_per_month[month]:
                raise ValueError(f"Day {day} is not valid for February in the year {year}. Max days: {days_per_month[2]}.")
            break
        except ValueError as e:
            print(e)

    date_input = f"{day:02d}{month:02d}{year}"

    
    print(f"\nValid date entered {day:02d}/{month:02d}/{year}")
    return date_input

def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input.
    Returns True if "Y" is entered, False if "N" is entered.
    """
    while True:
        try:
            continue_input = input("\nDo you wish to load another dataset ('Y' for Yes or 'N' for No): ").strip().upper()
            if continue_input == "Y":
                return True
            elif continue_input == "N":
                return False
            else:
                raise ValueError("Invalid input. Please enter 'Y' for Yes or 'N' for No.")
        except ValueError as e:
            print(e)
        
class HistogramApp:
    def __init__(self, traffic_data, date):
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=1300, height=650, bg='white')
        self.root.resizable(True, True)
        self.canvas.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.close_window) #handling the window close event

    def setup_window(self):
        self.canvas.create_line(70, 550, 1261, 550, width=2)
        self.canvas.create_text(650, 590, text="Hours 00:00 to 23:00", font=("Arial", 12, "bold"))

    def draw_histogram(self):
        bar_width = 20
        starting_x = 70

        pair_spacing = 10
        max_height = 400

        #To distinguish the maximum value out of a particular dataset as well as apaart from different datasets
        max_frequency = max(max(self.traffic_data['elm'].values()), max(self.traffic_data['hanley'].values()))
        scale = max_height / max_frequency if max_frequency > 0 else 1

#Mathematical adaptations down below were done with the aid of ChatGPT
        for hour in range(24):
            #Bar representing vehicle frequency in Elm Avenue
            elm_freq = self.traffic_data['elm'].get(hour, 0)
            elm_x1 = starting_x + (hour * 2 * bar_width)
            elm_x2 = elm_x1 + bar_width
            elm_y1 = 550 - (elm_freq * scale)   
            self.canvas.create_rectangle(elm_x1, elm_y1, elm_x2, 549, fill="#00539C", outline="#003366")
            self.canvas.create_text((elm_x1 + elm_x2)/ 2, elm_y1 - 10, text=str(elm_freq), font=("Arial", 10), fill="dark blue")

            #Bar representing vehicle frequency in Hanley Highway
            hanley_freq = self.traffic_data['hanley'].get(hour, 0)
            hanley_x1 = starting_x + (hour * 2 * bar_width) + bar_width 
            hanley_x2 = hanley_x1 + bar_width
            hanley_y1 = 550 - (hanley_freq * scale)
            self.canvas.create_rectangle(hanley_x1, hanley_y1, hanley_x2, 549, fill="#A0A4A8", outline="#6C757D")
            self.canvas.create_text((hanley_x1 + hanley_x2)/ 2, hanley_y1 - 10, text=str(hanley_freq), font=("Arial", 10), fill="black")

            #Lable of hour under each grouped bar
            hour_label_x = (elm_x1 + hanley_x2) / 2 #Positioning the lable under the midpoint
            self.canvas.create_text(hour_label_x, 560, text=str(hour).zfill(2), font=("Arial", 10, "bold"))

            starting_x += pair_spacing #leaving out a space between two particular groups of bars
            

    def add_legend(self):
        self.canvas.create_text(70, 70, text=f"Histogram of Vehicle Frequency per Hour  ({self.date[:2]}/{self.date[2:4]}/{self.date[4:]})", anchor="w", font=("Helvetica", 14, "bold"))
        self.canvas.create_rectangle(70, 100, 90, 120, fill="#00539C", outline="#003366")
        self.canvas.create_text(95, 110, text="Elm Avenue/Rabbit Road", anchor="w", font=("Arial", 12))
        self.canvas.create_rectangle(70, 140, 90, 160, fill="#A0A4A8", outline="#6C757D")
        self.canvas.create_text(95, 150, text="Hanley Highway/Westway", anchor="w", font=("Arial", 12))

    def run(self):
        self.root.title(f"Vehicle Frequency Histogram  ({self.date[:2]}/{self.date[2:4]}/{self.date[4:]})")
        self.root.resizable(True, True)
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()

    def close_window(self): #Clean exit of tkinter mainloop
        self.root.quit()
        self.root.destroy()

class MultiCSVProcessor:
    def __init__(self):
        self.traffic_data = None

    def load_csv_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()

                #intiating a dictionary for the grouped data 
                data = {"elm": {hour: 0 for hour in range(24)}, "hanley": {hour: 0 for hour in range(24)}}

                for line in lines[1:]:  # Skip the header
                    columns = line.strip().split(',')  # Manually split columns by comma
                    location = columns[0].strip().lower()
                    time = columns[2].strip()

                    # Validate and extract the hour
                    try:
                        # Extract hour assuming time is in HH:MM format
                        hour_str = time.split(":")[0]
                        hour = int(hour_str)
                        if hour < 0 or hour > 23:
                            raise ValueError
                    except ValueError:
                        print(f"Skipping invalid time entry: {time}")
                        continue

                    if "elm avenue" in location:
                        data["elm"][hour] += 1
                    elif "hanley highway" in location:
                        data["hanley"][hour] += 1

                self.traffic_data = data
                
        except Exception as e:
            print(f"Error loading file: {e}")
            self.traffic_data = None

    def clear_previous_data(self):
        self.traffic_data = None

    def handle_user_interaction(self, selected_date):
        print(f"Dataset for {selected_date[:2]}/{selected_date[2:4]}/{selected_date[4:]} loaded successfully. Displaying Histogram.")

    def process_files(self, file_path, selected_date):
        file_map = {
            "15062024": "traffic_data15062024.csv",
            "16062024": "traffic_data16062024.csv",
            "21062024": "traffic_data21062024.csv"
        }
             
        if selected_date not in file_map:
            print("No data available for this date")
            return
            
        file_path = file_map[selected_date]
        self.clear_previous_data()
        self.load_csv_file(file_path)

        if self.traffic_data:
            self.handle_user_interaction(selected_date)
            app = HistogramApp(self.traffic_data, selected_date)
            app.run()
                

def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts metrics.
    """
    try:
        with open(file_path, "r") as dataSet:
            data = dataSet.readlines()
            dataSet.close()

        # Process the data
        for i in range(len(data)):
            data[i] = data[i].strip().split(",")

        rain_hours = []

        for record in data[1:]: 
            weather_condition = record[5].strip().lower() 
            time = record[2] 
            
            if 'rain' in weather_condition:  # If "rain" is mentioned in the weather column
                hour_str = time[:2]  # Extract hour from time (assuming time is in HH:MM format)
                if hour_str not in rain_hours:  # If this hour isn't already in the list, add it
                    rain_hours.append(hour_str)        

        Tot_hanley_vehicles = [i for i in data[1:] if "hanley highway/westway" in i[0].strip().lower()]
        
        highest_count = 0
        busiest_hour = 0   
        
        for hour in range(0,24):  # Hours from 0 to 23
            hour_str = f"{hour:02d}"  # Format hour as "00", "01", ..., "23"
            count = 0

            for record in Tot_hanley_vehicles:
                time = record[2]
                if time.startswith(hour_str):  
                    count += 1
                    
            if count > highest_count:
                highest_count = count
                busiest_hour_start = hour_str

        busiest_hour_end = f"{int(busiest_hour_start) + 1:02d}" if busiest_hour_start != "23" else "00:00"

        peak_hour_range = f"{busiest_hour_start}:00 - {busiest_hour_end}:00"
        
        # Extract metrics
        Tot_vehicles = [i[8] for i in data[1:]] #'[1:]' to skip the header row
        Tot_trucks = [i[8] for i in data[1:] if i[8].strip().lower() == "truck"]
        Elm_buses_north = [i[8] for i in data[1:] if i[8].strip().lower() == "buss" and "elm avenue" in i[0].strip().lower() and i[4].strip().lower() == "n"]
        Vehicles_no_turn = [i[8] for i in data[1:] if i[3].strip().lower() == i[4].strip().lower()]
        Tot_twoWheel_vehicles = [i[8] for i in data[1:] if i[8].strip().lower() in ["bicycle", "scooter", "motorcycle"]]
        Tot_elec_vehicles = [i[8] for i in data[1:] if i[9].strip().lower() == "true"]
        Tot_elm_vehicles = [i[8] for i in data[1:] if "elm avenue" in i[0].strip().lower()]
        Scooters_elm = [i for i in Tot_elm_vehicles if i.strip().lower() == "scooter"]
        Tot_bikes = [i for i in Tot_twoWheel_vehicles if i.strip().lower() == "bicycle"]

        elm_speedLimit = 30
        hanley_speedLimit = 20
        Vehicles_over_speedLimit = [i[8] for i in data[1:] if ("elm avenue" in i[0].strip().lower() and int(i[7]) > elm_speedLimit) or ("hanley highway" in i[0].strip().lower() and int(i[7]) > hanley_speedLimit)]

        total_bikes = len(Tot_bikes)
        
        # Return results as a dictionary
        return {
            "Total Vehicles": len(Tot_vehicles),
            "Total Trucks": len(Tot_trucks),
            "Total Electric Vehicles": len(Tot_elec_vehicles),
            "Total Two-Wheeled Vehicles": len(Tot_twoWheel_vehicles),
            "Total Buses leaving elm heading north": len(Elm_buses_north),
            "Vehicles no turn": len(Vehicles_no_turn),
            "Total Trucks percentage": int(round(len(Tot_trucks)/len(Tot_vehicles)*100)),
            "Average Bikes per hour": round((total_bikes)/24),
            "Vehicles over speed limit": len(Vehicles_over_speedLimit),
            "Total vehicles in Elm": len(Tot_elm_vehicles),
            "Total vehicles in Hanley": len(Tot_hanley_vehicles),
            "Scooters through Elm percentage": int(round(len(Scooters_elm)/len(Tot_elm_vehicles)*100)),
            "Max vehicles in peak hour": highest_count,
            "Peak hour": peak_hour_range,
            "Rain hours": len(rain_hours)
        }
    except Exception as e:
        print(f"An error occurred: {e}.")
        return None


def display_outcomes(outcomes):
    """
    Displays the calculated outcomes in a formatted way.
    """
    if outcomes:
        print(f"The total number of vehicles recorded for this date is {outcomes['Total Vehicles']}")
        print(f"The total number of trucks recorded for this date is {outcomes['Total Trucks']}")
        print(f"The total number of electric vehicles recorded for this date is {outcomes['Total Electric Vehicles']} ")
        print(f"The total number of two-wheeled vehicles recorded for this date is {outcomes['Total Two-Wheeled Vehicles']}")
        print(f"The total number of buses leaving Elm Avenue/Rabbit Road heading North is {outcomes['Total Buses leaving elm heading north']}")
        print(f"The total number of Vehicles through both junctions without turning left or right is {outcomes['Vehicles no turn']}")
        print(f"The percentage of total vehicles recorded that are trucks for this date is {outcomes['Total Trucks percentage']}%")
        print(f"The average number of bikes per hour for this date is {outcomes['Average Bikes per hour']}")
        print(f"The total number of vehicles recorded as over the speed limit for this date is {outcomes['Vehicles over speed limit']}")
        print(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['Total vehicles in Elm']}")
        print(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['Total vehicles in Hanley']}")
        print(f"{outcomes['Scooters through Elm percentage']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters")
        print(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['Max vehicles in peak hour']}")
        print(f"The most vehicles through Hanley Highway/Westway were recorded between {outcomes['Peak hour']}")
        print(f"The number of hours of rain for this date is {outcomes['Rain hours']}")
        print("\n*************************************************************")
    else:
        print("No data to display.")
        

# Task C: Save Results to Text File
def save_results_to_file(outcomes, selected_date, mode = "a"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    file_name = "results.txt"

    try:
        with open(file_name, mode) as file:
            file.write(f"---Processed Outcomes for {selected_date[:2]}/{selected_date[2:4]}/{selected_date[4:]}---\n")
            file.write(f"The total number of vehicles recorded for this date is {outcomes['Total Vehicles']}\n")
            file.write(f"The total number of trucks recorded for this date is {outcomes['Total Trucks']}\n")  
            file.write(f"The total number of electric vehicles recorded for this date is {outcomes['Total Electric Vehicles']} \n")
            file.write(f"The total number of two-wheeled vehicles recorded for this date is {outcomes['Total Two-Wheeled Vehicles']}\n")
            file.write(f"The total number of buses leaving Elm Avenue/Rabbit Road heading North is {outcomes['Total Buses leaving elm heading north']}\n")
            file.write(f"The total number of Vehicles through both junctions without turning left or right is {outcomes['Vehicles no turn']}\n")
            file.write(f"The percentage of total vehicles recorded that are trucks for this date is {outcomes['Total Trucks percentage']}%\n")
            file.write(f"The average number of bikes per hour for this date is {outcomes['Average Bikes per hour']}\n")
            file.write(f"The total number of vehicles recorded as over the speed limit for this date is {outcomes['Vehicles over speed limit']}\n")
            file.write(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['Total vehicles in Elm']}\n")
            file.write(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['Total vehicles in Hanley']}\n")
            file.write(f"{outcomes['Scooters through Elm percentage']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters\n")
            file.write(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['Max vehicles in peak hour']}\n")
            file.write(f"The most vehicles through Hanley Highway/Westway were recorded between {outcomes['Peak hour']}\n")
            file.write(f"The number of hours of rain for this date is {outcomes['Rain hours']}\n\n")
            file.write("*************************************************************\n\n")                          
        print(f"\nOutcomes saved to the {file_name} successfully.")
    except Exception as e:
        print(f"Unexpected error occured when saving {file_name}: {e}")
        

# Main Program
def main():
    file_name = "results.txt"

    #Erases all the content from previous operations
    with open(file_name, "w")as file:
        file.close()
        pass
    
    processor = MultiCSVProcessor()
    
    while True:
        selected_date = validate_date_input()

        # Map selected_date to file_path
        try:
            if selected_date.strip() == "15062024":
                file_path = "traffic_data15062024.csv"
            elif selected_date.strip() == "16062024":
                file_path = "traffic_data16062024.csv"
            elif selected_date.strip() == "21062024":
                file_path = "traffic_data21062024.csv"
            else:
                print("No data available for this date.")
                continue

            # Process and display outcomes
            outcomes = process_csv_data(file_path)

            if outcomes:
                print("\ndata file selected is", file_path)
                display_outcomes(outcomes)

            #Save to results.txt
            save_results_to_file(outcomes, selected_date)

            #Process the dataset for the histogram
            processor.process_files(file_path, selected_date)

        except FileNotFoundError:
            print("File not found for the entered date")

        if not validate_continue_input():
            print("End of run.")
            break
        
if __name__ == "__main__": #Calls out the main function
    main()

    
# if you have been contracted to do this assignment please do not remove this line
