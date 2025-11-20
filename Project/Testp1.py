import time
import os
import sys
import random

# ==========================================
# PART 1: SYSTEM UTILITIES (เครื่องมือระบบ)
# ==========================================

def clear_screen():
    """ล้างหน้าจอ"""
    os.system('cls' if os.name == 'nt' else 'clear')

def type_writer(text, speed=0.03):
    """พิมพ์ตัวหนังสือทีละตัว"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print("")

def loading_bar():
    """สร้างหลอดโหลดข้อมูล"""
    print("Processing: [", end="")
    for _ in range(20):
        time.sleep(0.05)
        sys.stdout.write("#")
        sys.stdout.flush()
    print("] 100% Complete\n")

# ==========================================
# PART 2: GAME LEVELS (ด่าน 1-5)
# ==========================================

def level_1_social():
    clear_screen()
    print("========================================")
    print(" LEVEL 1: TARGET RECONNAISSANCE")
    print("========================================")
    type_writer("[Mission] Access Admin Profile: 'Mr. Robot'")
    
    print("\n[Intel Gathered]:")
    print("   - Year of Birth: 1988")
    print("   - Favorite Color: Red")
    print("   - First Pet: Dog named 'Buddy'")
    print("----------------------------------------")
    type_writer("[Hint] He often uses: PetName + BirthYear")
    
    attempts = 3
    correct_pass = "Buddy1988"

    while attempts > 0:
        print(f"\nAttempts remaining: {attempts}")
        user_input = input("Enter Password > ")

        if user_input == correct_pass:
            print("\n[+] Password Accepted.")
            time.sleep(1)
            return True
        else:
            print("[-] Access Denied.")
            attempts -= 1
            
    return False

def level_2_crypto():
    clear_screen()
    print("========================================")
    print(" LEVEL 2: DECRYPTION CHALLENGE")
    print("========================================")
    type_writer("[Mission] Crack the encrypted file.")
    
    print("\n[INTERCEPTED MESSAGE]:")
    print("   >> URRW_ACCESS_XA <<") 
    print("----------------------------------------")
    type_writer("[Hint] Caesar Cipher: Shift -3 (e.g., D -> A)")
    
    # เฉลยคือ ROOT (URRW ถอยหลัง 3 ตัวอักษร)
    correct_answer = "ROOT"

    user_input = input("\nEnter Decrypted Keyword > ").upper()
    loading_bar()

    if user_input == correct_answer:
        print("[+] Decryption Successful. Key matched.")
        time.sleep(1)
        return True
    else:
        print("[-] Decryption Failed. Data corrupted.")
        return False

def level_3_sql():
    clear_screen()
    print("========================================")
    print(" LEVEL 3: DATABASE INJECTION")
    print("========================================")
    type_writer("[Mission] Bypass the Mainframe Login.")
    print("\n[STATUS] Admin Password: UNKNOWN (Encrypted)")
    print("----------------------------------------")
    type_writer("[Hint] Input field is vulnerable to SQL Injection.")
    type_writer("[Tip] Use payload: ' OR '1'='1")
    
    user_input = input("\nUsername Input > ")
    
    # ตรวจสอบ SQL Injection Payload
    if "' OR '" in user_input or "' or '" in user_input:
        print("\n[!] SQL Syntax Error Detected... but Access Granted!")
        print("[+] Dumping Database...")
        time.sleep(1)
        return True
    else:
        print("\n[-] Login Failed. Invalid Credentials.")
        return False

def level_4_network_scan():
    clear_screen()
    print("========================================")
    print(" LEVEL 4: PORT SCANNING")
    print("========================================")
    type_writer("[Mission] Find the vulnerable open port.")
    
    print("\n[SYSTEM] Scanning Target IP...")
    time.sleep(1)
    
    target_port = random.choice([21, 22, 80, 8080, 31337])
    possible_ports = [21, 22, 53, 80, 443, 8080, 31337]
    
    for port in possible_ports:
        time.sleep(0.2)
        if port == target_port:
            print(f"   [+] Port {port} : OPEN (VULNERABLE!)")
        else:
            status = random.choice(["CLOSED", "FILTERED"])
            print(f"   [-] Port {port} : {status}")

    print("----------------------------------------")
    try:
        user_input = int(input("\nEnter Vulnerable Port Number > "))
        if user_input == target_port:
            print(f"\n[+] Connected to Port {target_port}.")
            return True
        else:
            print("\n[-] Connection Refused.")
            return False
    except ValueError:
        return False

def level_5_privilege():
    clear_screen()
    print("========================================")
    print(" LEVEL 5: ROOT PRIVILEGE ESCALATION")
    print("========================================")
    type_writer("[Mission] Escalate from 'guest' to 'root'.")
    
    print("\nguest@server:~$ whoami")
    print("guest")
    print("----------------------------------------")
    type_writer("[Hint] Switch user command: sudo su")
    
    user_input = input("\nguest@server:~$ ")
    loading_bar()

    if user_input.strip() in ["sudo su", "su root", "su"]:
        print("\nroot@server:~# ACCESS GRANTED.")
        return True
    else:
        print(f"\n-bash: {user_input}: command not found")
        return False

# ==========================================
# PART 3: MAIN CONTROL (ส่วนควบคุมหลัก)
# ==========================================

def main():
    clear_screen()
    print(r"""
      _____  _  _  ____  ____  ____  
     / ____|| || ||  _ \|  __||  _ \ 
    | |     \  /  | |_) | |_   | |_) |
    | |___   ||   |  _ <|  _|  |  _ < 
     \____|  ||   | |_) | |__  | | \ \
            |__|  |____/|____| |_|  \_\
    """)
    print("    - THE TERMINAL BREACH: FULL VERSION -")
    time.sleep(1)
    
    input("\nPress [ENTER] to Initialize Attack...")

    # Flow การเล่นเกม: ด่าน 1 -> 2 -> 3 -> 4 -> 5
    if level_1_social():
        type_writer("\n[SYSTEM] Level 1 Cleared. Moving deeper...", 0.02)
        time.sleep(1)
        
        if level_2_crypto():
            type_writer("\n[SYSTEM] Level 2 Cleared. Decrypting traffic...", 0.02)
            time.sleep(1)
            
            if level_3_sql():
                type_writer("\n[SYSTEM] Level 3 Cleared. Database dumped.", 0.02)
                time.sleep(1)

                if level_4_network_scan():
                    type_writer("\n[SYSTEM] Level 4 Cleared. Backdoor found.", 0.02)
                    time.sleep(1)

                    if level_5_privilege():
                        # ฉากจบ (WIN)
                        clear_screen()
                        print("\n\n")
                        print("########################################")
                        print("#         MISSION ACCOMPLISHED         #")
                        print("#     YOU HAVE FULL ROOT ACCESS        #")
                        print("########################################")
                        print("\n[CREDITS]")
                        print("Hacker: Player 1") # แก้ชื่อตรงนี้ได้
                        print("Language: Python 3")
                        input("\nPress Enter to exit...")
                    else:
                         print("\n[GAME OVER] Failed to gain Root access.")
                else:
                    print("\n[GAME OVER] Connection closed by target.")
            else:
                print("\n[GAME OVER] Firewall blocked SQL query.")
        else:
            print("\n[GAME OVER] Decryption failed.")
    else:
        print("\n[GAME OVER] Intrusion detected at entry.")

if __name__ == "__main__":
    main()