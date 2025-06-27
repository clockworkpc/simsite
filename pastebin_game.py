import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box
import tempfile
import webbrowser


class SimSiteGame:
    def __init__(self):
        self.console = Console()
        self.components = set(["Web Server"])
        self.stage = 0
        self.emojis = {
            "Client": "🧑‍💻",
            "Web Server": "🌐",
            "CDN": "🚀",
            "DNS": "📡",
            "Write API": "✍️",
            "Read API": "📖",
            "Analytics": "📊",
            "SQL": "🗄️",
            "Object Store": "🧺",
        }

    def run(self):
        def center(text):
            term_width = self.console.size.width
            return "\n".join(line.center(term_width) for line in text.split("\n"))

        self.center = center
        stage_descriptions = [
            "[i]You're starting with a simple web server. Let's add persistent storage.[/i]",
            "[i]Your write throughput is becoming a bottleneck. Time to scale smartly.[/i]",
            "[i]Reading pastes is slowing down. How can you optimize for read traffic?[/i]",
            "[i]Users want to store more data — even large files. What now?[/i]",
            "[i]Global users complain about load times. What can help distribute content?[/i]",
            "[i]Product is growing. You need insights into user behavior.[/i]",
            "[i]Latency complaints from global users. Resolve DNS smarter.[/i]",
        ]
        self.console.clear()
        self.console.print(
            self.center(
                "[bold green]Welcome to SimSite: Build a Scalable Pastebin Clone![/bold green]"
            )
        )

        while self.stage < len(self.stages()):
            # Show stage description and diagram once
            self.console.print("\n")
            self.typewriter(stage_descriptions[self.stage])
            self.console.print("\n")
            self.render_state()

            stage_data = self.stages()[self.stage]
            prompt = stage_data["prompt"]
            option_objs = stage_data["options"]
            options = [opt["text"] for opt in option_objs]

            correct = stage_data["correct"]

            self.console.print(
                Panel.fit(
                    self.center(f"Stage {self.stage + 1}: {prompt}"), style="bold blue"
                )
            )

            table = Table(title="Options", box=box.SIMPLE)
            table.add_column("#", justify="center")
            table.add_column("Option")
            for idx, opt in enumerate(options):
                table.add_row(str(idx + 1), opt)
            self.console.print(table, justify="center")

            # Ask until correct
            while True:
                choice = self.get_choice(len(options))
                if options[choice - 1] == correct["text"]:
                    self.console.print(
                        "[bold green]✅ Correct! Advancing...[/bold green]"
                    )
                    self.components.add(correct["component"])
                    self.stage += 1
                    break  # move to next stage
                else:
                    wrong_choice = options[choice - 1]
                    explanation = "(no explanation available)"
                    for opt in option_objs:
                        if opt["text"] == wrong_choice:
                            explanation = opt["reason"]
                            break
                    self.console.print(
                        f"[bold red]❌ Incorrect:[/bold red] {wrong_choice} — {explanation}.  Try again."
                    )

        self.render_state()
        self.console.print(
            "[bold yellow]\n🎉 Congratulations! You've built a production-grade Pastebin system![/bold yellow]"
        )
        self.render_mermaid()

    def get_choice(self, num):
        while True:
            try:
                choice = int(Prompt.ask("Choose an option"))
                if 1 <= choice <= num:
                    return choice
            except ValueError:
                pass
            self.console.print("[italic red]Invalid input. Try again.[/italic red]")

    def render_state(self):
        self.console.print("[bold]Current System Architecture:[/bold]", style="cyan")

        lines = []

        if "DNS" in self.components:
            lines.append(f"{self.emojis['DNS']} DNS")
            lines.append("  |")

        lines.append(f"{self.emojis['Client']} Client")

        if "CDN" in self.components:
            lines.append("  |")
            lines.append(f"{self.emojis['CDN']} CDN")

        lines.append("  |")
        lines.append(f"{self.emojis['Web Server']} Web Server")

        if "Write API" in self.components:
            lines.append("  |--> " + f"{self.emojis['Write API']} Write API")

        if "Read API" in self.components:
            lines.append("  |--> " + f"{self.emojis['Read API']} Read API")

        if "SQL" in self.components:
            lines.append("        |--> " + f"{self.emojis['SQL']} SQL")

        if "Object Store" in self.components:
            lines.append(
                "        |--> " + f"{self.emojis['Object Store']} Object Store"
            )

        if "Analytics" in self.components:
            lines.append("  |--> " + f"{self.emojis['Analytics']} Analytics")

        ascii_output = "\n".join(lines)

        self.console.print(
            Panel.fit(ascii_output, title="Architecture Diagram", style="magenta")
        )

    def load_stages_from_json(self):
        import json
        from pathlib import Path

        with open(Path(__file__).parent / "stages.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def stages(self):
        if not hasattr(self, "_stages"):
            self._stages = self.load_stages_from_json()
        return self._stages

    def render_mermaid(self):
        import tempfile
        import webbrowser

        c = self.components
        mermaid_lines = ["graph TD"]

        def node_id(name):
            return name.lower().replace(" ", "_")

        def edge(a, b):
            aid = node_id(a)
            bid = node_id(b)
            alabel = f'{self.emojis.get(a, "")} {a}'
            blabel = f'{self.emojis.get(b, "")} {b}'
            return f'    {aid}["{alabel}"] --> {bid}["{blabel}"]'

        # Core graph
        if "DNS" in c:
            mermaid_lines.append(edge("DNS", "Client"))
        else:
            mermaid_lines.append(f'    client["{self.emojis["Client"]} Client"]')

        if "CDN" in c:
            mermaid_lines.append(edge("Client", "CDN"))
            mermaid_lines.append(edge("CDN", "Web Server"))
        else:
            mermaid_lines.append(edge("Client", "Web Server"))

        if "Read API" in c:
            mermaid_lines.append(edge("Web Server", "Read API"))
            mermaid_lines.append(edge("Read API", "SQL"))
            mermaid_lines.append(edge("Read API", "Object Store"))

        if "Write API" in c:
            mermaid_lines.append(edge("Web Server", "Write API"))
            mermaid_lines.append(edge("Write API", "SQL"))

        if "Analytics" in c:
            mermaid_lines.append(edge("Web Server", "Analytics"))

        html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <script src="https://cdn.jsdelivr.net/npm/mermaid@11.7.0/dist/mermaid.min.js"></script>
    </head>
    <body>
      <div class="mermaid">
    {chr(10).join(mermaid_lines)}
      </div>
      <script>mermaid.initialize({{ startOnLoad: true }});</script>
    </body>
    </html>
    """

        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
            f.write(html)
            webbrowser.open_new_tab(f.name)
        _new_tab(f.name)

    def typewriter(self, text):
        import time
        from rich.markup import render

        rendered = render(text)
        for line in rendered.plain.splitlines():
            centered_line = line.center(self.console.size.width)
            for char in centered_line:
                self.console.print(char, end="", soft_wrap=True, highlight=False)
                time.sleep(0.001)
            self.console.print()


if __name__ == "__main__":
    SimSiteGame().run()
