lessonsCadets= []
with open ("lessonsCadets.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip().split(",")
        mydict = {"id":(line[0]),
                  "title":(line[1]),}
        lessonsCadets.append(mydict)

print (lessonsCadets)

lessonsRecruits= []
with open ("lessonsRecruits.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip().split(",")
        mydict = {"id":(line[0]),
                  "title":(line[1]),
                  "type":(line[2]),
                  "order":int(line[3]),}
        lessonsRecruits.append(mydict)

print (lessonsRecruits)

LESSONS = {"cadet": lessonsCadets,
           "recruit": lessonsRecruits}

print (LESSONS)

INSTRUCTORS= []
with open ("instructors.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip().split(",")
        mydict = {"id":(line[0]),
                  "name":(line[1]),
                  "rank":(line[2]),
                  "cadet":[line[3],line[4],line[5]],
                  "recruit":[line[6],line[7],line[8]],}
        INSTRUCTORS.append(mydict)

print (INSTRUCTORS)

RECRUIT_INSTRUCTORS= []
with open ("recruitInstructors.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip().split(",")
        mydict = {"id":(line[0]),
                  "name":(line[1]),
                  "rank":(line[2]),
                  "cadet":[line[3],line[4],line[5]],
                  "recruit":[line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17]],}
        RECRUIT_INSTRUCTORS.append(mydict)

print (RECRUIT_INSTRUCTORS)

import tkinter as tk
from tkinter import ttk, messagebox

INSTRUCTORS = []  # pretend this is already loaded from instructors.txt


def save_instructor_to_file(instr):
	# Rebuild one comma-separated line matching instructors.txt's format:
	# id,name,rank,cadet1,cadet2,...,recruit1,recruit2,...
	fields = [instr["id"], instr["name"], instr["rank"]] + instr["cadet"] + instr["recruit"]
	line = ",".join(fields)
	with open("instructors.txt", "a", encoding="utf-8") as file:
		file.write(line + "\n")


def open_add_instructor_window():
	# Toplevel = a new pop-up window on top of the main one.
	# This is how Tkinter does "another page" without a separate app.
	window = tk.Toplevel(root)
	window.title("Add Instructor")
	window.geometry("350x350")

	ttk.Label(window, text="ID (e.g. I009):").pack(pady=(10, 0))
	id_entry = ttk.Entry(window)
	id_entry.pack()

	ttk.Label(window, text="Name:").pack(pady=(10, 0))
	name_entry = ttk.Entry(window)
	name_entry.pack()

	ttk.Label(window, text="Rank:").pack(pady=(10, 0))
	rank_entry = ttk.Entry(window)
	rank_entry.pack()

	ttk.Label(window, text="Cadet lessons (comma separated, e.g. C001,C002):").pack(pady=(10, 0))
	cadet_entry = ttk.Entry(window)
	cadet_entry.pack()

	ttk.Label(window, text="Recruit lessons (comma separated, e.g. R001,R002):").pack(pady=(10, 0))
	recruit_entry = ttk.Entry(window)
	recruit_entry.pack()

	def submit():
		new_id = id_entry.get().strip()
		new_name = name_entry.get().strip()
		new_rank = rank_entry.get().strip()
		new_cadet = [c.strip() for c in cadet_entry.get().split(",") if c.strip()]
		new_recruit = [r.strip() for r in recruit_entry.get().split(",") if r.strip()]

		if not new_id or not new_name or not new_rank:
			messagebox.showerror("Missing info", "ID, Name, and Rank are required.")
			return

		new_instructor = {
			"id": new_id,
			"name": new_name,
			"rank": new_rank,
			"cadet": new_cadet,
			"recruit": new_recruit,
		}

		INSTRUCTORS.append(new_instructor)
		save_instructor_to_file(new_instructor)

		# Add a live checkbox for this instructor immediately, without
		# needing to restart the program.
		var = tk.BooleanVar(value=True)
		present_vars[new_instructor["id"]] = var
		idx = len(present_vars) - 1
		cols = 2
		ttk.Checkbutton(frame, text=new_instructor["name"], variable=var).grid(
			row=idx // cols, column=idx % cols, sticky="w", padx=10, pady=2
		)

		messagebox.showinfo("Added", f"{new_name} added successfully.")
		window.destroy()

	ttk.Button(window, text="Add Instructor", command=submit).pack(pady=20)


# --- demo main window ---
root = tk.Tk()
root.title("Demo")
ttk.Button(root, text="Add Instructor", command=open_add_instructor_window).pack(pady=50)
root.mainloop()