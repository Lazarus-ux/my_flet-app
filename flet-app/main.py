from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote

import flet as ft


REPO_ROOT = Path(__file__).resolve().parents[1]
ASSETS_ROOT = Path(os.environ.get("FLET_ASSETS_DIR", str(REPO_ROOT / "public"))).resolve()
IMAGE_DIR = ASSETS_ROOT / "images"
VIDEO_DIR = ASSETS_ROOT / "videos"
CERT_DIR = ASSETS_ROOT / "certificates"
REPORT_DIR = ASSETS_ROOT / "reports"
PROFILE_IMAGE = IMAGE_DIR / "portrait-lasarus.jpg"
PROJECT_VIDEO = VIDEO_DIR / "Video Project 1.mp4"
BUTTON_ORANGE = "#F05A00"
BUTTON_ORANGE_SOFT = "#FF7A2F"
BUTTON_ORANGE_DARK = "#C94700"

PALETTE = {
    "bg": "#F5F8FC",
    "panel": "#FFFFFF",
    "panel_soft": "#FFF4EB",
    "ink": "#1F2730",
    "muted": "#66737C",
    "accent": "#F05A00",
    "accent_soft": "#FFE7D6",
    "border": "#D7E2EE",
    "dark": "#13232C",
}

PANEL_BORDER = ft.Border(
    left=ft.border.BorderSide(1, PALETTE["border"]),
    top=ft.border.BorderSide(1, PALETTE["border"]),
    right=ft.border.BorderSide(1, PALETTE["border"]),
    bottom=ft.border.BorderSide(1, PALETTE["border"]),
)
PANEL_SHADOW = ft.BoxShadow(
    spread_radius=0,
    blur_radius=20,
    color="#1F273014",
    offset=ft.Offset(0, 6),
)
ROUNDED_BUTTON_STYLE = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=16))
ORANGE_BUTTON_OVERLAY = {
    ft.ControlState.HOVERED: "#F05A0018",
    ft.ControlState.FOCUSED: "#F05A0018",
    ft.ControlState.PRESSED: "#F05A0022",
}


def file_bytes(path: Path) -> bytes | None:
    try:
        return path.read_bytes() if path.exists() else None
    except OSError:
        return None


def asset_url(path: Path) -> str:
    relative = path.relative_to(ASSETS_ROOT).as_posix()
    return f"/{quote(relative, safe='/')}"


def profile_avatar(path: Path, *, radius: int = 92) -> ft.CircleAvatar:
    data = file_bytes(path)
    if data is None:
        return ft.CircleAvatar(
            content=ft.Text(
                "LS",
                size=30,
                weight=ft.FontWeight.BOLD,
                color=PALETTE["accent"],
            ),
            radius=radius,
            bgcolor=PALETTE["accent_soft"],
        )

    return ft.CircleAvatar(
        foreground_image_src=data,
        radius=radius,
        bgcolor=PALETTE["accent_soft"],
    )


def image_control(
    path: Path,
    *,
    width: int | None = None,
    height: int | None = None,
    fit: str = "cover",
) -> ft.Image | ft.Container:
    data = file_bytes(path)
    if data is None:
        return ft.Container(
            width=width,
            height=height,
            padding=14,
            border_radius=14,
            bgcolor=PALETTE["panel_soft"],
            content=ft.Text(
                path.name,
                size=12,
                color=PALETTE["muted"],
                selectable=True,
            ),
            expand=width is None,
        )

    if width is None:
        return ft.Image(src=data, height=height, fit=fit, expand=True)
    return ft.Image(src=data, width=width, height=height, fit=fit)


def pill(label: str, *, filled: bool = False) -> ft.Container:
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=12, vertical=7),
        border_radius=999,
        border=ft.Border(
            left=ft.border.BorderSide(1, PALETTE["border"]),
            top=ft.border.BorderSide(1, PALETTE["border"]),
            right=ft.border.BorderSide(1, PALETTE["border"]),
            bottom=ft.border.BorderSide(1, PALETTE["border"]),
        ),
        bgcolor=PALETTE["accent"] if filled else PALETTE["accent_soft"],
        content=ft.Text(
            label,
            size=12,
            weight=ft.FontWeight.W_600,
            color="white" if filled else PALETTE["accent"],
        ),
    )


def section_header(
    eyebrow: str,
    title: str,
    description: str | None = None,
    *,
    icon: ft.IconData | None = None,
) -> ft.Column:
    eyebrow_row: ft.Control
    if icon is None:
        eyebrow_row = ft.Text(
            eyebrow,
            size=12,
            weight=ft.FontWeight.W_600,
            color=PALETTE["accent"],
            style=ft.TextStyle(letter_spacing=1.2),
        )
    else:
        eyebrow_row = ft.Row(
            controls=[
                ft.Icon(icon, size=14, color=PALETTE["accent"]),
                ft.Text(
                    eyebrow,
                    size=12,
                    weight=ft.FontWeight.W_600,
                    color=PALETTE["accent"],
                    style=ft.TextStyle(letter_spacing=1.2),
                ),
            ],
            spacing=6,
        )

    controls: list[ft.Control] = [
        eyebrow_row,
        ft.Text(
            title,
            size=34,
            weight=ft.FontWeight.BOLD,
            color=PALETTE["ink"],
        ),
        ft.Container(
            width=72,
            height=4,
            border_radius=999,
            bgcolor=PALETTE["accent_soft"],
        ),
    ]
    if description:
        controls.append(
            ft.Text(
                description,
                size=15,
                color=PALETTE["muted"],
                selectable=True,
            )
        )

    return ft.Column(controls=controls, spacing=8)


def framed_panel(
    content: ft.Control,
    *,
    bgcolor: str = PALETTE["panel"],
    padding: int = 20,
) -> ft.Card:
    return ft.Card(
        elevation=0,
        content=ft.Container(
            padding=padding,
            bgcolor=bgcolor,
            border_radius=18,
            border=PANEL_BORDER,
            shadow=PANEL_SHADOW,
            content=content,
        ),
    )


