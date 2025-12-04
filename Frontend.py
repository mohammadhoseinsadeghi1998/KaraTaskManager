from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import Backend


def centerWindow(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f'{width}x{height}+{x}+{y}')


def messageBox(message, imageName):
    successBoxWindow = Toplevel()
    successBoxWindow.iconphoto(False,photoIcon)
    centerWindow(successBoxWindow, 450, 160)
    successBoxWindow.resizable(width=False, height=False)

    tick = Image.open(imageName)
    tick = tick.resize((40, 40))
    tick_icon = ImageTk.PhotoImage(tick)
    successBoxWindow.tick_icon = tick_icon

    content_frame = Frame(master=successBoxWindow)
    content_frame.place(relx=0.5, rely=0.4, anchor="center")

    img = Label(master=content_frame, image=tick_icon)
    img.pack(side="right", padx=(5, 10))

    text = Label(master=content_frame)
    text.configure(text=message, font=('b nazanin', 12), wraplength=350, justify="right")
    text.pack(side="right", padx=(20, 5))

    closeButton = Button(master=successBoxWindow)
    closeButton.config(width=10, text="بستن", command=successBoxWindow.destroy, font=('b nazanin', 12, 'bold'))
    closeButton.place(relx=0.5, rely=0.8, anchor="center")

    successBoxWindow.grab_set()


def personPage():
    addPersonPage = Toplevel()
    addPersonPage.iconphoto(False,photoIcon)
    addPersonPage.title("مدیریت نفرات")

    centerWindow(addPersonPage, 450, 230)
    addPersonPage.resizable(False, False)

    crudLable = Label(master=addPersonPage)
    crudLable.configure(text="نوع عملیات", font=('b nazanin', 12, 'bold'))
    crudLable.grid(row=1, column=2, pady=5, padx=5)

    personLable = Label(master=addPersonPage)
    personLable.configure(text="لیست نفرات", font=('b nazanin', 12, 'bold'))
    personLable.grid(row=2, column=2, pady=5, padx=5)

    firstnameLable = Label(master=addPersonPage)
    firstnameLable.configure(text="نام", font=('b nazanin', 12, 'bold'))
    firstnameLable.grid(row=3, column=2, pady=5, padx=5)

    lastnameLable = Label(master=addPersonPage)
    lastnameLable.configure(text="نام خانوادگی", font=('b nazanin', 12, 'bold'))
    lastnameLable.grid(row=4, column=2, pady=5, padx=5)

    crudEntry = ttk.Combobox(master=addPersonPage)
    crudEntry.configure(width=38, font=('b nazanin', 12), justify="right")
    crudEntry['values'] = ["افزودن","ویرایش","حذف"]
    crudEntry.grid(row=1, column=1)

    personListEntry = ttk.Combobox(master=addPersonPage)
    personListEntry.configure(width=38, font=('b nazanin', 12), justify="right", state="readonly")
    personListEntry['values'] = fillPerson()
    personListEntry.grid(row=2, column=1)

    firstnameText = StringVar()
    firstnameEntry = Entry(master=addPersonPage, textvariable=firstnameText)
    firstnameEntry.configure(width=40, font=('b nazanin', 12), justify="right")
    firstnameEntry.grid(row=3, column=1, pady=5, padx=5)

    lastnameText = StringVar()
    lastnameEntry = Entry(master=addPersonPage, textvariable=lastnameText)
    lastnameEntry.configure(width=40, font=('b nazanin', 12,), justify="right")
    lastnameEntry.grid(row=4, column=1, pady=5, padx=5)

    def updateFields(event=None):
        if crudEntry.get() == "حذف":
            firstnameEntry.configure(state="readonly")
            lastnameEntry.configure(state="readonly")
            personListEntry.configure(state="readonly")
        elif crudEntry.get() == "افزودن":
            firstnameEntry.configure(state="normal")
            lastnameEntry.configure(state="normal")
            personListEntry.configure(state="disabled")
            personListEntry.set("")
        elif crudEntry.get() == "ویرایش":
            firstnameEntry.configure(state="normal")
            lastnameEntry.configure(state="normal")
            personListEntry.configure(state="readonly")

    crudEntry.bind("<<ComboboxSelected>>", updateFields)

    def crudExecute():
        if crudEntry.get() == "حذف":
            if len(personListEntry.get()) == 0:
                messageBox("لطفا یک فرد را انتخاب نمایید", "cross.png")
            else:
                Backend.deletePerson(personListEntry.get())
                messageBox(f"کاربر با نام {personListEntry.get()} با موفقیت حذف شد", "check.png")
                addPersonPage.destroy()
                assigneTaskEntry['values'] = fillPerson()

        elif crudEntry.get() == "افزودن":
            if len(firstnameText.get()) == 0 or len(lastnameText.get()) == 0:
                messageBox("نام و نام خانوادگی نمی تواند خالی باشد", "cross.png")
            elif len(Backend.duplicatePerson(f"{firstnameText.get()} {lastnameText.get()}")) != 0:
                messageBox(f"کاربر با نام {firstnameText.get()} {lastnameText.get()} قبلا اضافه گردیده است",
                           "cross.png")
            else:
                Backend.insertPerson(firstnameText.get(), lastnameText.get())
                assigneTaskEntry['values'] = fillPerson()
                messageBox(f"کاربر با نام {firstnameText.get()} {lastnameText.get()} با موفقیت اضافه گردیده است",
                           "check.png")
                addPersonPage.destroy()

        elif crudEntry.get() == "ویرایش":
            if len(personListEntry.get()) == 0:
                messageBox("لطفا نام یک کاربر را انتخاب نمایید", "cross.png")
            elif len(firstnameEntry.get()) == 0 and len(lastnameEntry.get()) == 0:
                messageBox("نام و نام خانوادگی نمی تواند خالی باشد", "cross.png")
            else:
                Backend.editPerson(personListEntry.get(),
                                   firstnameEntry.get() or personListEntry.get().split(' ')[0],
                                   lastnameEntry.get() or personListEntry.get().split(' ')[1])
                assigneTaskEntry['values'] = fillPerson()
                messageBox("کاربر با موفقیت ویرایش شد", "check.png")
                addPersonPage.destroy()

    addButton = Button(master=addPersonPage, command=crudExecute)
    addButton.configure(width=29, text="انجام", font=('b nazanin', 12, 'bold'))
    addButton.grid(row=5, column=1, pady=5, padx=5)

    addPersonPage.grab_set()


