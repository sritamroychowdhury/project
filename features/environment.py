import time
import csv

# Define a global list to store test results
test_results = []


def before_scenario(context, scenario):
    # Capture scenario start time
    scenario.start_time = time.time()
    context.failed_scenario_error_message = None



def after_scenario(context, scenario):
    # Get scenario result details


    result = {
        'Scenario_name': scenario.name,
        'Status': scenario.status.name,
        'Note': None
    }

    if scenario.status == "failed":
        for step in scenario.steps:
            if step.status.name == "failed":
                if 'Assertion Failed' in step.error_message:
                    result['Note'] = step.error_message
                    break
    # Append result to global list
    test_results.append(result)


def write_results_to_csv(results, csv_file):
    # Define CSV column headers
    fieldnames = ['Scenario_name', 'Status', 'Note']

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write headers
        writer.writeheader()

        # Write results row by row
        for result in results:
            writer.writerow(result)


def after_all(context):
    # Define the path to the CSV file
    csv_file_path = 'test_results.csv'

    # Write results to CSV after all scenarios are executed
    write_results_to_csv(test_results, csv_file_path)
