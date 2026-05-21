#!/usr/bin/env python3
"""
MK-Aurelura-3 Daily Performance Tracker
Tracks: 11th PCM Academics | Designs | Code Learning | Research/GATE Prep
No external libraries needed. Python 3.6+
"""

import json
import os
from datetime import date, timedelta

FILE = "mk_aurelura_progress.json"
TODAY = str(date.today())

# XP system - adjust these rates if you want
XP_RATES = {
    "academics": {"per_hour": 20, "per_problem": 5, "name": "11th PCM/HC Verma"},
    "designs": {"per_model": 15, "per_hour": 10, "name": "Blender/Jewelry/Design"},
    "code": {"per_hour": 20, "per_pset": 25, "name": "CS50x/Python"},
    "research": {"per_idea": 10, "per_hour": 15, "name": "Research/GATE Prep"}
}

LEVEL_TITLES = {
    1: "Research Dropout",
    2: "Design Intern",
    3: "CS50x Cadet",
    4: "HC Verma Survivor",
    5: "Night Download CEO",
    6: "Blender Gremlin",
    7: "Future DRDO Candidate",
    8: "Nanotech Padawan",
    9: "Paper Publishing Menace",
    10: "CEO of mk-aurelura-3"
}

def load_data():
    if os.path.exists(FILE):
        with open(FILE, 'r') as f:
            return json.load(f)
    return {"streak": 0, "last_date": "", "level": 1, "total_xp": 0, "days": {}}

def save_data(data):
    with open(FILE, 'w') as f:
        json.dump(data, f, indent=2)

def draw_bar(name, xp, max_xp=100):
    percent = min(100, int(xp / max_xp * 100))
    filled = '█' * (percent // 10)
    empty = '░' * (10 - percent // 10)
    return f"{name:<22} [{filled}{empty}] {xp:>3}/100 XP"

def update_streak(data):
    yesterday = str(date.today() - timedelta(days=1))
    if data["last_date"] == yesterday:
        data["streak"] += 1
    elif data["last_date"]!= TODAY:
        data["streak"] = 1
    data["last_date"] = TODAY

def get_title(level):
    return LEVEL_TITLES.get(level, f"Level {level} Legend")

def main():
    data = load_data()
    if TODAY not in data["days"]:
        data["days"][TODAY] = {"academics": 0, "designs": 0, "code": 0, "research": 0}

    today = data["days"][TODAY]

    print(f"\n=== MK-AURELURA-3 DAILY CHECK-IN ===")
    print(f"Date: {TODAY} | Streak: 🔥 {data['streak']} days | Level: {data['level']} - {get_title(data['level'])}")
    print("="*50)
    for key in today:
        print(draw_bar(XP_RATES[key]["name"], today[key]))
    print("="*50)

    print("\nWhat did you complete today, bro?")
    print("[1] Academics: 11th PCM hours or HC Verma problems")
    print("[2] Designs: Blender hours or models/sketches done")
    print("[3] Code: CS50x/Python hours or pset finished")
    print("[4] Research: GATE prep hours or new ideas written")
    print("[v] View weekly summary")
    print("[q] Save & quit")

    while True:
        choice = input("\n> ").lower().strip()

        if choice == 'q':
            break
        elif choice == 'v':
            show_weekly(data)
            continue
        elif choice == '1':
            h = float(input("Hours spent on 11th PCM: ") or 0)
            p = int(input("HC Verma problems solved: ") or 0)
            xp = int(h * XP_RATES["academics"]["per_hour"] + p * XP_RATES["academics"]["per_problem"])
            today["academics"] += xp
            print(f"+{xp} XP to Academics")
        elif choice == '2':
            h = float(input("Hours in Blender/design: ") or 0)
            m = int(input("Models/sketches finished: ") or 0)
            xp = int(h * XP_RATES["designs"]["per_hour"] + m * XP_RATES["designs"]["per_model"])
            today["designs"] += xp
            print(f"+{xp} XP to Designs")
        elif choice == '3':
            h = float(input("Hours coding CS50x/Python: ") or 0)
            p = int(input("CS50x pset completed? 1=yes 0=no: ") or 0)
            xp = int(h * XP_RATES["code"]["per_hour"] + p * XP_RATES["code"]["per_pset"])
            today["code"] += xp
            print(f"+{xp} XP to Code")
        elif choice == '4':
            h = float(input("Hours GATE prep/research reading: ") or 0)
            i = int(input("New research ideas written down: ") or 0)
            xp = int(h * XP_RATES["research"]["per_hour"] + i * XP_RATES["research"]["per_idea"])
            today["research"] += xp
            print(f"+{xp} XP to Research")
        else:
            print("Invalid option. Use 1,2,3,4,v,q")
            continue

        print("\n" + "="*50)
        for key in today:
            print(draw_bar(XP_RATES[key]["name"], today[key]))
        print("="*50)

    total_today = sum(today.values())
    if total_today > 0:
        update_streak(data)
        data["total_xp"] += total_today
        new_level = data["total_xp"] // 500 + 1
        if new_level > data["level"]:
            print(f"\n🎉 LEVEL UP! You are now Level {new_level} – {get_title(new_level)}")
            data["level"] = new_level

    save_data(data)
    print(f"\nSaved. Streak: 🔥 {data['streak']} days. Total XP: {data['total_xp']}")
    print("See you tomorrow, CEO.")

def show_weekly(data):
    print("\n=== LAST 7 DAYS ===")
    for i in range(7):
        d = str(date.today() - timedelta(days=i))
        if d in data["days"]:
            day_data = data["days"][d]
            total = sum(day_data.values())
            print(f"{d}: {total:>3} XP | A:{day_data['academics']:>3} D:{day_data['designs']:>3} C:{day_data['code']:>3} R:{day_data['research']:>3}")
        else:
            print(f"{d}: No data")
    print("===================")

if __name__ == "__main__":
    main()
