import sys
from subprocess import Popen, PIPE

def displayMenu():
    print("-----------------------------------------------------")
    print("                       Menu                          ")
    print("-----------------------------------------------------")

    print("password - set the password for encryption/decryption")
    print("encrypt  - encrypt a string")
    print("decrypt  - decrypt a string")
    print("history  - show history")
    print("quit     - exit the program")
    print("-----------------------------------------------------")


def is_alpha_only(s, allow_space=True):
    
    if s is None:
        return False
    if allow_space:
        return all(ch.isalpha() or ch.isspace() for ch in s)
    return all(ch.isalpha() for ch in s)


def sendCommand(user_input):
    if user_input is None:
        return None
    line = user_input.strip()
    if line == '':
        return None

    parts = line.split(' ', 1)
    command = parts[0].upper()
    argument = parts[1] if len(parts) > 1 else None

    proc = globals().get('ENCRYPTION_PROC')
    if not proc:
        
        try:
            process = Popen([sys.executable, 'encryption.py'], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
            if argument:
                full_command = f"{command} {argument}\n"
            else:
                full_command = f"{command}\n"
            stdout, stderr = process.communicate(full_command)
            if stdout:
                return stdout.strip()
            if stderr:
                return f"ERROR {stderr.strip()}"
            return None
        except Exception as e:
            return f"ERROR {e}"

    
    if argument:
        out_line = f"{command} {argument}\n"
    else:
        out_line = f"{command}\n"
    try:
        proc.stdin.write(out_line)
        proc.stdin.flush()
        resp = proc.stdout.readline()
        if not resp:
            return None
        return resp.strip()
    except Exception as e:
        return f"ERROR {e}"

def displayHistory(history):
    if not history:
        print("No history available.")
        return
    print("History:")
    for x, entry in enumerate(history):
        print(f"{x}) {entry}")


def choose_from_history(history):
    
    if not history:
        print("No history available to choose from.")
        return None
    print("Choose from history:")
    for i, entry in enumerate(history):
        print(f"{i}) {entry}")
    while True:
        sel = input("Enter index of item to use (or press Enter to cancel): ").strip()
        if sel == '':
            return None
        if sel.isdigit():
            idx = int(sel)
            if 0 <= idx < len(history):
                return history[idx]
        print("Invalid selection, try again.")


def get_argument(history):
    
    while True:
        s = input("Enter argument (or type 'H' to pick from history): ").strip()
        if not s:
            print("Argument cannot be empty.")
            continue
        if s.upper() == 'H':
            chosen = choose_from_history(history)
            if chosen is None:
                
                continue
            return chosen, True
        
        if not is_alpha_only(s, allow_space=True):
            print("Argument must contain only alphabetic characters and spaces. Try again.")
            continue
        return s, False


def log_message(action, message):
    
    logger = globals().get('LOGGER_PROC')
    if not logger or not logger.stdin:
        return
    try:
        
        logger.stdin.write(f"{action} {message}\n")
        logger.stdin.flush()
    except Exception:
        pass
   

# Using a persistent backend allows the PASS command to set a password that persists across multiple commands

def main():
    if len(sys.argv) < 2:
        print('Usage: driver.py <logfile>')
        return

    log_process = Popen([sys.executable, 'logger.py', sys.argv[1]], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
    globals()['LOGGER_PROC'] = log_process
    try:
        log_process.stdin.write('START Logging Started.\n')
        log_process.stdin.flush()
    except Exception:
        pass


    history = []


    try:
        ENCRYPTION_PROC = Popen([sys.executable, 'encryption.py'], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True, bufsize=1)
        globals()['ENCRYPTION_PROC'] = ENCRYPTION_PROC
    except Exception as e:
        print(f'Warning: could not start persistent encryption backend: {e}')

    try:
        while True:
            displayMenu()
            command = input("Enter command: ")
            if command is None:
                break

            command = command.strip().upper()

            if not command:
                continue

            if command == 'QUIT':
                
                log_message('STOPPED', 'Logging Stopped.')
                proc = globals().get('ENCRYPTION_PROC')
                if proc and proc.stdin:
                    try:
                        proc.stdin.write('QUIT\n')
                        proc.stdin.flush()
                    except Exception:
                        pass
                break

            if command == 'HISTORY':
                displayHistory(history)
                history_process = globals().get('LOGGER_PROC')
                history_process.stdin.write('HISTORY Viewed history.\n')
                history_process.stdin.flush()
                
                continue

            
            if command not in ['PASS', 'PASSWORD', 'ENCRYPT', 'DECRYPT']:
                print('Invalid command, please try again.')
                continue

            arg = None

            if command in ['PASS', 'PASSWORD', 'ENCRYPT', 'DECRYPT']:
               
                arg = get_argument(history)
                if command in ['PASS', 'PASSWORD']:
                    command_to_send = 'PASS'
                else:
                    command_to_send = command

            if arg:
               
                if command_to_send == 'PASS':
                    log_message('SET_PASSWORD', 'Success.')
                else:
                    log_message(command_to_send, arg)

                
                if command_to_send in ('ENCRYPT', 'DECRYPT'):
                    history.append(arg)

                response = sendCommand(f"{command_to_send} {arg}")
                
                if response is not None:
                    if response.startswith('RESULT'):
                        payload = response[len('RESULT'):].strip()
                        log_text = f"Success: {payload}" if payload else 'Success'
                    elif response.startswith('ERROR'):
                        payload = response[len('ERROR'):].strip()
                        log_text = f"Error: {payload}" if payload else 'Error'
                    else:
                        log_text = response
                    log_message('RESULT', log_text)
                    print(response)
            else:
                response = sendCommand(command_to_send if 'command_to_send' in locals() else command)
                if response is not None:
                    if response.startswith('RESULT'):
                        payload = response[len('RESULT'):].strip()
                        log_text = f"Success: {payload}" if payload else 'Success'
                    elif response.startswith('ERROR'):
                        payload = response[len('ERROR'):].strip()
                        log_text = f"Error: {payload}" if payload else 'Error'
                    else:
                        log_text = response
                    log_message('RESULT', log_text)
                    print(response)
    finally:
        
        proc = globals().get('ENCRYPTION_PROC')
        if proc:
            try:
                proc.stdin.close()
            except Exception:
                pass
            try:
                proc.wait(timeout=1)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass
        
        logger = globals().get('LOGGER_PROC')
        if logger:
            try:
                logger.stdin.write('QUIT\n')
                logger.stdin.flush()
            except Exception:
                pass
            try:
                logger.stdin.close()
            except Exception:
                pass
            try:
                logger.wait(timeout=1)
            except Exception:
                try:
                    logger.kill()
                except Exception:
                    pass


if __name__ == "__main__":
    main()