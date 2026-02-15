from pathlib import Path
import time, re, string, soundfile, sounddevice
from winpty import PtyProcess
from simple_tts import speak
from simple_stt import transcribe
HERE = Path(__file__).parent
ZORK = HERE / "zork1.z3"
FROTZ = HERE / "dumb-frotz.exe"
volume = 0.1
# Audio Mini Setup
STATIC = HERE / "static"
BELL = STATIC / "bell_02.ogg"
GONG = STATIC / "gong_short.ogg"
gong, _ = soundfile.read(GONG)
bell, _ = soundfile.read(BELL)

zork_homophones = ["zork", "zor", "zorc", "thankyou", "clique", "orc", "zorque", "zorg", "work"]
# STT
norm_dict = {
    # Zorks
    "zork": "zork",
    "zor": "zork",
    "zorc": "zork",
    "thankyou": "zork",
    "clique": "zork",
    "orc": "zork",
    "zorque": "zork",
    "zorg": "zork",
    "work": "zork",
    # Numbers:
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
    "10": "ten",
    # Directions:
    "feast": "east",
    "mouth": "south",
    "self": "south",
    "south east": "southeast",
    "south west": "southwest",
    "north east": "northeast",
    "north west": "northwest",
    # Misc
    "back": "bag",
    "jealous": "chalice",
    "boats": "boat",
}

number_list = ["1", "one", "2", "two", "3", "three", "4", "four", "5", "five", "6", "six", "7", "seven", "8", "eight", "9", "nine", "10", "ten",]
number_reverse = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
}
# clean spoken input
def clean_shoxx(text: str, more: str):
    translator = str.maketrans("","", string.punctuation + more)
    clean_text = text.translate(translator)
    return clean_text

def direction_tester(dir_list:list)-> bool:
    for item in dir_list:
        if item not in ["north", "east", "south", "west", "northeast","northwest","southeast","southwest", "up", "down"]:
            return False
    return True

# zork poll
def zork_test():
    while True:
        # print("Testing")
        sounddevice.play(0.1*bell, 48000)
        sounddevice.wait() 
        result = transcribe(duration=1)
        # print(result)
        clean_result = clean_shoxx(result, more = " ")
        if clean_result.lower() in norm_dict:
            clean_result = norm_dict[clean_result.lower()]
        
        if clean_result.lower() == "zork":
            # print("HERE")
            sounddevice.play(0.1*gong, 48000)
            sounddevice.wait() 
            try:
                the_text = transcribe(duration=3)
                if the_text[0] == " ":
                    the_text = the_text[1:]
                if the_text.lower() in norm_dict:
                    the_text = norm_dict[the_text.lower()]
                return clean_shoxx(the_text, more="")
            except IndexError:
                pass
        elif clean_result.lower() == "loop":
            sounddevice.play(0.1*gong, 48000)
            sounddevice.play(0.1*gong, 48000)
            sounddevice.wait() 
            result = transcribe(duration=1)
            # print(result)
            clean_result = clean_shoxx(result, more = " ")
            if clean_result.lower() == "directions":
                sounddevice.play(0.1*gong, 48000)
                sounddevice.wait() 
                the_text = transcribe(duration=5)
                clean_directions = clean_shoxx(the_text, more = "").lower()
                directions_list = clean_directions.split(" ")[1:]
                print("Loop: " + " ".join(directions_list))
                for i, direction in enumerate(directions_list):
                    if direction in norm_dict:
                        directions_list[i] = norm_dict[direction]
                all_valid = direction_tester(directions_list)
                if all_valid:
                    for direction in directions_list[:-1]:
                        proc.write(direction + "\r")
                        read_available()
                    if directions_list:
                        return directions_list[-1]                 

            elif clean_result.lower() in number_list:
                sounddevice.play(0.1*gong, 48000)
                sounddevice.play(0.1*gong, 48000)
                sounddevice.wait() 
                if clean_result in number_reverse.values():
                    number = int(clean_result)
                else:
                    number = int(number_reverse[clean_result.lower()])
                for _ in range(number - 1):
                    proc.write("g" + "\r")
                    read_available()
                return "g"
        # elif clean_result.lower() == "volume":
        #     sounddevice.play(0.1*gong, 48000)
        #     sounddevice.wait() 
        #     result = transcribe(duration=1)
        #     clean_result = clean_shoxx(result, more = " ")
        #     if clean_result.lower() == "quiet":
        #         global volume
        #         volume = 0.1


ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
def clean_text(text: str) -> str:
    return ansi_escape.sub('', text)

def speak_clean(message: str) -> None:
    speak(clean_text(message), volume)

def mini_sanitize(command: str) -> str:
    if command:
        if command[0] == " ":
            command = command[1:]
    return command.lower()


# Extract everything after the last "Moves: <number>"
def trim_to_moves(text: str) -> str:
    match = list(re.finditer(r'Moves:\s*\d+', text))
    if match:
        # Take the last occurrence of Moves: <number>
        last_moves = match[-1]
        return text[last_moves.end():].lstrip()
    return text

def trim_to_moves_2(text: str) -> str:
    # Match either Moves: <number> or Serial number <number>
    matches = list(re.finditer(r'(Moves:\s*\d+|Serial number\s*\d+)', text))
    if matches:
        last_match = matches[-1]
        return text[last_match.end():].lstrip()
    return text

# Start the PTY process
proc = PtyProcess.spawn([str(FROTZ), str(ZORK)])

def normalize_terminal_output(text: str) -> str:
    return text.replace("\r", "") #+ "\n\n"
    # lines = []
    # current_line = ""

    # for part in text.split("\n"):
    #     if "\r" in part:
    #         segments = part.split("\r")
    #         current_line = segments[-1]  # last overwrite wins
    #     else:
    #         current_line = part
    #     lines.append(current_line)

    # return "\n".join(lines)

# Small helper to read available output
def read_available():
    output = ""
    start = time.time()
    while proc.isalive():
        try:
            chunk = proc.read(91024)
            if not chunk:
                # print("noChunk")
                break
            output += chunk
            if "\r\n\r\n>" in output.lower():  # crude stop condition for demo
                break
            # elif "[story.sav]:" in output.lower():
            #     break
            elif "overwrite existing file?" in output.lower():
                break
            elif "]:" in output.lower():
                break
            elif "***more***" in output.lower():
                break
            elif "quit):" in output.lower():
                break

            if time.time() - start>10:
                # print("Timeout")
                break
        except EOFError:
            # print("EOFError")
            break
        except OSError:
            # print("OSError")
            break
    return output

print("\n"*50)

# Read initial banner
time.sleep(0.2)
initial = read_available()
# print(initial)
lineskips = initial.count("\r\n")
print("\n"*(lineskips + 20))
print(normalize_terminal_output(initial))
trimmed_initial = trim_to_moves_2(clean_text(initial))
# print("INITIAL OUTPUT:")
speak_clean(trimmed_initial)
command = zork_test()
print("\n"*5)
while True:

    # Send a command
    # print("Responding: ", command )
    san_command = mini_sanitize(command)
    # print(san_command)
    proc.write(san_command + "\r")

    time.sleep(0.2)
    response = read_available()
    # print("Z:", response)
    # print(response)
    lineskips = response.count("\r\n")
    print("\n"*(lineskips + 2))
    print(normalize_terminal_output(response)) #, end="", flush=True)
    
    trimmed_response = trim_to_moves(clean_text(response))
    # print("RESPONSE:")
    speak_clean(trimmed_response)
    command = zork_test()

proc.close()