def video_card(page: ft.Page, title: str, description: str, video_url: str) -> ft.Card:
    share_url = video_url

    def open_video(_: ft.ControlEvent) -> None:
        page.launch_url(share_url, web_popup_window=True)

    return framed_panel(
        ft.Column(
            spacing=10,
            controls=[
                ft.Container(
                    height=180,
                    border_radius=18,
                    alignment=ft.Alignment.CENTER,
                    bgcolor=PALETTE["panel_soft"],
                    content=ft.Column(
                        spacing=6,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.PLAY_ARROW, size=56, color=PALETTE["accent"]),
                            ft.Text(
                                "Video ready to play",
                                size=13,
                                weight=ft.FontWeight.W_600,
                                color=PALETTE["ink"],
                            ),
                        ],
                    ),
                ),
                pill("Video"),
                ft.Text(
                    title,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=PALETTE["ink"],
                ),
                ft.Text(
                    description,
                    size=13,
                    color=PALETTE["muted"],
                    selectable=True,
                ),
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=12, vertical=10),
                    border_radius=14,
                    bgcolor=PALETTE["accent_soft"],
                    content=ft.Column(
                        spacing=4,
                        controls=[
                            ft.Text(
                                "Hosted link",
                                size=12,
                                weight=ft.FontWeight.W_600,
                                color=PALETTE["accent"],
                            ),
                            ft.Text(
                                share_url,
                                size=12,
                                color=PALETTE["accent"],
                                selectable=True,
                            ),
                        ],
                    ),
                ),
                link_button("Open video link", share_url, icon=ft.Icons.LINK),
                ft.Button(
                    content="Play video",
                    icon=ft.Icons.PLAY_ARROW,
                    icon_color="white",
                    on_click=open_video,
                    bgcolor=BUTTON_ORANGE,
                    color="white",
                    height=46,
                    style=ROUNDED_BUTTON_STYLE.copy(overlay_color=ORANGE_BUTTON_OVERLAY),
                    expand=True,
                ),
            ],
        ),
        bgcolor=PALETTE["panel"],
        padding=18,
    )


def link_button(
    label: str,
    url: str,
    *,
    primary: bool = False,
    icon: ft.IconData | None = None,
) -> ft.Button:
    button_color = "white"
    return ft.Button(
        content=label,
        icon=icon,
        icon_color="white",
        url=url,
        bgcolor=BUTTON_ORANGE,
        color=button_color,
        height=46,
        style=ROUNDED_BUTTON_STYLE.copy(overlay_color=ORANGE_BUTTON_OVERLAY),
        expand=True,
    )


def stat_card(value: str, label: str, detail: str) -> ft.Card:
    return framed_panel(
        ft.Column(
            controls=[
                ft.Text(
                    value,
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=PALETTE["ink"],
                ),
                ft.Text(
                    label,
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color=PALETTE["accent"],
                ),
                ft.Text(
                    detail,
                    size=13,
                    color=PALETTE["muted"],
                    selectable=True,
                ),
            ],
            spacing=5,
        ),
        bgcolor=PALETTE["panel"],
        padding=18,
    )


def build_topbar(jump_to, active_key: str = "home") -> ft.Container:
    nav_items = [
        ("Home", "home", ft.Icons.HOME),
        ("Timeline", "timeline", ft.Icons.TIMELINE),
        ("MATLAB", "matlab", ft.Icons.SCHOOL),
        ("Projects", "projects", ft.Icons.FOLDER_OPEN),
        ("Blog", "blog", ft.Icons.FEATURED_VIDEO),
        ("GitHub", "github", ft.Icons.CODE),
        ("Contact", "contact", ft.Icons.EMAIL),
    ]

    def nav_button(label: str, key: str, icon: ft.IconData) -> ft.Container:
        active = key == active_key
        return ft.Container(
            col={
                ft.ResponsiveRowBreakpoint.XS: 6,
                ft.ResponsiveRowBreakpoint.SM: 4,
                ft.ResponsiveRowBreakpoint.MD: 3,
            },
            content=ft.Button(
                content=ft.Row(
                    spacing=8,
                    tight=True,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(
                            icon,
                            size=16,
                            color="white" if active else "#F3F6F7",
                        ),
                        ft.Text(
                            label,
                            size=13,
                            weight=ft.FontWeight.W_600,
                            color="white" if active else "#F7FBFC",
                        ),
                    ],
                ),
                on_click=lambda e, target=key: jump_to(target),
                bgcolor=BUTTON_ORANGE_DARK if active else BUTTON_ORANGE,
                color="white",
                elevation=0,
                height=52,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=18),
                    overlay_color=ORANGE_BUTTON_OVERLAY,
                ),
                expand=True,
            ),
        )

    nav_buttons = ft.ResponsiveRow(
        spacing=8,
        run_spacing=8,
        controls=[nav_button(label, key, icon) for label, key, icon in nav_items],
    )

    return ft.Container(
        expand=True,
        padding=ft.Padding.symmetric(horizontal=18, vertical=14),
        gradient=ft.LinearGradient(
            begin=ft.Alignment.CENTER_LEFT,
            end=ft.Alignment.CENTER_RIGHT,
            colors=[BUTTON_ORANGE_DARK, BUTTON_ORANGE, BUTTON_ORANGE_SOFT],
        ),
        border=ft.Border(
            left=ft.border.BorderSide(1, "#FFFFFF22"),
            top=ft.border.BorderSide(1, "#FFFFFF22"),
            right=ft.border.BorderSide(1, "#FFFFFF22"),
            bottom=ft.border.BorderSide(1, "#FFFFFF22"),
        ),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=28,
            color="#0D172126",
            offset=ft.Offset(0, 10),
        ),
        border_radius=30,
        content=ft.Container(
            padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            border_radius=22,
            bgcolor="#F05A0014",
            border=ft.Border(
                left=ft.border.BorderSide(1, "#FFFFFF1C"),
                top=ft.border.BorderSide(1, "#FFFFFF1C"),
                right=ft.border.BorderSide(1, "#FFFFFF1C"),
                bottom=ft.border.BorderSide(1, "#FFFFFF1C"),
            ),
            content=nav_buttons,
        ),
    )


