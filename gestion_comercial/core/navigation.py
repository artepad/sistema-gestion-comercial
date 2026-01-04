import tkinter as tk

class Navigator:
    def __init__(self, container):
        self.container = container
        self.views = {}
        self.current_view = None
    
    def register_view(self, name, view_class):
        """Registers a view class with a name."""
        self.views[name] = view_class
        
    def show_view(self, name, **kwargs):
        """Switches to the specified view."""
        if name not in self.views:
            raise ValueError(f"View '{name}' not registered.")
            
        # Destroy current view if it exists
        if self.current_view:
            self.current_view.destroy()
            
        # Create and show new view
        view_class = self.views[name]
        self.current_view = view_class(self.container, self, **kwargs)
        self.current_view.pack(fill='both', expand=True)
