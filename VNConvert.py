import sys, glob, re

#filename = input("Enter the file name: ")

def errorHalt(error):
    print("An error occurred:", error)
    print(file)
    sys.exit()


def parseDialogText(dialogToParse):
    if "\"" in dialogToParse:
        dialogToParse = dialogToParse.replace("[pg]", "")
        dialogToParse = dialogToParse.replace("[sl]", "")
        dialogToParse = dialogToParse.replace("\"", "\"\\\"", 1)
        dialogToParse = re.sub("\"$", "\\\"\"", dialogToParse)
        dialogToParse = "    unknownspeaker " + dialogToParse + "\n"
        newFile.write(dialogToParse)
    else:
        dialogToParse = dialogToParse.replace("[pg]", "")
        dialogToParse = dialogToParse.replace("[sl]", "")
        dialogToParse = dialogToParse.replace("\n", "")
        dialogToParse = "    \"" + dialogToParse + "\"" + "\n"
        newFile.write(dialogToParse)
    return "Dialog text successfuly parsed?"

def parseLines(line):
    if line == "\n":
        newFile.write("\n")
        return "Line is nothing"                        
    if "//" in line:
        line = line.replace("//", "    #", 1)
        newFile.write(line)
        return "Line is a comment"
    if "*start" in line:
        newFile.write("    #start\n")
        return "Start of script"
    if "[" in line:
        if "[wait time=\"" and "input=\"1\"" in line:
            #parse wait command
            line = line.replace("[wait time=\"", "")
            line = line.replace("\" input=\"1\"]", "")
            line = float(line)/1000.0
            line = "    $ renpy.pause(" + str(line) + ")\n"
            newFile.write(line)
            return "Wait for X milliseconds"
        if "[wait time=\"" and "input=1" in line:
            #parse wait command
            line = line.replace("[wait time=\"", "")
            line = line.replace("\" input=1]", "")
            line = float(line)/1000.0
            line = "    $ renpy.pause(" + str(line) + ")\n"
            newFile.write(line)
            return "Wait for X milliseconds"
        if "[wait time=\"" in line:
            #parse wait command
            line = line.replace("[wait time=\"", "")
            line = line.replace("\"]", "")
            line = float(line)/1000.0
            line = "    $ renpy.pause(" + str(line) + ")\n"
            newFile.write(line)
            return "Wait for X milliseconds"
        if "[wait time=" in line:
            #parse wait command
            line = line.replace("[wait time=", "")
            line = line.replace("]", "")
            line = float(line)/1000.0
            line = "    $ renpy.pause(" + str(line) + ")\n"
            newFile.write(line)
            return "Wait for X milliseconds"
        if "[wait  time=" in line:
            return "oh no"
        if "[SAVELABLE TEXT=" in line:
            line = line.replace("[SAVELABLE TEXT=\"", "")
            line = line.replace("]", "")
            line = "    $ save_name = \"" + line + "\n"
            newFile.write(line)
            return "Save label set to X"
        if "[cm]" in line:
            #unknown command
            return "Unknown command handled: [cm]"
        if "[wit time=" in line:
            #unknown command
            return "Unknown command handled: wit"
        if "[cross_kirikae" in line:
            #unknown command
            return "Unknown command handled: cross_kirikae"
        if "[call" in line:
            #unknown command
            return "Unknown command handled: call"
        if "[i_kirikae]" in line:
            #unknown command
            return "Unknown command handled: [i_kirikae]"
        if "[wb]" in line:
            #wait for completion of fade
            return "Sure"
        if "[ws]" in line:
            return "Sure"
        if "[l]" in line:
            #pause until click
            return "Unknown command handled: [l]"
        if "[tclear]" in line:
            #unknown, could be text clear
            return "Unknown command handled: [tclear]"
        if "[stopbgm]" in line:
            #stop background music
            newFile.write("    stop music\n")
            return "Stop background music"
        if "[STOPBGM]" in line:
            #stop background music
            newFile.write("    stop music\n")
            return "Stop background music"
        if "[fbgm]" in line:
            return "Fade out background music"
        if "[tips]" in line:
            #line is just text with a tip highlighted
            #run as text but with highlight code
            #temporarily
            line.replace("[tips]", "{color=#00ff00}")
            if "[/tips]" in line:
                line.replace("[/tips]", "{/color}")
            else:
                errorHalt("oh no")
            parseDialogText(line)
            return "dialog with tips"
        if "[it]" in line:
            parseDialogText(line)
            return "dialog that contain italians"
        if "[TEXT C = " in line:
            return "text color???"
        if "[video" in line:
            return "Play a video"
        if "[bg_hyojib" in line:
            #parse new background
            if "[bg_hyojib bgb=" in line:
                return "Background changed to X"
            if "[bg_hyojib bg=" in line:
                return "probably an issue"
            else:
                errorMSG = "Failed to parse BG command - Invalid format" + line
                errorHalt(errorMSG)
        if "[bg_kirikae]" in line:
            #background gets displayed
            return "Displaying new background"
        if "[bg_kirikae ms=" in line:
            return "Display new background with delay?"
        if "[bg_hyoji" in line:
            return "Change background immediately?"
        if "[bg_houji" in line:
            return "It's probably bg related"
        if "[bgm" in line:
            #parse new background music
            return "Changing BGM to X"
        if "[fadeoutbgm" in line:
            return "bgm fade?"
        if "[Scroll_H_img" in line:
            return "Does something"
        if "[Scroll_img" in line:
            return "Does something 2"
        if "[clear_Scroll_H_img]" in line:
            return "Clear the something?"
        if "[clear_Scroll_img]" in line:
            return "Clear the something?"
        if "[cut_in img=" in line:
            return "unknown"
        if "[cut_in_clear time=" in line:
            return "unknown clear"
        if "[se" in line:
            return "Playing Sound Effect"
        if "[ se" in line:
            return "Playing Sound Effect"
        if "[SE_STOP();]" in line:
            return "Probably not functional"
        if "[qk time=" in line:
            return "Quake the screen"
        if "[qk tm]" in line:
            return "Quake?"
        if "[qk tm=" in line:
            return "Quake"
        if "[STOPQK]" in line:
            return "Stop quake?"
        if "[QKSTOP]" in line:
            return "Stop quake but different???"
        if "[fadeoutse]" in line:
            return "SE fadeout?"
        if "[fadeinse]" in line:
            return "SE fadein?"
        if "[fadeoutse time=" in line:
            return "SE fadeout with time?"
        if "[fadeinse time=" in line:
            return "SE fadein with time?"
        if "[fse]" in line:
            return "unknown, fade?"
        if "[sl]" in line:
            #new line
            parseDialogText(line)
            return "dialog with line"
        if "[pg]" in line:
            #new page
            parseDialogText(line)
            return "dialog with page"
        if "[r]" in line:
            return "do a line of new"
        if "[char_all_clear]" in line:
            #clear all characters
            return "Cleared all characters"
        if "[char_all_clear ]" in line:
            #clear all characters
            return "Cleared all characters"
        if "[ char_all_clear ]" in line:
            #clear all characters
            return "Cleared all characters"    
        if "[char_c_clear]" in line:
            return "Cleared center character"
        if "[char_r_clear]" in line:
            return "Cleared right character"
        if "[char_l_clear]" in line:
            return "Cleared left character"
        if "[char_double_clear]" in line:
            return "clear the double"
        if "[char" in line and "tatie" in line:
            #handle displaying of characters
            if "[char_c tatie=" in line:
                return "center"
            if "[char_r tatie=" in line:
                return "right"
            if "[char_l tatie=" in line:
                return "left"
            if "[char_l tatie1=" in line:
                return "left1"
            if "[char_double tatie1=" in line:
                return "double1"
            if "[char_all tatie1=" in line:
                return "all1"
            else:
                errorHalt("panic")
            return "Displayed a character"
        if "[tatie_right tatie=" in line:
            return "another char?"
        if "[jump" in line:
            return "Jump to a new file"
        if "[]" in line:
            return "whoops"
        if "[char_ll_clear]" in line:
            return "probably a whoops"
        if "[u_trans_black storage=" in line:
            return "unknown"
        if ";[layopt layer=message0" in line:
            return "commented code"
        if ";[eval exp=\"sf.game_select=11\"]" in line:
            return "commented code"
        if "When I glanced her way, I could see her mouth was slightly open. I could also see into her collar, which had gaped slightly open from her movement.[sl" in line:
            return "handle this line"
        if "[cm}" in line:
            return "mistake"
        if "[var name=\"g.clear\" data=\"1\"]" in line:
            return "unknown"
        if "[end_kirikae time=\"2800\"]" in line:
            return "unknown"
        else:
            errorMSG = "Unknown line: " + line
            errorHalt(errorMSG)
    else:
        parseDialogText(line)
        return "done the text thing"


for file in glob.glob("./*/**.iet"):
    originalFile = open(file, "r", encoding="utf-8-sig")
    newFilename = file.replace(".iet", ".rpy")
    levelName = newFilename.replace(".rpy", "")
    newFile = open(newFilename, "w+", encoding="utf8")

    fileContents = originalFile.readlines()




    newFile.write("label " + levelName + ":\n")

    coolLines = 0
    for x in fileContents:
        coolLines += 1
        result = parseLines(x)
        print("{}, {}".format(coolLines, file))
        print(result)
    originalFile.close()
    newFile.close()