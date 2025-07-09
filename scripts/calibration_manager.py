

import yaml
import argparse
import datetime
from typing import Any, Dict, List

def load_calibrations(file_path: str) -> List[Dict[str, Any]]:
    """Loads calibration data from a YAML file."""
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
            if data is None:
                return []
            return data
    except FileNotFoundError:
        return []

def save_calibrations(file_path: str, calibrations: List[Dict[str, Any]]):
    """Saves calibration data to a YAML file."""
    with open(file_path, 'w') as f:
        yaml.dump(calibrations, f, default_flow_style=False, sort_keys=False)

def print_calibration(calibration: Dict[str, Any]):
    """Prints a single calibration entry in a readable format."""
    print(f"ID: {calibration['id']}")
    print(f"  Date: {calibration['date']}")
    print(f"  Scene: {calibration['scene']}")
    print("  Cameras:")
    for camera in calibration['cameras']:
        print(f"    - Name: {camera['name']}")
        print(f"      Model: {camera['model']}")
        print(f"      Serial Number: {camera['serial_number']}")
        print(f"      Position: {camera['position']}")
        print(f"      Distortion: {camera['distortion']}")
        print(f"      In Focus: {camera['in_focus']}")
        print(f"      FOV: {camera['fov']}")
    print(f"  Baseline: {calibration['baseline']}")
    print(f"  GStreamer Pipeline: {calibration['gstreamer_pipeline']}")
    print(f"  Resolution: {calibration['resolution']}")
    print("  Calibration Program:")
    print(f"    Name: {calibration['calibration_program']['name']}")
    print(f"    Version: {calibration['calibration_program']['version']}")
    print("  Platform:")
    print(f"    Recording: {calibration['platform']['recording']}")
    print(f"    Calibration: {calibration['platform']['calibration']}")
    print(f"  Notes: {calibration['notes']}")
    print("-" * 20)

def get_input(prompt: str, default: str = "") -> str:
    """Gets user input with an optional default value."""
    return input(f"{prompt} [{default}]: ") or default

def get_bool_input(prompt: str) -> bool:
    """Gets a boolean input from the user."""
    while True:
        val = input(f"{prompt} (y/n): ").lower()
        if val in ['y', 'yes']:
            return True
        elif val in ['n', 'no']:
            return False
        print("Invalid input. Please enter 'y' or 'n'.")

def add_calibration(file_path: str):
    """Interactively adds a new calibration entry."""
    calibrations = load_calibrations(file_path)
    today = datetime.date.today()
    new_id = f"{today.strftime('%Y%m%d')}-{len(calibrations) + 1:02d}"

    new_calibration = {
        'id': new_id,
        'date': str(today),
        'scene': get_input("Enter the scene description"),
        'cameras': [],
        'baseline': get_input("Enter the baseline"),
        'gstreamer_pipeline': get_input("Enter the GStreamer pipeline"),
        'resolution': get_input("Enter the resolution (e.g., 1920x1080)"),
        'calibration_program': {
            'name': get_input("Enter the calibration program name"),
            'version': get_input("Enter the calibration program version")
        },
        'platform': {
            'recording': get_input("Enter the recording platform"),
            'calibration': get_input("Enter the calibration platform")
        },
        'notes': get_input("Enter any notes")
    }

    num_cameras = int(get_input("Enter the number of cameras", "3"))
    for i in range(num_cameras):
        print(f"\n--- Entering details for Camera {i+1} ---")
        camera = {
            'name': get_input("Enter camera name (e.g., left, right, center)"),
            'model': get_input("Enter camera model"),
            'serial_number': get_input("Enter camera serial number"),
            'position': get_input("Enter camera position"),
            'distortion': get_bool_input("Does the camera have distortion?"),
            'in_focus': get_bool_input("Is the camera in focus?"),
            'fov': get_input("Enter the camera field of view (FOV)")
        }
        new_calibration['cameras'].append(camera)

    calibrations.append(new_calibration)
    save_calibrations(file_path, calibrations)
    print(f"\nSuccessfully added new calibration with ID: {new_id}")

def main():
    """Main function to manage calibrations."""
    parser = argparse.ArgumentParser(description="Manage camera calibration data.")
    parser.add_argument("--file", default="calibrations.yaml", help="The path to the calibrations YAML file.")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # List command
    list_parser = subparsers.add_parser('list', help='List all calibrations')

    # View command
    view_parser = subparsers.add_parser('view', help='View a specific calibration')
    view_parser.add_argument('id', type=str, help='The ID of the calibration to view')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search for calibrations')
    search_parser.add_argument('term', type=str, help='The term to search for')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new calibration')

    args = parser.parse_args()
    calibrations = load_calibrations(args.file)

    if args.command == 'list':
        if not calibrations:
            print("No calibrations found.")
            return
        for calibration in calibrations:
            print_calibration(calibration)
    elif args.command == 'view':
        for calibration in calibrations:
            if calibration['id'] == args.id:
                print_calibration(calibration)
                return
        print(f"Calibration with ID '{args.id}' not found.")
    elif args.command == 'search':
        results = []
        search_term = args.term.lower()
        for calibration in calibrations:
            if search_term in str(calibration).lower():
                results.append(calibration)
        if not results:
            print(f"No calibrations found matching '{args.term}'.")
            return
        print(f"Found {len(results)} match(es) for '{args.term}':")
        for result in results:
            print_calibration(result)
    elif args.command == 'add':
        add_calibration(args.file)

if __name__ == "__main__":
    main()
