import random
import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext
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


   except Exception as e:
       print("Error:", e)




# LESSON DATA




LESSONS = {
   "cadet": [
       {"id": "C001", "title": "Map Reading & Navigation"},
       {"id": "C002", "title": "First Aid"},
       {"id": "C003", "title": "Aircraft Recognition"},
       {"id": "C004", "title": "Drill"},
       {"id": "C005", "title": "Radio Communications"},
       {"id": "C006", "title": "Leadership Exercises"},
       {"id": "C007", "title": "Aerospace Technology"},
       {"id": "C008", "title": "Shooting Safety"},
       {"id": "C009", "title": "Teamwork & JNCO Development"},
       {"id": "C010", "title": "Cyber & STEM Challenge"},
   ],
   "recruit": [
       {"id": "R001", "title": "Attention & Stand At Ease", "type": "drill", "order": 1},
       {"id": "R002", "title": "Uniform & Turnout Standards", "type": "theory", "order": 2},
       {"id": "R003", "title": "Turning", "type": "drill", "order": 3},
       {"id": "R004", "title": "ATC Structure & Ranks", "type": "theory", "order": 4},
       {"id": "R005", "title": "Saluting", "type": "drill", "order": 5},
       {"id": "R006", "title": "Core Values & Code of Conduct", "type": "theory", "order": 6},
       {"id": "R007", "title": "Marching", "type": "drill", "order": 7},
       {"id": "R008", "title": "First Aid Basics", "type": "theory", "order": 8},
       {"id": "R009", "title": "Turning on the march", "type": "drill", "order": 9},
       {"id": "R010", "title": "Cadet Citizenship", "type": "theory", "order": 10},
       {"id": "R011", "title": "Drill mock", "type": "drill", "order": 11},
       {"id": "R012", "title": "Theory test mock", "type": "theory", "order": 12},
   ]
}




INSTRUCTORS = [
   {"id": "I001", "name": "Fg Off Smith", "rank": "Staff", "cadet": ["C001","C002","C005"], "recruit": ["R002","R004","R006"]},
   {"id": "I002", "name": "Sgt Johnson", "rank": "Staff", "cadet": ["C003","C004","C006"], "recruit": ["R001","R003","R005"]},
   {"id": "I003", "name": "FS Williams", "rank": "Staff", "cadet": ["C009","C010"], "recruit": ["R007","R008","R009","R010"]},
   {"id": "I004", "name": "Cpl Davies", "rank": "NCO", "cadet": ["C001","C004","C009"], "recruit": ["R001","R003","R005"]},
   {"id": "I005", "name": "Cpl Evans", "rank": "NCO", "cadet": ["C003","C007","C010"], "recruit": ["R002","R006","R010"]},
   {"id": "I006", "name": "Sgt Brown", "rank": "Staff", "cadet": ["C002","C005","C008"], "recruit": ["R004","R008","R011","R012"]},
   {"id": "I007", "name": "Cpl Harris", "rank": "NCO", "cadet": ["C006","C007","C008"], "recruit": ["R007","R009","R011"]},
   {"id": "I008", "name": "Fg Off Taylor", "rank": "Staff", "cadet": ["C001","C003","C005","C009"], "recruit": ["R002","R004","R008","R012"]},
]




# Designated recruit instructors


RECRUIT_INSTRUCTORS = [
   {"id": "RI001", "name": "Cpl Jackson", "rank": "NCO",
    "cadet": ["C002","C006","C008"],
    "recruit": ["R001","R002","R003","R004","R005","R006","R007","R008","R009","R010","R011","R012"]},


   {"id": "RI002", "name": "Cpl Turc", "rank": "NCO",
    "cadet": ["C003","C007","C010"],
    "recruit": ["R001","R002","R003","R004","R005","R006","R007","R008","R009","R010","R011","R012"]},
]


RECRUIT_PRIORITY_IDS = {i["id"] for i in RECRUIT_INSTRUCTORS}


# incase of no RECRUIT_INSTRUCTORS
ALL_INSTRUCTORS = INSTRUCTORS + RECRUIT_INSTRUCTORS




# GUI




root = tk.Tk()
root.title("Parade Night Programme Generator")
root.geometry("900x650")




output_box = scrolledtext.ScrolledText(root, width=100, height=25)
output_box.pack(fill="both", expand=True)




present_vars = {}




def show(text=""):
   output_box.insert(tk.END, str(text) + "\n")




def clear_output():
   output_box.delete("1.0", tk.END)




# MAIN




