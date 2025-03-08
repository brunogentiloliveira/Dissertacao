import csv
import time
from camera_manager import CameraManager

def main():
    # Initialize camera manager
    manager = CameraManager()
    
    # Load cameras from CSV
    with open("cameras.csv", newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=";")
        for row in csvreader:
            manager.add_camera(
                ip=row[0],
                port=row[1],
                user=row[2],
                password=row[3]
            )
    
    try:
        # Main monitoring loop
        while True:
            statuses = manager.get_status()
            for status in statuses:
                print(f"Camera {status['ip']}: {status['status']}")
                if 'hostname' in status:
                    print(f"Hostname: {status['hostname']}")
                if 'error' in status:
                    print(f"Error: {status['error']}")
                print("---")
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        manager.stop_all()

if __name__=="__main__":
    main()