def build_hero(*, avatar_radius: int = 150, bio_width: int | None = None) -> ft.Container:
    hero_bio = (
        "My name is Lasarus Shiyelekeni, a third-year Electrical Engineering student, developer, "
        "and technology enthusiast. I enjoy transforming ideas into practical solutions by combining "
        "engineering principles with software development. From proposing the QuoteWise concept to "
        "leading a team of 12 members throughout its development, I am driven by innovation, "
        "continuous learning, and the desire to create technology that makes a meaningful impact."
    )

    return ft.Container(
        key=ft.ScrollKey("home"),
        padding=ft.Padding.symmetric(horizontal=24, vertical=22),
        content=ft.Container(
            border_radius=24,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            border=PANEL_BORDER,
            shadow=PANEL_SHADOW,
            image=ft.DecorationImage(
                src=asset_url(IMAGE_DIR / "hero-bg.png"),
                fit=ft.BoxFit.COVER,
            ),
            content=ft.Container(
                padding=28,
                bgcolor="#FFF4EDEA",
                border_radius=24,
                content=ft.Container(
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        spacing=18,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            profile_avatar(PROFILE_IMAGE, radius=avatar_radius),
                            ft.Container(
                                width=bio_width,
                                alignment=ft.Alignment.CENTER,
                                content=ft.Text(
                                    hero_bio,
                                    size=17,
                                    weight=ft.FontWeight.W_500,
                                    color=PALETTE["muted"],
                                    text_align=ft.TextAlign.CENTER,
                                    selectable=True,
                                ),
                            ),
                        ],
                    ),
                ),
            ),
        ),
    )


def make_timeline_card(week: str, title: str, description: str) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    width=14,
                    content=ft.Container(
                        width=12,
                        height=12,
                        bgcolor=PALETTE["accent_soft"],
                        border_radius=6,
                    ),
                    padding=ft.Padding.only(top=16),
                ),
                ft.Container(
                    expand=True,
                    content=framed_panel(
                        ft.Column(
                            spacing=6,
                            controls=[
                                ft.Text(
                                    week,
                                    size=12,
                                    weight=ft.FontWeight.W_600,
                                    color=PALETTE["accent"],
                                ),
                                ft.Text(
                                    title,
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=PALETTE["ink"],
                                ),
                                ft.Text(
                                    description,
                                    size=13,
                                    color=PALETTE["muted"],
                                    selectable=True,
                                ),
                            ],
                        ),
                        bgcolor=PALETTE["panel"],
                        padding=18,
                    ),
                ),
            ],
        ),
    )


def build_timeline_section() -> ft.Container:
    milestones = [
        (
            "Week 1",
            "Proposed the QuoteWise concept",
            "I brought the idea and name to the team, framing a budgeting and quotation app that would serve the civil engineering context well.",
        ),
        (
            "Week 2",
            "Mapped the user flow",
            "I helped define the app structure, navigation, and the major sections that later became the web portfolio proof trail.",
        ),
        (
            "Week 3",
            "Coordinated the UI direction",
            "I guided the warm design language, reusable cards, and the visual hierarchy so the project felt coherent across sections.",
        ),
        (
            "Week 4",
            "Organized implementation details",
            "I kept the team focused on the screens that mattered most: budgeting, drafts, saved items, and evidence-ready documentation.",
        ),
        (
            "Week 5",
            "Collected GitHub evidence",
            "I assembled commit and pull-request proof so my individual contribution would be easy to verify during assessment.",
        ),
        (
            "Week 6",
            "Prepared the final submission story",
            "I turned the work into a concise narrative that links the app, the documentation, and the engineering use case.",
        ),
    ]

    return ft.Container(
        key=ft.ScrollKey("timeline"),
        padding=ft.Padding.symmetric(horizontal=24, vertical=22),
        content=ft.Column(
            spacing=14,
            controls=[
                section_header(
                    "The journey",
                    "Project Timeline",
                    "A weekly log of my personal contributions to QuoteWise and the portfolio itself.",
                    icon=ft.Icons.TIMELINE,
                ),
                ft.Container(
                    padding=ft.Padding.all(20),
                    bgcolor=PALETTE["panel_soft"],
                    border_radius=22,
                    content=ft.Column(
                        spacing=10,
                        controls=[make_timeline_card(*entry) for entry in milestones],
                    ),
                ),
            ],
        ),
    )


def make_course_card(title: str, description: str, cert: Path | None, report: Path | None) -> ft.Card:
    buttons: list[ft.Control] = []
    if cert is not None and cert.exists():
        buttons.append(
            ft.Container(
                col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.SM: 6},
                content=link_button("Certificate", asset_url(cert), primary=True, icon=ft.Icons.SCHOOL),
            )
        )
    if report is not None and report.exists():
        buttons.append(
            ft.Container(
                col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.SM: 6},
                content=link_button("Report", asset_url(report), primary=False, icon=ft.Icons.DESCRIPTION),
            )
        )

    return framed_panel(
        ft.Column(
            spacing=8,
            controls=[
                ft.Text(title, size=17, weight=ft.FontWeight.BOLD, color=PALETTE["ink"]),
                ft.Text(description, size=13, color=PALETTE["muted"], selectable=True),
                ft.ResponsiveRow(spacing=8, run_spacing=8, controls=buttons),
            ],
        ),
        bgcolor=PALETTE["panel"],
        padding=18,
    )


