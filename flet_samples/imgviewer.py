import flet as ft


def main(page: ft.Page):
    
    viewer = ft.InteractiveViewer(
            min_scale=0.1,
            max_scale=15,
            boundary_margin=ft.margin.all(20),
            content=ft.Image(
                src="https://picsum.photos/500/500",
            ),
        )
    
    def clear(e):
        viewer.visible= False
        viewer.content = None
        
        page.add(ft.Text("Cleared"))
        page.update()

    
    page.add(
        viewer,
        ft.ElevatedButton(
            text="Reset",
            on_click=clear,
            
        ),
        
    )
    

ft.app(main)