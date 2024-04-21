from utils.ConvoCoach import ConvoCoach

if __name__ == "__main__":
    machine = ConvoCoach()

    with open("tempnew.webm", "rb") as audio_file:
        audio_data = audio_file.read()

    deedback = machine.add_clip(audio_data, 0, "tempnew.webm")
    print(deedback)
    deedback = machine.add_clip(audio_data, 2, "temp.webm")
    print(deedback)
    print(machine.get_highlights())