def generate():
   clear_output()


   show("=" * 60)
   show("PARADE NIGHT PROGRAMME")
   show("=" * 60)


   present_ids = [i for i, v in present_vars.items() if v.get()]
   present = [i for i in ALL_INSTRUCTORS if i["id"] in present_ids]


   if not present:
       show("ERROR: No instructors selected.")
       return


   try:
       last_drills_done = int(drill_progress_entry.get())
   except:
       last_drills_done = 0


   try:
       last_theory_done = int(theory_progress_entry.get())
   except:
       last_theory_done = 0


   used_instructors = set()


   # recruit


   recruit_sorted = sorted(LESSONS["recruit"], key=lambda x: x["order"])


   def pick_recruit_instructor(lesson):
       # Build the pool of present, qualified, not-yet-used instructors.
       qualified = [
           i for i in present
           if lesson["id"] in i["recruit"] and i["id"] not in used_instructors
       ]
       if not qualified:
           return None


       # Prefer the designated recruit instructors if any are in the pool.
       priority_qualified = [i for i in qualified if i["id"] in RECRUIT_PRIORITY_IDS]
       if priority_qualified:
           return random.choice(priority_qualified)


       # Fall back to anyone else who is present and qualified.
       return random.choice(qualified)


   def next_of_type(rtype, completed_count):
       type_lessons = [l for l in recruit_sorted if l["type"] == rtype]
       for index, l in enumerate(type_lessons):
           if index >= completed_count:
               instr = pick_recruit_instructor(l)
               if instr:
                   return l, instr
       return None, None


   r_drill, r_drill_instr = next_of_type("drill", last_drills_done)
   if r_drill_instr:
       used_instructors.add(r_drill_instr["id"])


   r_theory, r_theory_instr = next_of_type("theory", last_theory_done)
   if r_theory_instr:
       used_instructors.add(r_theory_instr["id"])


   # CADETS excludes anyone already used for a recruit lesson tonight.
   cadet_options = []
   for l in LESSONS["cadet"]:
       qualified = [
           i for i in present
           if l["id"] in i["cadet"] and i["id"] not in used_instructors
       ]
       if qualified:
           cadet_options.append((l, qualified))


   if len(cadet_options) < 2:
       show("Not enough cadet lessons available.")
       return


   random.shuffle(cadet_options)
   cadet_slots = []


   for lesson, qualified in cadet_options[:2]:
       # Reroll in case an instructor was used by the previous slot pick.
       qualified = [i for i in qualified if i["id"] not in used_instructors]
       if not qualified:
           continue
       instr = random.choice(qualified)
       cadet_slots.append((lesson, instr))
       used_instructors.add(instr["id"])


   if len(cadet_slots) < 2:
       show("Not enough cadet lessons available after avoiding double-booking.")
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




Recruits: {r_drill['title'] if r_drill else 'None'}
Instructor: {r_drill_instr['name'] if r_drill_instr else 'UNASSIGNED'}




20:30 LESSON 2
Cadets: {cadet_slots[1][0]['title']}
Instructor: {cadet_slots[1][1]['name']}




Recruits: {r_theory['title'] if r_theory else 'None'}
Instructor: {r_theory_instr['name'] if r_theory_instr else 'UNASSIGNED'}




21:45 End
"""


   send_to_discord(discord_message)




# VIEW




def view_lessons():
   clear_output()
   show("CADET LESSONS:\n")
   for l in LESSONS["cadet"]:
       show(f"{l['id']} - {l['title']}")


   show("\nRECRUIT LESSONS:\n")
   for l in sorted(LESSONS["recruit"], key=lambda x: x["order"]):
       show(f"{l['id']} [{l['order']}] {l['type']} - {l['title']}")




def view_instructors():
   clear_output()
   show("INSTRUCTORS:\n")
   for i in INSTRUCTORS:
       show(f"{i['id']} - {i['name']} ({i['rank']})")


   show("\nRECRUIT INSTRUCTORS (priority for recruit lessons):\n")
   for i in RECRUIT_INSTRUCTORS:
       show(f"{i['id']} - {i['name']} ({i['rank']})")




def exit_app():
   root.destroy()




# UI




frame = ttk.LabelFrame(root, text="Instructors Present")
frame.pack(fill="x", padx=10, pady=5)




cols = 2
for idx, i in enumerate(ALL_INSTRUCTORS):
   var = tk.BooleanVar(value=True)
   present_vars[i["id"]] = var


   ttk.Checkbutton(frame, text=i["name"], variable=var).grid(
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
ttk.Button(btn_frame, text="Exit", command=exit_app).grid(row=0, column=3, padx=5)




root.mainloop()