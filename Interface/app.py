import customtkinter

def button_callback():
    print("Clicked")

app = customtkinter.Ctk()
app.geometry("500*400")

button = customtkinter.CTkButton(app, text="my button", command=button_callback)
app.mainloop()