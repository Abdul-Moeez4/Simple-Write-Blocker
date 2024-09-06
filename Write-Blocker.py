import os
import sys
import ctypes
import winreg as reg

#makes.takes to path/key in registry
usb_write_protect_key = r"SYSTEM\CurrentControlSet\Control\StorageDevicePolicies"
usb_write_protect_value = "WriteProtect"  #name of DWORD FILE

def is_admin():  #checks if user is admin or not
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() 
    except:
        return False

def run_as_admin():
    # Re-run the script with admin privileges
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def set_usb_write_protection(enable: bool):
    try:
        reg_key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, usb_write_protect_key, 0, reg.KEY_SET_VALUE)
        
        if enable:
            value = 1  # Enable write protection
        else:
            value = 0  # Disable write protection
            
        reg.SetValueEx(reg_key, usb_write_protect_value, 0, reg.REG_DWORD, value)
        reg.CloseKey(reg_key)
        
        if enable:
            print("USB write protection enabled.")
        else:
            print("USB write protection disabled.")
        
        #os.system("shutdown /r /t 0")  # Prompt for restart to apply changes
    
    except Exception as e:
        print(f"Failed to modify USB write protection: {e}")

def restart_prompt():
        choice = input('Would you like to restart your system? (y/n): ')

        if choice == 'y':
            os.system("shutdown /r /t 0")

        elif choice == 'n':
            print("System will not be restarted.")

        else:
            print("Invalid input. No restart will be performed.")

if __name__ == "__main__":
    
    if is_admin():
        # If the script is running with admin privileges, execute the main logic
        print("Welcome to the MOEEZ WRITE-BLOCKER")
        user_choice = input("Do you want to enable (e/E) or disable (d/D) USB write protection? (e/d): ")
        
        if user_choice == 'e' or user_choice == 'E':
            set_usb_write_protection(True)
            restart_prompt()

        elif user_choice =='d' or user_choice == 'D':
            set_usb_write_protection(False)
            restart_prompt()
        
        else:
            print("Invalid choice. Please enter 'e' to enable or 'd' to disable.")
    else:
        # If the script is not running with admin privileges, prompt user to re-run with admin privileges
        print("Please re-run this script with admin privileges.")
        run_as_admin()
