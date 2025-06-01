import csv
import random
from datetime import datetime
from collections import defaultdict

# Disclosure: This code was wholly written by Gemini AI.

# Day mapping for consistency
DAY_MAP = {
    'M': 'M', # Monday
    'T': 'T', # Tuesday
    'W': 'W', # Wednesday
    'H': 'H', # Thursday (as specified by user)
    'F': 'F', # Friday
    'S': 'S', # Saturday
    'U': 'U'  # Sunday (as specified by user)
}

def parse_time(time_str):
    """Parses a time string (HHMM) into a datetime.time object."""
    return datetime.strptime(time_str, "%H%M").time()

def is_time_overlap(start1, end1, start2, end2):
    """Checks if two time intervals overlap."""
    start1_minutes = start1.hour * 60 + start1.minute
    end1_minutes = end1.hour * 60 + end1.minute
    start2_minutes = start2.hour * 60 + start2.minute
    end2_minutes = end2.hour * 60 + end2.minute

    return max(start1_minutes, start2_minutes) < min(end1_minutes, end2_minutes)

def check_conflicts(chosen_classes):
    """
    Checks for conflicts (time overlap or same subject) among a list of chosen classes.
    Returns a list of conflicting class pairs.
    """
    conflicts = []
    num_chosen = len(chosen_classes)
    for i in range(num_chosen):
        for j in range(i + 1, num_chosen):
            class1 = chosen_classes[i]
            class2 = chosen_classes[j]

            # 1. Check for same subject conflict
            if class1['Subject Code'] == class2['Subject Code']:
                conflicts.append((class1, class2, "Same Subject"))
                continue

            # 2. Check for time overlap conflict
            days1 = set(class1['Days'])
            days2 = set(class2['Days'])

            common_days = days1.intersection(days2)

            if common_days:
                start_time1 = parse_time(class1['Start Time'])
                end_time1 = parse_time(class1['End Time'])
                start_time2 = parse_time(class2['Start Time'])
                end_time2 = parse_time(class2['End Time'])

                if is_time_overlap(start_time1, end_time1, start_time2, end_time2):
                    conflicts.append((class1, class2, "Time Overlap"))
    return conflicts

def resolve_conflicts(chosen_classes_raw):
    """
    Resolves conflicts based on rank: keeps the higher-ranked class, drops the lower-ranked.
    Assumes chosen_classes_raw is a list of dictionaries, each with 'Rank' and other class info.
    Returns the final non-conflicting list of classes.
    """
    final_roster = []
    sorted_chosen = sorted(chosen_classes_raw, key=lambda x: x['Rank'])

    acquired_subjects = set()
    acquired_schedules = [] # Stores (day_char, start_time_obj, end_time_obj) for each acquired class's specific days

    for current_class in sorted_chosen:
        can_add = True

        if current_class['Subject Code'] in acquired_subjects:
            can_add = False
            continue

        current_class_days = set(current_class['Days'])
        current_class_start = parse_time(current_class['Start Time'])
        current_class_end = parse_time(current_class['End Time'])

        for acquired_day, acquired_start, acquired_end in acquired_schedules:
            if acquired_day in current_class_days:
                if is_time_overlap(current_class_start, current_class_end, acquired_start, acquired_end):
                    can_add = False
                    break

        if can_add:
            final_roster.append(current_class)
            acquired_subjects.add(current_class['Subject Code'])
            for day_char in current_class_days:
                acquired_schedules.append((day_char, current_class_start, current_class_end))
    return final_roster

def run_simulation(classes_data, num_simulations=100000):
    """
    Runs Monte Carlo simulations to estimate the probability of getting the desired roster.
    """
    successful_simulations = 0

    # Pre-calculate individual probabilities (no longer printed)
    for class_info in classes_data:
        prob = class_info['Available Slots'] / class_info['Demand'] if class_info['Demand'] > 0 else 1.0
        class_info['Probability'] = min(prob, 1.0) # Cap probability at 1.0

    print(f"\nRunning {num_simulations} simulations...")

    for _ in range(num_simulations):
        chosen_in_run = []
        for class_info in classes_data:
            if random.random() < class_info['Probability']:
                chosen_in_run.append(class_info)

        final_roster_in_run = resolve_conflicts(chosen_in_run)

        desired_subjects = set(c['Subject Code'] for c in classes_data)
        acquired_subjects_in_run = set(c['Subject Code'] for c in final_roster_in_run)

        if desired_subjects.issubset(acquired_subjects_in_run) and \
           len(final_roster_in_run) == len(desired_subjects):
            successful_simulations += 1

    overall_probability = (successful_simulations / num_simulations) * 100
    return overall_probability

