import random
import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests



# DISCORD CONFIG




DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1517655700791361577/PWGoOoqccwcCOlzI1K5al-rKFGlFTUOVnJ7xX19cNvdtByaiFNkGp4I939KJ7E1ShJzp"
NCO_ROLE_ID = "999662869840920657"




def send_to_discord(message):
    data = {"content": message}

    try:
        response = requests.post(DISCORD_WEBHOOK, json=data)

        print("Discord status:", response.status_code)
        print("Response:", response.text)

        if response.status_code == 204:
            return True
        else:
            return False

    except Exception as e:
        print("Error:", e)
        return False




# LESSON DATA

lessonsCadets= []
try:
    with open ("lessonsCadets.txt", "r", encoding="utf-8") as file:
         for line in file:
              line = line.strip().split(",")
              mydict = {"id":(line[0]),
                            "title":(line[1]),
                                "score":int(line[2])}
              lessonsCadets.append(mydict)
except FileNotFoundError:
    print("Error: lessonsCadets.txt could not be found.")

lessonsRecruits= []
try:
    with open ("lessonsRecruits.txt", "r", encoding="utf-8") as file:
         for line in file:
              line = line.strip().split(",")
              mydict = {"id":(line[0]),
                            "title":(line[1]),
                                "type":(line[2]),
                                    "order":int(line[3])}
              lessonsRecruits.append(mydict)
except FileNotFoundError:
    print("Error: lessonsRecruits.txt could not be found.")

#score based system makes new list based of score to give each lesson a different weighting

lessonsCadetsWeighted = []
for line in lessonsCadets:
    for order in range(line['score']):
        mydict = {"id":(line['id']),
                      "title":(line['title'])}
        lessonsCadetsWeighted.append(mydict)

print(lessonsCadetsWeighted)

LESSONS = {"cadet": lessonsCadetsWeighted,
              "recruit": lessonsRecruits}

#Instructors

INSTRUCTORS= []
try:
    with open ("instructors.txt", "r", encoding="utf-8") as file:
         for line in file:
              line = line.strip().split(",")
              mydict = {"id":(line[0]),
                            "name":(line[1]),
                                "rank":(line[2]),
                                    "cadet":[line[3],line[4],line[5]],
                                        "recruit":[line[6],line[7],line[8]]}
              INSTRUCTORS.append(mydict)
except FileNotFoundError:
    print("Error: instructors.txt could not be found.")

# Designated recruit instructors

RECRUIT_INSTRUCTORS= []
try:
    with open ("recruitInstructors.txt", "r", encoding="utf-8") as file:
         for line in file:
              line = line.strip().split(",")
              mydict = {"id":(line[0]),
                                "name":(line[1]),
                                    "rank":(line[2]),
                                        "cadet":[line[3],line[4],line[5]],
                                            "recruit":[line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17]],}
              RECRUIT_INSTRUCTORS.append(mydict)
except FileNotFoundError:
    print("Error: recruitInstructors.txt could not be found.")

RECRUIT_PRIORITY_IDS = {i['id'] for i in RECRUIT_INSTRUCTORS}


# in case of no RECRUIT_INSTRUCTORS
ALL_INSTRUCTORS = INSTRUCTORS + RECRUIT_INSTRUCTORS




# GUI




root = tk.Tk()
root.title("Parade Night Programme Generator")
root.geometry("900x650")

def file_error(filename):
    messagebox.showerror(
        "File Error",
        f"The file '{filename}' could not be found.\n\n"
        "Please make sure all required files are in the program folder."
    )


output_box = scrolledtext.ScrolledText(root, width=100, height=25)
output_box.pack(fill="both", expand=True)




present_vars = {}


def show(text=""):
    output_box.insert(tk.END, str(text) + "\n")




def clear_output():
    output_box.delete("1.0", tk.END)

# DISCORD FAIL

def discord_failed_window():
    window = tk.Toplevel(root)
    window.title("Discord Error")
    window.geometry("400x200")

    ttk.Label(
        window,
        text="The message didn't send to the Discord server.",
        wraplength=350
    ).pack(pady=(35, 10))

    ttk.Label(
        window,
        text="Please check your internet connection."
    ).pack(pady=5)

    ttk.Button(
        window,
        text="OK",
        command=window.destroy
    ).pack(pady=20)

