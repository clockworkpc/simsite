#!/usr/bin/env python3
import os
import sys
import time
import random
from datetime import datetime, timedelta

# Game state
state = {
    "stage": 0,
    "load_balancer": None,
    "reverse_proxy": False,
    "cdn": None,
    "paste_storage": {},
    "daily_writes": 0,
    "last_write_reset": datetime.now(),
}

# Stage descriptions
stages = [
    "Start: Single server. Basic paste acceptance.",
    "Add Load Balancer (⚖).",
    "Add Reverse Proxy (🔐).",
    "Add CDN (☁️).",
    "Implement Pastebin logic: ID generation, expiration, rate-limiter, analytics.",
]


def intro_screen():
    clear()
    print("────────────────────────────────────────────────────────────")
    print("🧠 Welcome to the Pastebin System Design CLI Challenge 🧠")
    print("────────────────────────────────────────────────────────────")
    print(
        """
You are the sole developer tasked with building a scalable version of pastebin.com.

Initial Requirements:
- Users can create short-lived text pastes (under 1MB).
- Each paste should be accessible via a unique short URL.
- Read traffic is expected to be ~100x higher than write traffic.
- Pastes must auto-expire after 5 days.
- Users should be rate-limited to prevent abuse (e.g. 10 pastes/day).
- System must be cost-effective and globally accessible over time.

You will progressively evolve the architecture:
1. Start with a single server.
2. Add components: Load Balancer, Reverse Proxy, CDN.
3. Implement core features like ID generation, expiration, and analytics.

Your goal is to make smart, incremental design decisions and finish with a production-ready system that meets the business and technical constraints.

Let’s begin!
    """
    )
    wait_input()


# Requirements
WRITE_LIMIT = 10  # max pastes per client per day
READ_WRITE_RATIO = 100


def clear():
    os.system("clear")


def wait_input():
    input("\nPress Enter to continue...")


def draw():
    lines = []
    if state["cdn"]:
        lines.append("CDN (☁️)")
        lines.append("  |")
    if state["reverse_proxy"]:
        lines.append("Reverse Proxy (🔐)")
        lines.append("  |")
    if state["load_balancer"]:
        lines.append(f"Load Balancer (⚖) [{state['load_balancer']}]")
        lines.append(" /           \\")
        lines.append("Server A 🖥️    Server B 🖥️")
    else:
        lines.append("Server (🖥️)")
    return "\n".join(lines)


def show_stage():
    clear()
    print(f"# Stage {state['stage'] + 1}")
    print(f"{stages[state['stage']]}\n")
    print("```")
    print(draw())
    print("```")


def load_balancer_decision():
    clear()
    print("────────────────────────────────────────────────────────────")
    print("🏗️  Architectural Decision: Load Balancer Strategy")
    print("────────────────────────────────────────────────────────────")
    print(
        """
Your site traffic is increasing, and a Load Balancer (LB) is needed.

Do you want a basic, cheap strategy or a scalable, production-grade solution?

Choose your architecture:
1. Basic Round Robin (Layer 4, Active-Passive)
2. Sticky Sessions (Layer 7, Session Affinity)
3. Weighted Round Robin (Layer 7, Active-Active, scalable)
"""
    )
    choice = input("Enter your choice [1-3]: ").strip()

    if choice == "1":
        state["load_balancer"] = "Layer 4 (RR)"
        state["architecture_notes"] = (
            "⚠️ Limited scalability. Single LB is a failure point. No smart routing."
        )
        state["lb_resilience"] = "low"
    elif choice == "2":
        state["load_balancer"] = "Layer 7 (Sticky)"
        state["architecture_notes"] = (
            "⚠️ Tied to individual server sessions. Limits scaling unless session store added."
        )
        state["lb_resilience"] = "medium"
    elif choice == "3":
        state["load_balancer"] = "Layer 7 (Weighted RR)"
        state["architecture_notes"] = (
            "✅ High availability with Active-Active. Supports traffic shaping and smart routing."
        )
        state["lb_resilience"] = "high"
    else:
        print("Invalid input. Defaulting to Round Robin (L4).")
        state["load_balancer"] = "Layer 4 (RR)"
        state["architecture_notes"] = "⚠️ Limited scalability."
        state["lb_resilience"] = "low"

    print(f"\n✅ Load Balancer set: {state['load_balancer']}")
    wait_input()


def choose_load_balancer():
    opts = {
        "1": "Random",
        "2": "Least Connections",
        "3": "Session (Sticky)",
        "4": "Round Robin",
        "5": "Weighted RR",
        "6": "Layer 4",
        "7": "Layer 7",
    }
    for k, name in opts.items():
        print(f"{k}. {name}")
    ch = input(">> ").strip()
    if ch in opts:
        state["load_balancer"] = opts[ch]
        print(f"✅ Added LB: {opts[ch]}")
        return True
    return False


def choose_cdn():
    opts = {"1": "Push", "2": "Pull"}
    for k, name in opts.items():
        print(f"{k}. {name}")
    ch = input(">> ").strip()
    if ch in opts:
        state["cdn"] = opts[ch]
        print(f"✅ Added CDN: {opts[ch]}")
        return True
    return False


def pastebin_logic():
    clear()
    print("# Pastebin Core Logic Stage")
    client = "user"
    now = datetime.now()
    if now - state["last_write_reset"] > timedelta(days=1):
        state["daily_writes"] = 0
        state["last_write_reset"] = now
    print(f"- Daily writes so far: {state['daily_writes']}/{WRITE_LIMIT}")
    action = input("Write a new paste? (y/N) ").strip().lower()
    if action == "y":
        if state["daily_writes"] >= WRITE_LIMIT:
            print("❌ Daily write limit reached (10). Try tomorrow.")
        else:
            pid = base62(random.getrandbits(48))
            content = input("Enter text (<1MB): ")[:1000]
            exp = datetime.now() + timedelta(days=5)
            state["paste_storage"][pid] = {
                "content": content,
                "expires": exp,
                "views": 0,
            }
            state["daily_writes"] += 1
            print(f"✅ Paste created with ID: {pid}, expires in 5 days.")
    key = input("Read a paste? (y/N) ").strip().lower()
    if key == "y":
        pid = input("Paste ID: ").strip()
        p = state["paste_storage"].get(pid)
        if p and p["expires"] > now:
            p["views"] += 1
            print(f"📄 Content:\n{p['content']}")
            print(f"(Views: {p['views']})")
        else:
            print("❌ Not found or expired.")
    wait_input()
    return True


def base62(num, length=8):
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    s = ""
    while num and len(s) < length:
        s += chars[num % 62]
        num //= 62
    return s.ljust(length, random.choice(chars))


def game_loop():
    intro_screen()
    while state["stage"] < len(stages):
        show_stage()
        if state["stage"] == 1:
            load_balancer_decision()
            state["stage"] += 1
            # wait_input()
        elif state["stage"] == 2:
            input("Enable Reverse Proxy? (Enter) ")
            state["reverse_proxy"] = True
            state["stage"] += 1
        elif state["stage"] == 3:
            if choose_cdn():
                state["stage"] += 1
                wait_input()
        elif state["stage"] == 4:
            pastebin_logic()
            state["stage"] += 1
        else:
            state["stage"] += 1
    show_stage()
    print("\n🎉 Completed! You built a Pastebin clone with real constraints.\n")


if __name__ == "__main__":
    try:
        game_loop()
    except KeyboardInterrupt:
        print("\n🛑 Exiting.")
