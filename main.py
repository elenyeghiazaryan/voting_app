import json
import os
import datetime
from colorama import Fore, Style, init

init(autoreset=True)

DATA_FILE = "people.json"
LOG_FILE = "log.txt"

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_vote(voter, voted_for):
    with open(LOG_FILE, "a") as log:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{time}] {voter} voted for {voted_for}\n")

def show_results(people):
    sorted_people = sorted(people, key=lambda p: p["votes"], reverse=True)

    print("\n🎉 " + Fore.YELLOW + "=== FINAL RESULTS ===" + Style.RESET_ALL)
    for i, person in enumerate(sorted_people, 1):
        print(f"{i}. {Fore.CYAN}{person['name']}{Style.RESET_ALL} - {Fore.GREEN}{person['votes']} votes")

    winner = sorted_people[0]
    print("\n🏆 " + Fore.MAGENTA + "WINNER" + Style.RESET_ALL)
    print(f"🎖 {winner['name']} with {winner['votes']} votes! 🎖")
    print(Fore.YELLOW + "👏 Congratulations!" + Style.RESET_ALL)

    total_votes = sum(p["votes"] for p in people)
    avg = total_votes / len(people)
    print(f"\n📊 Average votes per person: {avg:.2f}")
    print(f"🔻 Least voted: {min(people, key=lambda p: p['votes'])['name']}")

def reset_votes(people):
    for person in people:
        person["votes"] = 0
        person["voted"] = False
    save_data(people)
    open(LOG_FILE, "w").close()
    print("\n🔄 All votes and statuses have been reset.")

def admin_panel(people):
    print(Fore.YELLOW + "\n🔐 ADMIN LOGIN" + Style.RESET_ALL)
    username = input("Username: ")
    password = input("Password: ")

    if username != "admin" or password != "1234":
        print("❌ Incorrect credentials.")
        return

    while True:
        print("\n" + Fore.MAGENTA + "=== ADMIN PANEL ===" + Style.RESET_ALL)
        print("1. View votes per person")
        print("2. See voting history (who voted for whom)")
        print("3. See who hasn't voted")
        print("4. Reset everything")
        print("5. Exit admin panel")

        choice = input("Select an option: ")

        if choice == "1":
            print("\nVOTES PER PERSON")
            for p in people:
                print(f"{p['name']}: {p['votes']} votes")

        elif choice == "2":
            print("\n📜 VOTING LOG")
            if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
                print("No votes have been cast yet.")
            else:
                with open(LOG_FILE, "r") as f:
                    print(f.read())

        elif choice == "3":
            print("\n🧾 PEOPLE WHO HAVE NOT VOTED:")
            for p in people:
                if not p["voted"]:
                    print(f"❌ {p['name']}")

        elif choice == "4":
            confirm = input("⚠️ Are you sure? This will reset everything (y/n): ").lower()
            if confirm == 'y':
                reset_votes(people)
                print("✅ All data has been reset.")
            else:
                print("❌ Cancelled.")

        elif choice == "5":
            print("👋 Exiting admin panel.")
            break
        else:
            print("❌ Invalid choice.")

def main():
    people = load_data()

    print("\n🏁 " + Fore.CYAN + "Welcome to Championship Voting!" + Style.RESET_ALL)
    print("Type 'admin' to enter admin mode or press Enter to start voting.")

    mode = input("> ").strip().lower()
    if mode == "admin":
        admin_panel(people)
        return

    while any(not p["voted"] for p in people):
        print("\n=== VOTER LIST ===")
        for i, person in enumerate(people, 1):
            # status = Fore.RED + "(already voted)" if person["voted"] else ""
            status = ""
            if person["voted"]:
                status = Fore.RED + "(already voted)"
            else:
                status = ""
            print(f"{i}. {person['name']} {status}{Style.RESET_ALL}")

        voter_input = input("\nWho are you? (choose number, type 'admin' to enter admin panel, or 'q' to quit): ")

        if voter_input.lower() == 'q':
            show_results(people)
            break
        elif voter_input.lower() == 'admin':
            admin_panel(people)
            continue
        elif not voter_input.isdigit() or not (1 <= int(voter_input) <= len(people)):
            print("❌ Invalid input.")
            continue

        voter_index = int(voter_input) - 1
        voter = people[voter_index]

        if voter["voted"]:
            print("⚠️ You have already voted.")
            continue

        print("\n=== CANDIDATES TO VOTE FOR ===")
        for i, person in enumerate(people, 1):
            if i - 1 != voter_index:
                print(f"{i}. {person['name']} ({person['votes']} votes)")

        vote_input = input("Who do you vote for? (choose number): ")
        if not vote_input.isdigit():
            print("❌ Invalid input.")
            continue

        vote_index = int(vote_input) - 1
        if vote_index == voter_index or not (0 <= vote_index < len(people)):
            print("❌ You cannot vote for yourself or invalid choice.")
            continue

        print(f"\nYou are about to vote for {Fore.CYAN}{people[vote_index]['name']}{Style.RESET_ALL}")
        confirm = input("Confirm? (y/n): ").lower()
        if confirm != 'y':
            print("❌ Vote cancelled.")
            continue

        people[vote_index]["votes"] += 1
        people[voter_index]["voted"] = True
        print(f"✅ {voter['name']} voted for {people[vote_index]['name']}")
        log_vote(voter["name"], people[vote_index]["name"])
        save_data(people)


if __name__ == "__main__":
    if not os.path.exists(DATA_FILE):
        print("❌ No data file found! Please create 'people.json'.")
    else:
        main()
