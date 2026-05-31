import tkinter as tk #For interactive GUI
from tkinter import messagebox #For Pop Up Message
import google.generativeai as genai #For Use of gemini ai
#PLATYPUS = Page Layout And Typography Using Scripts
from reportlab.platypus import Paragraph, Spacer, SimpleDocTemplate 
#reportlab = A Python Library used to create PDF Files
from reportlab.lib.styles import getSampleStyleSheet

#Gemini Set Up
genai.configure(api_key="YOUR_API_KEY")
model=genai.GenerativeModel("gemini-2.5-flash")

#Generate Resume Function
def generate_resume():
    prompt=f"""
Create an ATS-Friendly and Professional Resume

Name: {entry_name.get()}

Email: {entry_email.get()}

Phone: {entry_phone.get()}

LinkedIn: {entry_linkedin.get()}

Education:
{txt_education.get("1.0",tk.END)}

Skills:
{txt_skills.get("1.0",tk.END)}

Projects:
{txt_projects.get("1.0",tk.END)}

Target Role:{entry_role.get()}

IMPORTANT:
Output ONLY the Resume

USE EXACTLY THESE HEADINGS ONLY:

PROFESSIONAL SUMMARY

PROJECTS

SKILLS

EDUCATION

No Markdowns.
No Tips.
No Explanations.
"""

    try:
        response=model.generate_content(prompt)

        output.delete("1.0",tk.END)
        output.insert(tk.END,response.text)

    except Exception as e:
        messagebox.showerror("Error",str(e))

def save_pdf():

    text=output.get("1.0",tk.END)

    if not text.strip():
        messagebox.showerror("Error","Generate Resume First")
        return
    
    pdf=SimpleDocTemplate("resume.pdf")
    styles=getSampleStyleSheet()
    headings=[
        "PROFESSIONAL SUMMARY",
        "PROJECTS",
        "SKILLS",
        "EDUCATION"
        ]
    content=[]

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        if line.upper() in headings:

            content.append(
                Paragraph(
                    f"<b>{line}</b>",
                    styles["Heading2"]
                )
            )

        else:

            content.append(
                Paragraph(
                    line,
                    styles["BodyText"]
                )
            )

        content.append(Spacer(1, 2))

    pdf.build(content)

    messagebox.showinfo(
        "Success",
        "resume.pdf saved successfully"
    )

#Main Window

root=tk.Tk()
root.title("Resume Builder")
root.geometry("900x700")

#Inputs 

#Name
tk.Label(root, text="Name").pack()
entry_name=tk.Entry(root, width=50)
entry_name.pack()

#Email
tk.Label(root, text="Email").pack()
entry_email=tk.Entry(root, width=50)
entry_email.pack()

#Phone
tk.Label(root, text="Phone").pack()
entry_phone=tk.Entry(root, width=50)
entry_phone.pack()

#LinkedIn
tk.Label(root, text="LinkedIn").pack()
entry_linkedin=tk.Entry(root, width=50)
entry_linkedin.pack()

#Education
tk.Label(root, text="Education").pack()
txt_education=tk.Text(root, height=3, width=60)
txt_education.pack()

#Skils
tk.Label(root, text="Skils").pack()
txt_skills=tk.Text(root, height=3, width=60)
txt_skills.pack()

#Projects
tk.Label(root, text="Projects").pack()
txt_projects=tk.Text(root, height=3, width=60)
txt_projects.pack()

#Role
tk.Label(root, text="Role").pack()
entry_role=tk.Entry(root, width=50)
entry_role.pack()

# Button Frame
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Generate Resume",
    command=generate_resume
).pack(side="left", padx=10)

tk.Button(
    button_frame,
    text="Save PDF",
    command=save_pdf
).pack(side="left", padx=10)

# Output Box

frame=tk.Frame(root)
frame.pack(fill="both", expand=True)

scroll=tk.Scrollbar(frame)

output=tk.Text(frame, wrap="word", yscrollcommand=scroll.set)

scroll.config(command=output.yview)
scroll.pack(side="right", fill="y")
output.pack(fill="both", expand=True)

root.mainloop()