def addTask():
    if len(summaryTextVariable.get()) == 0 or len(assigneeTextVariable.get()) == 0 or len(dueTextVariable.get()) == 0:
        messageBox("مقادیر توضیحات، مسئول و تاریخ سررسید نمی تواند خالی باشد", "cross.png")
    else:
        Backend.insertTask(summaryTextVariable.get(),
                           assigneeTextVariable.get(),
                           "برای انجام",
                           dueTextVariable.get())
        clearTask()
        fillTask()
        summaryTaskEntry.delete(0, "end")
        assigneTaskEntry.set("")
        dueTaskEntry.delete(0, "end")
        messageBox("تسک جدید با موفقیت اضافه شد", "check.png")


def deleteTask():
    selectedItem = taskTable.selection()
    if not selectedItem:
        messageBox("هیچ ردیفی انتخاب نشده است", "cross.png")

    for item in selectedItem:
        itemData = taskTable.item(item)
        selectedValues = itemData['values'][::-1]
    print()
    Backend.deleteTask(selectedValues[1], selectedValues[3])
    clearTask()
    fillTask()
    messageBox(f'تسک {selectedValues[1]} با موفقیت حذف شد', "check.png")


def updatePage():
    selectedItem = taskTable.selection()

    if not selectedItem:
        messageBox("هیچ ردیفی انتخاب نشده است", "cross.png")
    else:
        for item in selectedItem:
            itemData = taskTable.item(item)
            selectedValues = itemData['values'][::-1]

        updatePage = Toplevel()
        updatePage.iconphoto(False,photoIcon)
        updatePage.title("ویرایش تسک")
        centerWindow(updatePage, 405, 210)
        updatePage.resizable(False, False)

        taskNameLable = Label(master=updatePage)
        taskNameLable.config(text=": توضیحات", font=('b nazanin', 12, 'bold'))
        taskNameLable.grid(row=1, column=2)

        taskNameEntry = Entry(master=updatePage)
        taskNameEntry.config(width=40, font=('b nazanin', 12), justify="right")
        taskNameEntry.grid(row=1, column=1, pady=5, padx=5)

        assigneeLable = Label(master=updatePage)
        assigneeLable.config(text=": مسئول", font=('b nazanin', 12, 'bold'))
        assigneeLable.grid(row=2, column=2)

        assigneeEntry = ttk.Combobox(master=updatePage)
        assigneeEntry.config(width=38, font=('b nazanin', 12), justify="right")
        assigneeEntry['values'] = fillPerson()
        assigneeEntry.grid(row=2, column=1, pady=5, padx=5)

        statusLable = Label(master=updatePage)
        statusLable.config(text=": وضعیت", font=('b nazanin', 12, 'bold'))
        statusLable.grid(row=3, column=2)

        statusEntry = ttk.Combobox(master=updatePage)
        statusEntry['values'] = ["برای انجام", "در حال انجام", "متوقف شده", "انجام شده"]
        statusEntry.config(width=38, font=('b nazanin', 12), justify="right", state="readonly")
        statusEntry.grid(row=3, column=1, pady=5, padx=5)

        dueLable = Label(master=updatePage)
        dueLable.config(text=": سررسید", font=('b nazanin', 12, 'bold'))
        dueLable.grid(row=4, column=2)

        dueEntry = Entry(master=updatePage)
        dueEntry.config(width=40, font=('b nazanin', 12), justify="right")
        dueEntry.grid(row=4, column=1, pady=5, padx=5)

        def updateSelectedTask():
            if len(taskNameEntry.get()) == 0 and len(assigneeEntry.get()) == 0 and len(statusEntry.get()) == 0 and len(
                    dueEntry.get()) == 0:
                messageBox("مقادیر توضیحات، مسئول و تاریخ سررسید نمی تواند خالی باشد", "cross.png")

            else:
                Backend.updateTask(selectedValues[1], selectedValues[3],
                                   taskNameEntry.get() or selectedValues[1],
                                   assigneeEntry.get() or selectedValues[3],
                                   statusEntry.get() or selectedValues[4],
                                   dueEntry.get() or selectedValues[5])
                clearTask()
                fillTask()
                updatePage.destroy()
                messageBox("بروزرسانی با موفقیت انجام شد", "check.png")

        closePage = Button(master=updatePage)
        closePage.config(text="بستن", command=updatePage.destroy, font=('b nazanin', 12, 'bold'), width=10)
        closePage.place(x=40, y=155)

        updateTask = Button(master=updatePage)
        updateTask.config(text="بروزرسانی", command=updateSelectedTask, font=('b nazanin', 12, 'bold'), width=10)
        updateTask.place(x=170, y=155)


