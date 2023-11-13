import utime

class AlarmClock:
    def __init__(self, hour, minute):
        self.alarm_time = (hour, minute)
    
    def is_alarm_time(self):
        current_time = utime.localtime()[3:5]  # Extract hour and minute from current time
        return current_time >= self.alarm_time
    
    def wait_for_alarm(self):
        while not self.is_alarm_time():
            utime.sleep(1)  # Sleep for 60 seconds, then check again
        print("Alarm time reached! Wake up!")

# Example usage
alarm = AlarmClock(hour=9, minute=46)  # Set the alarm for 8:30 AM
print("Waiting for the alarm...")
alarm.wait_for_alarm()