# MAIN




def generate():
    clear_output()


    show("=" * 60)
    show("PARADE NIGHT PROGRAMME")
    show("=" * 60)


    present_ids = [i for i, v in present_vars.items() if v.get()]
    present = [i for i in ALL_INSTRUCTORS if i['id'] in present_ids]

    if not present:
        messagebox.showerror(
            "No Instructors",
            "No instructors have been selected.\n\n"
            "Please select at least one instructor."
        )
        return

    try:
        last_drills_done = int(drill_progress_entry.get())

        if last_drills_done < 0:
            messagebox.showerror(
                "Invalid Input",
                "Drill lessons completed cannot be negative."
            )
            return

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Drill lessons completed must be a whole number."
        )
        return

    try:
        last_theory_done = int(theory_progress_entry.get())

        if last_theory_done < 0:
            messagebox.showerror(
                "Invalid Input",
                "Theory lessons completed cannot be negative."
            )
            return

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Theory lessons completed must be a whole number."
        )
        return

    used_instructors = set()


    # recruit


    recruit_sorted = sorted(LESSONS["recruit"], key=lambda x: x['order'])


    def pick_recruit_instructor(lesson):
         # Build the pool of present, qualified, not-yet-used instructors.
         qualified = [
              i for i in present
              if lesson['id'] in i["recruit"] and i['id'] not in used_instructors
         ]
         if not qualified:
              return None


         # Prefer the designated recruit instructors if any are in the pool.
         priority_qualified = [i for i in qualified if i['id'] in RECRUIT_PRIORITY_IDS]
         if priority_qualified:
              return random.choice(priority_qualified)


         # Fall back to anyone else who is present and qualified.
         return random.choice(qualified)


    def next_of_type(rtype, completed_count):
         type_lessons = [l for l in recruit_sorted if l['type'] == rtype]
         for index, l in enumerate(type_lessons):
              if index >= completed_count:
                    instr = pick_recruit_instructor(l)
                    if instr:
                         return l, instr
         return None, None


    r_drill, r_drill_instr = next_of_type("drill", last_drills_done)
    if r_drill_instr:
         used_instructors.add(r_drill_instr['id'])


    r_theory, r_theory_instr = next_of_type("theory", last_theory_done)
    if r_theory_instr:
         used_instructors.add(r_theory_instr['id'])

     
    # CADETS excludes anyone already used for a recruit lesson tonight.
    cadet_options = []
    for l in LESSONS["cadet"]:
        qualified = [
              i for i in present
              if l['id'] in i["cadet"] and i['id'] not in used_instructors
         ]

        #Bypass lesson qualification requirement if there is not enough instructors
        if not qualified:
            qualified = [i for i in present if i['id'] not in used_instructors]

        if qualified:
            cadet_options.append((l, qualified))

    if len(cadet_options) < 2:
        messagebox.showerror(
            "Not Enough Instructors",
            "There are not enough available instructors "
            "to create two cadet lessons."
        )
        return


    random.shuffle(cadet_options)
    cadet_slots = []


    for lesson, qualified in cadet_options[:2]:
         # Reroll in case an instructor was used by the previous slot pick.
         qualified = [i for i in qualified if i['id'] not in used_instructors]

         if not qualified:
             qualified = [i for i in present if i['id'] not in used_instructors]
         if not qualified:
              continue

         instr = random.choice(qualified)
         cadet_slots.append((lesson, instr))
         used_instructors.add(instr['id'])

    if len(cadet_slots) < 2:
        messagebox.showerror(
            "Programme Error",
            "The programme could not be generated because "
            "there are not enough instructors available."
        )
        return


    # OUTPUT


    today = datetime.date.today().strftime("%d/%m/%Y")


    show(f"Date: {today}\n")
    show("19:10 Opening Parade\n")


    show("19:30 LESSON 1")
    show(f"Cadets: {cadet_slots[0][0]['title']}")
    show(f"Instructor: {cadet_slots[0][1]['name']}\n")


    if r_drill:
         show(f"Recruits: {r_drill['title']} [Drill]")
         show(f"Instructor: {r_drill_instr['name']}\n")


    show("20:15 Break\n")


    show("20:30 LESSON 2")
    show(f"Cadets: {cadet_slots[1][0]['title']}")
    show(f"Instructor: {cadet_slots[1][1]['name']}\n")


    if r_theory:
         show(f"Recruits: {r_theory['title']} [Theory]")
         show(f"Instructor: {r_theory_instr['name']}\n")


    show("21:45 End")
    show("=" * 60)


    # DISCORD


    discord_message = f"""
<@&{NCO_ROLE_ID}>




**PARADE NIGHT PROGRAMME**
Date: {today}




19:10 Opening Parade




19:30 LESSON 1
Cadets: {cadet_slots[0][0]['title']}
Instructor: {cadet_slots[0][1]['name']}




Recruits: {r_drill['title'] if r_drill else "None"}
Instructor: {r_drill_instr['name'] if r_drill_instr else "UNASSIGNED"}




20:30 LESSON 2
Cadets: {cadet_slots[1][0]['title']}
Instructor: {cadet_slots[1][1]['name']}




Recruits: {r_theory['title'] if r_theory else "None"}
Instructor: {r_theory_instr['name'] if r_theory_instr else "UNASSIGNED"}




21:45 End
"""

    discord_sent = send_to_discord(discord_message)

    if not discord_sent:
        discord_failed_window()




