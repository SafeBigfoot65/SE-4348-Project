from datetime import datetime, date
import sys


def getDate():
    return date.today().strftime("%Y-%m-%d")


def getTime():
    return datetime.now().strftime("%H:%M")


def logMessage(filename, message):
    if not message:
        return
    parts = message.split(" ", 1)
    if len(parts) == 1:
        command = parts[0]
        rest = ''
    else:
        command, rest = parts

    current_date = getDate()
    current_time = getTime()
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"{current_date} {current_time} [{command}] {rest}\n")


def main():
    if len(sys.argv) >= 2:
        logfile = sys.argv[1]
    else:
        logfile = None
        for driver_input in sys.stdin:
            if driver_input is None:
                break
            first = driver_input.rstrip('\n').strip()
            if first == '':
                continue
           
            if first.upper().startswith('FILE '):
                logfile = first.split(' ', 1)[1].strip()
            else:
                logfile = first
            break
        if not logfile:
            return

    for driver_input in sys.stdin:
        if driver_input is None:
            break
        line = driver_input.rstrip('\n')
        if line is None:
            break
        line = line.strip()
        if line == '':
            continue
        if line.upper() == 'QUIT':
            break
        try:
            logMessage(logfile, line)
        except Exception:
            continue


if __name__ == "__main__":
    main()
    