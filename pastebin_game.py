import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box


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
        self.console.print(
            self.center("[bold]Current System Architecture:[/bold]"), style="cyan"
        )
        diagram = [
            f"{self.emojis['Client']} Client",
            "  |",
            f"{self.emojis['Web Server']} Web Server",
        ]

        if "CDN" in self.components:
            diagram.insert(1, f"{self.emojis['CDN']} CDN")
        if "DNS" in self.components:
            diagram.insert(0, f"{self.emojis['DNS']} DNS")
        if "Write API" in self.components:
            diagram.append(f"  |--> {self.emojis['Write API']} Write API")
        if "Read API" in self.components:
            diagram.append(f"  |--> {self.emojis['Read API']} Read API")
        if "Analytics" in self.components:
            diagram.append(f"  |--> {self.emojis['Analytics']} Analytics")
        if "SQL" in self.components:
            diagram.append(f"        |--> {self.emojis['SQL']} SQL")
        if "Object Store" in self.components:
            diagram.append(f"        |--> {self.emojis['Object Store']} Object Store")

        ascii_output = "\n".join(diagram)
        self.console.print(
            Panel.fit(
                self.center(ascii_output), title="Architecture Diagram", style="magenta"
            )
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

    def typewriter(self, text):
        import time
        from rich.markup import render

        rendered = render(text)
        for line in rendered.plain.splitlines():
            centered_line = line.center(self.console.size.width)
            for char in centered_line:
                self.console.print(char, end="", soft_wrap=True, highlight=False)
                time.sleep(0.01)
            self.console.print()


if __name__ == "__main__":
    SimSiteGame().run()