# VIEW




def view_lessons():
    clear_output()
    show("CADET LESSONS:\n")
    for l in lessonsCadets:
         show(f"{l['id']} - {l['title']} - {l['score']}")


    show("\nRECRUIT LESSONS:\n")
    for l in sorted(LESSONS["recruit"], key=lambda x: x['order']):
         show(f"{l['id']} [{l['order']}] {l['type']} - {l['title']}")




def view_instructors():
    clear_output()
    show("INSTRUCTORS:\n")
    for i in INSTRUCTORS:
         show(f"{i['id']} - {i['name']} ({i['rank']})")


    show("\nRECRUIT INSTRUCTORS (priority for recruit lessons):\n")
    for i in RECRUIT_INSTRUCTORS:
         show(f"{i['id']} - {i['name']} ({i['rank']})")


def open_add_lesson_window():
    window = tk.Toplevel(root)
    window.title("Add lesson")
    window.geometry("350x350")

    ttk.Label(window, text="ID (e.g. C009):").pack(pady=(10, 0))
    id_entry = ttk.Entry(window)
    id_entry.pack()

    ttk.Label(window, text="Lesson Title").pack(pady=(10, 0))
    title_entry = ttk.Entry(window)
    title_entry.pack()

    def submit():
        id_value = id_entry.get()
        title_value = title_entry.get()
        score_value = "10"
        line = ",".join([id_value, title_value, score_value])

        with open("lessonsCadets.txt", "a", encoding="utf-8") as file:
            file.write(line + "\n")

        window.destroy()

    ttk.Button(window, text="Add lesson", command=submit).pack(pady=20)


def open_add_instructor_window():
     window = tk.Toplevel(root)
     window.title("Add Instructor")
     window.geometry("350x350")

     ttk.Label(window, text="ID (e.g. I009):").pack(pady=(10, 0))
     id_entry = ttk.Entry(window)
     id_entry.pack()

     ttk.Label(window, text="Rank + name:").pack(pady=(10, 0))
     name_entry = ttk.Entry(window)
     name_entry.pack()

     ttk.Label(window, text="Rank (Staff or NCO):").pack(pady=(10, 0))
     rank_entry = ttk.Entry(window)
     rank_entry.pack()

     ttk.Label(window, text="Cadet lessons (max 3, comma separated, e.g. C001,C002):").pack(pady=(10, 0))
     cadet_entry = ttk.Entry(window)
     cadet_entry.pack()

     ttk.Label(window, text="Recruit lessons (max 3, comma separated, e.g. R001,R002):").pack(pady=(10, 0))
     recruit_entry = ttk.Entry(window)
     recruit_entry.pack()

     def submit():
          id_value = id_entry.get()
          name_value = name_entry.get()
          rank_value = rank_entry.get()
          cadet_value = cadet_entry.get()
          recruit_value = recruit_entry.get()

          line = ",".join([id_value, name_value, rank_value, cadet_value, recruit_value])

          with open("instructors.txt", "a", encoding="utf-8") as file:
              file.write(line + "\n")

          window.destroy()

     ttk.Button(window, text="Add Instructor", command=submit).pack(pady=20)