def build_matlab_section() -> ft.Container:
    courses = [
        {
            "title": "MATLAB Onramp",
            "description": "The foundational MATLAB course covering the core environment, syntax, and basic operations.",
            "cert": CERT_DIR / "MATLAB Onramp certificate.pdf",
            "report": REPORT_DIR / "MATLAB Onramp report.pdf",
            "featured": True,
        },
        {
            "title": "Simulink Onramp",
            "description": "Model-based design fundamentals with Simulink and basic block diagrams.",
            "cert": CERT_DIR / "Simulink Onramp certificate.pdf",
            "report": REPORT_DIR / "Simulink Onramp report.pdf",
        },
        {
            "title": "Introduction to Linear Algebra with MATLAB",
            "description": "Linear algebra workflows and matrix operations in MATLAB.",
            "cert": CERT_DIR / "Introduction to Linear Algebra with MATLAB certificate.pdf",
            "report": REPORT_DIR / "Introduction to Linear Algebra with MATLAB report.pdf",
        },
        {
            "title": "Introduction to Solving Ordinary Differential Equations",
            "description": "Numerical ODE solving and time-based simulation workflows.",
            "cert": CERT_DIR / "Introduction to Solving Ordinary Differential Equations certificate.pdf",
            "report": REPORT_DIR / "Introduction to Solving Ordinary Differential Equations report.pdf",
        },
        {
            "title": "Make and Manipulate Matrices",
            "description": "Matrix creation, indexing, reshaping, and manipulation basics.",
            "cert": CERT_DIR / "Make and Manipulate Matrices certificate.pdf",
            "report": REPORT_DIR / "Make and Manipulate Matrices report.pdf",
        },
        {
            "title": "Calculations with Vectors and Matrices",
            "description": "Vector arithmetic, matrix calculations, and numeric workflows.",
            "cert": CERT_DIR / "Calculations with Vectors and Matrices certificate (1).pdf",
            "report": REPORT_DIR / "Calculations with Vectors and Matrices report.pdf",
        },
        {
            "title": "Explore Data with MATLAB Plots",
            "description": "Plotting, visual inspection, and exploratory analysis with MATLAB figures.",
            "cert": CERT_DIR / "Explore Data with MATLAB Plots certificate.pdf",
            "report": REPORT_DIR / "Explore Data with MATLAB Plots report.pdf",
        },
    ]

    featured = courses[0]
    others = courses[1:]

    featured_buttons = ft.ResponsiveRow(
        spacing=10,
        run_spacing=10,
        controls=[
            ft.Container(
                col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.SM: 6},
                content=link_button("Certificate", asset_url(featured["cert"]), primary=True, icon=ft.Icons.SCHOOL),
            ),
            ft.Container(
                col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.SM: 6},
                content=link_button("Report", asset_url(featured["report"]), primary=False, icon=ft.Icons.DESCRIPTION),
            ),
        ],
    )

    return ft.Container(
        key=ft.ScrollKey("matlab"),
        padding=ft.Padding.symmetric(horizontal=24, vertical=22),
        content=ft.Column(
            spacing=14,
            controls=[
                section_header(
                    "Verified skills",
                    "MATLAB Certificates",
                    "Completed MathWorks certificates and proof files.",
                    icon=ft.Icons.SCHOOL,
                ),
                framed_panel(
                    ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text(
                                featured["title"],
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color=PALETTE["ink"],
                            ),
                            ft.Text(
                                featured["description"],
                                size=14,
                                color=PALETTE["muted"],
                                selectable=True,
                            ),
                            featured_buttons,
                        ],
                    ),
                    bgcolor=PALETTE["panel"],
                    padding=20,
                ),
                ft.ResponsiveRow(
                    spacing=12,
                    run_spacing=12,
                    controls=[
                        ft.Container(
                            col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 6},
                            content=make_course_card(
                                course["title"],
                                course["description"],
                                course["cert"],
                                course["report"],
                            ),
                        )
                        for course in others
                    ],
                ),
            ],
        ),
    )


def _build_blog_section_legacy() -> ft.Container:
    posts = [
        {
            "title": "Parallel RLC Resonance",
            "description": "A concise explanation of resonance in parallel RLC circuits, including impedance balance, quality factor, and why the circuit behaves sharply at the resonant frequency.",
            "category": "Circuits",
            "read_time": "6 min",
            "image": IMAGE_DIR / "texture-glass.png",
            "featured": True,
        },
        {
            "title": "Python Functions",
            "description": "A practical guide to writing clean, reusable functions in Python. It covers parameters, return values, scope, and lambda expressions.",
            "category": "Programming",
            "read_time": "5 min",
            "image": IMAGE_DIR / "texture-concrete.png",
            "featured": False,
        },
        {
            "title": "Object-Oriented Programming",
            "description": "An approachable explanation of encapsulation, inheritance, and polymorphism using Python examples and everyday analogies.",
            "category": "OOP",
            "read_time": "7 min",
            "image": IMAGE_DIR / "texture-workspace.png",
            "featured": False,
        },
    ]

    featured = next(post for post in posts if post["featured"])
    others = [post for post in posts if not post["featured"]]

    featured_card = framed_panel(
        ft.ResponsiveRow(
            spacing=0,
            run_spacing=0,
            controls=[
                ft.Container(
                    col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 6},
                    content=image_control(featured["image"], height=250, fit="cover"),
                ),
                ft.Container(
                    col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 6},
                    padding=20,
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text(
                                featured["category"],
                                size=12,
                                weight=ft.FontWeight.W_600,
                                color=PALETTE["accent"],
                            ),
                            ft.Text(
                                featured["title"],
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=PALETTE["ink"],
                            ),
                            ft.Text(
                                featured["description"],
                                size=14,
                                color=PALETTE["muted"],
                                selectable=True,
                            ),
                            ft.Text(
                                featured["read_time"],
                                size=13,
                                color=PALETTE["muted"],
                            ),
                        ],
                    ),
                ),
            ],
        ),
        bgcolor=PALETTE["panel"],
        padding=0,
    )

    notation_card = framed_panel(
        ft.Markdown(
            value="""
### Confidence in Concepts

When I explain a calculation, I keep the intuition and the symbols together.

`Total Cost = Σ (Qi × Pi) + Overheads`

- `Qi` = quantity
- `Pi` = unit price
- `Overheads` = transport, handling, administration, contingency

This notation is short, precise, and easy to reference in a live portfolio review.
""",
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        ),
        bgcolor=PALETTE["panel"],
        padding=18,
    )

    notation_card_clean = framed_panel(
        ft.Markdown(
            value="""
### Confidence in Concepts

I keep the explanation close to the symbols so the idea stays easy to review.

`Total Cost = Σ (Qi × Pi) + Overheads`

- `Qi` = quantity
- `Pi` = unit price
- `Overheads` = transport, handling, administration, contingency

That gives the blog a short, formal notation block without making it hard to read.
""",
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        ),
        bgcolor=PALETTE["panel"],
        padding=18,
    )

    video_slots = ft.ResponsiveRow(
        spacing=12,
        run_spacing=12,
        controls=[
            ft.Container(
                col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 6},
                content=framed_panel(
                    ft.Column(
                        spacing=8,
            controls=[
                            image_control(IMAGE_DIR / "texture-glass.png", height=150, fit="cover"),
                            pill("Video insert"),
                            ft.Text(
                                "Python Functions video",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=PALETTE["ink"],
                            ),
                            ft.Text(
                                "Insert a short walkthrough about parameters, return values, and scope.",
                                size=13,
                                color=PALETTE["muted"],
                                selectable=True,
                            ),
                        ],
                    ),
                    bgcolor=PALETTE["panel"],
                    padding=18,
                ),
            ),
            ft.Container(
                col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 6},
                content=framed_panel(
                    ft.Column(
                        spacing=8,
                        controls=[
                            image_control(IMAGE_DIR / "texture-workspace.png", height=150, fit="cover"),
                            pill("Video insert"),
                            ft.Text(
                                "OOP video",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=PALETTE["ink"],
                            ),
                            ft.Text(
                                "Insert a walkthrough about encapsulation, inheritance, and polymorphism.",
                                size=13,
                                color=PALETTE["muted"],
                                selectable=True,
                            ),
                        ],
                    ),
                    bgcolor=PALETTE["panel"],
                    padding=18,
                ),
            ),
        ],
    )

    return ft.Container(
        key=ft.ScrollKey("blog"),
        padding=ft.Padding.symmetric(horizontal=24, vertical=22),
        content=ft.Column(
            spacing=14,
            controls=[
                section_header(
                    "Confidence in Concepts",
                    "Technical Blog",
                    "One technical blog post and your project video.",
                    icon=ft.Icons.FEATURED_VIDEO,
                ),
                featured_card,
                video_card(
                    "Video Project 1",
                    "The MP4 from your desktop folder, shown directly from the portfolio.",
                    asset_url(PROJECT_VIDEO),
                ),
            ],
        ),
    )


