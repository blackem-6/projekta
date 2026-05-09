import customtkinter as ctk
import tkinter as tk
from datetime import datetime
import random
import time
import math


# ─── Online209 HUD Color Scheme (unique dark-blue / cyan theme) ───
C = {
    "bg": "#0b0e14",
    "panel_bg": "#11151c",
    "panel_border": "#1e2a3a",
    "accent": "#00d4ff",
    "accent2": "#7b5cff",
    "accent3": "#ff5c8a",
    "green": "#3ddc84",
    "red": "#ff4757",
    "orange": "#ffb347",
    "yellow": "#ffd93d",
    "text": "#e8edf3",
    "text_dim": "#6b7b8d",
    "text_muted": "#3a4a5c",
    "separator": "#1a2435",
    "notif_bg": "#151b27",
    "bar_bg": "#0d1219",
    "highlight": "#1a3050",
}


class HUDPanel(ctk.CTkFrame):
    """Floating HUD panel with header."""

    def __init__(self, master, title, icon="", width=220, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            fg_color=("#11151c", "#11151c"),
            corner_radius=6,
            border_width=1,
            border_color=C["panel_border"],
            width=width,
        )

        header = ctk.CTkFrame(self, fg_color=("#151c28", "#151c28"), corner_radius=0, height=30)
        header.pack(fill="x", padx=1, pady=(1, 0))
        header.pack_propagate(False)

        dot = ctk.CTkFrame(header, width=6, height=6, corner_radius=3, fg_color=C["accent"])
        dot.pack(side="left", padx=(10, 6), pady=0)

        ctk.CTkLabel(
            header,
            text=f"{icon} {title}".strip(),
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=C["text"],
        ).pack(side="left", padx=2)

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=8, pady=(6, 8))


class NotificationItem(ctk.CTkFrame):
    """Module toggle notification (center-bottom popups)."""

    def __init__(self, master, icon, text, enabled=True, **kwargs):
        super().__init__(master, **kwargs)
        color = C["green"] if enabled else C["red"]
        self.configure(
            fg_color=C["notif_bg"],
            corner_radius=6,
            border_width=1,
            border_color=color,
        )

        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(padx=12, pady=6)

        ctk.CTkLabel(
            inner,
            text=icon,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=color,
            width=20,
        ).pack(side="left", padx=(0, 6))

        ctk.CTkLabel(
            inner,
            text=text,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=C["text"],
        ).pack(side="left")