def lessonScore():

    window = tk.Toplevel(root)
    window.title("Lesson Evaluation")
    window.geometry("400x300")

    ttk.Label(window,text="Select lesson:").pack(pady=(20, 5))

    # Get all cadet lesson titles

    lesson_titles = []

    for lesson in lessonsCadets:
        lesson_titles.append(lesson['title'])

    # Variable that stores the selected lesson

    selected_lesson = tk.StringVar()

    # Creates dropdown menu

    lesson_dropdown = ttk.Combobox(window,textvariable=selected_lesson, values=lesson_titles, state="readonly")

    lesson_dropdown.pack(pady=10)

    lesson_dropdown.current(0)

    def bad():

        new_lines = []

        with open("lessonsCadets.txt", "r", encoding="utf-8") as file:

            for line in file:

                parts = line.strip().split(",")

                if parts[1] == selected_lesson.get():
                    score = int(parts[2])

                    score = score - 1

                    parts[2] = str(score)

                new_lines.append(",".join(parts))

        with open("lessonsCadets.txt", "w", encoding="utf-8") as file:
            for line in new_lines:
                file.write(line + "\n")

        window.destroy()

    def ok():
        window.destroy()

    def good():

        new_lines = []

        with open("lessonsCadets.txt", "r", encoding="utf-8") as file:

            for line in file:

                parts = line.strip().split(",")

                if parts[1] == selected_lesson.get():
                    score = int(parts[2])

                    score = score + 1

                    parts[2] = str(score)

                new_lines.append(",".join(parts))

        with open("lessonsCadets.txt", "w", encoding="utf-8") as file:
            for line in new_lines:
                file.write(line + "\n")
        window.destroy()

    ttk.Button(window,text="bad",command=bad).pack(pady=20)
    ttk.Button(window,text="ok",command=ok).pack(pady=20)
    ttk.Button(window,text="good",command=good).pack(pady=20)


def exit_app():
    root.destroy()




# UI




frame = ttk.LabelFrame(root, text="Instructors Present")
frame.pack(fill="x", padx=10, pady=5)




cols = 2
for idx, i in enumerate(ALL_INSTRUCTORS):
    var = tk.BooleanVar(value=True)
    present_vars[i['id']] = var


    ttk.Checkbutton(frame, text=i['name'], variable=var).grid(
         row=idx // cols, column=idx % cols, sticky="w", padx=10, pady=2
    )




progress_frame = ttk.Frame(root)
progress_frame.pack(fill="x", padx=10, pady=5)




ttk.Label(progress_frame, text="Drill lessons completed:").pack(side="left")


drill_progress_entry = ttk.Entry(progress_frame, width=5)
drill_progress_entry.insert(0, "0")
drill_progress_entry.pack(side="left", padx=10)


ttk.Label(progress_frame, text="Theory lessons completed:").pack(side="left")


theory_progress_entry = ttk.Entry(progress_frame, width=5)
theory_progress_entry.insert(0, "0")
theory_progress_entry.pack(side="left", padx=10)




btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)




ttk.Button(btn_frame, text="Generate Programme", command=generate).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame, text="View Lessons", command=view_lessons).grid(row=0, column=1, padx=5)
ttk.Button(btn_frame, text="View Instructors", command=view_instructors).grid(row=0, column=2, padx=5)
ttk.Button(btn_frame, text="Add Lesson", command=open_add_lesson_window).grid(row=0, column=3, padx=5)
ttk.Button(btn_frame, text="Add Instructor", command=open_add_instructor_window).grid(row=0, column=4, padx=5)
ttk.Button(btn_frame, text="Lesson Evaluation", command=lessonScore).grid(row=0, column=5, padx=5)
ttk.Button(btn_frame, text="Exit", command=exit_app).grid(row=0, column=6, padx=5)




root.mainloop()