def build_blog_section(page: ft.Page) -> ft.Container:
    featured = {
        "title": "Parallel RLC Resonance",
        "description": "A concise explanation of resonance in parallel RLC circuits, including impedance balance, quality factor, and why the circuit behaves sharply at the resonant frequency.",
        "category": "Circuits",
        "read_time": "6 min",
        "image": IMAGE_DIR / "texture-glass.png",
    }

    featured_card = framed_panel(
        ft.ResponsiveRow(
            spacing=0,
            run_spacing=0,
            controls=[
                ft.Container(
                    col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 6},
                    content=image_control(featured["image"], height=250, fit="cover"),
                ),
                ft.Container(
                    col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 6},
                    padding=20,
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text(
                                featured["category"],
                                size=12,
                                weight=ft.FontWeight.W_600,
                                color=PALETTE["accent"],
                            ),
                            ft.Text(
                                featured["title"],
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=PALETTE["ink"],
                            ),
                            ft.Text(
                                featured["description"],
                                size=14,
                                color=PALETTE["muted"],
                                selectable=True,
                            ),
                            ft.Text(
                                featured["read_time"],
                                size=13,
                                color=PALETTE["muted"],
                            ),
                        ],
                    ),
                ),
            ],
        ),
        bgcolor=PALETTE["panel"],
        padding=0,
    )

    notation_card = framed_panel(
        ft.Markdown(
            value="""
### Mathematical Notation Requirement

All technical posts must use proper notation.

For material cost discussions, write it like this:

`Total Cost = Σ_{i=1}^{n} (Q_i × P_i) + Overheads`

- `Q_i` = quantity of item `i`
- `P_i` = price of item `i`
- `n` = number of items
- `Overheads` = transport, handling, administration, contingency
""",
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        ),
        bgcolor=PALETTE["panel"],
        padding=18,
    )

    return ft.Container(
        key=ft.ScrollKey("blog"),
        padding=ft.Padding.symmetric(horizontal=24, vertical=22),
        content=ft.Column(
            spacing=14,
            controls=[
                section_header(
                    "Confidence in Concepts",
                    "Technical Blog",
                    "One technical post, proper notation, and a hosted project video.",
                    icon=ft.Icons.FEATURED_VIDEO,
                ),
                featured_card,
                notation_card,
                video_card(
                    page,
                    "Video Project 1",
                    "The MP4 from your desktop folder is hosted locally and can open inside the app.",
                    asset_url(PROJECT_VIDEO),
                ),
            ],
        ),
    )


