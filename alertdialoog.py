from flet import Page, Text, TextField, ElevatedButton, Column, colors

def main(page: Page):
    # Username and password fields
    username_field = TextField(label="Username")
    password_field = TextField(label="Password", password=True)

    # Error message (initially hidden)
    error_message = Text(
        "",
        color=colors.RED,
        visible=False,  # Start with the message hidden
    )

    # Function to handle login
    def handle_login(e):
        username = username_field.value
        password = password_field.value

        # Simulated validation (replace with your actual logic)
        if username != "admin" or password != "1234":
            error_message.value = "Invalid username or password!"
            error_message.visible = True
        else:
            error_message.value = ""
            error_message.visible = False
            page.snack_bar.content.value = "Login successful!"
            page.snack_bar.open = True
            page.update()
        
        # Update the UI
        page.update()

    # Login button
    login_button = ElevatedButton(text="Login", on_click=handle_login)

    # Add widgets to the page
    page.add(
        Column([
            username_field,
            password_field,
            error_message,  # Show error message here
            login_button,
        ])
    )

# Run the app
if __name__ == "__main__":
    import flet as ft
    ft.app(target=main)
