import customtkinter

def button_callback():
    print("Clicked")

app = customtkinter.CTk()
app.geometry("900*900")

button = customtkinter.CTkButton(app, text="my button", command=button_callback)

app.mainloop()