def build_projects_section() -> ft.Container:
    scope_points = [
        "Manage supplier quotations for construction work.",
        "Track project budgets in Namibian Dollars.",
        "Save and archive finalized estimates.",
        "Draft quotations before submission.",
    ]

    completed_points = [
        "Premium warm design system.",
        "Animated splash and hero sections.",
        "Unified status badges and cards.",
        "Navigation built without a heavy stack.",
        "EAS build path for Android delivery.",
    ]

    planned_points = [
        "Firebase Authentication.",
        "Firestore quotation storage.",
        "Fiber (Go) API connection.",
        "Quotation editing and PDF export.",
        "Push notifications and offline mode.",
    ]

    def bullet(text: str, *, icon: ft.IconData = ft.Icons.CHECK) -> ft.Row:
        return ft.Row(
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Icon(icon, size=14, color=PALETTE["accent"]),
                ft.Text(text, size=13, color=PALETTE["muted"], selectable=True),
            ],
        )

    overview = framed_panel(
        ft.ResponsiveRow(
            spacing=0,
            run_spacing=0,
            controls=[
                ft.Container(
                    col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 5},
                    content=image_control(IMAGE_DIR / "texture-facade.png", height=270, fit="cover"),
                ),
                ft.Container(
                    col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 7},
                    padding=22,
                    content=ft.Column(
                        spacing=12,
                        controls=[
                            pill("README Snapshot", filled=True),
                            ft.Text(
                                "QuoteWise",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                color=PALETTE["ink"],
                            ),
                            ft.Text(
                                "A cross-platform mobile app built with Expo and React Native for the construction industry. It helps contractors manage quotations, track budgets, and archive estimates cleanly.",
                                size=15,
                                color=PALETTE["muted"],
                                selectable=True,
                            ),
                            ft.ResponsiveRow(
                                spacing=8,
                                run_spacing=8,
                                controls=[
                                    ft.Container(col={ft.ResponsiveRowBreakpoint.XS: 6, ft.ResponsiveRowBreakpoint.SM: 4, ft.ResponsiveRowBreakpoint.MD: 3}, content=pill("Civil Engineering")),
                                    ft.Container(col={ft.ResponsiveRowBreakpoint.XS: 6, ft.ResponsiveRowBreakpoint.SM: 4, ft.ResponsiveRowBreakpoint.MD: 3}, content=pill("Expo SDK 55")),
                                    ft.Container(col={ft.ResponsiveRowBreakpoint.XS: 6, ft.ResponsiveRowBreakpoint.SM: 4, ft.ResponsiveRowBreakpoint.MD: 3}, content=pill("React Native")),
                                    ft.Container(col={ft.ResponsiveRowBreakpoint.XS: 6, ft.ResponsiveRowBreakpoint.SM: 4, ft.ResponsiveRowBreakpoint.MD: 3}, content=pill("12 Member Team")),
                                ],
                            ),
                            ft.Text(
                                "Lead Developer: Lasarus Shiyelekeni",
                                size=13,
                                weight=ft.FontWeight.W_600,
                                color=PALETTE["accent"],
                            ),
                        ],
                    ),
                ),
            ],
        ),
        bgcolor=PALETTE["panel"],
        padding=0,
    )

    stats_row = ft.ResponsiveRow(
        spacing=10,
        run_spacing=10,
        controls=[
            ft.Container(
                col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.SM: 6, ft.ResponsiveRowBreakpoint.MD: 3},
                content=stat_card("12", "Team members", "The README lists the full project roster."),
            ),
            ft.Container(
                col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.SM: 6, ft.ResponsiveRowBreakpoint.MD: 3},
                content=stat_card("55", "Expo SDK", "The mobile app is built on Expo SDK 55."),
            ),
            ft.Container(
                col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.SM: 6, ft.ResponsiveRowBreakpoint.MD: 3},
                content=stat_card("4", "Core features", "Quotes, budgets, drafts, and archives."),
            ),
            ft.Container(
                col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.SM: 6, ft.ResponsiveRowBreakpoint.MD: 3},
                content=stat_card("2", "Platforms", "Android and iOS support from the README."),
            ),
        ],
    )

    scope_card = framed_panel(
        ft.Column(
            spacing=10,
            controls=[
                ft.Text("What QuoteWise does", size=20, weight=ft.FontWeight.BOLD, color=PALETTE["ink"]),
                ft.Text(
                    "The repository README frames the app around construction budgeting and quotation management.",
                    size=13,
                    color=PALETTE["muted"],
                    selectable=True,
                ),
                ft.Column(spacing=8, controls=[bullet(point) for point in scope_points]),
            ],
        ),
        bgcolor=PALETTE["panel"],
        padding=18,
    )

    tech_card = framed_panel(
        ft.Column(
            spacing=10,
            controls=[
                ft.Text("Tech stack", size=20, weight=ft.FontWeight.BOLD, color=PALETTE["ink"]),
                ft.Markdown(
                    value="""
| Layer | Technology |
|---|---|
| Framework | Expo SDK 55 |
| UI runtime | React Native 0.83.6 |
| UI library | React 19.2.0 |
| Animations | React Native Animated API |
| Navigation | useState screen stack |
| Backend planned | Fiber (Go) + Firebase |
| Language | JavaScript |
| Platform | Android and iOS |
""",
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                ),
            ],
        ),
        bgcolor=PALETTE["panel"],
        padding=18,
    )

    structure_card = framed_panel(
        ft.Column(
            spacing=10,
            controls=[
                ft.Text("Project structure", size=20, weight=ft.FontWeight.BOLD, color=PALETTE["ink"]),
                ft.Column(
                    spacing=8,
                    controls=[
                        bullet("App.js for screens, components, and styles.", icon=ft.Icons.CODE),
                        bullet("app.json, package.json, index.js, metro.config.js, and eas.json.", icon=ft.Icons.SETTINGS),
                        bullet("docs/QuoteWise_SRS_13691CP.pdf.pdf for the requirements spec.", icon=ft.Icons.DESCRIPTION),
                        bullet("assets/images for splash and header visuals.", icon=ft.Icons.IMAGE),
                    ],
                ),
            ],
        ),
        bgcolor=PALETTE["panel"],
        padding=18,
    )

    roadmap_card = framed_panel(
        ft.Column(
            spacing=10,
            controls=[
                ft.Text("Roadmap snapshot", size=20, weight=ft.FontWeight.BOLD, color=PALETTE["ink"]),
                ft.ResponsiveRow(
                    spacing=12,
                    run_spacing=12,
                    controls=[
                        ft.Container(
                            col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 6},
                            content=framed_panel(
                                ft.Column(
                                    spacing=8,
                                    controls=[
                                        ft.Text("Completed foundations", size=14, weight=ft.FontWeight.W_600, color=PALETTE["accent"]),
                                        ft.Column(spacing=6, controls=[bullet(point) for point in completed_points]),
                                    ],
                                ),
                                bgcolor=PALETTE["panel_soft"],
                                padding=14,
                            ),
                        ),
                        ft.Container(
                            col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 6},
                            content=framed_panel(
                                ft.Column(
                                    spacing=8,
                                    controls=[
                                        ft.Text("Planned next steps", size=14, weight=ft.FontWeight.W_600, color=PALETTE["accent"]),
                                        ft.Column(
                                            spacing=6,
                                            controls=[
                                                bullet(point, icon=ft.Icons.ARROW_FORWARD)
                                                for point in planned_points
                                            ],
                                        ),
                                    ],
                                ),
                                bgcolor=PALETTE["panel_soft"],
                                padding=14,
                            ),
                        ),
                    ],
                ),
            ],
        ),
        bgcolor=PALETTE["panel"],
        padding=18,
    )

    team_roster_card = framed_panel(
        ft.Column(
            spacing=10,
            controls=[
                ft.Text("Team roster", size=20, weight=ft.FontWeight.BOLD, color=PALETTE["ink"]),
                ft.Text(
                    "The full 12-member team listed in the QuoteWise README. Student numbers remain in the source README for verification.",
                    size=13,
                    color=PALETTE["muted"],
                    selectable=True,
                ),
                ft.Markdown(
                    value="""
| Name | Role |
|---|---|
| Immanuel Oliveira | Project Manager |
| Nailoke Nghiiteka | Project Manager Assistant |
| Lasarus Shiyelekeni | Lead Developer |
| Wilhelm WS Moses | Lead Developer Assistant |
| Benhard Handura | Firebase Lead |
| Erikson Shapwa | Firebase Assistant |
| Veikko Shikage | UI/UX Lead |
| Kandjimwena Dison | UI/UX Assistant |
| Lavmo Shiweda | Documentation Lead |
| Kambonde Lehabeam | Documentation Assistant |
| Pehovelo Halwoodi | GitHub Manager |
| Michael Kautuara | GitHub Assistant |
""",
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                ),
            ],
        ),
        bgcolor=PALETTE["panel"],
        padding=18,
    )

    return ft.Container(
        key=ft.ScrollKey("projects"),
        padding=ft.Padding.symmetric(horizontal=24, vertical=22),
        content=ft.Column(
            spacing=14,
            controls=[
                section_header(
                    "From the repository",
                    "Projects",
                    "QuoteWise README details, team roster, stack, and roadmap.",
                    icon=ft.Icons.FOLDER_OPEN,
                ),
                overview,
                stats_row,
                ft.ResponsiveRow(
                    spacing=12,
                    run_spacing=12,
                    controls=[
                        ft.Container(
                            col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 6},
                            content=scope_card,
                        ),
                        ft.Container(
                            col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 6},
                            content=tech_card,
                        ),
                    ],
                ),
                ft.ResponsiveRow(
                    spacing=12,
                    run_spacing=12,
                    controls=[
                        ft.Container(
                            col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 6},
                            content=structure_card,
                        ),
                        ft.Container(
                            col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 6},
                            content=roadmap_card,
                        ),
                    ],
                ),
                team_roster_card,
            ],
        ),
    )


