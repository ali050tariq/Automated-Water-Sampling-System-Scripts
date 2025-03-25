from __future__ import absolute_import, division


# submitUiMachineTask should be used for all code that interacts
# with the machine. It guarantees that operations happen in the
# correct order, and that the user is presented with a dialog
# if there is an error.
from org.openpnp.util.UiUtils import submitUiMachineTask


from org.openpnp.model import LengthUnit, Location, Length, Package
from org.openpnp.util.UiUtils import submitUiMachineTask
from org.openpnp.model import Part  # Importing Part
from java.lang import System
import subprocess


def main():
    submitUiMachineTask(pick_and_place_chip)

def pick_and_place_chip():


    nozzle = machine.defaultHead.getNozzles()[0]
    nozzle2 = machine.defaultHead.getNozzles()[1]  # Second nozzle

    location = nozzle.location
    print_location(location) 

    # Parameters for first nozzle
    feeder = machine.getFeederByName("Chip_Position")  # Replace with your feeder's name
    chip_spacing_y = -28  # Y-spacing between chips in mm
    num_chips = 1       # Number of chips to pick
    place_x = 212       # X coordinate to place the chip
    place_y_start = 234# Starting Y coordinate for placing chips
    safe_z = 30           # Safe height above the parts in mm
    z_pick_place = 5     # Z height for picking and placing chips
    part = Part('R0603-1K')
    length_in_mm = Length(0.5, LengthUnit.Millimeters)
    part.setHeight(length_in_mm )
    partPackage = Package('R0603')
    part.setPackage(partPackage)


    # Parameters for Pipettes water Reserviors

    clean_water_x =  360
    clean_water_y = 280

    waste_water_x = 370
    waste_water_y = 179

    water_aspire_z = 2

    chip_dispense_x = 285
    chip_dispense_y = 120
    
    
    # Paramters for water pipeette dispensing in reference to N1
    # Clean water pipette dispensing location

    clean_pipette_x_dispense = 213
    clean_pipette_y_dispense = 268

    # Waste water pipette dispensing location

    waste_pipette_x_dispense = 216
    waste_pipette_y_dispense = 268

    # Parameters for chip discartion

    x_discard_coordinate = 270
    y_discard_coordinate = 240
  
    # Get the initial position of the feeder
    feeder_start_location = feeder.location

    safe_location = Location(LengthUnit.Millimeters,
                             feeder_start_location.x,
                             feeder_start_location.y,
                             safe_z,
                             0)
    #nozzle.moveTo(safe_location)

    safe_location_chip = Location(LengthUnit.Millimeters,
                             0,
                            0,
                             safe_z,
                             0)
    #nozzle.moveTo(safe_location)



    clean_water_dispesing_loc = Location(LengthUnit.Millimeters,
                             clean_pipette_x_dispense,
                             clean_pipette_y_dispense,
                             safe_z,
                             0)


    waste_water_dispensing_loc = Location(LengthUnit.Millimeters,
                             waste_pipette_x_dispense,
                             waste_pipette_y_dispense,
                             safe_z,
                             0)                   
    
    chip_dicard_location = Location(LengthUnit.Millimeters,
                             x_discard_coordinate,
                             y_discard_coordinate,
                             safe_z,
                             0)
    
    wastechip_pick_safe_location =  Location(LengthUnit.Millimeters,
                             place_x,
                             place_y_start,
                             z_pick_place,
                             0)
    
    wastechip_pick_location =  Location(LengthUnit.Millimeters,
                             place_x,
                             place_y_start,
                             -z_pick_place,
                             0)
    
    clear_water_location =  Location(LengthUnit.Millimeters,
                             clean_water_x,
                             clean_water_y,
                             safe_z,
                             0)

    waste_water_location =  Location(LengthUnit.Millimeters,
                             waste_water_x,
                             waste_water_y,
                             safe_z,
                             0)
                               
     
    chip_dispense_location =  Location(LengthUnit.Millimeters,
                             chip_dispense_x,
                             chip_dispense_y,
                             safe_z,
                             0)
                               
    
 

    # Asipre maximum amount of water in each pipette

  



    # Move to the feeder's first chip position


    for i in range(num_chips):
        # Calculate the position of the chip in the feeder



        nozzle.moveTo(clear_water_location)
        delay(3500)
        aspire_water_clean = clear_water_location.add(Location(LengthUnit.Millimeters, 0, 0, -40, 0))
        nozzle.moveTo(aspire_water_clean)    
        delay(11000)
        nozzle.moveTo(clear_water_location)
        delay(500)



        nozzle2.moveTo(waste_water_location)
        delay(3000)
        aspire_water_waste = waste_water_location.add(Location(LengthUnit.Millimeters, 0, 0, -18, 0))
        nozzle2.moveTo(aspire_water_waste)  
        delay(10500)
        nozzle2.moveTo(waste_water_location)
        delay(500)

        chip_y_position = feeder_start_location.y + (chip_spacing_y * i)
        chip_location = Location(LengthUnit.Millimeters,
                                 feeder_start_location.x,  # Keep X constant
                                 chip_y_position,          # Adjust Y based on index
                                 safe_z,  # Keep Z constant
                                 0)                        # Rotation not needed

        # Move the nozzle to pick up the chip
        nozzle.moveTo(chip_location)
        print_location(chip_location)
        delay(1000)

        # Move to pick locations but be a safe Z distance up:

        #safe_chip_location = chip_location.add(Location(LengthUnit.Millimeters, 0, 0, 10, 0))
        #nozzle.moveTo(safe_chip_location)
        #delay(1000)

        # Move down to the pick height

        
        pick_location = chip_location.add(Location(LengthUnit.Millimeters, 0, 0, -23, 0))
        nozzle.moveTo(pick_location)
        delay(500)
        nozzle.pick(part)  

        pick_location_safe_z = chip_location.add(Location(LengthUnit.Millimeters, 0, 0, 23, 0))

        nozzle.moveTo(pick_location_safe_z)

        delay(500)
        # Move back to the safe height after picking
        nozzle.moveTo(safe_location)

        # Calculate the placement location
        place_location = Location(LengthUnit.Millimeters, place_x, place_y_start, safe_z, 0)  

        # Move the nozzle to place the chip

        nozzle.moveTo(place_location)
        print_location(place_location)

         # Move down to the place height
        place_location_z = place_location.add(Location(LengthUnit.Millimeters, 0, 0, -21, 0))
        nozzle.moveTo(place_location_z)
        delay(500)
        nozzle.place()

        # Move back to safe height after placing
        place_location_z = place_location.add(Location(LengthUnit.Millimeters, 0, 0, 21, 0))
        nozzle.moveTo(place_location_z)

        delay(1000)


        # Water dispensing 


        nozzle.moveTo(clean_water_dispesing_loc)
        delay(500)
        dispense_water_clean = clean_water_dispesing_loc.add(Location(LengthUnit.Millimeters, 0, 0, -20, 0))
        nozzle.moveTo(dispense_water_clean)  
        delay(8000)
        dispense_water_clean = clean_water_dispesing_loc.add(Location(LengthUnit.Millimeters, 0, 0, 20, 0))
        nozzle.moveTo(dispense_water_clean)  
        delay(5000)
        dispense_water_clean = clean_water_dispesing_loc.add(Location(LengthUnit.Millimeters, 0, 0, -24, 0))
        nozzle.moveTo(dispense_water_clean)  
        delay(10000)
        dispense_water_clean = clean_water_dispesing_loc.add(Location(LengthUnit.Millimeters, 0, 0, 20, 0))
        nozzle.moveTo(dispense_water_clean) 
        delay(1000)



        
        nozzle2.moveTo(waste_water_dispensing_loc)
        delay(1000)
        dispense_water_waste = waste_water_dispensing_loc.add(Location(LengthUnit.Millimeters, 0, 0, -19, 0))
        nozzle2.moveTo(dispense_water_waste)  
        delay(8000)
        dispense_water_waste = waste_water_dispensing_loc.add(Location(LengthUnit.Millimeters, 0, 0, 19, 0))
        nozzle2.moveTo(dispense_water_waste) 
        delay(5000)
        dispense_water_waste = waste_water_dispensing_loc.add(Location(LengthUnit.Millimeters, 0, 0, -20, 0))
        nozzle2.moveTo(dispense_water_waste) 
        delay(8000)
        dispense_water_waste = waste_water_dispensing_loc.add(Location(LengthUnit.Millimeters, 0, 0, 19, 0))
        nozzle2.moveTo(dispense_water_waste) 
        delay(1000)



        #nozzle.moveTo(chip_dicard_location)
        #delay(1000)

        nozzle.moveTo(place_location)
        delay(1000)
        

        pick_location_discard = place_location.add(Location(LengthUnit.Millimeters, 0, 0, -23, 0))
        nozzle.moveTo(pick_location_discard)    
        
        nozzle.pick(part)
        delay(500)

        pick_location_discard = place_location.add(Location(LengthUnit.Millimeters, 0, 0, 12, 0))
        nozzle.moveTo(pick_location_discard)  
        delay(500)

        #pick_location_discard = pick_location_discard.add(Location(LengthUnit.Millimeters, 0, 0, 60, 0))
        #nozzle.moveTo(pick_location_discard)
        #delay(500)

        nozzle.moveTo(chip_dispense_location)
        delay(500)
        
        nozzle.place()
        delay(500)

        chip_dispense_location = chip_dispense_location.add(Location(LengthUnit.Millimeters, 0, 0, -50, 0))
        nozzle.moveTo(chip_dispense_location)
        delay(100)
        chip_dispense_location = chip_dispense_location.add(Location(LengthUnit.Millimeters, 0, 0, 50, 0))
        nozzle.moveTo(chip_dispense_location)
        delay(100)
        chip_dispense_location = chip_dispense_location.add(Location(LengthUnit.Millimeters, 0, 0, -50, 0))
        nozzle.moveTo(chip_dispense_location)
        delay(100)
        chip_dispense_location = chip_dispense_location.add(Location(LengthUnit.Millimeters, 0, 0, 50, 0))
        nozzle.moveTo(chip_dispense_location)
        delay(5000)
        

 

def print_location(location):
    print('Location: {}'.format(location.toString()))

def delay(milliseconds):
    end_time = System.currentTimeMillis() + milliseconds
    while System.currentTimeMillis() < end_time:
        pass

def send_hex():
    try:
        # Update the path to use raw string or forward slashes
        process = subprocess.Popen(
            ["python", r"C:\Users\AliTariq\.openpnp2\scripts\bluetoothTest.py"],  # Update path
            stdout=subprocess.PIPE,  # Capture stdout
            stderr=subprocess.PIPE   # Capture stderr
        )
        
        # Read the output and error
        stdout, stderr = process.communicate()
        
        # Print the output from the script
        if stdout:
            print("STDOUT: {}".format(stdout.decode('utf-8')))
        if stderr:
            print("STDERR: {}".format(stderr.decode('utf-8')))
        
        # Check for errors
        if process.returncode != 0:
            print("Error: {}".format(process.returncode))

    except Exception as e:
        print("An error occurred: {}".format(e))


main()