def clearTask():
    for task in taskTable.get_children():
        taskTable.delete(task)


def fillTask():
    tasks = Backend.viewTask()
    rowNumber = 1
    for task in tasks:
        values = task + (rowNumber,)
        taskTable.insert("", "end", values=values)
        rowNumber += 1


def fillPerson():
    list = []
    person = Backend.viewPerson()
    for p in person:
        list.append(f"{p[1]} {p[2]}")
    return list


def exportToExcel():
    Backend.exportToExcel()
    messageBox("خروجی با موفقیت ذخیره شد", "check.png")


mainWindow = Tk()
centerWindow(mainWindow, 780, 460)
mainWindow.resizable(False, False)
mainWindow.title("کارا")
photoIcon = PhotoImage(file='clipboard.png')
mainWindow.iconphoto(False,photoIcon)

style = ttk.Style()
style.configure("Treeview", font=('B Nazanin', 11), rowheight=40)
style.configure("Treeview.Heading", font=('B Nazanin', 12, 'bold'))

mainWindow.option_add('*TCombobox*Listbox.font', ('B Nazanin', 11))
mainWindow.option_add('*TCombobox*Listbox.justify', 'right')

# ================================= TextVariable =================================
summaryTextVariable = StringVar()
assigneeTextVariable = StringVar()
dueTextVariable = StringVar()

# ================================= Widgets =================================
# =========== Label ===========
summaryLable = Label(master=mainWindow)
dueTaskLable = Label(master=mainWindow)
assigneLable = Label(master=mainWindow)