def build_github_section() -> ft.Container:
    evidence_quote = (
        "I proposed the name and idea for QuoteWise, which was accepted by all 13 team members. "
        "As Lead Developer I coordinated development, contributed to system design, and guided feature implementation throughout the semester."
    )

    screenshots = [
        ("Commit History", IMAGE_DIR / "github-commits.png", "A visual record of my commits on the main repository."),
        ("Pull Requests", IMAGE_DIR / "github-prs.png", "The PR log that shows features I proposed and the code reviews I completed."),
        ("Contribution Activity", IMAGE_DIR / "github-evidence.jpg", "A broader activity capture that supports the individual contribution story."),
    ]

    screenshot_cards = [
        ft.Container(
            col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 4},
            content=framed_panel(
                ft.Column(
                    spacing=8,
                    controls=[
                        ft.Text(title, size=13, weight=ft.FontWeight.W_600, color=PALETTE["ink"]),
                        image_control(path, height=180, fit="contain"),
                        ft.Text(description, size=12, color=PALETTE["muted"], selectable=True),
                    ],
                ),
                bgcolor=PALETTE["panel"],
                padding=14,
            ),
        )
        for title, path, description in screenshots
    ]

    return ft.Container(
        key=ft.ScrollKey("github"),
        padding=ft.Padding.symmetric(horizontal=20, vertical=18),
        content=ft.Column(
            spacing=14,
            controls=[
                section_header(
                    "Open source proof",
                    "GitHub Evidence & Documentation",
                    "Commit history, pull requests, screenshots, and an impact summary that ties the work back to the app itself.",
                    icon=ft.Icons.CODE,
                ),
                framed_panel(
                    ft.Text(
                        evidence_quote,
                        size=16,
                        weight=ft.FontWeight.W_600,
                        color="white",
                        selectable=True,
                    ),
                    bgcolor=PALETTE["dark"],
                    padding=20,
                ),
                ft.ResponsiveRow(
                    spacing=12,
                    run_spacing=12,
                    controls=screenshot_cards,
                ),
                framed_panel(
                    ft.Markdown(
                        value="""
### Impact Summary

My code and documentation solved a verification problem for the civil engineering module of the app by making my own contribution easy to audit:

- I centralized the timeline so reviewers can see exactly what I contributed and when.
- I linked each proof item directly from the portfolio so there is no guesswork during assessment.
- I paired the GitHub evidence with a concise narrative, which turns commit history into readable documentation.

The result is a portfolio that is both visually tidy and academically defensible.
""",
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    ),
                    bgcolor=PALETTE["panel"],
                    padding=18,
                ),
            ],
        ),
    )


