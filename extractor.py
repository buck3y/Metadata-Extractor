'''
Script:  First Script
Author:  Buck3y
Date:    April 1, 2026
Version: 1.0
Purpose: Extract Metatdata from a specificed directory path and report back findings in a simple list.
'''

''' IMPORT STANDARD LIBRARIES '''
import os       # File System Methods
import time     # Time Conversion Methods
import sys      # System Methods
from pathlib import Path # Consistent Paths 

''' IMPORT 3RD PARTY LIBRARIES '''
from prettytable import PrettyTable # Optional Table formatting

''' DEFINE PSEUDO CONSTANTS '''
# NONE

''' LOCAL FUNCTIONS '''
def GetFileMetaData(fileName):
    ''' 
        obtain filesystem metadata
        from the specified file
        specifically, fileSize and MAC Times
        
        return True, None, fileSize and MacTimeList
    '''    
    try:
        metaData         = os.stat(fileName)       # Use the stat method to obtain meta data
        fileSize         = metaData.st_size         # Extract fileSize and MAC Times
        timeLastAccess   = metaData.st_atime
        timeLastModified = metaData.st_mtime
        timeCreated      = metaData.st_ctime
        
        macTimeList = [timeLastModified, timeLastAccess, timeCreated] # Group the MAC Times in a List
        print("="*60)
        return True, None, fileSize, macTimeList
    
    except Exception as err:
        return False, str(err), None, None

def GetOperatingSystem():
    ''' 
        obtain operating system information
        and change prompt hint accordingly
    '''    
    if sys.platform == "linux" or sys.platform == "linux2": #Changes hint prompt based on operating system
        return "i.e /var/lib >>>"
    elif sys.platform == "darwin":
        return "i.e /usr/bin >>>" 
    elif sys.platform == "win32":
        return "i.e c:\\ >>>"
    
def ReloadScript():
    ''' 
         Allows for seamless reusability, enabling multiple
         directories to be scanned without having to re run
         the script    
    '''    
    while True:
        print("")
        print("")
        userResponse = input("Type 's' to Scan Another Directory Path or 'q' to Quit the Script >>> ").lower() 
        if userResponse == 'q':
            return True
        
        if userResponse == 's':
            return False
        
        if userResponse != 'q' or 's':
            print("")
            print("Invalid Response")
            continue 
        
def Main():
    ''' 
       Main function of the script. Core logic of 
       the script.
        
    '''    
    print("\nWK-2 : Myles Hurlbut - Version One\n")    
    while True:
        tbl = PrettyTable(['FilePath', 'Status', 'FileSize', 'Modified-Time', 'Access-Time', 'Created-Time', "Error Info"])        
        targetFolder = input(f"\nEnter a Directory Path {GetOperatingSystem()} ")
        if targetFolder == 'q' or targetFolder == 'Q':
            sys.exit()                
            
        try:
            targetFolderList = os.listdir(targetFolder)
            print(f"Accessing Metadata for each entry in : ", Path(targetFolder))
            print("")
            for eachEntry in targetFolderList:   
                
                fullPath = Path(os.path.join(targetFolder, eachEntry)) # Using path from pathlib to maintain consistency throughout operating systems

                success, errInfo, fileSize, macList = GetFileMetaData(fullPath)
                    
                    # Obtain epoch values from macList
                lastMod = macList[0]
                lastAcc = macList[1]
                lastCrea = macList[2] 
                    
                    # Convert epoch values into human readable format
                modReadable = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(lastMod))
                accReadable = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(lastAcc))
                creaReadable = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(lastCrea))
                successReadable = "OK"
                
                # Format optional pretty Table
                tbl.add_row( [ fullPath, successReadable, fileSize, modReadable, accReadable, creaReadable, errInfo ] )    
                    
                # if success, print out metadata
                print(eachEntry)                    
                print("Success:    ", fullPath)
                print("File Size:   {:,.0f}".format(fileSize))
                print("Modified-Time: ", modReadable)
                print("Access-Time:   ", accReadable)  
                print("Created-Time:  ", creaReadable)       
            
               # if errors found, print out errors
        except Exception as err:
            print("\n\nScan borted     ", "Exception =     ", err)
            print("")
            print("")
            if not os.path.isdir(targetFolder):
                print(f"'{targetFolder}' is not a valid Path. \n")         
                continue
        
        # Optionally prompt user for additional formatting options 
        while success:
            print("")
            formatPrettyTable = input("Would you like to format this output into a sorted pretty table? (y)es or (n)o >>> ").lower()
            if formatPrettyTable == 'y':
                print("")   
                print("Formating Data into Pretty Table....")
                print("")                                        
                tbl.align = "l" 
                resultString = tbl.get_string(sortby="FileSize", reversesort=True)
                print(resultString)
                break
            elif formatPrettyTable == 'n':
                break
            else:
                print("Invalid Response. Type 'y' for yes or 'n' for no")
                continue                 
                
                    
        if ReloadScript() == True:
            print("")
            print("Exiting Script...")
            sys.exit()
        else:
            continue


''' LOCAL CLASSES '''
# NONE

''' MAIN ENTRY POINT '''

if __name__ == '__main__':
    Main()
