from module.voice import speak, listen, mute_mode

# Standby mode loop
def enter_standby():
    speak("Going into standby. Say 'Tess' when you need me.")
    
    while True:
        trigger = listen().lower().strip()
        if "tess" in trigger:
            speak("Hey, I'm back.")
            return  # Exit standby and return control
