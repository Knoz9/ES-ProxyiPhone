import subprocess
import time
import os
import kmbotfilemanager as filemanager
import kmbotnetwork as netmanager
import kmbotos as kmos
import kmbot as kmbot
global test
test = False
def testmode(message,feed):
    global test
    if test == False:
        netmanager.uplink(message, feed)
    else:
        print("Testmode on, not uplinking...")
        

def restart_apple_mobile_device_service():
    """Restart the Apple Mobile Device Service."""
    
    # Try to stop the service
    try:
        subprocess.run(["net", "stop", "Apple Mobile Device Service"], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop Apple Mobile Device Service. Error: {e.output}")
    

    # Try to start the service
    try:
        subprocess.run(["net", "start", "Apple Mobile Device Service"], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Apple Mobile Device Service. Error: {e.output}")




def mainscript():
    file_path = "passed_urls.txt"
    # Check if the internet connection is available
    connected_last_time = netmanager.is_connected()
    count = 0
    countapple = 0
    firstp = True
    previous_totalcount = 0
    previous_iteration_time = time.time()
    cumulative_tickets_per_hour = 0
    num_iterations = 0
    while True:
        print("Heartbeat")
        connected_this_time = netmanager.is_connected_stably()
        # Check how many new accounts need to be created
        to_create = filemanager.urls_to_create_count(file_path)
        if to_create > 0 and not connected_last_time and connected_this_time:
            testmode("Inte bajs", "ddd")
            print(f"Creating {to_create} new accounts...")
            count = 0
            countapple = 0
            firstp = True
            try:
                kmbot.createNewAccount()
                testmode("Bajs", "ddd")
            except Exception as e:
                print(e)
                kmos.restart_program()

        elif not connected_last_time and connected_this_time:
            #os.system("cls")
            print("\nRunning the main script...")
            testmode("Inte bajs", "ddd")
            count = 0
            countapple = 0
            firstp = True
            successrate, totalcount, totaltickets = (
                kmbot.run_script_in_threads(num_threads=kmbot.threadcount)
            )
            testmode(totalcount, "temperature")
            if totaltickets is not None:
                testmode(totaltickets, "total-tickets")
            if successrate != 0:
                testmode(successrate, "pass")
            print(
                f"Iteration: {kmbot.passes + kmbot.nonpasses + 1} Passes: " +
                f"{kmbot.passes} Fails: {kmbot.nonpasses} Ticket Count: " +
                f"{totalcount} Total Ticket Count: {totaltickets}"
            )
            if num_iterations != 0:
                last_iteration = time.time()
                iteration_duration = last_iteration - previous_iteration_time

                if totalcount is not None and previous_totalcount is not None:
                    # Calculate tickets processed in this iteration
                    tickets_processed_this_iteration = (
                        totalcount - previous_totalcount
                    )
                    # Calculate tickets per hour for this iteration
                    tickets_per_hour_this_iteration = (
                        tickets_processed_this_iteration
                        / iteration_duration
                        * 3600
                    )

                    print(f"Tickets processed this iteration: "
                          f"{tickets_processed_this_iteration}")

                    print(f"Tickets per hour this iteration: "
                          f"{tickets_per_hour_this_iteration:.2f}")
                    # Update cumulative_tickets_per_hour and num_iterations
                    cumulative_tickets_per_hour += (
                        tickets_per_hour_this_iteration
                    )

                num_iterations += 1
                if totalcount is not None:
                    # Calculate average tickets per hour across all iterations
                    average_tickets_per_hour = (
                        cumulative_tickets_per_hour / num_iterations
                    )
                    print(
                        f"Average tickets per hour across all iterations: "
                        f"{average_tickets_per_hour:.2f}"
                    )

                    # Store current values for the next iteration's comparison
                    previous_totalcount = totalcount
                    previous_iteration_time = last_iteration
                    if average_tickets_per_hour > 0:
                        testmode(average_tickets_per_hour, "tph")
            else:
                previous_totalcount = totalcount
                previous_iteration_time = time.time()
                num_iterations += 1
            testmode("Bajs", "ddd")
            time.sleep(2)
        connected_last_time = connected_this_time
        if not connected_this_time:
            if firstp:
                print("Waiting for internet connection...", end="", flush=True)
                firstp = False
            count = count + 1
            countapple = countapple + 1
            if countapple >= 60:
                print("\nRestarting Apple Mobile Device Service due to prolonged disconnection...")
                restart_apple_mobile_device_service()
                countapple = 0
            print(f"\rWaiting for internet connection... "
                  f"{count}", end="", flush=True)

            time.sleep(1)


if __name__ == "__main__":
    pid = os.getpid()
    print(f"Current process ID: {pid}")
    testmode("Bajs", "ddd")
    #kmbot.run_script()
    mainscript()