class KeybindRow(ctk.CTkFrame):
    """Single keybind entry row."""

    def __init__(self, master, icon, module_name, key, color=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent", height=22)

        if color is None:
            color = C["accent"]

        ctk.CTkLabel(
            self,
            text=icon,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=color,
            width=16,
        ).pack(side="left", padx=(0, 6))

        ctk.CTkLabel(
            self,
            text=module_name,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=C["text"],
        ).pack(side="left", fill="x", expand=True)

        key_frame = ctk.CTkFrame(
            self,
            fg_color=C["highlight"],
            corner_radius=4,
            border_width=1,
            border_color=C["panel_border"],
        )
        key_frame.pack(side="right")

        ctk.CTkLabel(
            key_frame,
            text=key,
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=C["text_dim"],
            width=28,
        ).pack(padx=4, pady=1)


class PlayerRow(ctk.CTkFrame):
    """Player list row with role and ping."""

    def __init__(self, master, name, role, ping, role_color=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent", height=22)

        if role_color is None:
            role_color = C["text_dim"]

        ctk.CTkLabel(
            self,
            text=name,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=C["text"],
        ).pack(side="left")

        ctk.CTkLabel(
            self,
            text=role,
            font=ctk.CTkFont(size=10),
            text_color=role_color,
        ).pack(side="left", padx=(6, 0))

        ctk.CTkLabel(
            self,
            text=f"{ping}ms",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=C["text_dim"],
        ).pack(side="right")


class EventRow(ctk.CTkFrame):
    """Event timer row."""

    def __init__(self, master, icon_color, event_name, event_id, time_str, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent", height=22)

        dot = ctk.CTkFrame(self, width=8, height=8, corner_radius=4, fg_color=icon_color)
        dot.pack(side="left", padx=(0, 8), pady=7)

        ctk.CTkLabel(
            self,
            text=event_name,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=C["text"],
        ).pack(side="left")

        ctk.CTkLabel(
            self,
            text=str(event_id),
            font=ctk.CTkFont(size=10),
            text_color=C["text_muted"],
        ).pack(side="left", padx=(4, 0))

        ctk.CTkLabel(
            self,
            text=time_str,
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=C["accent"],
        ).pack(side="right")


class ModuleListItem(ctk.CTkFrame):
    """Active module in the module list."""

    def __init__(self, master, name, category_color, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent", height=20)

        bar = ctk.CTkFrame(self, width=3, height=14, corner_radius=1, fg_color=category_color)
        bar.pack(side="left", padx=(0, 8), pady=3)

        ctk.CTkLabel(
            self,
            text=name,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=C["text"],
        ).pack(side="left")


class Online209HUD(ctk.CTk):
    """Main HUD-style overlay window for Online209 client."""

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")

        self.title("Online209 - HUD Preview")
        self.geometry("1100x720")
        self.minsize(1000, 650)
        self.configure(fg_color=C["bg"])

        self._build_top_bar()
        self._build_keybinds_panel()
        self._build_active_modules_panel()
        self._build_server_panel()
        self._build_players_panel()
        self._build_online_panel()
        self._build_events_panel()
        self._build_notifications()
        self._build_bottom_bar()
        self._build_watermark()

        self._start_clock()

    # ─── Top Bar ────────────────────────────────────────

    def _build_top_bar(self):
        bar = ctk.CTkFrame(self, fg_color=C["bar_bg"], corner_radius=0, height=32)
        bar.pack(fill="x", side="top")
        bar.pack_propagate(False)

        left = ctk.CTkFrame(bar, fg_color="transparent")
        left.pack(side="left", padx=12)

        # Client branding
        ctk.CTkLabel(
            left,
            text="\u26a1",
            font=ctk.CTkFont(size=14),
            text_color=C["accent"],
        ).pack(side="left", padx=(0, 4))

        ctk.CTkLabel(
            left,
            text="Online209",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=C["accent"],
        ).pack(side="left", padx=(0, 16))

        # Player info
        self._stat_pill(left, "\u25cf", "Player209", C["green"])
        self._stat_pill(left, "\u2588", "165 fps", C["text_dim"])
        self._stat_pill(left, "\u2588", "23ms", C["green"])

        # Center - server info
        center = ctk.CTkFrame(bar, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")

        server_frame = ctk.CTkFrame(
            center,
            fg_color=C["highlight"],
            corner_radius=4,
            border_width=1,
            border_color=C["panel_border"],
        )
        server_frame.pack()

        ctk.CTkLabel(
            server_frame,
            text="\u2588  1.21.4",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=C["text_dim"],
        ).pack(side="left", padx=(8, 12))

        ctk.CTkLabel(
            server_frame,
            text="play.example.net",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=C["text"],
        ).pack(side="left", padx=(0, 12))

        self.time_label = ctk.CTkLabel(
            server_frame,
            text=datetime.now().strftime("%H:%M"),
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=C["accent"],
        )
        self.time_label.pack(side="left", padx=(0, 8))

        # Right side
        right = ctk.CTkFrame(bar, fg_color="transparent")
        right.pack(side="right", padx=12)

        for icon in ["\u25a0", "\u25a0", "\u25a0"]:
            ctk.CTkLabel(
                right,
                text=icon,
                font=ctk.CTkFont(size=10),
                text_color=C["text_muted"],
                width=18,
            ).pack(side="left")

    def _stat_pill(self, parent, icon, text, color):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(side="left", padx=(0, 12))

        ctk.CTkLabel(
            frame,
            text=icon,
            font=ctk.CTkFont(size=6),
            text_color=color,
            width=10,
        ).pack(side="left", padx=(0, 4))

        ctk.CTkLabel(
            frame,
            text=text,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=color,
        ).pack(side="left")

    # ─── Keybinds Panel (top-left) ──────────────────────

    def _build_keybinds_panel(self):
        panel = HUDPanel(self, "Keybinds", "\u2328", width=230)
        panel.place(x=16, y=50)

        keybinds = [
            ("\u00bb", "KillAura", "R", C["accent3"]),
            ("\u2716", "Speed", "V", C["accent"]),
            ("\u21e7", "Fly", "G", C["accent2"]),
            ("\u25ce", "ESP", "H", C["orange"]),
            ("\u25c6", "AutoClicker", "F", C["green"]),
        ]

        for icon, name, key, color in keybinds:
            row = KeybindRow(panel.content, icon, name, key, color)
            row.pack(fill="x", pady=2)

    # ─── Active Modules (left, below keybinds) ──────────

    def _build_active_modules_panel(self):
        panel = HUDPanel(self, "Active Modules", "\u25a6", width=200)
        panel.place(x=16, y=230)

        modules = [
            ("Sprint", C["accent"]),
            ("FullBright", C["orange"]),
            ("NoFall", C["green"]),
            ("Velocity", C["accent3"]),
            ("AutoTotem", C["accent2"]),
            ("FastPlace", C["yellow"]),
        ]

        for name, color in modules:
            item = ModuleListItem(panel.content, name, color)
            item.pack(fill="x", pady=1)

        # Count label
        ctk.CTkLabel(
            panel.content,
            text=f"{len(modules)} modules active",
            font=ctk.CTkFont(size=10),
            text_color=C["text_muted"],
        ).pack(anchor="w", pady=(6, 0))

    # ─── Server Panel (top-center) ──────────────────────

    def _build_server_panel(self):
        panel = HUDPanel(self, "Server", "\u2601", width=220)
        panel.place(relx=0.5, y=50, anchor="n")

        rows = [
            ("Address", "play.example.net"),
            ("TPS", "20.0"),
            ("Players", "47 / 100"),
            ("Gamemode", "Survival"),
        ]

        for label, value in rows:
            row = ctk.CTkFrame(panel.content, fg_color="transparent")
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(
                row,
                text=label,
                font=ctk.CTkFont(size=11),
                text_color=C["text_dim"],
            ).pack(side="left")

            val_color = C["green"] if label == "TPS" else C["text"]
            ctk.CTkLabel(
                row,
                text=value,
                font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
                text_color=val_color,
            ).pack(side="right")

    # ─── Players Panel (top-right) ──────────────────────

    def _build_players_panel(self):
        panel = HUDPanel(self, "Nearby", "\u263a", width=240)
        panel.place(relx=1.0, x=-16, y=50, anchor="ne")

        players = [
            ("xDreamz", "Owner", 12, C["accent3"]),
            ("NetherKing", "Admin", 34, C["red"]),
            ("SkyWalker99", "VIP", 8, C["orange"]),
            ("CraftMaster", "", 56, C["text_dim"]),
            ("BlockBreaker", "", 128, C["text_dim"]),
        ]

        for name, role, ping, role_color in players:
            row = PlayerRow(panel.content, name, role, ping, role_color)
            row.pack(fill="x", pady=2)

    # ─── Online Panel (right, below players) ────────────

    def _build_online_panel(self):
        panel = HUDPanel(self, "Online209 Users", "\u2606", width=210)
        panel.place(relx=1.0, x=-16, y=240, anchor="ne")

        users = [
            ("Player209", C["green"]),
            ("Destroyer_X", C["accent"]),
            ("VoidRunner", C["accent"]),
            ("PhantomBlade", C["accent"]),
        ]

        for name, color in users:
            row = ctk.CTkFrame(panel.content, fg_color="transparent")
            row.pack(fill="x", pady=2)

            dot = ctk.CTkFrame(row, width=6, height=6, corner_radius=3, fg_color=color)
            dot.pack(side="left", padx=(0, 8), pady=7)

            ctk.CTkLabel(
                row,
                text=name,
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color=C["text"],
            ).pack(side="left")

    # ─── Events Panel (bottom-left) ─────────────────────

    def _build_events_panel(self):
        panel = HUDPanel(self, "Events", "\u231a", width=240)
        panel.place(x=16, rely=1.0, y=-80, anchor="sw")

        events = [
            (C["accent3"], "Dragon Fight", "#7", "2:45"),
            (C["orange"], "Tournament", "#12", "15:30"),
            (C["green"], "Build Contest", "#3", "48:12"),
        ]

        for color, name, eid, time_str in events:
            row = EventRow(panel.content, color, name, eid, time_str)
            row.pack(fill="x", pady=2)

    # ─── Notifications (center-bottom) ──────────────────

    def _build_notifications(self):
        notif_frame = ctk.CTkFrame(self, fg_color="transparent")
        notif_frame.place(relx=0.5, rely=0.72, anchor="center")

        notifications = [
            ("\u2716", "KillAura was Disabled!", False),
            ("\u2191", "Speed was Enabled!", True),
            ("\u00bb", "NoFall was Enabled!", True),
        ]

        for icon, text, enabled in notifications:
            notif = NotificationItem(notif_frame, icon, text, enabled)
            notif.pack(pady=3)

    # ─── Bottom Bar ─────────────────────────────────────

    def _build_bottom_bar(self):
        bar = ctk.CTkFrame(self, fg_color=C["bar_bg"], corner_radius=0, height=28)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)

        left = ctk.CTkFrame(bar, fg_color="transparent")
        left.pack(side="left", padx=12)

        # Coordinates
        ctk.CTkLabel(
            left,
            text="\u25cf",
            font=ctk.CTkFont(size=8),
            text_color=C["accent"],
            width=10,
        ).pack(side="left", padx=(0, 4))

        self.coords_label = ctk.CTkLabel(
            left,
            text="X: 1,492  Y: 76  Z: -780",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=C["text_dim"],
        )
        self.coords_label.pack(side="left", padx=(0, 20))

        # Direction
        ctk.CTkLabel(
            left,
            text="\u25cf",
            font=ctk.CTkFont(size=8),
            text_color=C["orange"],
            width=10,
        ).pack(side="left", padx=(0, 4))

        ctk.CTkLabel(
            left,
            text="Facing: NW (-135.4\u00b0)",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=C["text_dim"],
        ).pack(side="left", padx=(0, 20))

        # Speed
        ctk.CTkLabel(
            left,
            text="\u25cf",
            font=ctk.CTkFont(size=8),
            text_color=C["green"],
            width=10,
        ).pack(side="left", padx=(0, 4))

        ctk.CTkLabel(
            left,
            text="18.48 b/s",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=C["text_dim"],
        ).pack(side="left")

        # Right side - biome
        right = ctk.CTkFrame(bar, fg_color="transparent")
        right.pack(side="right", padx=12)

        ctk.CTkLabel(
            right,
            text="Plains",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=C["text_muted"],
        ).pack(side="right")

        ctk.CTkLabel(
            right,
            text="Biome:",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=C["text_dim"],
        ).pack(side="right", padx=(0, 4))

    # ─── Watermark ──────────────────────────────────────

    def _build_watermark(self):
        ctk.CTkLabel(
            self,
            text="ONLINE209 CLIENT",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=C["text_muted"],
        ).place(x=16, rely=0.0, y=36, anchor="sw")

    # ─── Clock Update ──────────────────────────────────

    def _start_clock(self):
        self._update_clock()

    def _update_clock(self):
        self.time_label.configure(text=datetime.now().strftime("%H:%M:%S"))
        self.after(1000, self._update_clock)


def main():
    app = Online209HUD()
    app.mainloop()


if __name__ == "__main__":
    main()