def provide_subject_recommendations(classes_data):
    """
    Provides recommendations for each unique subject based on the probability of getting at least one class for that subject.
    """
    print("\n--- Subject-wise Recommendations ---")

    subjects = defaultdict(list)
    for class_info in classes_data:
        subjects[class_info['Subject Code']].append(class_info)

    for subject_code, subject_classes in subjects.items():
        # Calculate probability of NOT getting any class for this subject
        prob_not_getting_any = 1.0
        for class_info in subject_classes:
            prob_not_getting_any *= (1.0 - class_info['Probability'])
        
        prob_getting_at_least_one = 1.0 - prob_not_getting_any

        print(f"\n  Subject: {subject_code}")
        print(f"    Probability of getting at least one class for '{subject_code}': {prob_getting_at_least_one:.2%}")

        if prob_getting_at_least_one >= 0.81: # 81%-100%
            if len(subject_classes) > 1:
                print(f"    Recommendation: HIGH PROBABILITY. You have a very good chance of getting a class for '{subject_code}'. Consider if you need multiple applications for this subject; you might be able to free up a slot for another subject by removing lower-ranked options for '{subject_code}'.")
            else:
                print(f"    Recommendation: HIGH PROBABILITY. You have a very good chance of getting this class. No action required for '{subject_code}'.")
        elif prob_getting_at_least_one >= 0.61: # 61%-80%
            print(f"    Recommendation: MEDIUM PROBABILITY. Your chances for '{subject_code}' are moderate. No action required, but if you have available slots, adding another alternative for this subject could slightly improve your odds.")
        else: # < 60%
            print(f"    Recommendation: LOW PROBABILITY. Your chances for '{subject_code}' are low. Strongly consider adding more alternative classes for '{subject_code}' to improve your odds, if you have available slots, or explore other subjects.")

def main():
    csv_file_path = '[csv file path directory here]' # Ensure this CSV is in the same directory as the script

    classes_data = []
    try:
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Basic validation for essential fields
                if not all(k in row and row[k] for k in ['Subject', 'Class Name', 'Available Slots', 'Demand', 'Rank', 'Days', 'Start Time', 'End Time']):
                    print(f"Warning: Skipping row due to missing essential data: {row}")
                    continue

                try:
                    # Rename 'Subject' to 'Subject Code' for consistency with internal logic
                    row['Subject Code'] = row.pop('Subject')
                    row['Available Slots'] = int(row['Available Slots'])
                    row['Demand'] = int(row['Demand'])
                    row['Rank'] = int(row['Rank'])

                    # Handle new day format
                    days_str_raw = row['Days'].strip().upper() # Convert to uppercase for robust matching
                    parsed_days = []
                    for char_day in days_str_raw:
                        if char_day in DAY_MAP:
                            parsed_days.append(DAY_MAP[char_day])
                        else:
                            print(f"Warning: Unexpected day character '{char_day}' in class '{row['Class Name']}'. Skipping this specific day entry for the class.")
                    row['Days'] = parsed_days # Store as a list of single characters

                    classes_data.append(row)
                except ValueError as e:
                    print(f"Error parsing numerical/time data in row: {row}. Skipping. Error: {e}")
                    continue
                except KeyError as e:
                    print(f"Error: Missing or misspelled column header: {e} in row: {row}. Please check CSV headers.")
                    continue
    except FileNotFoundError:
        print(f"Error: The CSV file '{csv_file_path}' was not found. Please make sure it's in the same directory as the script.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the CSV: {e}")
        return

    if not classes_data:
        print("No valid class data found in the CSV. Please check the file format and content.")
        return

    # Sort classes by rank initially, as this is important for consistent conflict resolution logic
    classes_data.sort(key=lambda x: x['Rank'])

    # Run the simulation
    overall_prob = run_simulation(classes_data)
    print(f"\n--- Overall Roster Probability ---")
    print(f"Based on {len(classes_data)} desired classes, your estimated probability of getting a non-conflicting final roster (where you obtain one class for each unique subject desired) is: {overall_prob:.2f}%")

    # Provide subject-wise recommendations
    provide_subject_recommendations(classes_data)

    print("\n--- Important Notes ---")
    print("1. The 'Overall Roster Probability' assumes that for each unique subject you desire, getting at least one class for that subject (the highest ranked non-conflicting one) counts as success.")
    print("2. The simulation accounts for time conflicts and 'same subject' conflicts, dropping lower-ranked classes as per UP rules.")
    print("3. This tool does NOT consider unit limits (e.g., 21 units max for undergrads) or PE class limits. You must ensure your desired classes adhere to these.")
    print("4. This tool does NOT optimize your schedule (e.g., minimize breaks). It focuses purely on probability of acquisition.")
    print("5. The accuracy of the probability depends on the 'Available Slots' and 'Demand' data being accurate for your specific enlistment period.")
    print("6. 'Demand' can change dynamically, so probabilities are a snapshot at the time of data collection.")
    print("7. Days are parsed as single concatenated letters: M=Monday, T=Tuesday, W=Wednesday, H=Thursday, F=Friday, S=Saturday, U=Sunday. Input is converted to uppercase for parsing.")
    print("8. Time (Start Time, End Time) is parsed in HHMM format (e.g., 0700 for 07:00, 1330 for 13:30).")


if __name__ == "__main__":
    main()