def build_contact_section() -> ft.Container:
    direct_links = ft.ResponsiveRow(
        spacing=10,
        run_spacing=10,
        controls=[
            ft.Container(
                col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.SM: 6, ft.ResponsiveRowBreakpoint.MD: 4},
                content=link_button("Phone", "tel:0813719608", primary=True, icon=ft.Icons.PHONE),
            ),
            ft.Container(
                col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.SM: 6, ft.ResponsiveRowBreakpoint.MD: 4},
                content=link_button("Email", "mailto:shiyellazarus4@gmail.com", primary=False, icon=ft.Icons.MAIL),
            ),
            ft.Container(
                col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.SM: 6, ft.ResponsiveRowBreakpoint.MD: 4},
                content=link_button("GitHub", "https://github.com/Lazarus-ux", primary=False, icon=ft.Icons.CODE),
            ),
            ft.Container(
                col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.SM: 6, ft.ResponsiveRowBreakpoint.MD: 4},
                content=link_button(
                    "LinkedIn",
                    "https://www.linkedin.com/in/lazarus-shiyelekeni-9a3752291/",
                    primary=False,
                    icon=ft.Icons.LINK,
                ),
            ),
            ft.Container(
                col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.SM: 6, ft.ResponsiveRowBreakpoint.MD: 4},
                content=link_button(
                    "Instagram",
                    "https://www.instagram.com/walasa_121/?hl=en",
                    primary=False,
                    icon=ft.Icons.LINK,
                ),
            ),
        ],
    )

    return ft.Container(
        key=ft.ScrollKey("contact"),
        padding=ft.Padding.symmetric(horizontal=20, vertical=18),
        content=ft.Column(
            spacing=14,
            controls=[
                section_header(
                    "Let's connect",
                    "Get in touch",
                    "Direct links and details.",
                    icon=ft.Icons.PHONE,
                ),
                framed_panel(
                    ft.Column(
                        spacing=12,
                        controls=[
                            ft.ResponsiveRow(
                                spacing=10,
                                run_spacing=10,
                                controls=[
                                    ft.Container(
                                        col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 4},
                                        content=framed_panel(
                                            ft.Row(
                                                spacing=10,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Container(
                                                        width=38,
                                                        height=38,
                                                        border_radius=12,
                                                        alignment=ft.Alignment.CENTER,
                                                        bgcolor=PALETTE["accent_soft"],
                                                        content=ft.Icon(ft.Icons.PERSON, size=18, color=PALETTE["accent"]),
                                                    ),
                                                    ft.Column(
                                                        spacing=2,
                                                        controls=[
                                                            ft.Text(
                                                                "Student number",
                                                                size=12,
                                                                color=PALETTE["muted"],
                                                            ),
                                                            ft.Text(
                                                                "224030698",
                                                                size=16,
                                                                weight=ft.FontWeight.BOLD,
                                                                color=PALETTE["ink"],
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            bgcolor=PALETTE["panel_soft"],
                                            padding=14,
                                        ),
                                    ),
                                    ft.Container(
                                        col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 4},
                                        content=framed_panel(
                                            ft.Row(
                                                spacing=10,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Container(
                                                        width=38,
                                                        height=38,
                                                        border_radius=12,
                                                        alignment=ft.Alignment.CENTER,
                                                        bgcolor=PALETTE["accent_soft"],
                                                        content=ft.Icon(ft.Icons.PHONE, size=18, color=PALETTE["accent"]),
                                                    ),
                                                    ft.Column(
                                                        spacing=2,
                                                        controls=[
                                                            ft.Text(
                                                                "Phone",
                                                                size=12,
                                                                color=PALETTE["muted"],
                                                            ),
                                                            ft.Text(
                                                                "081 371 9608",
                                                                size=16,
                                                                weight=ft.FontWeight.BOLD,
                                                                color=PALETTE["ink"],
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            bgcolor=PALETTE["panel_soft"],
                                            padding=14,
                                        ),
                                    ),
                                    ft.Container(
                                        col={ft.ResponsiveRowBreakpoint.XS: 12, ft.ResponsiveRowBreakpoint.MD: 4},
                                        content=framed_panel(
                                            ft.Row(
                                                spacing=10,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Container(
                                                        width=38,
                                                        height=38,
                                                        border_radius=12,
                                                        alignment=ft.Alignment.CENTER,
                                                        bgcolor=PALETTE["accent_soft"],
                                                        content=ft.Icon(ft.Icons.MAIL, size=18, color=PALETTE["accent"]),
                                                    ),
                                                    ft.Column(
                                                        spacing=2,
                                                        controls=[
                                                            ft.Text(
                                                                "Email",
                                                                size=12,
                                                                color=PALETTE["muted"],
                                                            ),
                                                            ft.Text(
                                                                "shiyellazarus4@gmail.com",
                                                                size=13,
                                                                weight=ft.FontWeight.BOLD,
                                                                color=PALETTE["ink"],
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            bgcolor=PALETTE["panel_soft"],
                                            padding=14,
                                        ),
                                    ),
                                ],
                            ),
                            direct_links,
                        ],
                    ),
                    bgcolor=PALETTE["panel"],
                    padding=18,
                ),
            ],
        ),
    )


def build_footer() -> ft.Container:
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=20, vertical=24),
        content=ft.Text(
            "Built with Flet for browser review.",
            size=12,
            color=PALETTE["muted"],
            text_align=ft.TextAlign.CENTER,
        ),
    )


def main(page: ft.Page) -> None:
    page.title = "Portfolio"
    page.bgcolor = PALETTE["bg"]
    page.padding = 0
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.DEEP_ORANGE)
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.DEEP_ORANGE)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    content_host = ft.Container(expand=True)
    current_section = "home"
    viewport_width = page.width or 1280
    hero_avatar_radius = 150 if viewport_width >= 1024 else 132 if viewport_width >= 768 else 104
    hero_bio_width = 820 if viewport_width >= 1024 else 640 if viewport_width >= 768 else max(260, viewport_width - 64)

    def build_home() -> ft.Container:
        return build_hero(avatar_radius=hero_avatar_radius, bio_width=hero_bio_width)

    def build_blog() -> ft.Container:
        return build_blog_section(page)

    section_builders = {
        "home": build_home,
        "timeline": build_timeline_section,
        "matlab": build_matlab_section,
        "projects": build_projects_section,
        "blog": build_blog,
        "github": build_github_section,
        "contact": build_contact_section,
    }

    def refresh_shell() -> None:
        page.appbar = ft.AppBar(
            automatically_imply_leading=False,
            bgcolor=PALETTE["bg"],
            elevation=0,
            toolbar_height=168,
            title=build_topbar(jump_to, current_section),
        )

    async def show_section(key: str) -> None:
        nonlocal current_section
        builder = section_builders.get(key, build_hero)
        current_section = key
        refresh_shell()
        content_host.content = builder()
        page.update()
        await page.scroll_to(offset=0, duration=0)

    def jump_to(key: str) -> None:
        page.run_task(show_section, key)

    refresh_shell()

    content_host.content = build_home()
    page.add(content_host)


if __name__ == "__main__":
    server_host = os.environ.get("FLET_SERVER_IP")
    if not server_host:
        server_host = "0.0.0.0" if os.environ.get("PORT") or os.environ.get("FLET_FORCE_WEB_SERVER") else "127.0.0.1"
    default_port = "8550" if os.name == "nt" else "8000"
    server_port = int(os.environ.get("PORT", os.environ.get("FLET_SERVER_PORT", default_port)))

    ft.run(
        main,
        view=ft.AppView.WEB_BROWSER,
        port=server_port,
        host=server_host,
        assets_dir=str(ASSETS_ROOT),
    )
