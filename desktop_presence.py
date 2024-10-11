import os
import tkinter as tk
from PIL import Image, ImageTk
from cai import Cai

ROOT_DIR: str = os.path.abspath(os.path.dirname(__file__))


class AnimatedGIF:
    def __init__(self, label, path, delay=100):
        """
        Initialize the AnimatedGIF object.

        :param label: The tkinter label widget to display the GIF.
        :param path: Path to the GIF file.
        :param delay: Delay between frames in milliseconds.
        """
        self.label = label
        self.path = path
        self.delay = delay
        self.frames = []
        self.current_frame = 0
        self.load_frames()
        self.running = False

    def load_frames(self):
        """Load all frames of the GIF into a list."""
        if not os.path.exists(self.path):
            print(f"Error: {self.path} does not exist.")
            return

        try:
            img = Image.open(self.path)
            for frame in range(0, img.n_frames):
                img.seek(frame)
                frame_image = ImageTk.PhotoImage(img.copy().convert('RGBA'))
                self.frames.append(frame_image)
        except Exception as e:
            print(f"Error loading GIF {self.path}: {e}")

    def start_animation(self):
        """Start the GIF animation."""
        if not self.frames:
            return
        self.running = True
        self.animate()

    def animate(self):
        """Update the label with the next frame."""
        if not self.running:
            return
        frame = self.frames[self.current_frame]
        self.label.config(image=frame)
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.label.after(self.delay, self.animate)

    def stop_animation(self):
        """Stop the GIF animation."""
        self.running = False


class DesktopPet:
    def __init__(self, root, cai):
        """
        Initialize the DesktopPet.

        :param root: The tkinter root window.
        :param cai: An instance of the Cai class.
        """
        self.root = root
        self.cai = cai
        self.root.title("Desktop Pet")
        self.root.geometry("300x300")  # Adjusted size for better visibility
        self.root.resizable(False, False)

        # Remove window decorations (optional)
        self.root.overrideredirect(True)

        # Set window to stay on top
        self.root.attributes("-topmost", True)

        # Initialize mode
        self.mode = "loading"
        self.loading_complete = False  # Flag to indicate if loading is done

        # Create a label to display the GIF
        self.label = tk.Label(root, bg="white")
        self.label.pack(expand=True, fill="both")

        # Initialize AnimatedGIF objects for each mode
        gif_folder: str = os.path.join(ROOT_DIR, "gifs")
        delay: int = 75
        self.animations = {
            "loading": AnimatedGIF(self.label, os.path.join(gif_folder, "loading.gif"), delay=delay),
            "idle": AnimatedGIF(self.label, os.path.join(gif_folder, "idle.gif"), delay=delay),
            "talking": AnimatedGIF(self.label, os.path.join(gif_folder, "talking.gif"), delay=delay)
        }

        # Start the loading sequence
        self.start_loading()

        # Handle window dragging
        self.label.bind("<ButtonPress-1>", self.start_move)
        self.label.bind("<ButtonRelease-1>", self.stop_move)
        self.label.bind("<B1-Motion>", self.do_move)
        self._offsetx = 0
        self._offsety = 0

        # Start polling Cai's state
        self.poll_cai_state()

    def start_move(self, event):
        """Record the initial position for window dragging."""
        self._offsetx = event.x
        self._offsety = event.y

    def stop_move(self, event):
        """Stop window dragging."""
        self._offsetx = None
        self._offsety = None

    def do_move(self, event):
        """Move the window based on mouse movement."""
        x = self.root.winfo_pointerx() - self._offsetx
        y = self.root.winfo_pointery() - self._offsety
        self.root.geometry(f'+{x}+{y}')

    def start_loading(self):
        """Start the loading mode."""
        self.mode = "loading"
        self.update_pet()

    def switch_to_idle(self):
        """Switch the pet to idle mode."""
        self.mode = "idle"
        self.update_pet()

    def switch_to_talking(self):
        """Switch the pet to talking mode."""
        self.mode = "talking"
        self.update_pet()

    def update_pet(self):
        """Update the pet's appearance based on the current mode."""
        # Stop all animations
        for anim in self.animations.values():
            anim.stop_animation()

        # Start the animation for the current mode
        current_anim = self.animations.get(self.mode)
        if current_anim:
            current_anim.start_animation()

    def poll_cai_state(self):
        """Poll the Cai object's state and update the mode accordingly."""
        if not self.loading_complete:
            if self.cai.is_making_sound():
                # Loading complete
                self.loading_complete = True
                self.mode = "talking"
                self.update_pet()
        else:
            # After loading, switch between idle and talking
            if self.cai.is_making_sound():
                if self.mode != "talking":
                    self.switch_to_talking()
            else:
                if self.mode != "idle":
                    self.switch_to_idle()

        # Schedule the next poll
        self.root.after(500, self.poll_cai_state)  # Poll every 500ms


def run(cai: Cai):
    # Initialize tkinter root
    root = tk.Tk()

    DesktopPet(root, cai)
    root.mainloop()