# =========== Entry ===========
summaryTaskEntry = Entry(master=mainWindow, textvariable=summaryTextVariable)

assigneTaskEntry = ttk.Combobox(master=mainWindow, textvariable=assigneeTextVariable)
assigneTaskEntry['values'] = fillPerson()

dueTaskEntry = Entry(master=mainWindow, textvariable=dueTextVariable)

# =========== Button ===========
addTaskButton = Button(master=mainWindow)
addPersonButton = Button(master=mainWindow)
updateButton = Button(master=mainWindow)
deleteButton = Button(master=mainWindow)
exportButton = Button(master=mainWindow)

# =========== Table ===========
taskTable = ttk.Treeview(master=mainWindow)
yScrollBar = Scrollbar(master=mainWindow)
yScrollBar.config(command=taskTable.yview)
taskTable.config(columns=("Due", "Status", "Assignee", "CreatedDate", "TaskName", "ID"),
                 show="headings",
                 height=5,
                 yscrollcommand=yScrollBar.set)

taskTable.heading("ID", text="ردیف")
taskTable.column("ID", anchor="center", width=50)

taskTable.heading("TaskName", text="توضیحات")
taskTable.column("TaskName", anchor="e", width=300)

taskTable.heading("CreatedDate", text="زمان ایجاد")
taskTable.column("CreatedDate", anchor="center", width=100)

taskTable.heading("Assignee", text="مسئول")
taskTable.column("Assignee", anchor="center", width=120)

taskTable.heading("Status", text="وضعیت")
taskTable.column("Status", anchor="center", width=80)

taskTable.heading("Due", text="زمان سررسید")
taskTable.column("Due", anchor="center", width=100)

# ================================= Config =================================
# =========== Label ===========
summaryLable.configure(text=": توضیحات",
                       font=('b nazanin', 12, 'bold'))

assigneLable.configure(text=": مسئول",
                       font=('b nazanin', 12, 'bold'))

dueTaskLable.configure(text=": تاریخ سررسید",
                       font=('b nazanin', 12, 'bold'))

# =========== Entry ===========
summaryTaskEntry.config(width=40,
                        font=('b nazanin', 12),
                        justify="right")

assigneTaskEntry.config(width=38,
                        font=('b nazanin', 12),
                        justify="right",
                        state="readonly")

dueTaskEntry.config(width=40,
                    font=('b nazanin', 12),
                    justify="right")

# =========== Button ===========
addTaskButton.config(width=15,
                     text="افزودن تسک",
                     font=('b nazanin', 12, 'bold'),
                     command=addTask)

addPersonButton.config(width=15,
                       text="مدیریت نفرات",
                       font=('b nazanin', 12, 'bold'),
                       command=personPage)

updateButton.config(width=15,
                    text="آپدیت تسک",
                    font=('b nazanin', 12, 'bold'),
                    command=updatePage)

deleteButton.config(width=15,
                    text="حذف تسک",
                    font=('b nazanin', 12, 'bold'),
                    command=deleteTask)

exportButton.config(width=15,
                    text="دریافت خروجی",
                    font=('b nazanin', 12, 'bold'),
                    command=exportToExcel)

# ================================= Grid =================================
# =========== Label ===========
summaryLable.grid(row=1, column=3, pady=5, padx=5, sticky="w")
dueTaskLable.grid(row=3, column=3, pady=5, padx=5, sticky="w")
assigneLable.grid(row=2, column=3, pady=5, padx=5, sticky="w")

# =========== Entry ===========
summaryTaskEntry.grid(row=1, column=2, pady=5, padx=5, sticky="e")
assigneTaskEntry.grid(row=2, column=2, pady=5, padx=5, sticky="e")
dueTaskEntry.grid(row=3, column=2, pady=5, padx=5, sticky="e")

# =========== Button ===========
addPersonButton.grid(row=2, column=1, pady=5, padx=5)
addTaskButton.grid(row=3, column=1, pady=5, padx=5)
updateButton.place(x=390, y=400)
deleteButton.place(x=580, y=400)
exportButton.place(x=20, y=400)

# =========== Table ===========
taskTable.grid(row=4, column=1, columnspan=3, padx=5, pady=5)
yScrollBar.place(x=757, y=160, height=228)
fillTask()

mainWindow.mainloop()
