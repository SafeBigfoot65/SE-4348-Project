from datetime import datetime, date
import sys

def getDate():
    return date.today().strftime("%Y-%m-%d")
def getTime():
    return datetime.now().strftime("%H:%M")

def logMessage(filename, message, current_date, current_time):

    command, message = message.split(" ", 1)
    
    with open(filename, 'a') as file:
        file.write(f"{current_date} {current_time} [{command}] {message}\n")



def main():
    current_date = getDate()
    current_time = getTime()
    logMessage(sys.argv[1], input("Enter log message: "), current_date, current_time)



if __name__ == "__main__":
    main()
    